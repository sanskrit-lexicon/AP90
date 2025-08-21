# coding=utf-8
""" LBdash.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outarr),"cases written to",fileout)

def change_line(line):
 newline = re.sub(r'[(]{#--([^#]*)#}[)]',
                  r'{#--(\1)#}',line)
 return newline

if __name__=="__main__":
 filein = sys.argv[1]  # xxx.txt
 fileout = sys.argv[2] # output file  adjusted xxx
 lines = read_lines(filein)
 newlines = [change_line(line) for line in lines]
 write_lines(fileout,newlines)
 

