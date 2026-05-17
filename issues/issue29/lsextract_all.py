#-*- coding:utf-8 -*-
"""lsextract_all.py -- summary stats
"""
import sys,re,codecs
from sort_iast import sort_iast_key
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 

class Tooltip(object):
 def __init__(self,dictlo,line):
  self.dictlo = dictlo
  line = line.rstrip('\r\n')
  if dictlo == 'pwg':
   try:
    # pwg has code, abbrevUpper, abbrevLower,tip
    self.code,self.abbrev,self.abbrevlo,self.tip = line.split('\t')
   except:
    print('Tooltip error:\n%s' %line)
    parts=line.split('\t')
    exit(1)
  elif dictlo in ('ap','ap90'):
   try:
    #  has abbrev, tip
    self.abbrev,self.tip = line.split('\t')
   except:
    print('Tooltip error:\n%s' %line)
    parts=line.split('\t')
    exit(1)
   
  self.total = 0
  
def init_tooltip(dictlo,filein):
 with codecs.open(filein,"r","utf-8") as f:
  ans = [Tooltip(dictlo,x) for x in f]
 print(len(ans),'tooltips from',filein)
 return ans

def dfirstchar(tooltips_sorted):
 d = {}
 for tip in tooltips_sorted:
  c = tip.abbrev[0]
  if c not in d:
   d[c] = []
  d[c].append(tip)
 return d

def findtip(ls,tiplist):
 for tip in tiplist:
  if ls.startswith(tip.abbrev):
   return tip
 return None

def count_tips(lines,tipd,numbertip,unknowntip):
 lsunknowns = []
 lsentries = []  # list of 'entry' with ls of given abbrev
 metaline = None
 imetaline1 = None
 page = None
 for iline,line in enumerate(lines):
  entry = [] # 05-31-2025
  if iline == 0: # %***This File is E:\\APTE.ALL, Last update 11.09.06 
   continue  # 
  line = line.rstrip('\r\n')
  if line == '':
   continue
  if line.startswith('<L>'):
   metaline = line
   imetaline1 = iline+1
   entry = [] 
   continue
  if line == '<LEND>':
   if len(entry)>0:
    lsentries.append(entry)
    # 
   metaline = None
   imetaline = None
   continue
  if line.startswith('[Page'):
   page = line
   continue
  for m in re.finditer(r'<ls([^>]*)>([^<]*)</ls>',line):
   attrib = m.group(1)
   elt = m.group(2)
   m1 = re.search(r' +n="(.*?)"',attrib)
   if m1 != None:
    nval = m1.group(1)
    elt = nval + ' ' + elt
   if re.search(r'^[0-9]',elt): # number
    tip = numbertip
   elif elt[0] not in tipd:
    tip = unknowntip
    lsunknowns.append((metaline,m.group(0)))
   else:
    tiplist = tipd[elt[0]]
    tip  = findtip(elt,tiplist)
    if tip == None:
     tip = unknowntip
     lsunknowns.append((metaline,m.group(0)))
   # found a match
   
   tip.total = tip.total + 1
   if False: # debug
    if iline == 21943:
     print("DBG: ",tip.abbrev)
 return lsunknowns

def parsels(ls):
 m = re.search(r'<ls([^>]*)>([^<]*)</ls>',ls)
 attrib = m.group(1)
 elt = m.group(2)
 m1 = re.search(r' +n="(.*?)"',attrib)
 elt1 = elt
 if m1 != None:
  n = m1.group(1)
  elt1 = n + elt
 m2 = re.search(r'^([^0-9]+)(.*)$',elt1)
 try:
  lsref = m2.group(1)
  lsparms = m2.group(2)
 except:
  print(f'parsels error: ls={ls}')
  lsref=ls
  lsparms = '?'
 return (lsref,lsparms)

def write_lsunknowns(fileout,lsunknowns):
 a = []
 for temp in lsunknowns:
  metaline,lsunknown = temp
  (lsref,lsparms) = parsels(lsunknown)
  a.append((metaline,lsunknown,lsref,lsparms))
 #a1 = sorted(a,key=lambda x: x[2].lower())
 a1 = sorted(a,key=lambda x: sort_iast_key(x[2]))
 outarr = []
 for x in a1:
  (metaline,lsunknown,lsref,lsparms) = x
  meta = re.sub(r'<k2>.*$','',metaline)
  meta1 = meta.ljust(30)
  #out = f'{meta1} : {lsunknown}'
  lsout = lsunknown.ljust(25)
  out = f'{lsout} : {meta1}'
  outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(lsunknowns),"unknown ls written to",fileout)

