#! /usr/bin/python3

import cgi

class processor():
    def __init__(self, openSymbol, closeSymbol, separator):
        self.closeSymbol	= closeSymbol
        self.openSymbol		= openSymbol
        self.separator		= separator
        self.dictionary        = dict()
        self.functions		= dict()
        self.functions["Get"] = self.Get
        self.functions["For"] = self.For
        self.functions["IfEqual"] = self.IfEqual
        self.functions["RecursiveFor"] = self.RecursiveFor
        self.strict             = True
        self.currentStrings     = dict()
        self.currentString      = str()
        self.ressource          = str()
        self.preProcessedStrings = dict()
        self.patternsIndex      = dict()
        self.errors             = list()

    def SetFunction(self, key, function):
        self.functions[key] = function

    def DelFunction(self, key):
        try:
            del self.functions[key]
        except:
            pass

    def IfEqual(self, argv):
        try:
            if argv[1] == self.dictionary[argv[0]]:
                return argv[2]
        except:
            return str()

    def DelValue(self, key):
        try:
            del self.dictionary[key]
        except:
            pass

    def SetWholeDictionary(self, dictionary):
        for key in dictionary:
            self.dictionary[key] = dictionary[key]

    def Set(self, symbol, value):
       self.dictionary[symbol] = value

    def Get(self, symbol):
        try:
            return self.dictionary[symbol[0]]
        except KeyError:
            return str()

    def For(self, argv):
        outputString = str()
        for Item in self.dictionary[argv[0]]:
            outputString += argv[1].format(Item) + argv[2]

        return outputString[:-len(argv[2])]

    def _RecursiveFor(self, openString, content, separator,closeString, nodes):
        outputString = openString
        for Key in sorted(nodes.keys()):
            variables = dict()
            for key in nodes[Key]:
                if key[:2] == '__':
                    variables[key[2:]] = nodes[Key][key]
            variables["item"] = Key
            if Key != "_nodes":
                if not "_nodes" in nodes[Key].keys():
                    outputString += content.format(variables) + separator
                else:
                    outputString += content.format(variables) + self._RecursiveFor(openString, content, separator, closeString, nodes[Key]["_nodes"])

        return outputString + closeString

    def RecursiveFor(self, argv):
        outputString = str()
        outputString += self._RecursiveFor(
            argv[1],
            argv[2],
            argv[3],
            argv[4],
            self.dictionary[argv[0]]
        )
        return outputString

    def preProcess(self, inputIndex, string):
        self.currentStrings[inputIndex] = str(string)
        self.preProcessedStrings[inputIndex] = list()
        self.patternsIndex[inputIndex] = list()
        closeSymbolPos	= list()
        openSymbolPos	= list()
        i		= int()
        
        while i < len(string):
            if i + len(self.openSymbol) <= len(string) and string[i:i+len(self.openSymbol)] == self.openSymbol:
                openSymbolPos.append(i)

            elif i + len(self.closeSymbol) <= len(string) and string[i:i+len(self.closeSymbol)] == self.closeSymbol:
                closeSymbolPos.append(i)

            if len(closeSymbolPos) == len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                self.preProcessedStrings[inputIndex].append(string[i-closeSymbolPos[-1]:openSymbolPos[0]])
                self.preProcessedStrings[inputIndex].append(string[openSymbolPos[0]:closeSymbolPos[-1]+len(self.closeSymbol)])
                self.patternsIndex[inputIndex].append(len(self.preProcessedStrings[inputIndex])-1)
                
                string = string[closeSymbolPos[-1]+len(self.closeSymbol):]
                openSymbolPos = list()
                closeSymbolPos = list()
                i=0
            else:
                i+=1

        self.preProcessedStrings[inputIndex].append(string)

    def parse(self, inputIndex, escape=False):
        if len(self.patternsIndex) == 0:
            return self.currentStrings[inputIndex]
        
        output = str()

        self.currentString = self.currentStrings[inputIndex]
        for index in range(0,len(self.preProcessedStrings[inputIndex])):
            if index in self.patternsIndex[inputIndex]:
                output += self._process(self.preProcessedStrings[inputIndex][index], escape)
            else:
                output += self.preProcessedStrings[inputIndex][index]

        return output

    def _process(self, string, escape):
        closeSymbolPos	= list()
        openSymbolPos	= list()
        output		= str()
        fields		= list()
        i		= int()


        while i < len(string):
            if i + len(self.openSymbol) <= len(string) and string[i:i+len(self.openSymbol)] == self.openSymbol:
                openSymbolPos.append(i)

            elif i + len(self.closeSymbol) <= len(string) and string[i:i+len(self.closeSymbol)] == self.closeSymbol:
                closeSymbolPos.append(i)

            if len(closeSymbolPos) <= len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                if openSymbolPos[-1] < closeSymbolPos[0]:
                    fields = [field for field in string[openSymbolPos[-1]+len(self.openSymbol):closeSymbolPos[0]].split(self.separator) if field != '']
                    if fields[0] in self.functions.keys():
                        output = self.functions[fields[0]](fields[1:])
                    
                    if escape:
                        return self._process(string[:openSymbolPos[-1]]+cgi.escape(output).encode('ascii', 'xmlcharrefreplace').decode(encoding='ascii')+string[closeSymbolPos[0]+len(self.closeSymbol):],escape=True)
                    else:
                        return self._process(string[:openSymbolPos[-1]]+str(output)+string[closeSymbolPos[0]+2:],escape=False)

            i+=1
    
        return string
