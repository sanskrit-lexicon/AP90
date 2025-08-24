# coding=utf-8
""" generate alternate headwords from <k2>X, Y
"""
from __future__ import print_function
import sys, re,codecs
import digentry1

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outarr),"cases written to",fileout)

def unused_outrec_entry(entry):
 outarr = []
 outarr.append(entry.metaline)
 for line in entry.datalines:
  outarr.append(line)
 outarr.append(entry.lend)
 return outarr

def unused_outrec_nonentry(nonentry):
 outarr = []
 outarr.append(nonentry.line)
 return outarr

def write_recs(fileout,dparents):
 outlines = []
 for Lparent in dparents:
  rec = digentry1.Entry.Ldict[Lparent]
  althw = dparents[Lparent]
  children = althw.children
  nc = len(children)
  assert Lparent == rec.metad['L']
  # outline = '%s : %s' %(rec.metaline,nc)
  k1p = rec.metad['k1']
  k2p = rec.metad['k2']
  a = []
  for Lchild in children:
   crec = digentry1.Entry.Ldict[Lchild]
   k1c = crec.metad['k1']
   if ' ' in k1c:
    print('write_recs ERROR.Lparent=%s, child=%s' % (Lparent,Lchild))
    print('children=',children)
    print('k1c="%s"' % k1c)
    exit(1)
   #assert ' ' not in k1c
   a.append(k1c)
  if len(a) == 0:
   aj = '?'
  else:
   aj = ' '.join(a)
  outfields = [Lparent,k2p,k1p,str(nc),aj]
  outline = ' : '.join(outfields)
  outlines.append(outline)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outlines:
    f.write(out+'\n')
 print('%s lines written to %s' %(len(outlines),fileout))

class ALTHW:
 def __init__(self,Lparent):
  self.Lparent = Lparent
  self.children = []
  

def get_parents(recs):
 d = {} 
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   continue
  assert type(rec) == digentry1.Entry
  L = rec.metad['L']
  m = re.search(r'^[a-zA-Z|]+$',rec.metad['k2'])
  if (m != None): # and (L != '10066'):
   # normal headword, no implied alternate headwords
   continue
  assert L not in d
  d[L] = ALTHW(L)
 keys = list(d.keys())
 print(len(keys),"parents")
 return d

def get_children(recs):
 d = {}
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   continue
  assert type(rec) == digentry1.Entry
  # recognize an alternate headword entry
  if len(rec.datalines) != 1:
   continue
  dataline = rec.datalines[0]
  m = re.search(r'^{{Lbody=(.*)}}$',dataline)
  if m == None:
   continue
  ## rec is an alternate headword entry
  Lparent = m.group(1)
  L = rec.metad['L']  # child L
  #d[L] = (Lparent,rec)
  d[L] = Lparent
 keys = list(d.keys())
 print(len(keys),"children")
 return d

def parents_and_children(dp,dc):
 for Lchild in dc:
  Lparent = dc[Lchild]
  if Lparent not in dp:
   print('get_althws ERROR. %s not a parent for Lchild=%s' %(Lparent,Lchild))
   continue
  althw = dp[Lparent]
  althw.children.append(Lchild)
if __name__=="__main__":
 filein = sys.argv[1]  #ap90.txt
 fileout = sys.argv[2] # output file 
 recs = digentry1.init(filein)
 dparents = get_parents(recs) # d[Lparent] = althw
 dchildren = get_children(recs) # d[Lchild] = Lparent
 parents_and_children(dparents,dchildren) # revise dparents
 write_recs(fileout,dparents)

