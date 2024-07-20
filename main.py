from nicegui import ui
import requests
from ffmpeg import audio
import tempfile
import shutil
import os
from datetime import datetime
import difflib

#from niceguiToolkit.layout import inject_layout_tool
#inject_layout_tool()

# audio file name: audio1.mp3, audio2.mp3, audio3.mp3, audio4.mp3
player = None

t = 1 # generate counter
audio_files = ["0.mp3", "1.mp3", "2.mp3", "3.mp3", "4.mp3"] # 0.mp3 is a file for placeholder
audio_ok = False

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
    
    b1.disabled = True
    b2.disabled = True
    b3.disabled = True
    b4.disabled = True

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
        b1.disabled = False
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        # 生成不同速度的音频文件
        change_speed(audio_files[1], 2, audio_files[2])
        b2.disabled = False
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed(audio_files[1],3, audio_files[3])
        b3.disabled = False
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    try:
        change_speed(audio_files[1],4, audio_files[4])
        b4.disabled = False
    except Exception as e:
        ui.notify(f"处理音频时出错: {str(e)}")

    ui.notify("音频文件生成完成")

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
        if auto_hide.value:
            on_en_disappear()
        else:
            on_en_display()
        ui.notify("翻译完成")
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
        on_cn_display()
        ui.notify("翻译完成")
    else:
        ui.notify("翻译失败")

def on_play(speed):
    global player
    global audio_files

    if os.path.exists(audio_files[speed]) == False:
        ui.notify("请先生成音频文件")
        return
    
    if player is None:
        player = ui.audio(audio_files[speed])
        player.set_visibility(False)
    else:
        player.pause()
        player.set_source(audio_files[speed])
        player.update()
    
    # need to destroy the player after using, cannot find the method yet
    player.play()

def on_cn_display():
    text_cn.set_visibility(True)
    text_cn_2.set_visibility(False)

def on_en_display():
    text_en.set_visibility(True)
    text_en_2.set_visibility(False)

def on_cn_disappear():
    if text_cn.value == "":
        return

    text_cn.set_visibility(False)
    text_cn_2.value = "内容已隐藏"
    text_cn_2.set_visibility(True)

def on_en_disappear():
    if text_en.value == "":
        return

    text_en.set_visibility(False)
    text_en_2.value = "内容已隐藏"
    text_en_2.set_visibility(True)


def highlight_differences(text1, text2):
    # Generate a sequence matcher object
    s = difflib.SequenceMatcher(None, text1, text2)
    output = []

    # Loop through the matching blocks and differences
    for opcode, a0, a1, b0, b1 in s.get_opcodes():
        if opcode == 'equal':
            output.append(text1[a0:a1])
        elif opcode in ('replace', 'delete'):
            output.append(f"<span style='color: red;'>{text1[a0:a1]}</span>")
        elif opcode == 'insert':
            output.append(f"<span style='color: red;'>{text2[b0:b1]}</span>")
    
    return ''.join(output)

def on_check():
    try:
        if text_en.value == "" or text_writing.value == "":
            result.set_content("")
            result.update()            
            ui.notify("请确保两个文本框都有内容")
            return
    
        if text_en.value == text_writing.value:
            result.set_content("")
            result.update()
            ui.notify("完全正确")
            return
    except Exception as e:
        ui.notify(f"检查时出错: {str(e)}")
        return

    # Highlight differences
    highlighted_diff = highlight_differences(text_en.value, text_writing.value)
    
    # Display the result
    # display with html format
    result.set_content("###" + highlighted_diff)
    result.update()

# Assuming text_en and text_writing are defined elsewhere in your NiceGUI app
# Example usage:

# on_check()

def on_gen_cn():
    text_cn.set_value(examples_cn[datetime.now().microsecond%len(examples_cn)])
    on_cn_display()

def on_gen_en():
    text_en.set_value(examples_en[datetime.now().microsecond%len(examples_en)])

def on_save():
    if text_cn.value == "" and text_en.value == "":
        return

    if len(text_cn.value) > 5:
        with open('examples_cn.txt', 'a', encoding='utf-8') as f:
            f.write(text_cn.value + '\n')
    if len(text_en.value) > 5:
        with open('examples_en.txt', 'a', encoding='utf-8') as f:
            f.write(text_en.value + '\n')

    ui.notify("保存成功")

