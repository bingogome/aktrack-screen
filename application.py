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

from connections import akConnections
from screendot import akScreenDot
import signal

class Application(akConnections):
    def __init__(self):
        super().__init__()
        width2, height2 = 2560, 1440
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
                self._data_buff = self._sock_receive.recv(256)
                self.handleReceivedData()
                self._sd._top.after(50, self.receive)
            except:
                self._sd._top.after(50, self.receive)

    def handleReceivedData(self):
        """
        Will need to be overriden
        """
        return

    def keyBindings(self):
        self._sd._top.bind("q", lambda e: self.clear())
        
    def clear(self, *args):
        super().clear()
        self._sd._top.destroy()

if __name__ == "__main__":
    app = Application()
    app.setup()