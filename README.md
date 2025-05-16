# Web_version_emotion_recognition_VAANet
A web version for VAANet-Multimodal emotion recognition Model

基于以下两个项目，实现了一个 **Web 端多模态情感识别模型**：

- [VAANet 原项目](https://github.com/maysonma/VAANet)  
- [Multimodal Emotion Recognition DEMO](https://github.com/Robin-WZQ/multimodal-emotion-recognition-DEMO)

在其基础上开发了一个 Web 页面，后期会持续更新。目前先上传所用到的数据集。


---

## 数据集下载

### 原始视频数据集

-链接: https://pan.baidu.com/s/13O4xDubynQPlteOtpfbPxA?pwd=u7rv
-提取码: u7rv 

---

### 已拆分视频数据  
（**第二批新增数据不包含**，建议下载“中国老人视频数据”与“原始视频数据集”，再根据下方的预处理步骤自行拆分）

-链接: https://pan.baidu.com/s/1qnaY0-rS1mnCbZUDwDrR8A?pwd=tq98
-提取码: tq98 

---

### 中国老人视频数据（包括录屏与 AI 生成）

-链接: https://pan.baidu.com/s/1DPY_RYs2onjSSTL81sZwog?pwd=egav
-提取码: egav 

## 数据集预处理

使用以下工具脚本对数据进行处理：

```bash
# 将 mp4 转为 jpg 图像序列
/tools/video2jpg.py

# 添加视频帧数信息
/tools/n_frames.py

# 生成 JSON 格式的标注文件
/tools/ve8_json.py

# 将 mp4 转为 mp3 音频文件
/tools/video2mp3.py
```

---

## 运行：
Assume the strcture of data directories is the following:
```bash
~/
  VideoEmotion8--imgs
    .../ (directories of class names)
      .../ (directories of video names)
        .../ (jpg files)
  VideoEmotion8--mp3
    .../ (directories of class names)
      .../ (mp3 files)
  results
  ve8_01.json
```

Confirm all options in ~/opts.py.

运行
```bash
python main.py
```
进行模型训练

---

## 致谢

本项目参考并基于以下开源项目开发：

- [VAANet](https://github.com/maysonma/VAANet)：多模态情感识别模型，提供了视觉和音频的融合架构。
- [Multimodal Emotion Recognition DEMO](https://github.com/Robin-WZQ/multimodal-emotion-recognition-DEMO)：演示了一个完整的情感识别流程，启发了 Web 端实现思路。

## 如有疑问，欢迎联系
yangruiyiouc@163.com
