#! /usr/bin/python3

class Termination(Exception):
    pass

class NonHtml(Exception):
    pass

class MainControler:
    def __init__(self):
        self.verbose = True
        self.call = 0

    def GetResponse(self, path):
        if path == "/":
            self.call += 1
            return str(self.call)

        else:
            raise NonHtml

