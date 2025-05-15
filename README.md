# Web-version-VAANet
A web version for VAANet-Multimodal emotion recognition Model

参考：
https://github.com/maysonma/VAANet
https://github.com/Robin-WZQ/multimodal-emotion-recognition-DEMO
在其基础上自己做了一个web端，！后期更新！，先上传用到的数据集

原始视频数据集：
链接: https://pan.baidu.com/s/13O4xDubynQPlteOtpfbPxA?pwd=u7rv 提取码: u7rv 

已拆分视频数据（第二批新增数据不包含在内，建议下载中国老人视频数据和原始视频数据集，再根据下面处理步骤自行拆分）：
链接: https://pan.baidu.com/s/1qnaY0-rS1mnCbZUDwDrR8A?pwd=tq98 提取码: tq98 


中国老人视频数据，包括录屏与ai生成：
链接: https://pan.baidu.com/s/1DPY_RYs2onjSSTL81sZwog?pwd=egav 提取码: egav 

数据集预处理：
Convert from mp4 to jpg files using /tools/video2jpg.py
Add n_frames information using /tools/n_frames.py
Generate annotation file in json format using /tools/ve8_json.py
Convert from mp4 to mp3 files using /tools/video2mp3.py

运行：
Assume the strcture of data directories is the following:
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
Confirm all options in ~/opts.py.

运行python main.py，进行模型训练

再次感谢：
参考链接1：https://github.com/maysonma/VAANet
参考链接2：https://github.com/Robin-WZQ/multimodal-emotion-recognition-DEMO

