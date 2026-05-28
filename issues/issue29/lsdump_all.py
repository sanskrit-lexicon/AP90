#-*- coding:utf-8 -*-
"""lsdump_all.py 
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
  self.lsinstances = []  # each item is a pair (metaline,lsinstance)
  
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
  #if iline == 0: # %***This File is E:\\APTE.ALL, Last update 11.09.06 
  #continue  # 
  line = line.rstrip('\r\n')
  if line == '':
   continue
  if line.startswith('<L>'):
   metaline = line
   imetaline1 = iline+1
   entry = [] # list of LSCase appearing in this entry
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
   ls = m.group(0) 
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
   tip.lsinstances.append((metaline,m.group(0)))
   if False: # debug
    if iline == 21943:
     print("DBG: ",tip.abbrev)
 return lsunknowns

def write_lsunknowns(fileout,lsunknowns):
 with codecs.open(fileout,"w","utf-8") as f:
  for temp in lsunknowns:
   metaline,lsunknown = temp
   meta = re.sub(r'<k2>.*$','',metaline)
   meta1 = meta.ljust(30)
   out = '%s : %s' %(meta1,lsunknown)
   f.write(out+'\n')
 print(len(lsunknowns),"unknown ls written to",fileout)

def make_outrecs(tips0):
 # sort by tip.abbrev
 tips = sorted(tips0,key = lambda tip: sort_iast_key(tip.abbrev))
 outrecs = []
 for tip in tips:
  lsinstances = tip.lsinstances
  n1 = 0
  n2 = 0 # number of lsinstances with parameter
  lsnoparm = f'<ls>{tip.abbrev}</ls>'
  lsparms = []
  lsnoparms = []
  for temp in lsinstances:
   metaline,ls = temp
   if ls == lsnoparm:
    lsnoparms.append(temp)
   else:
    lsparms.append(temp)
  n1 = len(lsparms)
  n2 = len(lsnoparms)
  outarr = []
  outarr.append(f"* {tip.abbrev} {n1} parms;  {n2} no parms")
  for temp in lsparms:
   metaline,ls = temp
   meta = re.sub(r'<k2>.*$','',metaline)
   meta1 = meta.ljust(30)
   out = '%s : %s' %(meta1,ls)
   outarr.append(out)
  outrecs.append(outarr)
 return outrecs
def write_outrecs(fileout,outrecs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
    n = n + 1
 print(f'{n} lines written to {fileout}')
 
def write_abbrev(fileout,tip):
 with codecs.open(fileout,"w","utf-8") as f:
  lsinstances = tip.lsinstances
  for temp in lsinstances:
   metaline,ls = temp
   meta = re.sub(r'<k2>.*$','',metaline)
   meta1 = meta.ljust(30)
   out = '%s : %s' %(meta1,ls)
   f.write(out+'\n')
 print(f'{len(lsinstances)} of abbrev "{tip.abbrev}" written to {fileout}')

def write_tips(fileout,tips0,numbertip,unknowntip):
 outrecs = []
 outrecs.append('')  # for totals
 tips = sorted(tips0,key = lambda tip: tip.total,reverse=True)
 def tipformat(tip):
  text = tip.tip
  text = re.sub(r'^.*? = ','',text)
  text = text.replace('[Cologne Addition]','')
  text = text[0:40]
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
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outrecs:
   f.write(out+'\n')
 print("write_tips Output in ",fileout)
 
def write_lsentries(fileout,lsentries,abbrev):
 f = codecs.open(fileout,"w","utf-8")
 n0 = 0
 ntot = 0
 for lscases in lsentries:
  # lscases is a non-empty list of LSCase objects
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
 filein = sys.argv[2] #  xxx.txt dictionary
 filetip = sys.argv[3] # tooltip file
 fileout = sys.argv[4] # all instances of abbrev in dictionary
 tips0 = init_tooltip(dictlo,filetip)
 tips = sorted(tips0,key = lambda tip: len(tip.abbrev),reverse=True)
 tipd = dfirstchar(tips)
 """
 tip_abbrev = None
 for tip in tips:
  if tip.abbrev == abbrev:
   tip_abbrev = tip
   break
 if tip_abbrev == None:
  print(f'No tip found with abbrev == "{abbrev}"')
  exit(1)
 """
 numbertip,unknowntip = make_dummytips(dictlo)
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # also, updates tip.changes
 lsunknowns = count_tips(lines,tipd,numbertip,unknowntip)
 outrecs = make_outrecs(tips)
 write_outrecs(fileout,outrecs)
 #
 #write_abbrev(fileout,tip_abbrev)
 # write_tips(fileout,tips0,numbertip,unknowntip)
 #write_lsunknowns(fileout1,lsunknowns)
 #write_lsentries(fileout,lsentries,abbrev)
