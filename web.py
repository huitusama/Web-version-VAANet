from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import time

from os import getcwd
import numpy as np
import cv2
import time
import logging
from base64 import b64decode
from os import remove
from slice_png import img as bgImg
import image1_rc
from PyQt5.QtWidgets import QApplication,QMainWindow;
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from myVideoWidget import myVideoWidget
import dlib
from threading import Thread  # 导入线程函数
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from main import *
from Video_main import *
from face_detect import show_face
import time
import pyaudio

from real_time_processing_v2 import real_time_processing,real,init
from tools.picture_capture import capture
from tools.write_wav import record

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

camera = cv2.VideoCapture(0)  # 打开摄像头

emotion_result_1 = 0
probabilities_1 = 0

detecting = True  # 控制识别状态的全局变量
thread = None  # 线程对象

def init2() -> str:
    print("正在初始化相关配置")
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dst_dir_path = 'data/Joy'
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    if not os.path.exists(dst_dir_path + "/" + name):
        os.mkdir(dst_dir_path + "/" + name)
    if not os.path.exists(dst_dir_path + "/" + name + "/images/"):
        os.mkdir(dst_dir_path + "/" + name + "/images/")
    if not os.path.exists(dst_dir_path + "/" + name + "/mp3/"):
        os.mkdir(dst_dir_path + "/" + name + "/mp3/")
        os.mkdir(dst_dir_path + "/" + name + "/mp3/mp3/")
    images_path = dst_dir_path + "/" + name + "/images/"

    n_frame_fix(name)
    rewrite_josn(name)
    json_processing()
    image_path = "data/Joy/" + name
    audio_path = "data/Joy/" + name + "/mp3/mp3/"
    log_dir = "save_30.pth"

    opt = parse_opts()
    opt.device_ids = list(range(device_count()))
    local2global_path(opt)
    model, parameters = generate_model(opt)

    criterion = get_loss(opt)
    criterion = criterion.cuda()
    optimizer = get_optim(opt, parameters)

    writer = SummaryWriter(logdir=opt.log_path)
    print("配置结束")
    return name, images_path, image_path, audio_path, log_dir, model, criterion, optimizer, writer

def real(opt, model, criterion, writer,image_path, optimizer,audio_path,i,log_dir):
    spatial_transform = get_spatial_transform(opt, 'test')
    temporal_transform = TSN(seq_len=opt.seq_len, snippet_duration=opt.snippet_duration, center=False)
    target_transform = ClassLabel()
    validation_data = get_validation_set(image_path,audio_path,opt, spatial_transform, temporal_transform, target_transform,i)
    val_loader = get_data_loader(opt, validation_data, shuffle=False)

    checkpoint = torch.load(log_dir,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    result,preds = test(1, val_loader, model, criterion, opt, writer, optimizer)

    EMOTIONS = ["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]

    label = None  # 预测的标签
    temp_max = -1
    global emotion_result_1
    global probabilities_1
    for (k, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
        # 用于显示各类别概率
        text = "{}: {:.2f}%".format(emotion, prob * 100)
        print(text)
        if prob>temp_max:
            temp_max = prob
            emotion_result_1 = emotion
            probabilities_1 = prob
    print("ok!!!!!!!!!!!!")
    print(emotion_result_1)
    emotion_text = "{}: {:.2f}%".format(emotion_result_1, probabilities_1 * 100)
    # 格式化数据
    # 生成正确的 JSON 数据格式
    emotion_data = [{"emotion": emotion, "probability": "{:.2f}%".format(prob * 100)} for emotion, prob in
                    zip(EMOTIONS, preds)]
    max_emotion = {"emotion": emotion_result_1, "probability": "{:.2f}%".format(probabilities_1 * 100)}

    socketio.emit('update_emotion', {'emotions': emotion_data, 'max_emotion': max_emotion})

def show_camera(name, images_path, image_path, audio_path, log_dir, model, criterion, optimizer, writer):
    # 定时器槽函数，每隔一段时间执行

    opt = parse_opts()
    tmp = open('slice.png', 'wb')
    tmp.write(b64decode(bgImg))
    tmp.close()
    canvas = cv2.imread('slice.png')  # 用于数据显示的背景图片
    remove('slice.png')

    # 使用模型预测

    # 创建PyAudio对象
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    # 录音时间
    RECORD_SECONDS = 2

    i = 0
    j = -56

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    global detecting
    while detecting:
        tsk = []
        i += 1
        j += 56
        t1 = Thread(target=record,
                    args=(p, stream, i, CHUNK, FORMAT, CHANNELS, RECORD_SECONDS, RATE, audio_path,))
        t2 = Thread(target=capture, args=(i, j, camera, images_path,))
        tsk.append(t1)
        tsk.append(t2)
        t2.start()
        t1.start()
        for tt in tsk:
            tt.join()
            # ==================================================
        real(opt, model, criterion, writer, image_path, optimizer, audio_path, i,
                    log_dir)
        # ==================================================
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()
    os._exit(0)

@socketio.on('start_detection')
def start_detection():
    """ 实时表情识别，并将结果发送到前端 """
    while True:
        success, frame = camera.read()
        if success:
            name, images_path, image_path, audio_path, log_dir, model, criterion, optimizer, writer = init2()
            t1 = Thread(target=show_camera(name, images_path, image_path, audio_path, log_dir, model, criterion, optimizer, writer))
            t1.start()

        time.sleep(0.5)  # 控制刷新频率，避免过于频繁

@socketio.on('stop_detection')
def stop_detection():
    """ 处理停止识别的请求 """
    global detecting, thread
    detecting = False
    if thread and thread.is_alive():
        thread.join()  # 等待线程结束

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

