#-*- coding:utf-8 -*-
"""mw_transcode.py
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

class Work(object):
 def __init__(self,line):
  abbrev,name = line.split(':')
  self.abbrev = abbrev.strip() # remove spaces at ends
  self.name = name.strip()
  
def init_recs(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   if line.startswith(';'):
    continue # skip comments
   rec = Work(line)
   recs.append(rec)
 print(len(recs),"Works read from",filein)
 return recs

def capitalize_words(x):
 words = x.split(' ')
 y = [w.capitalize() for w in words]
 z = ' '.join(y)
 return z
     
def transcode_rec(rec,tranin,tranout):
 a,n = (rec.abbrev,rec.name)
 a1 = transcode(a,tranin,tranout)
 n1 = transcode(n,tranin,tranout)
 if tranout == 'roman':
  # capitalize
  a1 = capitalize_words(a1)
  n1 = capitalize_words(n1)
 line = '%s : %s' %(a1,n1)
 return line

if __name__=="__main__":
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 

 recs = init_recs(filein)
 
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   out = transcode_rec(rec,tranin,tranout)
   f.write(out + '\n')
 print(len(recs),"records written to",fileout)
