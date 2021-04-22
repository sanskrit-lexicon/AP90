#-*- coding:utf-8 -*-
"""abbrauth.py for pwg
 
"""
import sys,re,codecs
sys.stdout.reconfigure(encoding='utf-8') 

class Abbrv(object):
 def __init__(self,code,line,idx):
  line = line.rstrip('\r\n')
  m = re.search(r'^<HI>(.*?)…(.*)$',line)
  if not m:
   print('parse Error',line)
   exit(1)
  self.code = code # 'ab' or 'ls'
  self.abbr = m.group(1)
  self.tooltip = m.group(2).strip()  # remove spaces at ends
  self.idx = idx  # index within input file
  if code == 'ls': # check ends with period
   if not self.abbr.endswith('.'):
    print('Abbrv warning',code,self.abbr,self.tooltip)
  if code == 'ab': # check ends with period or .%}
   if not self.abbr.endswith(('.','.%}')):
    print('Abbrv warning',code,self.abbr,self.tooltip)
  assert ':' not in self.tooltip

def abbr_out(abbr,iabbr=0):
 arr = []
 arr.append(abbr.abbr)
 arr.append(abbr.code)
 arr.append(str(abbr.idx))
 arr.append(abbr.tooltip)
 out = ':'.join(arr)
 out = '%s:%s:%s:%s' %(arr[0],arr[1],arr[2],arr[3])
 return [out]

def write_abbrs(fileout,abbrs):
 #abbrs1 = sorted(abbrs , key = lambda x : len(x.abbr),reverse=True)
 abbrs1 = abbrs
 with codecs.open(fileout,"w","utf-8") as f:
  for iabbr,abbr in enumerate(abbrs1):
   outarr = abbr_out(abbr,iabbr)
   for out in outarr:
    f.write(out+'\n')
 print(len(abbrs),"written to",fileout)

def check1(abbrs):
 d = {}
 for x in abbrs:
  ab = x.abbr
  if ab not in d:
   d[ab] = []
  d[ab].append(x)
 for ab in d:
  recs = d[ab]
  if len(recs) > 1:
   for ix,x in enumerate(recs):
    out = abbr_out(x)
    out = out[0]
    print('dup',ix+1,out)
   print()

def check2(abbrs):
 """ Example
4 matches for "^A[.]" in buffer: abbrauth_1.txt
    115:A. S.:ab:8:Anglo-Saxon.
    132:A. L.:ls:2:Ānandalaharī.
    133:A. R.:ls:5:Anargharāghava (published in the Kāvyamālā).
    252:A.:ab:0:Ātmanepada.

  Suppose we have 'A.' at the end of a line.  Then this could be
  any of the 4 possibilities above.
  We want to enumerate these.
  find all abbreviations X for which there are other abbreviations Y
    such that Y.abbr starts with X.abbr.
 """
 dups = []
 dups0 = []
 for x in abbrs:
  ab = x.abbr
  xdups = [x]
  for y in abbrs:
   if y == x:
    continue
   if y.abbr.startswith(ab):
    xdups.append(y)
  if len(xdups) != 1:
   dups.append(xdups)
   dups0.append(ab)
 print(len(dups),"type 2 duplicates")
 for idup,dup in enumerate(dups):
   for ix,x in enumerate(dup):
    out = abbr_out(x)
    out = out[0]
    print('dup',ix+1,out)
   print()
 print(dups0)
 
if __name__=="__main__":
 filein1 = sys.argv[1] #  abbr_1.txt
 filein2 = sys.argv[2] #  auth_1.txt
 fileout = sys.argv[3] #  file merged. Sorted by decreasing length of abbr.
 n = 0
 abbrs = []
 with codecs.open(filein1,"r","utf-8") as f:
  code = 'ab'
  for i,x in enumerate(f):
   abbrs.append(Abbrv(code,x,i))
 with codecs.open(filein2,"r","utf-8") as f:
  code = 'ls'
  for i,x in enumerate(f):
   abbrs.append(Abbrv(code,x,i))
 print(len(abbrs),"total abbreviations")
 write_abbrs(fileout,abbrs)
 check1(abbrs)  # duplicates
 check2(abbrs)  # 

