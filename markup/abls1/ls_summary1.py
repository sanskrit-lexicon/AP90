#-*- coding:utf-8 -*-
"""ls_summary.py for ap90
 
"""
import sys,re,codecs
sys.stdout.reconfigure(encoding='utf-8') 

class Tooltip(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  parts = line.split('\t')
  (self.abbr,self.tooltip) = parts
  
  self.numnums = [0,0,0,0]  # count of instances
  self.count = 0 # total of self.numnums
  assert len(self.numnums) == 4
  
def init_abbr(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Tooltip(x) for x in f]
 return recs

def init_regex(x):
 # x is an Tooltip object
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
 m = -1
 imax = 0
 for i,n in enumerate(x.numnums):
  if n > m:
   m = n
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
 return None

def update_abbrs(line,abbrs,flog,iline):
 for m in re.finditer(r'<ls(.*?)>(.*?)</ls>',line):
  lselt = m.group(0)
  attribs = m.group(1)
  text = m.group(2)
  m1 = re.search(r' n="(.*?)"',attribs)
  if m1:
   n = m1.group(1)
   lsbody = '%s %s'%(n,text)
   lsbody = re.sub(r' +',' ',lsbody)
  else:
   n = None
   lsbody = text
  abbr = find_abbr(lsbody,abbrs)
  if abbr == None:
   print('update_abbrs error:',iline+1,line)
   print('lselt=',lselt)
   continue
  lsrest = lsbody[len(abbr.abbr):]
  # find longest number sequence in lsrest
  n,numseq = abbrv_chapter_instance(lsrest)
  #if (abbr.abbr == 'Y.') and (n == 1):print(iline+1,line)
  abbr.numnums[n] = abbr.numnums[n] + 1
  #if n > abbr.idxmax:
  # update_log(flog,line,lselt,iline,n,abbr.idxmax)
   
def update_log(f,line,lselt,iline,n,idxmax):
 outarr = []
 outarr.append('; lselt=%s: too many numbers: %s > %s' %(lselt,n,idxmax))
 lnum = iline + 1
 outarr.append('%s old %s' %(lnum,line))
 outarr.append('%s new %s' %(lnum,line))
 outarr.append(';')
 for out in outarr:
  f.write(out+'\n')

def abbr_out(x):
 x.count = sum(x.numnums)
 out = '%s:%s:%s' %(x.abbr,x.tooltip,x.count)
 numnumsstr = ['%s' %n for n in x.numnums]
 out1 = ','.join(numnumsstr)
 out = '%s:%s' %(out,out1)
 """
 imax = 0
 for i,n in enumerate(x.numnums):
  if n != 0:
   imax = i
 out = '%s:%s:%s' %(out,out1,imax)
 if x.idxmax != imax:
  out = out + ':?'
 """
 return out

def write_abbrs(fileout,abbrs):
 with codecs.open(fileout,"w","utf-8") as f:
  for x in abbrs:
   out = abbr_out(x)
   f.write(out+'\n')
 print(len(abbrs),'records written to',fileout)

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # tooltip.txt
 fileout = sys.argv[3] # ls_summary1.txt
 
 abbrs = init_abbr(filein1)
 abbrs1 = sorted(abbrs , key = lambda x : len(x.abbr),reverse=True)
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 #abbrs0 = [x for x in abbrs if x.code == 'ls']
 #init_regexes(abbrs0)  # compute regexes used by replace_abbr

                 
 count = 0
 #filelog = 'temp_ls_summary1.txt'
 #flog = codecs.open(filelog,"w","utf-8")
 flog=None
 for iline,line in enumerate(lines):
  update_abbrs(line,abbrs1,flog,iline)
 write_abbrs(fileout,abbrs)
 #flog.close()
 #print('please check temp_ls_summary.txt')
 
