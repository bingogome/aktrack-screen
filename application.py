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

from math import pi
from connections import akConnections
from screendot import akScreenDot
import signal
import json

class Application(akConnections):

    def __init__(self):
        super().__init__()
        width2, height2 = 1600, 1200
        self._sd = akScreenDot(width2, height2)
        self._sd._connections = self
        self.keyBindings()
        signal.signal(signal.SIGINT, self.clear)
        signal.signal(signal.SIGTERM, self.clear)

    def setup(self):
        super().setup()
        self._sd.setup()
        
    def clear(self, *args):
        if self._sd._flag_running:
            self._sd.resetMotionFlag()
            self.utilSendJson({"commandtype":"trialStop", \
                "commandcontent":"trialstop"})
        super().clear()
        self._sd._top.destroy()

    def receive(self):
        if self._flag_receiving:
            # print("receiving")
            try:
                self._data_buff = self._sock_receive.recv(2048)
                self.handleReceivedData()
                self._sd._top.after(80, self.receive)
            except:
                self._sd._top.after(80, self.receive)

    def handleReceivedData(self):
        func = self.utilMsgParse()
        func()

    def keyBindings(self):
        self._sd._top.bind("q", lambda e: self.clear())

    def utilSendJson(self, j):
        comm_out = json.dumps(j)
        self._sock_send.sendto(comm_out.encode('UTF-8'), \
            (self._sock_ip, self._sock_port_send))

    def utilSendTextCmdack(self, t):
        self._sock_cmdack.sendto(
            t.encode('UTF-8'), (self._sock_ip, self._sock_port_cmdack))
    
    def utilMsgParse(self):
        data = self._data_buff.decode("UTF-8")
        self._jsondata = json.loads(data)
        if self._jsondata["commandtype"] == "trialcommand":
            return self.utilTrialCommandCallBack
        if self._jsondata["commandtype"] == "trialstopcommand":
            return self.utilTrialCommandStopCallBack

    def utilCheckRunningFlag(self):
        if self._sd._flag_running == True:
            self._sd._top.after(100, self.utilCheckRunningFlag)
        else:
            if self._sd._flag_complete:
                self.utilSendJson({"commandtype":"trialStop", \
                    "commandcontent":"trialcomplete"})
                self._sd._flag_complete = False

    def utilTrialCommandCallBack(self):

        self.utilSendTextCmdack("ack")
        
        msg = self._jsondata["commandcontent"]
        msgarr = msg.split("-")

        def helper(m):
            if m == "R":
                self._sd.visualStimulusMotion(dir=2)
            if m == "L":
                self._sd.visualStimulusMotion(dir=3)
            if m == "U":
                self._sd.visualStimulusMotion(dir=4)
            if m == "D":
                self._sd.visualStimulusMotion(dir=5)

        if msgarr[0] == "VPM":
            self._sd._dotspeed = float(msgarr[1]) * (1.0/180.0*pi*405.0/(1500.0/1600.0))
            # pixels / second, r is the subject-screen dist * 0.3?, n is mm/px: (xdeg/sec) * (1/180*pi*r/n)
            helper(msgarr[2])
            
        if msgarr[0] == "VPC":
            self._sd._dotspeed = 2.0 * (1.0/180.0*pi*405.0/(1500.0/1600.0))   
            # pixels / second, r is the subject-screen dist * 0.3?, n is mm/px: (xdeg/sec) * (1/180*pi*r/n)
            helper(msgarr[1])

        if msgarr[0] == "VPB":
            self._sd.visualStimulusMotion(dir=1)
            self._sd._top.after(1000*5*60, self._sd.trialComplete)
            
        self._sd._top.after(100 , self.utilCheckRunningFlag)
        print("Trial started")

    def utilTrialCommandStopCallBack(self):
        self.utilSendTextCmdack("ack")
        self._sd.resetMotionFlag()
        self.utilSendJson({"commandtype":"trialStop", \
            "commandcontent":"trialstop"})
        
if __name__ == "__main__":
    app = Application()
    app.setup()