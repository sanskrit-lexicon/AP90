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

def adjust1(recs):
 # remove space at end of lines of Entry records
 nchg = 0
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   # no change
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  newlines = []
  for line in entry.datalines:
   newline = re.sub(r' +$','',line)
   if newline != line:
    nchg = nchg + 1
   newlines.append(newline)
  entry.datalines = newlines
 print('adjust1 change to %s lines' % nchg)

def adjust1a(recs):
 # remove spaces at start of lines in entries
 nchg = 0
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   # no change
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  newlines = []
  for line in entry.datalines:
   newline = re.sub(r'^ +','',line)
   if newline != line:
    nchg = nchg + 1
   newlines.append(newline)
  entry.datalines = newlines
 print('adjust1a change to %s lines' % nchg)

def adjust2(recs):
 # " zu\n<ls>X</ls>Y" -> "zu<ls>X</ls>\nY"  Note Y could be empty
 nchg = 0
 nempty = 0
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   # no change
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  oldlines = entry.datalines
  txtold = '\n'.join(oldlines)
  txtnew = re.sub(r' zu\n(<ls.*?</ls>) *',r' zu \1\n',txtold,re.DOTALL)
  if txtold == txtnew:
   # no change
   continue
  newlines = txtnew.split('\n')
  # update nchg
  assert len(oldlines) == len(newlines)
  for iline,newline in enumerate(newlines):
   line = oldlines[iline]
   if newline != line:
    nchg = nchg + 1
  entry.datalines = newlines
 print('adjust2 change to %s lines' % nchg)

def adjust3(recs):
 # " zu\n[Page..]<ls>X</ls>Y" -> "zu<ls>X</ls>\nY"  Note Y could be empty
 nchg = 0
 nempty = 0
 for rec in recs:
  if type(rec) == digentry1.nonEntry:
   # no change
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  oldlines = entry.datalines
  txtold = '\n'.join(oldlines)
  txtnew = re.sub(r' zu\n(\[Page.*?\])\n(<ls.*?</ls>) *',
                  r' zu \2\n\1\n',txtold,re.DOTALL)
  if txtold == txtnew:
   # no change
   continue
  newlines = txtnew.split('\n')
  # update nchg
  assert len(oldlines) == len(newlines)
  for iline,newline in enumerate(newlines):
   line = oldlines[iline]
   if newline != line:
    nchg = nchg + 1
  entry.datalines = newlines
 print('adjust3 change to %s lines' % nchg)

def althws(recs):
 #nchg = 0
 #nempty = 0
 nalt = 0 # number of althw entries added
 newrecs = []
 for irec,rec in enumerate(recs):
  if type(rec) == digentry1.nonEntry:
   # no change
   newrecs.append(rec)
   continue
  assert type(rec) == digentry1.Entry
  entry = rec
  meta = entry.metaline
  # <L>L<pc>pc<k1>k1<k2>k2a, k2b
  m = re.search(r'<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>([a-zA-Z]+), *([a-zA-Z]+)$',meta)
  if m == None:
   # nothing to do here
   newrecs.append(rec)
   continue
  # extract fields from meta
  L = m.group(1)
  pc = m.group(2)
  k1 = m.group(3)
  k2a = m.group(4)   
  k2b = m.group(5)  # new hw
  assert k2a == k1
  
  # metaline fields for new headword
  entry_next = recs[irec + 1]  # theoretically, could fail
  assert type(entry_next) == digentry1.Entry
  L_next = entry_next.metad['L']
  m1 = re.search(r'^[0-9]+$',L_next)
  if m1 == None:
   print('ERROR meta_next=',entry_next.metaline)
   newrecs.append(rec)
   continue
  # add rec to newrecs, since we keep it
  newrecs.append(rec)
  # so L_next is a digit sequence
  # Thus, safe to construct L_new  (e.g. if L=1234, then L=1234.1
  L_new = '%s.1' % L
  pc_new = pc
  k1_new = k2b
  k2_new = k2b
  # construct 3 lines for new entry
  meta_new = '<L>%s<pc>%s<k1>%s<k2>%s' % (L_new, pc_new, k1_new, k2_new)
  body_new = '{{Lbody=%s}}' % L
  lend_new = '<LEND>'
  newlines = [meta_new,body_new,lend_new]
  for newline in newlines:
   linenum_dummy = 0
   nonentry = digentry1.nonEntry(newline,linenum_dummy)
   newrecs.append(nonentry)
  nalt = nalt + 1
 print('%s althw entries constructed' % nalt)
 return newrecs
if __name__=="__main__":
 filein = sys.argv[1]  # xxx.txt
 fileout = sys.argv[2] # output file  adjusted xxx
 recs = digentry1.init(filein)
 recs1 = althws(recs)
 
 #adjust1(recs)  # remove spaces at end
 #adjust1a(recs) # remove spaces at beginning
 #adjust2(recs)  # merge zu\n<ls>X</ls.
 #adjust3(recs)  # with [Page..]
 write_recs(fileout,recs1)

