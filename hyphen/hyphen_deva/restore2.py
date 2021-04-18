#-*- coding:utf-8 -*-
"""restore2.py  for ap90
 
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
  self.wordold = None  # the hyphenated word
  self.wordnew = None  # the unhyphenated word
  

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
  if iline1 != None:
   change = Change(metaline,page,iline1,line1,iline,line)
   compute_new(change)
   changes.append(change)
   if change.new2 != None:
    line = change.new2
  m = re.search(r'^(.*) <lbinfo n="(.*?)#(.*?)"/>',line)
  if m and (not m.group(2).startswith('--')):
   iline1 = iline
   line1 = line
  else:
   iline1 = None
 print(len(changes),'potential changes found')
 #exit(1)
 return changes

def compute_new(change):
 """compute new1 and new2
  This version assumes that:
  old1 = a1 + a2 + ' ' + <lbinfo n="x#y"/> 
     a2 is one character, either  '}' or not
  old2 = '<>' '{#'+ x + y + b1
  Construct:
   if a2 is not '}':
    new1 = a1 + '{#' + x + '-#}'
    new2 = '<>{#' + y + b1
   if as is '}':
    a3 = a1[0:-1]  # drop
    a4 = a1[-1] should be '#'
    new1 = a3 + x + '-#}
    new2 = '<>{#' + y + b1
 """
 # Note the space before lbinfo
 m1 = re.search(r'^(.*)(.) <lbinfo n="(.*?)#(.*?)"/>',change.old1)
 if not m1:
  return
 a1 = m1.group(1)
 a2 = m1.group(2)
 """
 if a2 not in ' }':
  # error
  print('ERROR 1: ',change.metaline)
  print('a2="%s"' %a2)
  print(change.i1,change.old1)
  print(change.i2,change.old2)
  exit(1)
 """
 x = m1.group(3)
 y = m1.group(4)
 a5 = x + y
 regex = r'^<>{#' + a5 + '(.*)$'
 #regex = re.sub(r"'",r"''",regex)  # since ' may be in a5
 try:
  m2 = re.search(regex,change.old2)
 except:
  print('re error: regex=',regex)
  exit(1)
 if not m2:
  # error
  print('ERROR 2: ',change.metaline)
  print('regex=',regex)
  print(change.i1,change.old1)
  print(change.i2,change.old2)
  exit(1)
 b1 = m2.group(1)
 if a2 != '}':
  change.new1 = a1 + a2 + '{#' + x + '-#}'
  change.new2 = new2 = '<>{#' + y + b1
 else: # a2='}'
  a3 = a1[0:-1]
  a4 = a1[-1]
  assert a4 == '#'
  change.new1 = a3 + x + '-#}'
  change.new2 = new2 = '<>{#' + y + b1
  
def change_out(change,ichange):
 assert (change.new1 != None) 
 outarr = []
 case = ichange + 1
 outarr.append('; Case %s' % (case,))
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
 #fileout1 = sys.argv[3] # anomalous
 #fileout2 = sys.argv[4] # new words (by removing hyphen)
 n = 0
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 changes = init_changes(lines)
 #changes_done = [c for c in changes if (c.new1 != None)]
 write_changes(fileout,changes)
 #changes_todo = [c for c in changes if c.new1 == None]
 #write_changes_todo(fileout1,changes_todo)
