#-*- coding:utf-8 -*-
"""
"""
from __future__ import print_function
import sys, re,codecs

class Raw(object):
 n = 0
 nhwprob = 0
 def __init__(self,line):
  self.status = True
  althws = []
  hw = ''
  parts = line.split('\t')
  a,b,c = parts
  self.a = a
  self.b = b
  self.c = c
  flag = False
  for u,v in (('<p>','<p>'),('<b>','<+>'),('<c>','<c>')):
   if b.startswith(u) and c.startswith(v):
    flag = True
    b0 = b[3:] # drop <p>
    c0 = c[3:]
    # b0 and c0 can be quite complex.
    # example: b0: SoRa a., (-RA or -RI f.)
    #          c0: SoRa a., (SoRA, SoRI f.)
    # no point in trying to parse at this point.
    hwsb = re.split(r'[,]+',b0)
    hwsc = re.split(r'[,]+',c0)
    # many times parenthetical
    if len(hwsb) != len(hwsc):
     #print('hw error:',line)
     self.status = False
    break
  if not flag:
   print('error?:',line)
  if re.search(r'^[0-9]',a):
   self.type = 'hw'
   m = re.search(r'^[0-9][0-9][0-9][0-9]-[0-9?]+/[0-9]+$',a)
   if m == None:
    print('error 1: ',line)
   if (u,v) != ('<p>','<p>'):
    print('error 2: ',line)
  elif a.startswith('Comp.'):
   self.type = 'cpd'
   m = re.search(r'^Comp[.] \((.*?)\)$',a)
   if m == None:
    print('error 3: ',line)
    self.status = False
   else:
    self.hwcpd = m.group(1)
   if(u,v) != ('<b>','<+>'):
    print('error 4: ',line)
    self.status = False
  elif a == '':
   self.type = ''
   

class Entry(object):
 def __init__(self):
  self.status = True
  self.hw = None
  self.althws = []
  self.hwcpd = None  # e.g. aMSa when hw is aMSaH
  self.cpds = []
  

def make_entries(raws):
 entry = Entry()
 entries = []
 for iraw,raw in enumerate(raws):
  assert raw.status  # redundant
  b0 = raw.b[3:]
  c0 = raw.c[3:]
  b0a = b0.split(',')
  c0a = c0.split(',')
  if raw.type == 'hw':
   if entry.hw != None:
    if entry.status:
     entries.append(entry)
   entry = Entry()
   entry.hw = c0a[0]
   entry.althws = c0a[1:]
  elif raw.type == 'cpd':
   entry.hwcpd = raw.hwcpd
   for j,x in enumerate(b0a):
    y = c0a[j]
    x = x.strip()
    y = y.strip()
    mx = re.search(r'^-[a-zA-Z]+$',x)
    my = re.search(r'^[a-zA-Z]+$',y)
    if (mx != None) and (my != None):
     entry.cpds.append((x,y))
  elif raw.type == '':
   if entry.hwcpd != None:
    for j,x in enumerate(b0a):
     y = c0a[j]
     x = x.strip()
     y = y.strip()
     mx = re.search(r'^-[a-zA-Z]+$',x)
     my = re.search(r'^[a-zA-Z]+$',y)
     if (mx != None) and (my != None):
      entry.cpds.append((x,y))
    
 if entry.status:
  entries.append(entry)
 return entries

def write_cpds(cpdentries,fileout):
 outrecs = []
 ncpds = 0
 for e in cpdentries:
  a = []
  a.append(e.hw)
  a.append(e.hwcpd)
  ncpds = ncpds + len(e.cpds)
  for e in e.cpds:
   pfx,sfx = e
   a.append('%s,%s'%(pfx,sfx))
  out = ':'.join(a)
  outrecs.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outrecs:
   f.write(out+'\n')
 print(len(outrecs),"records written to",fileout)
 print(ncpds,'Total number of compounds')

def write_cpds1(cpdentries,fileout):
 # slightly different format. Appropriate for
 # hwnorm2/keydoc/distinctfiles/ap90_keydoc_ptrs.txt
 outrecs = []
 ncpds = 0
 for e in cpdentries:
  ncpds = ncpds + len(e.cpds)
  hw = e.hw
  hw = re.sub(r'[^a-zA-z].*$','',hw)  # remove 'comments'
  a = []
  for e in e.cpds:
   pfx,sfx = e
   a.append('%s'% sfx)
  s = ','.join(a)  # pointers to hw
  out = '%s\t%s' %(hw,s)
  outrecs.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outrecs:
   f.write(out+'\n')
 print(len(outrecs),"records written to",fileout)
 print(ncpds,'Total number of compounds')

if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 fileout1 = sys.argv[3]
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"in",filein)
 recs = [Raw(x) for x in lines]
 recs1 = [r for r in recs if r.status]
 print(len(recs1),"records with status = True")
 entries = make_entries(recs1)
 print(len(entries),'entries')
 cpdentries = [e for e in entries if e.cpds != []]
 print(len(cpdentries),'entries with compounds')
 write_cpds(cpdentries,fileout)
 write_cpds1(cpdentries,fileout1)
