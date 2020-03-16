#-*- coding:utf-8 -*-
"""util_mw.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None
  
def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def mark_entries(entries,hws):
 d = {}
 hwrecs = []
 for ihw,hw in enumerate(hws):
  d[hw] = ihw
  hwrecs.append([hw,None])

 for entry in entries:
  k1  = entry.metad['k1']
  if k1 in d:
   entry.marked = True
   ihw = d[k1]
   hwrec = hwrecs[ihw]
   hwrec[1] = entry
  
 return hwrecs

def write_lines(fileout,hwrecs):
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for ihw0,hwrec in enumerate(hwrecs):
   hw,entry = hwrec
   if entry == None:
    outarr = []
    outarr.append('; %s not found'%hw)
    outarr.append(';')
   else:
    n = n + 1
    outarr = [entry.metaline]
    for iline,line in enumerate(entry.datalines):
     if iline < 2:
      outarr.append(';' + entry.datalines[iline]) # first line
    outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
 print('%04d' %n,"records written to",fileout)

def init_hws(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [line.rstrip() for line in f]
 print(len(recs),"records read from",filein)
 return recs

def init_hws1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip() for line in f]
 recs = []
 for line in lines:
  m = re.search('k1=([a-zA-Z|]+)',line)
  if m:
   k1 = m.group(1)
   recs.append(k1)

 print(len(recs),"records read from",filein)
 return recs

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # file containing possible headwords
 fileout = sys.argv[3] # 
 entries = init_entries(filein)
 hws = init_hws1(filein1)
 hwrecs = mark_entries(entries,hws)
 write_lines(fileout,hwrecs)
