#-*- coding:utf-8 -*-
"""prep3.py for ap90
 
"""
import sys,re,codecs
sys.stdout.reconfigure(encoding='utf-8') 

class Abbrv(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.abbr,self.code,self.idxstr,self.tooltip,countstr,numnumstr,maxstr) = line.split(':')
  self.numnums = [int(x) for x in numnumstr.split(',')]
  self.count = int(countstr)
  assert len(self.numnums) == 4
  self.idxmax = int(maxstr)  # numnums[idxmax] max(numnums[i] for all i)

  if self.abbr in ['Bk.','Ki.', 'Ku.' ,'Māl.' ,'Ms.' ,'R.' ,'Ś.' ,'Śi.' ,'Y.' ]:
   idxmax1 = 2
   print(self.abbr,'Change idxmax from',self.idxmax,'to',idxmax1)
   self.idxmax = idxmax1
  elif self.abbr in ['Dk.', 'Gīt.', 'K.' , 'Me.' , 'A. R.' ]:
   idxmax1 = 1
   print(self.abbr,'Change idxmax from',self.idxmax,'to',idxmax1)
   self.idxmax = idxmax1
   
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
 exit(1)
 
def update_lines(iline,lines,lselt,abbrs):
 """
  abbrs assumed sorted by descending length of abbreviation.
  line = lines[iline]  line ends with lselt
  may change lines array
  lselt = '<ls>X</ls>'
 """
 line = lines[iline]
 assert line.endswith(lselt)
 start = line[0:-len(lselt)]
 lsbody = lselt[4:-5]  # remove <ls> and </ls> 
 # find abbr 
 abbr = find_abbr(lsbody,abbrs)
 lsrest = lsbody[len(abbr.abbr):]
 # find longest number sequence in lsrest
 n,numseq = abbrv_chapter_instance(lsrest)
 if n == abbr.idxmax:
  # nothing to do if n is maximum for this abbreviation
  return False
 dbg = False
 if n > abbr.idxmax:
  return  # needs a warning
 # look for more numbers in next line (but skip [Page
 iline1 = iline + 1
 line1 = lines[iline1]
 if line1.startswith('[Page'):
  iline1 = iline + 2
  line1 = lines[iline1]
 if dbg:print('* update_lines case')
 if dbg:print('line=',line,'\nline1=',line1)
 if not line1.startswith('<>'): # peculiar to ap90
  return False
 line1a = ' ' + line1[2:] # drop <>; space for chapterinstance
 # look for missing numbers on line1.
 nlook = abbr.idxmax - n
 temp = [(k,regex) for (k,regex) in regexnums if k == nlook]
 if len(temp) != 1:
  print('update_lines error 1',n,nlook,abbr.abbr)
  return False
 _,regexlook = temp[0]
 m = re.search(regexlook,line1a)
 if m == None:
  return False
 lsextra = m.group(0)  # the added numbers needed
 lselt1 = '<ls>%s%s%s</ls>' %(abbr.abbr,lsrest,lsextra)
 lbinfo = '<lbinfo n="ls:%s+%s"/>' %(lsbody,lsextra)
 newline = start + ' ' + lbinfo
 newlsbody = lsbody + lsextra
 newlselt = '<ls>%s</ls>' % newlsbody
 line1a_rest = line1a[len(lsextra):]
 newline1 = '<>' + newlselt + line1a_rest
 if dbg:
  print('newline= ',newline)
  print('newline1=',newline1)
 lines[iline] = newline
 lines[iline1] = newline1
 return True

def write_changes(fileout,oldlines,newlines):
 with codecs.open(fileout,"w","utf-8") as f:
  case = 0
  metaline = None
  for iline,old in enumerate(oldlines):
   new = newlines[iline]
   if old.startswith('<L>'):
    metaline = old
   if old == new:
    continue
   case = case + 1
   outarr = []
   outarr.append('; Case %d: %s' %(case,metaline))
   lnum = iline + 1
   outarr.append('%s old %s' %(lnum,old))
   outarr.append('%s new %s' %(lnum,new))
   outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
 print(case,'line changes written to',fileout)
 
if __name__=="__main__":
 #testsplit()
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # auth_2.txt
 fileout = sys.argv[3] # possible change transactions
 fileout1 = sys.argv[4] # abbr_2.txt  - has counts
 abbrs = init_abbr(filein1)

 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]

 #skip_abbrs = ['A.','N.','P.','U.','Dāy.','H.','K.','N.','P.','R.','Ś.','Subh.','U.','V.','Vaiś.']
 abbrs0 = [x for x in abbrs if x.code == 'ls']
 init_regexes(abbrs0)  # compute regexes used by replace_abbr
 abbrs1 = sorted(abbrs0 , key = lambda x : len(x.abbr),reverse=True)

 # save copy of lines for write_changes
 lines0 = []
 for line in lines:
  lines0.append(line)
                 
 count = 0
 for iline,line in enumerate(lines):
  m = re.search(r'<ls>[^<]*</ls>$',line)
  if m == None:
   continue
  changed = update_lines(iline,lines,m.group(0),abbrs1)
  if changed:
   count = count + 1
 print(count,'lines changed')
 write_new(fileout,lines)

 write_changes(fileout1,lines0,lines)
