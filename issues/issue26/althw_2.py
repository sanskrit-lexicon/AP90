# coding=utf-8
""" althw_2.py 
  generate alternate headwords from <k2>X, Y
"""
from __future__ import print_function
import sys, re,codecs
import digentry1

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines from",filein)
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outarr),"cases written to",fileout)

def outrec_entry(entry):
 outarr = []
 outarr.append(entry.metaline)
 for line in entry.datalines:
  outarr.append(line)
 outarr.append(entry.lend)
 return outarr

def outrec_nonentry(nonentry):
 outarr = []
 outarr.append(nonentry.line)
 return outarr

def write_recs(fileout,recs):
 n1 = 0 # number of Entry records
 n2 = 0 # number of nonEntry records
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   if type(rec) == digentry1.Entry:
    outlines = outrec_entry(rec)
    n1 = n1 + 1
   elif type(rec) == digentry1.nonEntry:
    outlines = outrec_nonentry(rec)
    n2 = n2 + 1
   for out in outlines:
    f.write(out+'\n')
 print('write_recs output to',fileout)
 print('%s Entry records, %s nonEntry records' %(n1,n2))

def althws(recs,daltins):
 newrecs = []
 newparents = []
 for irec,rec in enumerate(recs):
  if type(rec) == digentry1.nonEntry:
   # no change
   newrecs.append(rec)
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  L = entry.metad['L']
  if not L in daltins:
   # no change
   newrecs.append(rec)
   continue
  altin = daltins[L]
  if altin.sourcecode in ['-0','00']:
   # this alternate headword candidate previously marked
   newrecs.append(rec)
   continue
  assert L == altin.Lparent
  entry1 = recs[irec+1] # next entry
  assert type(entry1) == digentry1.Entry
  L1 = entry1.metad['L']
  assert '.' not in L1  # L1 should be a digit sequence
  # we have room for no more than 9 children
  children = altin.children
  nc = len(children)
  assert 0 < nc < 10
  # add rec to newrecs, since we keep the parent
  newrecs.append(rec)
  # for documentation, keep this parent
  newparents.append(nc)
  # contruct lines of a new entry for each child
  newlines = []
  for ic,c in enumerate(children):
   # c is k1
   Lc = '%s.%s' %(L,ic+1)  # so 123.1, 123.2, etc
   pc = entry.metad['pc']  # same pc as parent
   k1c = c
   k2c = k1c  # so no longer recognized as an althw parent
   meta_new = '<L>%s<pc>%s<k1>%s<k2>%s' %(Lc,pc,k1c,k2c)
   body_new = '{{Lbody=%s}}' % L  # parent L
   lend_new = '<LEND>'
   newlines = [meta_new,body_new,lend_new]
   for newline in newlines:
    # insert newline as a nonEntry into newrecs
    linenum_dummy = 0 # unused
    nonentry = digentry1.nonEntry(newline,linenum_dummy)
    newrecs.append(nonentry)
 nctot = sum(newparents)
 nalt  = len(newparents)
 print('%s althw entries constructed from %s parents' % (nctot,nalt))
 return newrecs

class ALTIN:
 def __init__(self,line):
  parts = line.split(' : ')
  if len(parts) != 6:
   print('ALTIN error. got %s parts, expected %s' %(len(parts),5))
   exit(1)
  self.sourcecode = parts[0]
  self.Lparent = parts[1]
  self.k2 = parts[2]
  self.k1 = parts[3]
  self.oldnc = parts[4]
  #assert self.oldnc != '0'  # ???
   
  rest = parts[5]
  self.children = rest.split(', ')
  self.used = 0
  
def init_altins(filein):
 lines = read_lines(filein)
 altins = [ALTIN(line) for line in lines]
 d = {}
 for altin in altins:
  L = altin.Lparent
  assert L not in d
  d[L] = altin
 return d
  
if __name__=="__main__":
 filein = sys.argv[1]  # xxx.txt
 filein1 = sys.argv[2] # L,sequence of althws to insert after L
 fileout = sys.argv[3] # output file  adjusted xxx
 daltins = init_altins(filein1)
 recs = digentry1.init(filein)
 # new entries
 recs1 = althws(recs,daltins)
 write_recs(fileout,recs1)

