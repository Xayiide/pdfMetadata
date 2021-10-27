#! /usr/bin/env python3
import PyPDF2
import argparse
import os.path

class keywords:
    action   = ""
    keywords = []

    def __init__(self, action, keywords):
        self.action   = action
        self.keywords = keywords

    def modify(self):
        print(":D")

class pdfMetadata:
    args = None
    name = None
    file = None
    keywords = None

    def __init__(self):
        self.parseArgs()
        self.openFile()
        if keywords != None:
            self.keywords.modify()




    def parseArgs(self):
        parser = argparse.ArgumentParser(description="Modify PDF metadata")
        parser.add_argument('-f', '--file', help="PDF file")
        parser.add_argument('-k','--keywords', nargs='+', \
                            help="Add or remove keywords")

        self.args = parser.parse_args()

        if not self.args.file:
            parser.error("Must specify a file")

        self.name = self.args.file

        if not '.' in self.args.file or \
        ('.' in self.args.file and self.args.file.split('.')[1]) != "pdf":
            parser.error("Must specify a PDF file")
        if not self.args.keywords:
            parser.error("One action must be specified (like -k)")
        if  len(self.args.keywords) < 2:
            parser.error("keyword argument must contain one order \
                         [rm, add, clr] and one or more keywords")
        if self.args.keywords[0] not in ['rm', 'add', 'clr']:
            parser.error("-k order not recognized. Accepted: rm, add, clr")

        a = self.args.keywords[0]
        k = self.args.keywords[1:]
        self.keywords = keywords(a, k)

    def openFile(self):
        if not os.path.isfile(self.name):
            print("Specified file does not exist")
            exit()
        else:
            self.file = open(self.name)


def main():
    pm = pdfMetadata()


if __name__ == '__main__':
    main()
