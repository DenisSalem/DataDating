#! /usr/bin/python3

import os
import io
import sys
import cgi
import socketserver

from DataDating.Controler.RequestHandler import RequestHandler
from DataDating.Controler.MainControler import Termination

class Server(socketserver.TCPServer):
    def __init__(self):
        self.allow_reuse_address = True
        super(Server, self).__init__(("127.0.0.1",8282), RequestHandler)

    def handle_error(self, request, client_address):
        if sys.exc_info()[0] == Termination:
            raise Termination()
        
        else:
            super(Server, self).handle_error(request, client_address)
        
