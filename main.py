from nicegui import ui
import requests
from ffmpeg import audio
import tempfile
import shutil
import os

# audio file name: audio1.mp3, audio2.mp3, audio3.mp3, audio4.mp3
player = None

t = 1 # generate counter
audio_files = ["0.mp3", "1.mp3", "2.mp3", "3.mp3", "4.mp3"] # 0.mp3 is a file for placeholder

# 使用免费的Text-to-Speech API
TTS_API_URL = "https://api.streamelements.com/kappa/v2/speech"

# 使用免费的翻译API
TRANSLATE_API_URL = "https://api.mymemory.translated.net/get"

def generate_speech(text):
    params = {
        "voice": "Brian",
        "text": text
    }
    response = requests.get(url_tts.value, params=params)
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
    global t
    global audio_files

    text = text_en.value
    if not text:
        ui.notify("请输入英文文本")
        return

    for f in audio_files:
        if os.path.exists(f):
            os.remove(f)

    t += 1
    audio_files[1] = f"{t}1.mp3"
    audio_files[2] = f"{t}2.mp3"
    audio_files[3] = f"{t}3.mp3"
    audio_files[4] = f"{t}4.mp3"

    # 保存原始语音文件到本地目录，文件名为audio.mp3
    try:
        speech_file = generate_speech(text)
        shutil.copy(speech_file, audio_files[1]) 
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        # 生成不同速度的音频文件
        change_speed(audio_files[1], 2, audio_files[2])
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed(audio_files[1],3, audio_files[3])
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed(audio_files[1],4, audio_files[4])
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

def on_translate_c2e():
    text = text_cn.value
    if not text:
        ui.notify("请输入中文文本")
        return
    
    params = {
        "q": text,
        "langpair": "zh-CN|en"
    }
    response = requests.get(url_trans.value, params=params)
    if response.status_code == 200:
        data = response.json()
        translated_text = data["responseData"]["translatedText"]
        text_en.value = translated_text
    else:
        ui.notify("翻译失败")


def on_translate_e2c():
    text = text_en.value
    if not text:
        ui.notify("请输入英文文本")
        return
    
    params = {
        "q": text,
        "langpair": "en|zh-CN"
    }
    response = requests.get(url_trans.value, params=params)
    if response.status_code == 200:
        data = response.json()
        translated_text = data["responseData"]["translatedText"]
        text_cn.value = translated_text
    else:
        ui.notify("翻译失败")

def on_play(speed):
    global player
    global audio_files
    
    if player is None:
        player = ui.audio(audio_files[speed])
        player.set_visibility(False)
    else:
        player.pause()
        player.set_source(audio_files[speed])
        player.update()
    
    # need to destroy the player after using, cannot find the method yet
    player.play()

# main 
with ui.row():
    text_cn = ui.textarea("输入中文文本").classes('w-full')
    with ui.row():
        ui.button("中文->英文", on_click=on_translate_c2e)
        ui.space()
        ui.button("英文->中文", on_click=on_translate_e2c)

    text_en = ui.textarea("输入英文文本").classes('w-full')

    with ui.column().classes('w-1/2'):
        ui.button("生成英文语音", on_click=on_generate)

    ui.separator()

    with ui.row():
        b1 = ui.button("1倍速播放", on_click=lambda: on_play(1))
        b2 = ui.button("2倍速播放", on_click=lambda: on_play(2))
        b3 = ui.button("3倍速播放", on_click=lambda: on_play(3))
        b4 = ui.button("4倍速播放", on_click=lambda: on_play(4))
    ui.separator()
    ui.separator()

    url_trans = ui.input("翻译api").classes('w-full')
    url_trans.value = TRANSLATE_API_URL

    url_tts = ui.input("TTS api").classes('w-full')
    url_tts.value = TTS_API_URL

ui.run(
    native = True,  # 本地运行，不使用浏览器   
    title  = "speed4 v0.1.0",  # 窗口标题
    reload = True,
    dark   = True,
    window_size = (700, 900),
    fullscreen = False,
    favicon = './favicon.ico', # 自定义图标
)       
