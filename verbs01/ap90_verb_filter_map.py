#-*- coding:utf-8 -*-
"""ap90_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Ap90verb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  try:
   m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
   self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  except:
   print('Ap90verb error: line=',line)
   exit(1)
  self.mw = None
  self.mwrec = None
def init_ap90verb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Ap90verb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

map2mw_special = {
 #ap90:mw
 'pUr':'pF', # passive, causal
 'BAj':'Baj', #causal
 'AMdol':'Andolaya',
 'aMdolayati':'andolaya',
 'avakarR':'avakarRaya',
 'AkarR':'AkarRaya', #den
 #'upakarR':'upakarRaya',  # MW has only upAkarRaya
 'unmUl':'unmUla',
 'nirmUl':'nirmUlaya',
 'anukfpAyate':'anukfp',
 'aMtarayati':'antaraya',
 'aMbaryati':'ambarya',
 'udvezwayati':'udvezw',
 'upasnehayati':'upasnih',
 'ullalayati':'ullal',
 'Urjayati':'Urj',
 'kaMqUyati':'kaRqUya',
 'kalaMkayati':'kalaNkaya',
 'kzArayati':'kzar', # causal
 'gadgadayati':'gadgadya',  # not exactly same, but certainly related
 'Calayati':'Cal', # class 10
 'daMqAyate':'daRqAya',
 'duMdumAyate':'dundumAya',
 'drAGayati':'drAG', # causal
 'pariKaMqayati':'pariKaRqaya',
 'puMjayati':'puYjaya',
 'pratibiMbayati':'pratibimbaya',
 'prapaMcayati':'prapaYcaya',
 'BaMgurayati':'BaNguraya',
 'maMqalayati':'maRqalaya',
 'maMqalAyate':'maRqalAya',
 'maMtUyati':'mantUya',
 'maMdayati':'mandaya',
 'maMdAyate':'mandAya',
 'muMqayati':'muRqaya',
 'vyaMgayati':'vyaNgaya',
 'sImaMtayati':'sImantaya',
 'sTUlayati':'sTUl',
 'aruzati':'aruza',
 'aSvati':'aSva',
 'utkaMWate':'utkaRWa',
 'upasAMtv':'upasAntvaya',
 'kraSayati':'kfS',
 'kzaMj':'kzaj',
 'gil':'gF',
 'guR':'guRaya',
 'gozW':'gozWa',
 'cihn':'cihnaya',
 'Card':'Cfd',  # causal
 'jfB':'jfmB',
 'taMtr':'tantraya',
 'tIr':'tIraya',
 'tuMj':'tuj',
 'tutT':'tutTaya',
 'daMq':'daRqaya',
 'daridrA':'drA', # intensive
 'duHK':'duHKaya',
 'nimasj':'nimajj',
 'nIlati':'nIl',
 'pallavati':'pallava',
 'pIv':'pIva',
 'puzp':'puzpya',
 'prakawati':'prakawa',
 'prabalati':'prabala',
 'pravaRAyati':'pravaRaya',
 'preMKol':'preNKolaya',
 'Brasj':'Brajj',
 'masj':'majj',
 'mitrati':'mitra',
 'larv':'larb',  # v/b
 'barv':'barb',  # v/b
 'lasj':'lajj',
 'lohitati':'lohita',
 'var':'vf', # causal, or of vF
 'valyUl':'valyUla',
 'vikal':'vikalaya',  # ap90 also has vikalayati
 'visTA':'vizWA',  # ap90 mis-spell?
 'Sur':'SUr',
 'saMciMt':'saMcint',
 'satrAyate':'sattrAya',
 'sapatrAkf':'sapattrAkf',
 'saMmurcC':'sammurC',
 'suKayati':'suK',
 'sPAl':'sPal',
 'svurcC':'svUrC',
 '':'',
 '':'',
 '':'',
 '':'',
}

# next 3 from hwnorm1/sanhw1/hwnorm1c.py
slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}

def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)

def homorganic_nasal(a):
 return re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)

def map2mw_nasal(k1,d):
 k = homorganic_nasal(k1)
 if k in d:
  return k
 return None

def map_3s(k,d):
 if k.endswith(('yati','yate')):
  k1 = k[0:-2]  # remove final ti, te
  if k1 in d:
   return k1
 return None

def map2mw(d,k1):
 """ for ap90
 """
 if k1 in map2mw_special:
  return map2mw_special[k1]
 if k1 in d:
  return k1
 if 'M' in k1:
  k = map2mw_nasal(k1,d)
  if k != None:
   return k
 if 'cC' in k1:
  k = re.sub('cC','C',k1)
  if k in d:
   return k
 # approx. 300 cases where ap90 has a 3rd singular present form as headword
 k = map_3s(k1,d)
 if k != None:
  return k
 return '?'

def ap90map(recs,mwd):
 
 for rec in recs:
  # try mw spelling directly
  rec.mw = map2mw(mwd,rec.k1)
  if rec.mw in mwd:
   rec.mwrec = mwd[rec.mw]

def write(fileout,recs):
 n = 0
 nprob = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw 
   out = '%s, mw=%s' %(line,rec.mw)
   # add parse when mw is a preverb
   if rec.mwrec != None:
    mwrec = rec.mwrec
    if mwrec.cat == 'preverb':
     out = '%s %s' %(out,mwrec.parse)
   f.write(out + '\n')
   if rec.mw == '?':
    nprob = nprob + 1
 print(n,"records written to",fileout)
 print(nprob,"verbs still not mapped to mw")

if __name__=="__main__": 
 filein = sys.argv[1] #  ap90_verb_filter.txt
 filein2 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_ap90verb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein2)
 ap90map(recs,mwverbsd)
 write(fileout,recs)
