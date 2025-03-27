from gtts import gTTS
import os

def text_to_speech(text, lang='yue'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    #os.system("start output.mp3")  # For Windows
    # os.system("afplay output.mp3")  # For macOS
    os.system("mpg321 output.mp3")  # For Linux

text_to_speech("你好，這是一個粵語語音合成範例。")
