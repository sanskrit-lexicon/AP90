#-*- coding:utf-8 -*-
"""prep2.py for ap90
 
"""
import sys,re,codecs

class Abbrv(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.abbr,self.code,self.idxstr,self.tooltip) = line.split(':')
  self.count = 0
  self.numnums = [0,0,0,0]

def init_abbr(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Abbrv(x) for x in f]
 return recs

def init_regex(x):
 # x is an Abbrv object
 a = x.abbr
 a1 = a.replace('.','[.]')
 if a == 'P.':
  # Panini  P. VI. 3. 73
  old = a1 + '( [VI]+[.] [0-9]+[.] [0-9]+[.]?)'
  new = ('<ls>%s'%a) + r'\1' + '</ls>'
 elif False and (a in ['R.']):
  # 2 numbers expected: R. 3. 34
  old = a1 + '( [0-9]+[.] [0-9]+[.]?)'
  new = ('<ls>%s'%a) + r'\1' + '</ls>'
 elif False and (a in ['P.','A.','U.']):
  old = r'([0-9]+[.]? )' + a1
  c = '<ls>%s</ls>' % a
  new = r'\1' + c
 elif False and (a == 'N.'):
  old = a1 + r'( of|$)'
  c = '<ab>%s</ab>' % a
  new = c + r'\1'
 else:
  old = r'\b' + a1
  new = '<ls>%s</ls>' % a
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
 assert c == 'ls'
 try:
  line = re.sub(abbr.regold,abbr.regnew,line)
 except:
  print('regex error. %s -> %s' %(abbr.regoldraw,abbr.regnewraw))
  print('abbr=',abbr.line)
  print('line=',line)
  exit(1)
 return line

regexparts_raw1 = r'(<ab>.*?</ab>)|(<ls>.*?</ls>)|(<lbinfo .*?/>)'
regexparts1 = re.compile(regexparts_raw1)

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

regexnums = [
 (3,re.compile(r'^ [0-9]+[.] [0-9]+[.] [0-9]+[.]?')),
 (2,re.compile(r'^ [0-9]+[.] [0-9]+[.]?')),
 (1,re.compile(r'^ [0-9]+[.]?'))
]
def abbrv_chapter_instance(s):
 for i,regex in regexnums:
  m = re.search(regex,s)
  if m != None:
   return i,m.group(0)
 return 0,''

def abbrv_chapter(line,x):
 tag = '<ls>%s</ls>' % x.abbr
 n = 0
 repls = []
 newline = line
 for m in re.finditer(tag,line):
  rest = line[m.end(0):]
  k,subnum  = abbrv_chapter_instance(rest)
  x.numnums[k] = x.numnums[k] + 1
  n = n + 1
  newline = newline.replace(tag + subnum, tag[0:-5]+subnum+'</ls>')
 return n,newline

def markabbrvs(line,abbrs):
 # skip certain 
 for x in abbrs:
  if x.abbr in line:
   line = new_replace_abbr(line,x)
   n,numline = abbrv_chapter(line,x)
   line = numline
   x.count = x.count + n
 return line

def write_new(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')
 print('write',len(lines),'lines to',fileout)

def abbr_out(x):
 out = '%s:%s:%s:%s:%s' %(x.abbr,x.code,x.idxstr,x.tooltip,x.count)
 numnums = ['%s' %n for n in x.numnums]
 out1 = ','.join(numnums)
 # find index of numnums that has greatest count
 """
 m = -1
 imax = 0
 for i,n in enumerate(x.numnums):
  if n > m:
   m = n
   imax = i
 """
 imax = 0
 for i,n in enumerate(x.numnums):
  if n != 0:
   imax = i
 out = '%s:%s:%s' %(out,out1,imax)
 return out

def write_abbr(fileout,abbrs):
 
 with codecs.open(fileout,"w","utf-8") as f:
  for x in abbrs:
   out = abbr_out(x)
   f.write(out+'\n')
 print(len(abbrs),'records written to',fileout)

def find_abbr(lsbody,abbrs):
 """ abbrs assumed sorted by descending length of abbreviation. 
  Find the longest abbreviation that starts lsbody.
  This is the FIRST abbreviation that starts lsbody
 """
 for abbr in abbrs:
  if lsbody.startswith(abbr.abbr):
   return abbr
 print('find_abbr error. lsbody=',lsbody)
 exit(1)
 
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # auth_2.txt
 fileout = sys.argv[3] # possible change transactions
 fileout1 = sys.argv[4] # abbr_2.txt  - has counts
 abbrs = init_abbr(filein1)

 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 skip_abbrs = ['A.','N.','P.','U.','Dāy.','H.','K.','N.','P.','R.','Ś.','Subh.','U.','V.','Vaiś.']
 abbrs0 = [x for x in abbrs if x.code == 'ls']
 init_regexes(abbrs0)  # compute regexes used by replace_abbr
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
