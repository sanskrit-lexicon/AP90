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

def wrong_capitalize_words(x):
 """ This doesn't handle extended Ascii"""
 parts = re.split(r'\b([a-zA-Z]+)\b',x)
 newparts = []
 for part in parts:
  if re.search(r'^[a-zA-Z]+$',part):
   newparts.append(part.capitalize())
  else:
   newparts.append(part)
 z = ''.join(newparts)
 return z

def capitalize_words(x0):
 x = x0.replace('(','( ')
 #x = x.replace(')',' )')
 words = x.split(' ')
 y = [w.capitalize() for w in words]
 z = ' '.join(y)
 z = z.replace('( ','(')
 return z

def transcode_abbrev(a,tranin,tranout):
 a1 = transcode(a,tranin,tranout)
 if tranout == 'roman':
  # capitalize
  a1 = capitalize_words(a1)
 return a1

def transcode_name(a,tranin,tranout):
 """ Leave <X> as X (English text X unchanged)
 """
 parts = re.split(r'(<.*?>)',a)
 newparts = []
 for part in parts:
  if part.startswith('<'):
   newparts.append(part[1:-1])  # <X> -> X
  else:
   # same as for abbreviations
   newpart = transcode_abbrev(part,tranin,tranout)
   newparts.append(newpart)
 # reconstruct
 ans = ''.join(newparts)
 return ans

def transcode_rec(rec,tranin,tranout):
 a,n = (rec.abbrev,rec.name)
 a1 = transcode_abbrev(a,tranin,tranout)
 n1 = transcode_name(n,tranin,tranout)
 line = '%s : %s' %(a1,n1)
 return line

def transcode_rec_version0(rec,tranin,tranout):
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
