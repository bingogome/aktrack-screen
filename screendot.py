"""
MIT License
Copyright (c) 2022 Yihao Liu, Johns Hopkins University
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter
import time
import winsound

class akScreenDot:
    
    def __init__(self, width2, height2):

        self._top = tkinter.Tk()
        self._dot = None
        self.monitorInfo(width2, height2)
        self.canvasSettings()
        self.keyBindings()
        self.subjectSetup()

    def monitorInfo(self, width2, height2):
        self._width1= self._top.winfo_screenwidth()
        self._height1= self._top.winfo_screenheight()
        self._width2 = width2
        self._height2 = height2
        self._top.geometry(f"{self._width2}x{self._height2}")
        # self._top.geometry(f"+0-{self._height2}") # use this to change the window location
    
    def canvasSettings(self):
        self._canvas = tkinter.Canvas(self._top, bg="black", \
            width=self._width2, height=self._height2, \
            highlightthickness=0, bd=0)

    def keyBindings(self):
        self._top.bind("a",  lambda e: self.fullScreen())
        self._top.bind("d",  lambda e: self.visualStimulusInit())
        self._top.bind("s",  lambda e: self.visualStimulusMotion(1))
        self._top.bind("<KeyPress-Right>",  lambda e: self.visualStimulusMotion(2))
        self._top.bind("<KeyPress-Left>",  lambda e: self.visualStimulusMotion(3))
        self._top.bind("<KeyPress-Up>",  lambda e: self.visualStimulusMotion(4))
        self._top.bind("<KeyPress-Down>",  lambda e: self.visualStimulusMotion(5))
        self._top.bind("<Escape>",  lambda e: self.resetMotionFlag())
        self._top.bind("q", lambda e: self._top.destroy())
    
    def subjectSetup(self):
        self._dotspeed = 500.0 # pixels/sec
        
    def setup(self):
        self._canvas.pack()
        self._top.mainloop()

    def clear(self, *args):
        self._top.destroy()

    def fullScreen(self, e=None):
        self._top.attributes("-topmost", 1)
        self._top.attributes("-fullscreen", True)

    def visualStimulusInit(self, e=None):
        rad = 10
        if self._dot:
            self._canvas.delete(self._dot)
            self._canvas.delete('all')
            self._dot = None
            self._canvas.config(bg="black", \
                width=self._width2, height=self._height2, \
                highlightthickness=0, bd=0)
            self._canvas.pack()
        
        self._dot = self._canvas.create_oval(\
            self._width2/2-rad, self._height2/2-rad, \
            self._width2/2+rad, self._height2/2+rad, \
            fill = "white",
            width = 0)
        self._flagMotion = False

    def visualStimulus(self, e=None):
        if not self._dot:
            self.visualStimulusInit()
        self._canvas.itemconfig(self._dot, fill = "red")

    def visualStimulusMotion(self, dir=5, e=None):
        self._flagMotion = False
        self.visualStimulus()
        if dir == 1:
            self._xdirection, self._ydirection = 0, 0
        if dir == 2:
            self._xdirection, self._ydirection = 1, 0
        if dir == 3:
            self._xdirection, self._ydirection = -1, 0
        if dir == 4:
            self._xdirection, self._ydirection = 0, -1
        if dir == 5:
            self._xdirection, self._ydirection = 0, 1
        self._flagMotion = True
        winsound.Beep(400, 500) # f, t
        self.visualStimulusMotionBind()
    
    def visualStimulusMotionBind(self):
        start = time.process_time()
        if not self._flagMotion:
            self._canvas.delete(self._dot)
            self._canvas.delete('all')
            self._dot = None
            self._canvas.config(bg="black", \
                width=self._width2, height=self._height2, \
                highlightthickness=0, bd=0)
            self._canvas.pack()
            winsound.Beep(400, 500) # f, t
            return
        # frame time is 5.0 msec (200 fps)
        self._canvas.move(self._dot, \
            0.005*self._dotspeed*self._xdirection, \
            0.005*self._dotspeed*self._ydirection)
        overhead = time.process_time() - start
        # frame time is 5.0 msec
        self._top.after(round(5.0 - overhead) , \
                self.visualStimulusMotionBind)

    def resetMotionFlag(self):
        self._flagMotion = False

if __name__ == "__main__":
    # Use monitorenum.py to determine the second monitor size and locations
    width2, height2 = 2560, 1600
    sd = akScreenDot(width2, height2)
    sd.setup()
