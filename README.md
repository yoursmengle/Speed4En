# 四倍速英语听力训练 

## 简介

本项目是一个英语听力训练工具，能够自动从网络获取听力材料，生成语音并以不同语速播放，提高听力训练效率。
本项目基于python下的nicegui开发，暂时只支持windows系统。

## 使用方法

点击左侧“随机”按钮，可以自动从网络获取一段英语听力材料，点击“生成英文语言”按钮，可以生成相关音频文件，可选择性点击“1倍速播放”等按钮，以各种速度播放听力材料。经过高速英语训练后，听力水平会有所提高。

## 进阶用法

可隐藏英文文本后在下方听写区域听写，点击“听写检查”按钮可查看听写结果。

可在右上方中文区输入自己想要表达的句子，然后点击中的翻译按钮，可将中文翻译为英文并显示在左侧，然后按照上面的方法生成语音并进行训练。



如果自动产生的英语听力材料不易理解，可再次点击“随机”按钮更换材料，或者点击中部的翻译按钮，翻译为中文并显示在右侧。

最下方列出了本软件所使用的获取英文句子、翻译、生成音频的API，如有需要，可自行更换更合适的API。

## 安装和运行

### 安装依赖包
```bash
python -m venv venv
venv/Scripts/activate.ps1
python -m pip install -r requirements.txt
```

### 安装 ffmpeg
```bash
wget https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z
7z x ffmpeg-git-essentials.7z
```
设置环境变量，将 ffmpeg.exe 所在目录添加到 PATH 环境变量中

### 运行
```bash
./running.ps1
```
### 打包
```bash
python ./build.py
```
打包后的文件在 dist 目录下




