#! /usr/bin/env python3
import argparse
import os # os.remove
import subprocess as sp

class command:
    cmd      = "exiftool "
    file     = ""
    kwaction = ""
    kwords   = []
    title    = ""
    author   = ""
    out      = ""

    def __init__(self, file):
        self.file = file

    def buildCommand(self):
        self.cmd += self.file
        if self.kwaction != "":
             self.cmd += " -keywords=\""
             self.cmd += ','.join(self.kwords)
             self.cmd += "\""
        if self.title:
            self.cmd += " -Title=\"" + self.title + "\""
        if self.author:
            self.cmd += " -Author=\"" + self.author + "\""
        print("[+] CMD: " + self.cmd)

    def execCommand(self):
        try:
            self.out = sp.check_output(self.cmd, shell=True, text=True)
        except sp.CalledProcessError as cpe:
            print(cpe.output)



class pdfMetadata:
    args = None
    file = None
    cmd  = None

    def __init__(self):
        self.parseArgs()
        self.cmd.title = self.file
        self.cmd.buildCommand()
        self.cmd.execCommand()
        self.clearOriginal()

    def parseArgs(self):
        parser = argparse.ArgumentParser(description="Modify PDF metadata")
        parser.add_argument('-f', '--file', help="PDF file")
        parser.add_argument('-k','--keywords', nargs='+', \
                            help="Add or remove keywords")
        parser.add_argument('-a', '--author', nargs='+', \
                            help="Author of the file, (\"\") to delete")

        self.args = parser.parse_args()

        if not self.args.file:
            parser.error("Must specify a file")

        self.file = self.args.file
        self.cmd  = command(self.file)

        if not '.' in self.args.file or \
        ('.' in self.args.file and self.args.file.split('.')[1]) != "pdf":
            parser.error("Must specify a PDF file")
        if not self.args.keywords and not self.args.author:
            parser.error("One action must be specified (like -k)")
        if  len(self.args.keywords) < 2:
            parser.error("keyword argument must contain one order \
                         [rm, add, clr] and one or more keywords")
        if self.args.keywords[0] not in ['rm', 'add', 'clr']:
            parser.error("-k order not recognized. Accepted: rm, add, clr")

        self.cmd.kwaction = self.args.keywords[0]
        self.cmd.kwords   = self.args.keywords[1:]

        if self.args.author:
            self.cmd.author = ' '.join(self.args.author)

    def clearOriginal(self):
        name = self.file + "_original"
        try:
            os.remove(name)
        except Exception as e:
            print(e)



def main():
    pm = pdfMetadata()


if __name__ == '__main__':
    main()

