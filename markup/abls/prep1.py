#-*- coding:utf-8 -*-
"""prep1.py for ap90
 
"""
import sys,re,codecs

class Abbrv(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.abbr,self.code,self.idxstr,self.tooltip) = line.split(':')
  self.count = 0
  #self.instances = []

def init_abbr(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Abbrv(x) for x in f]
 return recs

def init_regex(x):
 # x is an Abbrv object
 a = x.abbr
 a1 = a.replace('.','[.]')
 if a in ['P.','A.','U.']:
  old = r'([0-9]+[.]? )' + a1
  c = '<ab>%s</ab>' % a
  new = r'\1' + c
 elif a.startswith('{'):
  # a = {%b%}
  b = a[2:-2]
  old = a1
  c = '<ab>%s</ab>' % b
  new = '{%' + c + '%}'
 elif a == 'N.':
  old = a1 + r'( of|$)'
  c = '<ab>%s</ab>' % a
  new = c + r'\1'
 else:
  old = r'\b' + a1
  new = '<ab>%s</ab>' % a
 # add attributes to x
 x.regoldraw = old
 x.regnewraw = new
 x.regold = re.compile(old)
 try:
  #x.regnew = re.compile(new)
  x.regnew = new
 except:
  print('init_regex ERROR',new)
  
def init_regexes(abbrs):
 for x in abbrs:
  init_regex(x)
  
def replace_abbr(line,abbr):
 a = abbr.abbr
 c = abbr.code
 assert c == 'ab'
 try:
  line = re.sub(abbr.regold,abbr.regnew,line)
 except:
  print('regex error. %s -> %s' %(abbr.regoldraw,abbr.regnewraw))
  print('abbr=',abbr.line)
  print('line=',line)
  exit(1)
 return line

regexparts_raw = r'(<(?P<tag>[^<]+).*?</(?P=tag)>)'
regexparts = re.compile(regexparts_raw)
regexparts_raw1 = r'(<ab>.*?</ab>)|(<ls>.*?</ls>)|(<lbinfo .*?/>)'
regexparts1 = re.compile(regexparts_raw1)
def testsplit():
 x = '<><ab>N.</ab> of Śiva, Brahmā, Vāyu, or <lbinfo n="Vaiśvā+nara"/>'
 print('USING ',regexparts_raw)
 parts = re.split(regexparts,x)
 print('x=',x)
 for part in parts:
  print('part=',part)

 print('USING ',regexparts_raw1)
 parts = re.split(regexparts1,x)
 print('x=',x)
 for part in parts:
  print('part=',part)

 newparts = []
 for part in parts:
  if part != None:
   newparts.append(part)
 newx = ''.join(newparts)
 print('x==newx:',x == newx)
 exit(1)
 
def new_replace_abbr(line,x):
 #print('line=',line)
 parts = re.split(regexparts1,line)
 newparts = []
 for part in parts:
  #print('part=',part)
  if part == None:
   pass
  elif part.startswith('<>'):  # peculiar to ap90
   newpart = replace_abbr(part,x)
   newparts.append(newpart)
   #print('%s -> %s' %(part,newpart))
  elif part.startswith('<'): # a true xml element
   newparts.append(part)
  else:
   newpart = replace_abbr(part,x)
   newparts.append(newpart)
   #print('%s -> %s' %(part,newpart))
 newline = ''.join(newparts)
 #print('newline=',newline)
 #exit(1)
 return newline

def markabbrvs(line,abbrs):
 # skip certain 
 for x in abbrs:
  if x.abbr in line:
   line = new_replace_abbr(line,x)
   x.count = x.count + 1
 return line

def write_new(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')
 print('write',len(lines),'lines to',fileout)

def abbr_out(x):
 out = '%s:%s:%s:%s:%s' %(x.abbr,x.code,x.idxstr,x.tooltip,x.count)
 return out

def write_abbr(fileout,abbrs):
 with codecs.open(fileout,"w","utf-8") as f:
  for x in abbrs:
   out = abbr_out(x)
   f.write(out+'\n')
 print(len(abbrs),'records written to',fileout)
 
if __name__=="__main__":
 #testsplit()
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # abbrauth_1.txt
 fileout = sys.argv[3] # possible change transactions
 fileout1 = sys.argv[4] # abbr_2.txt  - has counts
 abbrs = init_abbr(filein1)

 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 skip_abbrs = ['A.','N.','P.','U.','Dāy.','H.','K.','N.','P.','R.','Ś.','Subh.','U.','V.','Vaiś.']
 #print('skipping abbreviatins',skip_abbrs)
 abbrs0 = [x for x in abbrs if x.code == 'ab']
 init_regexes(abbrs0)  # compute regexes used by replace_abbr
 #abbrs0 = [x for x in abbrs if x.abbr not in skip_abbrs]
 abbrs1 = sorted(abbrs0 , key = lambda x : len(x.abbr),reverse=True)

 newlines = []
 metaline = None
 count = 0
 for line in lines:
  if line.startswith('<L>'):
   metaline = line
  elif line.startswith('<LEND>'):
   metaline = None
  if metaline == None:
   newline = line
  elif line.startswith('[Page'):
   newline = line
  else:
   newline = markabbrvs(line,abbrs1)
  if newline != line:
   count = count + 1
  newlines.append(newline)
 print(count,'lines changed')
 write_new(fileout,newlines)
 write_abbr(fileout1,abbrs0)
