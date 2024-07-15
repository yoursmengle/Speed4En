from nicegui import ui
import requests
from ffmpeg import audio
import tempfile
import shutil
import os

# audio file name: audio1.mp3, audio2.mp3, audio3.mp3, audio4.mp3
player = None

# 使用免费的Text-to-Speech API
TTS_API_URL = "https://api.streamelements.com/kappa/v2/speech"

# 使用免费的翻译API
TRANSLATE_API_URL = "https://api.mymemory.translated.net/get"

def generate_speech(text):
    params = {
        "voice": "Brian",
        "text": text
    }
    response = requests.get(TTS_API_URL, params=params)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        return None

def change_speed(input_file, speed, output_file):
    try:
        audio.a_speed(input_file, speed, output_file)
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

def on_generate():

    text = text_en.value
    if not text:
        ui.notify("请输入英文文本")
        return

    # 保存原始语音文件到本地目录，文件名为audio.mp3
    try:
        speech_file = generate_speech(text)
        shutil.copy(speech_file, "audio1.mp3")
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        # 生成不同速度的音频文件
        change_speed("audio1.mp3", 2, "audio2.mp3")
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed("audio1.mp3", 3, "audio3.mp3")
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed("audio1.mp3", 4, "audio4.mp3")
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

def on_translate():
    text = text_cn.value
    if not text:
        ui.notify("请输入中文文本")
        return
    
    params = {
        "q": text,
        "langpair": "zh-CN|en"
    }
    response = requests.get(TRANSLATE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        translated_text = data["responseData"]["translatedText"]
        text_en.value = translated_text
    else:
        ui.notify("翻译失败")

def on_play(speed):
    global player
    
    if player is None:
        pass
    elif player is ui.audio:
        player.pause()
        player.set_source("test.mp3")
        player.update()

    audio_name = f"audio{speed}.mp3"
    ui.notification(f"正在播放 {audio_name}，请稍等...")
    player = ui.audio(audio_name)
    player.set_visibility(False)

    player.play()

with ui.row():
    with ui.column().classes('w-1/2'):
        text_cn = ui.textarea("输入中文文本").classes('w-full')
        ui.button("翻译", on_click=on_translate)
        text_en = ui.textarea("输入英文文本").classes('w-full')
    
    with ui.column().classes('w-1/2'):
        ui.button("生成语音", on_click=on_generate)
    
    with ui.row():
        b1 = ui.button("1倍速", on_click=lambda: on_play(1))
        b2 = ui.button("2倍速", on_click=lambda: on_play(2))
        b3 = ui.button("3倍速", on_click=lambda: on_play(3))
        b4 = ui.button("4倍速", on_click=lambda: on_play(4))

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        native = True,  # 本地运行，不使用浏览器   
        title  = "speed4 v0.1.0",  # 窗口标题
        reload = False,
        dark   = False,
        window_size = (1080, 1920),
        fullscreen = False,
        favicon = './favicon.ico', # 自定义图标，暂时未生效，待解决
    )