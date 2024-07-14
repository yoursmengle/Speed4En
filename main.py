from nicegui import ui
import requests
import os
from pydub import AudioSegment
import tempfile
import shutil
from ffmpeg import audio

audio_file1 = "audio1.mp3"
audio_file2 = "audio2.mp3"
audio_file3 = "audio3.mp3"
audio_file4 = "audio4.mp3"

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
        audio.a_speed(input_file, str(speed), output_file)
        ui.notify(f"音频处理成功: {output_file}")
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

def on_generate():
    text = text_en.value
    if not text:
        ui.notify("请输入文本")
        return
    
    ui.notify("正在生成语音...")
    speech_file = generate_speech(text)
    
    if speech_file:
        ui.notify("语音生成成功")
        # 保存原始语音文件到本地目录，文件名为audio.mp3
        shutil.copy(speech_file, audio_file1)
        audio1.bind_source(audio_file1)
        # 生成不同速度的音频文件
        change_speed(audio_file1, 2, audio_file2)
        audio2.bind_source(audio_file2)

        change_speed(audio_file1, 3, audio_file3)
        audio3.bind_source(audio_file3)

        change_speed(audio_file1, 4, audio_file4)
        audio4.bind_source(audio_file4)
    else:
        ui.notify("语音生成失败")

def on_translate():
    text = text_cn.value
    if not text:
        ui.notify("请输入中文文本")
        return
    
    ui.notify("正在翻译...")
    params = {
        "q": text,
        "langpair": "zh-CN|en"
    }
    response = requests.get(TRANSLATE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        translated_text = data["responseData"]["translatedText"]
        text_en.value = translated_text
        ui.notify("翻译成功")
        os.remove(audio_file1)
        os.remove(audio_file2)
        os.remove(audio_file3)
        os.remove(audio_file4)
    else:
        ui.notify("翻译失败")

with ui.row():
    with ui.column().classes('w-1/2'):
        text_cn = ui.textarea("输入中文文本").classes('w-full')
        ui.button("翻译", on_click=on_translate)
        text_en = ui.textarea("输入英文文本").classes('w-full')
    
    with ui.column().classes('w-1/2'):
        ui.button("生成语音", on_click=on_generate)
    
    with ui.column():
        if os.path.exists(audio_file1):
            with ui.row():
                ui.label(f"1倍速")
                audio1 = ui.audio(audio_file1)
        if os.path.exists(audio_file2):
            with ui.row():
                ui.label(f"2倍速")
                audio2 = ui.audio(audio_file2)
        if os.path.exists(audio_file3):
            with ui.row():
                ui.label(f"3倍速")
                audio3 = ui.audio(audio_file3)
        if os.path.exists(audio_file4):
            with ui.row():
                ui.label(f"4倍速")
                audio4 = ui.audio(audio_file4)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080)