import wx
from gtts import gTTS
import os
import subprocess

def text_to_speech(text, lang='yue'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    
    # Suppress output by redirecting to os.devnull
    with open(os.devnull, 'w') as devnull:
        subprocess.run(["mpg321", "output.mp3"], stdout=devnull, stderr=devnull)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython + gTTS test", size=(500, 500))
        panel = wx.Panel(self.frame)

        self.button = wx.Button(panel, label="Listen", pos=(200, 200))
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.frame.Show()
        return True

    def on_button_click(self, event):
        text_to_speech("俾我死咗去算啦。")

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()


""" This program is a rough outline of what my real thing is going to do more or less. Basically I need a way to take from a csv or something, and then throw the canto into the tts. """
