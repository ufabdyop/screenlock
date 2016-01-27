#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, sys
import logging
import struct
import threading
import Queue
import pprint

def print_bytes(b_list):
    buffer = ''
    for b in b_list:
        buffer += str(b) + ','
    return buffer.strip(',')

class SocketClient(object):

    """ Implements the threading.Thread interface (start, join, etc.) and
        can be controlled via the cmd_q Queue attribute. Replies are
        placed in the reply_q Queue attribute.
    """

    def __init__(self, host, port):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.logger = logging.getLogger('SocketClient')
        self.socket = socket.socket(socket.AF_INET,
                socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    def send(self, cmd):
        try:
            self.logger.debug('sending bytes %s'
                              % print_bytes(cmd))
            self.socket.sendall(cmd)
            self.receiveall(cmd, 1)
        except IOError, e:
            print("Error")
            pprint.pprint(e)

    def receiveall(self, cmd, msg_len):
        try:
            data = self._recv_min(msg_len)
            self.logger.debug('got response bytes %s'
                              % print_bytes(bytearray(data)))
            if len(data) == msg_len:
                return
            self.logger.error('Expected %s bytes, but got %s bytes'
                              % (msg_len, len(data)))
            print('Socket closed prematurely: %s' \
                % bytearray(data))
        except IOError, e:
            print('Socket receive error: %s' \
                % bytearray(data))

    def _recv_min(self, length):
        data = self.socket.recv(length)
        buffer = ''
        buffer += data
        while len(buffer) < length:
            data = self.socket.recv(length - len(buffer))
            buffer += data

        return buffer

def main():
    if len(sys.argv) != 5:
        print("usage: ncdClient host port byte1 byte2")
        print("example (lock): ncdClient host port 250 1")
        print("example (unlock): ncdClient host port 250 9")
        print("example (sense): ncdClient host port 250 17")
        print("got %s args" % len(sys.argv))
        sys.exit(1)
    host = sys.argv[1]
    port = sys.argv[2]
    byte1 = int(sys.argv[3])
    byte2 = int(sys.argv[4])
    print("Sending [%s, %s] to %s:%s" % (byte1, byte2, host, int(port)))
    sc = SocketClient(host, int(port))
    sc.send(bytearray([byte1, byte2]))
    sc.close()

main()