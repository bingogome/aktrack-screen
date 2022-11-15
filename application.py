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
        self._connections = akConnections()
        self.keyBindings()
        signal.signal(signal.SIGINT, self.clear)
        signal.signal(signal.SIGTERM, self.clear)

    def setup(self):
        super().setup()
        self._sd.setup()
    
    def receive(self):
        if self._flag_receiving:
            # print("receiving")
            try:
                self._data_buff = self._sock_receive.recv(2048)
                self.handleReceivedData()
                self._sd._top.after(50, self.receive)
            except:
                self._sd._top.after(50, self.receive)

    def handleReceivedData(self):
        """
        Will need to be overriden
        """
        func = self.utilMsgParse()
        func()
    
    def utilMsgParse(self):
        data = self._data_buff.decode("UTF-8")
        self._jsondata = json.loads(data)
        if self._jsondata["commandtype"] == "trialcommand":
            return self.utilTrialCommandCallBack
        if self._jsondata["commandtype"] == "trialstopcommand":
            return self.utilTrialCommandStopCallBack

    def utilTrialCommandCallBack(self):
        msg = "ack"
        self._sock_cmdack.sendto(
                msg.encode('UTF-8'), (self._sock_ip, self._sock_port_cmdack))
        msg = self._jsondata["commandcontent"]
        msgarr = msg.split("-")
        if msgarr[0] == "VPM":
            self._sd._dotspeed = float(msgarr[1]) * (1.0/180.0*pi*405.0/(1500.0/1600.0))
            # pixels / second, r is the subject-screen dist * 0.3?, n is mm/px: (xdeg/sec) * (1/180*pi*r/n)
            if msgarr[2] == "R":
                self._sd.visualStimulusMotion(dir=2)
            if msgarr[2] == "L":
                self._sd.visualStimulusMotion(dir=3)
            if msgarr[2] == "U":
                self._sd.visualStimulusMotion(dir=4)
            if msgarr[2] == "D":
                self._sd.visualStimulusMotion(dir=5)
        if msgarr[0] == "VPC":
            self._sd._dotspeed = 2.0 * (1.0/180.0*pi*405.0/(1500.0/1600.0))   
            # pixels / second, r is the subject-screen dist * 0.3?, n is mm/px: (xdeg/sec) * (1/180*pi*r/n)
            if msgarr[1] == "R":
                self._sd.visualStimulusMotion(dir=2)
            if msgarr[1] == "L":
                self._sd.visualStimulusMotion(dir=3)
            if msgarr[1] == "U":
                self._sd.visualStimulusMotion(dir=4)
            if msgarr[1] == "D":
                self._sd.visualStimulusMotion(dir=5)

    def utilTrialCommandStopCallBack(self):
        msg = "ack"
        self._sock_cmdack.sendto(
                msg.encode('UTF-8'), (self._sock_ip, self._sock_port_cmdack))
        self._sd.resetMotionFlag()
        comm = {"commandtype":"trialStop", \
            "commandcontent":"trialstop"}
        comm_out = json.dumps(comm)
        self._sock_send.sendto(
            comm_out.encode('UTF-8'), (self._sock_ip, self._sock_port_send))

    def keyBindings(self):
        self._sd._top.bind("q", lambda e: self.clear())
        
    def clear(self, *args):
        super().clear()
        self._sd._top.destroy()

if __name__ == "__main__":
    app = Application()
    app.setup()