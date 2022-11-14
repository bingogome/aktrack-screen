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

import socket
import signal

class akConnections:

    def __init__(self):
        self._sock_port_receive = 8753
        self._sock_port_send = 8757
        self._sock_port_cmdack = 8769

        self._sock_ip = "localhost"

        self._sock_receive = None
        self._sock_cmdack = None
        self._sock_send = None

        self._flag_receiving = False
        self._data_buff = None
        signal.signal(signal.SIGINT, self.clear)
        signal.signal(signal.SIGTERM, self.clear)

    def setup(self):
        self._sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock_cmdack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        self._sock_receive.bind((self._sock_ip, self._sock_port_receive))
        self._sock_receive.setblocking(0)
        self._flag_receiving = True
        print("Sockets opened")
        self.receive()

    def clear(self, *args):
        self._flag_receiving = False
        if self._sock_receive:
            self._sock_receive.close()
        if self._sock_send:
            self._sock_send.close()
        print("Sockets closed")

    def receive(self):
        """
        Will need to be overriden
        """
        while self._flag_receiving:
            # print("receiving")
            try:
                self._data_buff = self._sock_receive.recv(2048)
                self.handleReceivedData()
            except:
                pass

    def handleReceivedData(self):
        """
        Will need to be overriden
        """
        return


if __name__ == "__main__":
    connections = akConnections()
    connections.setup()