# main 

examples_cn = []
examples_en = []

# 读取示例文本, 并将每一行保存到一个列表中
with open('examples_cn.txt', 'r', encoding='utf-8') as f:
    examples_cn = f.readlines()

with open('examples_en.txt', 'r', encoding='utf-8') as f:
    examples_en = f.readlines()

with ui.row().style("height:auto;width:auto"):
    with ui.card().classes('no-shadow border-[3px]'):
        ui.markdown("中文文本")
        ui.separator()
        text_cn = ui.textarea("输入中文文本").classes('w-full').props('clearable')
        text_cn_2 = ui.textarea("输入中文文本").classes('w-full')
        text_cn_2.set_visibility(False)

        with ui.row():
            ui.button("生成", icon='history', on_click=on_gen_cn, color='lightgreen')
            ui.button("隐藏", icon='lock', on_click=on_cn_disappear, color='lightgreen')
            ui.button("显示", icon='visibility', on_click=on_cn_display, color='lightgreen')
            ui.button("清空", icon='clear', on_click=lambda: text_cn.set_value(''), color='lightgreen')

    with ui.column():
        ui.html('<center>翻   译</center>').style('color: #6E93D6; font-size: 150%; font-weight: 300').classes('w-full')
        ui.button(icon='arrow_forward', on_click=on_translate_c2e, color='lightblue').classes('w-full')
        ui.button(icon='arrow_back', on_click=on_translate_e2c, color='lightgreen').classes('w-full')
        ui.separator()
        ui.button("保存", icon='save', on_click=on_save, color='lightblue')
        ui.separator()
        auto_hide = ui.checkbox("自动隐藏", value=False)

    with ui.card().classes('no-shadow border-[3px]'):
        ui.markdown("英文文本")
        ui.separator()
        text_en = ui.textarea("输入英文文本").classes('w-full').props('clearable')
        text_en_2 = ui.textarea("输入英文文本").classes('w-full')
        text_en_2.set_visibility(False)

        with ui.row():
            ui.button("生成", icon='history', on_click=on_gen_en, color='lightblue')
            ui.button("隐藏", icon='lock', on_click=on_en_disappear, color='lightblue')
            ui.button("显示", icon='visibility', on_click=on_en_display, color='lightblue')
            ui.button("清空", icon='clear', on_click=lambda: text_en.set_value(''), color='lightblue')

ui.separator()

with ui.card().classes('no-shadow border-[3px]'):
    with ui.row():
        ui.button("生成英文语音", icon='audio_file', on_click=on_generate, color='green')
        ui.space()
        ui.space()
        ui.space()
        b1 = ui.button("1倍速播放", icon='play_circle', on_click=lambda: on_play(1), color='lightblue')
        b2 = ui.button("2倍速播放", icon='play_circle', on_click=lambda: on_play(2), color='lightblue')
        b3 = ui.button("3倍速播放", icon='play_circle', on_click=lambda: on_play(3), color='lightblue')
        b4 = ui.button("4倍速播放", icon='play_circle', on_click=lambda: on_play(4), color='lightblue')
        ui.space()
        ui.space()
        ui.space()
        ui.button("听写检查", icon='check', on_click=on_check, color='green')
    
    ui.separator()
    text_writing = ui.textarea("听写区域").classes('w-full').props('clearable').style('color: #6E93D6; font-size: 150%; font-weight: 300')
    result = ui.markdown("")

ui.separator()

# 用于用户输入翻译API的URL
url_trans = ui.input("翻译api").classes('w-full')
url_trans.value = TRANSLATE_API_URL
url_tts = ui.input("TTS api").classes('w-full')
url_tts.value = TTS_API_URL

ui.run(
    native = True,  # 本地运行，不使用浏览器   
    title  = "四倍速英语听力训练 v0.1.0",  # 窗口标题
    reload = False,
    dark   = False,
    window_size = (1800, 1200),
    fullscreen = False,
    favicon = './favicon.ico', # 自定义图标
)       