def write_lsunknowns_v1(fileout,lsunknowns):
 with codecs.open(fileout,"w","utf-8") as f:
  for temp in lsunknowns:
   metaline,lsunknown = temp
   meta = re.sub(r'<k2>.*$','',metaline)
   meta1 = meta.ljust(30)
   out = '%s : %s' %(meta1,lsunknown)
   f.write(out+'\n')
 print(len(lsunknowns),"unknown ls written to",fileout)

def write_tips(fileout,tips0,numbertip,unknowntip):
 dbg = True
 print(f'write_tips: dbg={dbg}')
 outrecs = []
 outrecs.append('')  # for totals
 if dbg:
  tips = sorted(tips0,key = lambda tip: sort_iast_key(tip.abbrev))
 else:
  tips = sorted(tips0,key = lambda tip: tip.total,reverse=True)
 if False:
  xtips0 = tips0[0:5]
  xtips = sorted(xtips0,key = lambda tip: sort_iast_key(tip.abbrev))
  print('write_tips dbg')
  for x in xtips:
   print(x.abbrev, x.total)
 def tipformat(tip):
  text = tip.tip
  text = re.sub(r'^.*? = ','',text)
  text = text.replace('[Cologne Addition]','')
  # text = text[0:40]
  if dbg:
   return '%05d\t%s' %(tip.total,tip.abbrev)
  else:
   return '%05d\t%s\t%s' %(tip.total,tip.abbrev,text)
 outrecs.append(tipformat(numbertip))
 outrecs.append(tipformat(unknowntip))
 tot = 0
 tot = tot + numbertip.total
 tot = tot + unknowntip.total
 for tip in tips:
  outrecs.append(tipformat(tip))
  tot = tot + tip.total
 #
 import datetime
 x = datetime.datetime.now()
 date = x.strftime("%Y-%m-%d")
 outrecs[0] = '%05d\t%s\tAs of %s' %(tot,'ALL',date)
 if dbg:
  #outrecs = sorted(outrecs)
  pass
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outrecs:
   f.write(out+'\n')
 print("write_tips Output in ",fileout)
 
def write_lsentries(fileout,lsentries,abbrev):
 f = codecs.open(fileout,"w","utf-8")
 n0 = 0
 ntot = 0
 for lscases in lsentries:
  # 
  metaline = lscases[0].metaline
  n = len(lscases)
  ntot = ntot + n
  f.write(';-----------------------------------------------------------\n')
  x = re.sub(r'<k2>.*$','',metaline)
  f.write('; %s {%s %s}\n' %(x,abbrev,n))
  #f.write(';-----------------------------------------------------------\n')
  
  for lscase in lscases:
   f.write(lscase.ls + '\n')
  #f.write(';-----------------------------------------------------------\n')
 f.close()
 print(ntot,'= number of %s ls references'%abbrev)

def make_dummytips(dictlo):
 if dictlo == 'pwg':
  # dummy tips for number and unknown
  numbertip = Tooltip(dictlo,"9.1\tNUMBER\tnumber\tls starts with number")
  unknowntip = Tooltip(dictlo,"9.2\tUNKNOWN\tunknown\tls is unknown")
 elif dictlo in ('ap','ap90'):
  numbertip = Tooltip(dictlo,"NUMBER\tls starts with number")
  unknowntip = Tooltip(dictlo,"UNKNOWN\tls is unknown")
 return (numbertip,unknowntip)

if __name__=="__main__":
 dictlo = sys.argv[1]   
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 filetip = sys.argv[3] # 
 fileout = sys.argv[4] # output summary
 fileout1 = sys.argv[5] # unknown tooltip instances
 tips0 = init_tooltip(dictlo,filetip)
 tips = sorted(tips0,key = lambda tip: len(tip.abbrev),reverse=True)
 tipd = dfirstchar(tips)
 numbertip,unknowntip = make_dummytips(dictlo)
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # # also, updates tip.changes
 lsunknowns = count_tips(lines,tipd,numbertip,unknowntip) 
 write_tips(fileout,tips0,numbertip,unknowntip)
 write_lsunknowns(fileout1,lsunknowns)
 #write_lsentries(fileout,lsentries,abbrev)
