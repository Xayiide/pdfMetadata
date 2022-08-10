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
    subject  = ""
    out      = ""

    def __init__(self, file):
        self.file = file

    def buildCommand(self):
        self.cmd += self.file
        keywords  = self.parseKeywords()
        self.cmd += keywords
        self.cmd += self.parseTitle()
        self.cmd += self.parseAuthor()
        self.cmd += self.parseSubject()

        print("[+] ", keywords)

    def parseKeywords(self):
        keywords = " -keywords=\"{}\""
        if   self.kwaction == "clr":
            keywords = keywords.format("")
        elif self.kwaction == "add":
            keywords = keywords.format(','.join(self.kwords))
        return keywords

    def parseTitle(self):
        title = ""
        if self.title:
            title = " -Title=\"{}\""
            title = title.format(self.title)
        return title

    def parseAuthor(self):
        author = ""
        if self.author:
            author = " -Author=\"{}\""
            author = author.format(self.author)
        return author

    def parseSubject(self):
        subject = ""
        if self.subject:
            subject = " -Subject=\"{}\""
            subject = subject.format(self.subject)
        return subject

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
        parser.add_argument('-s', '--subject', nargs='+', \
                            help="Add subject")

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
        if self.args.keywords[0] == "clr" and len(self.args.keywords) > 1:
            parser.error("'-k clr' does not accept keywords")
        if self.args.keywords[0] == "rm" and len(self.args.keywords) < 2:
            parser.error("'-k rm' must contain at least one keyword")
        if self.args.keywords[0] not in ['add', 'clr']:
            parser.error("-k needs one of these orders: rm, add, clr")

        self.cmd.kwaction = self.args.keywords[0]
        aux = self.args.keywords[1:]
        self.cmd.kwords = [w.strip() for w in ' '.join(aux).split(',')]

        if self.args.author:
            self.cmd.author = ' '.join(self.args.author)

        if self.args.subject:
            self.cmd.subject = ' '.join(self.args.subject)

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

