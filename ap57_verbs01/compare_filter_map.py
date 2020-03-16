#-*- coding:utf-8 -*-
"""compare_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Verb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  try:
   m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',line)
   self.L,self.k1,self.k2,self.code,self.mw = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  except:
   print('Verb error: line=',line)
   exit(1)
  # nomalize k1 w.r.t. nasals
  self.k1norm = normalize(self.k1)
  # translate for sorting
  self.k1norm_tran = self.k1norm.translate(slp_from_to)

slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
slp_from_to = str.maketrans(slp_from,slp_to)

def init_verb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Verb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 # sort by k1norm
 recs.sort(key = lambda rec: rec.k1norm_tran)
 return recs

class unused_MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def unused_init_mwverbs(filein):
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

def normalize(a):
 a1 = homorganic_nasal(a)
 return a1

def unused_map2mw_nasal(k1,d):
 k = homorganic_nasal(k1)
 if k in d:
  return k
 return None

def unused_map_3s(k,d):
 if k.endswith(('yati','yate')):
  k1 = k[0:-2]  # remove final ti, te
  if k1 in d:
   return k1
 return None

def unused_map2mw(d,k1):
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

def write(fileout,recs,dict1,dict2):
 n = 0
 nmiss1 = 0
 nmiss2 = 0
 outarr = []
 t1 = '.......%s..........' % dict1
 t2 = '.......%s..........' % dict2
 filemiss = 'temp_compare_missing.txt'
 f = codecs.open(filemiss,'w','utf-8')
 outarr.append(t1 + ('%5s'% '') + t2)
 for rec1,rec2 in recs:
  n = n + 1
  if (rec1 != None) and (rec2 != None):
   x1 = rec1.k1.ljust(12)
   x2 = rec2.k1.ljust(12)
   out1 = '%6s %12s' %(rec1.L,x1)
   out2 = '%6s %12s' %(rec2.L,x2)
   #out1 = '%6s %12s' %(rec1.L,rec1.k1)
   #out2 = '%6s %12s' %(rec2.L,rec2.k1)
  elif rec1 != None:
   x1 = rec1.k1.ljust(12)
   out1 = '%6s %12s' %(rec1.L,x1)
   #out1 = '%6s %12s' %(rec1.L,rec1.k1)
   out2 = ' ---------------' 
   f.write('%s:k1=%s\n' %(dict2,rec1.k1))
   nmiss2 = nmiss2 + 1
  else:
   out1 = ' ---------------' 
   x2 = rec2.k1.ljust(12)
   out2 = '%6s %12s' %(rec2.L,x2)
   #out2 = '%6s %12s' %(rec2.L,rec2.k1)
   f.write('%s:k1=%s\n' %(dict1,rec2.k1))
   nmiss1 = nmiss1 + 1
  out = out1 + ('%5s'% '') + out2
  outarr.append(out)
 f.close()
 print(dict1,'has',nmiss1,'misses')
 print(dict2,'has',nmiss2,'misses')
 print('see',filemiss)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out + '\n')
 print(len(outarr),"records written to",fileout)

def merge(recs1,recs2):
 n1 = len(recs1)
 n2 = len(recs2)
 i1 = 0
 i2 = 0
 ans = []  
 while (i1 < n1) or (i2 < n2):
  if (i1 < n1) and (i2 == n2): 
   rec1 = recs1[i1]
   ans.append((rec1,None))
   i1 = i1 + 1
   continue
  if (i1 == n1) and (i2 < n2):
   rec2 = recs2[i2]
   ans.append((None,rec2))
   i2 = i2 + 1
   continue
  #  i1<n1 and i2 < n2
  rec1 = recs1[i1]
  rec2 = recs2[i2]
  if rec1.k1norm == rec2.k1norm:
   ans.append((rec1,rec2))
   i1 = i1 + 1
   i2 = i2 + 1
   continue
  if rec1.k1norm_tran < rec2.k1norm_tran:
   ans.append((rec1,None))
   i1 = i1 + 1
   continue
  # rec2 is smaller
  ans.append((None,rec2))
  i2 = i2 + 1
 print(len(ans),"records after merge")
 return ans
    
if __name__=="__main__": 
 filein = sys.argv[1] #  xxx_verb_filter_map.txt
 filein1 = sys.argv[2] # yyy_verb_filter_map.txt
 fileout = sys.argv[3]
 m = re.search('([a-zA-Z0-9]+)_verb_filter_map.txt',filein)
 dict1 = m.group(1) # xxx
 m = re.search('([a-zA-Z0-9]+)_verb_filter_map.txt',filein1)
 dict2 = m.group(1) # yyy
 print(dict1,dict2)
 recs1 = init_verb(filein)
 recs2 = init_verb(filein1)
 recs3 = merge(recs1,recs2)
 write(fileout,recs3,dict1,dict2)
 exit(1)
 mwverbrecs,mwverbsd= init_mwverbs(filein2)
 ap90map(recs,mwverbsd)
 write(fileout,recs)
