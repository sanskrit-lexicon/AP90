#-*- coding:utf-8 -*-
"""hyphen3.py  for ap90
 
"""
import sys,re,codecs

class Change(object):
 def __init__(self,metaline,page,iline1,line1,iline2,line2):
  self.metaline = metaline
  self.page = page
  self.i1 = iline1
  self.old1 = line1
  self.i2 = iline2
  self.old2 = line2
  self.new1 = None
  self.new2 = None
 
def init_changes(lines):
 changes = [] # array of Change objects
 iline1 = None
 metaline = None
 page = None
 for iline,line in enumerate(lines):
  line = line.rstrip('\r\n')
  if line.startswith('<L>'):
   metaline = line
   iline1 = None
   continue
  if line == '<LEND>':
   metaline = None
   iline1 = None
   continue
  if line.startswith('[Page'):
   page = line
   continue  
  #if metaline == None:
  # iline1 = None
  # continue
  if iline1 != None:
   change = Change(metaline,page,iline1,line1,iline,line)
   compute_new(change)
   changes.append(change)
   if change.new2 != None:
    line = change.new2
  if re.search(r'^(.*?){#--#}$',line):
   iline1 = iline
   line1 = line
  else:
   iline1 = None
 print(len(changes),'potential changes found')
 return changes

def compute_new(change):
 """compute new1 and new2
  This version assumes that:
  old1 = a1 + '{#--#}',  
  old2 = '<>{#' + b1
          
  Construct:
   trace = '--'  The '#' a reminder of Devanagari
   new1 = a1 + ' ' + <lbinfo n="trace"/>
   new2 = '<>{#--' b1 

 """
 m1 = re.search(r'^(.*?){#--#}$',change.old1)
 if not m1:
  print('hyphen3 ERROR 1')
  exit(1)
 a1 = m1.group(1)
 m2 = re.search(r'^<>{#(.*)$',change.old2)
 if not m2:
  print('hyphen3 ERROR 2')
  exit(1)
 b1 = m2.group(1)
 trace0 = '--' 
 trace = ' <lbinfo n="%s"/>'% trace0
 change.new1 = a1 + trace
 change.new2 = '<>{#--' + b1
 
def change_out_todo(change,ichange):
 assert (change.new1 == None)
 outarr = []
 case = ichange + 1
 outarr.append('; TODO Case %s ' % case)
 ident = change.metaline
 if ident == None:
  ident = change.page
 outarr.append('; ' + ident)
 lnum = change.i1 + 1
 outarr.append('%s old %s' % (lnum,change.old1))
 outarr.append('%s new %s' % (lnum,change.old1))
 outarr.append(';')
 lnum = change.i2 + 1
 outarr.append('%s old %s' % (lnum,change.old2))
 outarr.append('%s new %s' % (lnum,change.old2))
 outarr.append(';')
 return outarr
 
def change_out(change,ichange):
 assert (change.new1 != None) 
 outarr = []
 case = ichange + 1
 #outarr.append('; TODO Case %s: %s -> %s' % (case,change.wordold,change.wordnew))
 outarr.append('; TODO Case %s' % (case,))
 ident = change.metaline
 if ident == None:
  ident = change.page
 outarr.append('; ' + ident)
 lnum = change.i1 + 1
 outarr.append('%s old %s' % (lnum,change.old1))
 outarr.append('%s new %s' % (lnum,change.new1))
 outarr.append(';')
 lnum = change.i2 + 1
 outarr.append('%s old %s' % (lnum,change.old2))
 outarr.append('%s new %s' % (lnum,change.new2))
 outarr.append(';')
 return outarr

def write_changes(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
  for ichange,change in enumerate(changes):
   outarr = change_out(change,ichange)
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),"written to",fileout)

def write_changes_todo(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
  for ichange,change in enumerate(changes):
   outarr = change_out_todo(change,ichange)
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),"written to",fileout)

def write_newwords(fileout,changes):
 # get distinct new words
 words = {}
 for c in changes:
  w = c.wordnew
  if w not in words:
   words[w] = 0
  words[w] = words[w] + 1
 keys = sorted(words.keys())
 with codecs.open(fileout,"w","utf-8") as f:
  for w in keys:
   out = '%s %s' %(w,words[w])
   f.write(out + '\n')
 print(len(keys),'records written to',fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # possible change transactions
 fileout1 = sys.argv[3] # anomalous
 #fileout2 = sys.argv[4] # new words (by removing hyphen)
 n = 0
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 changes = init_changes(lines)
 changes_done = [c for c in changes if (c.new1 != None)]
 write_changes(fileout,changes_done)
 changes_todo = [c for c in changes if c.new1 == None]
 write_changes_todo(fileout1,changes_todo)
