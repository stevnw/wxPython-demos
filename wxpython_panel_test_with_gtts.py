import wx
from gtts import gTTS
import os
import subprocess

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='wxPython panel demo with gTTS')
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # panel switch buttons
        self.button1 = wx.Button(self.panel, label='Show Panel 1')
        self.button2 = wx.Button(self.panel, label='Show Panel 2')

        self.sizer.Add(self.button1, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.button2, 0, wx.ALL | wx.CENTER, 5)

        # panel logic
        self.panel1 = wx.Panel(self.panel)
        self.panel1.SetBackgroundColour('light blue')
        self.panel1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel1_sizer.Add(wx.StaticText(self.panel1, label='This is Panel 1'), 0, wx.ALL | wx.CENTER, 5)
        
        # panel 1 gtts shite
        self.gtts_button1 = wx.Button(self.panel1, label='Say Yes in Cantonese')
        self.panel1_sizer.Add(self.gtts_button1, 0, wx.ALL | wx.CENTER, 5)
        
        self.panel1.SetSizer(self.panel1_sizer)

        self.panel2 = wx.Panel(self.panel)
        self.panel2.SetBackgroundColour('light green')
        self.panel2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel2_sizer.Add(wx.StaticText(self.panel2, label='This is Panel 2'), 0, wx.ALL | wx.CENTER, 5)
        
        # panel 2 gtts shite
        self.gtts_button2 = wx.Button(self.panel2, label='Say No in Cantonese')
        self.panel2_sizer.Add(self.gtts_button2, 0, wx.ALL | wx.CENTER, 5)
        
        self.panel2.SetSizer(self.panel2_sizer)

        self.sizer.Add(self.panel1, 1, wx.EXPAND)
        self.sizer.Add(self.panel2, 1, wx.EXPAND)

        self.panel.SetSizer(self.sizer)

        # panel 1 is default
        self.panel2.Hide()

        self.button1.Bind(wx.EVT_BUTTON, self.on_show_panel1)
        self.button2.Bind(wx.EVT_BUTTON, self.on_show_panel2)
        
        self.gtts_button1.Bind(wx.EVT_BUTTON, self.say_yes_cantonese)
        self.gtts_button2.Bind(wx.EVT_BUTTON, self.say_no_cantonese)

        self.Show()

    def on_show_panel1(self, event):
        self.panel1.Show()
        self.panel2.Hide()
        self.panel.Layout()

    def on_show_panel2(self, event):
        self.panel2.Show()
        self.panel1.Hide()
        self.panel.Layout()

    def say_yes_cantonese(self, event):
        tts = gTTS(text='係', lang='yue')
        tts.save('yes.mp3')
        # subprocess so no terminal spam
        subprocess.run(['mpg321', 'yes.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def say_no_cantonese(self, event):
        tts = gTTS(text='唔係', lang='yue')
        tts.save('no.mp3')
        subprocess.run(['mpg321', 'no.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
