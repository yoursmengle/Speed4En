from nicegui import ui
import requests
from pydub import AudioSegment
from pydub.effects import speedup
import tempfile
import shutil

t = 0
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
    audio = AudioSegment.from_file(input_file)
    audio = speedup(audio, speed)
    audio.export(output_file, format="mp3")

def on_generate():
    global t
    global audio_file1
    global audio_file2
    global audio_file3
    global audio_file4

    t = t + 1
    audio_file1 = f"audio1_{t}.mp3"
    audio_file2 = f"audio2_{t}.mp3"
    audio_file3 = f"audio3_{t}.mp3"
    audio_file4 = f"audio4_{t}.mp3"

    text = text_en.value
    if not text:
        ui.notify("请输入英文文本")
        return
    
    speech_file = generate_speech(text)
    
    if speech_file:
        ui.notify("语音生成成功")
        # 保存原始语音文件到本地目录，文件名为audio.mp3
        shutil.copy(speech_file, audio_file1)
        # 生成不同速度的音频文件
        change_speed(audio_file1, 2, audio_file2)
        change_speed(audio_file1, 3, audio_file3)
        change_speed(audio_file1, 4, audio_file4)
        update_audio()

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

def update_audio():
    try:
        audio1.source = audio_file1 
        audio1.update()
    except:
        pass
    try:
        audio2.source = audio_file2
        audio2.update()
    except:
        pass
    try:
        audio3.source = audio_file3
        audio3.update()
    except:
        pass
    try:
        audio4.source = audio_file4
        audio4.update()
    except:
        pass

with ui.row():
    with ui.column().classes('w-1/2'):
        text_cn = ui.textarea("输入中文文本").classes('w-full')
        ui.button("翻译", on_click=on_translate)
        text_en = ui.textarea("输入英文文本").classes('w-full')
    
    with ui.column().classes('w-1/2'):
        ui.button("生成语音", on_click=on_generate)

    with ui.column():
        with ui.row():
            lbl1 = ui.label(f"1倍速")
            audio1 = ui.audio(audio_file1)
        with ui.row():
            lbl2 = ui.label(f"2倍速")
            audio2 = ui.audio(audio_file2)
        with ui.row():
            lbl3 = ui.label(f"3倍速")
            audio3 = ui.audio(audio_file3)
        with ui.row():
            lbl4 = ui.label(f"4倍速")
            audio4 = ui.audio(audio_file4)

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