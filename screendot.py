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

import datetime
import tkinter
import time
import winsound
import json

class akScreenDot:
    
    def __init__(self, width2, height2):

        self._top = tkinter.Tk()
        self._dot = None
        self.monitorInfo(width2, height2)
        self.canvasSettings()
        self.keyBindings()
        self.subjectSetup()
        self.trialSettings()
        self._connections = None

    def monitorInfo(self, width2, height2):
        self._width1= self._top.winfo_screenwidth()
        self._height1= self._top.winfo_screenheight()
        self._width2 = width2
        self._height2 = height2
        self._top.geometry(f"{self._width2}x{self._height2}")
        # self._top.geometry(f"+0-{self._height2}") # use this to change the window location
        self._fps = 120.0

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
        self._top.bind("q", lambda e: self.cleanUp())
    
    def subjectSetup(self):
        self._dotspeed = 200.0 # pixels/sec
    
    def trialSettings(self):
        self._flag_running = False
        self._flag_complete = False
        
    def setup(self):
        self._canvas.pack()
        self._top.mainloop()

    def clear(self, *args):
        self._top.destroy()
    
    def cleanUp(self):
        self._top.clear()

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
        self._dot_init_pos = [float(self._width2/2), float(self._height2/2)]
        self._dot = self._canvas.create_oval(\
            self._width2/2-rad, self._height2/2-rad, \
            self._width2/2+rad, self._height2/2+rad, \
            fill = "white",
            width = 0)
        self._flag_running = False

    def visualStimulus(self, e=None):
        if not self._dot:
            self.visualStimulusInit()
        self._canvas.itemconfig(self._dot, fill = "red")

    def visualStimulusMotion(self, dir=5, e=None):
        self._flag_running = False
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
        self._flag_running = True
        winsound.Beep(400, 500) # f, t
        self._start_time = datetime.datetime.now()
        self.visualStimulusMotionBind()
    
    def visualStimulusMotionBind(self):

        coor = self._canvas.coords(self._dot)
        coorx, coory = (coor[0] + coor[2]) / 2.0, (coor[1] + coor[3]) / 2.0
        if coorx >= self._width2/2+450 or coorx <= self._width2/2-450 \
            or coory >= self._height2/2+450 or coory <= self._height2/2-450:
            self.trialComplete()
            
        if not self._flag_running:
            self._canvas.delete(self._dot)
            self._canvas.delete('all')
            self._dot = None
            self._canvas.config(bg="black", \
                width=self._width2, height=self._height2, \
                highlightthickness=0, bd=0)
            self._canvas.pack()
            winsound.Beep(400, 500) # f, t
            return
        
        time_elapsed = (datetime.datetime.now() - \
            self._start_time).total_seconds()

        coorx_delta = time_elapsed*self._dotspeed*self._xdirection \
            - (coorx - self._dot_init_pos[0])
        coory_delta = time_elapsed*self._dotspeed*self._ydirection \
            - (coory - self._dot_init_pos[1])
        self._canvas.move(self._dot, coorx_delta, coory_delta)
        
        self._top.after(round((1000.0/self._fps)) , \
            self.visualStimulusMotionBind)

    def trialComplete(self):
        self._flag_running = False
        self._flag_complete = True

    def resetMotionFlag(self):
        self._flag_running = False

if __name__ == "__main__":
    # Use monitorenum.py to determine the second monitor size and locations
    width2, height2 = 2560, 1600
    sd = akScreenDot(width2, height2)
    sd.setup()
