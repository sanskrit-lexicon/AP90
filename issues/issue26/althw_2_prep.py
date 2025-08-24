# coding=utf-8
""" althw_2_prep.py 
"""
from __future__ import print_function
import sys, re,codecs
from althw_2_man_1 import althw_2_man_1_data

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines from",filein)
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outarr),"lines written to",fileout)

class ALTIN:
 def __init__(self,line):
  self.line = line
  parts = line.split(' : ')
  if len(parts) != 5:
   print('ALTIN error. got %s parts, expected %s' %(len(parts),5))
   exit(1)
  self.Lparent = parts[0]
  self.k2 = parts[1]
  self.k1 = parts[2]
  self.nc = parts[3]
  self.rest = parts[4]
  if self.rest == '?':
   self.children = []
   self.code = '99'
  else:
   self.children = self.rest.split(', ')
   if '(' in self.k2:
    self.code = '-0'
   else:
    self.code = '00'
  
def init_altins(filein):
 lines = read_lines(filein)
 altins = [ALTIN(line) for line in lines]
 return altins

def split_01(k2,k1):
 # k2 = XtA --tvaM  -> XtvaM
 m = re.search(r'^(.*?)tA --tvaM$',k2)
 if m == None:
  return
 X = m.group(1)
 child = '%stvaM' % X
 children = [child]
 return children

def split_02(k2,k1):
 # example: aMkuraH --raM -> aMkuraM
 # or comma: AyuDaH, --DaM -> AyuDaM
 m = re.search(r'^([a-zA-Z]+)(.a)H,? --\2M',k2)
 if m == None:
  return None
 a1 = m.group(1)
 a2 = m.group(2)
 assert k1 == '%s%sH' %(a1,a2)
 child = '%s%sM' %(a1,a2)
 children = [child]
 return children

def split_03(k2,k1):
 # example: amamatA, --tvaM  -> amamatvaM
 m = re.search(r'^([a-zA-Z]+)tA, --tvaM',k2)
 if m == None:
  return None
 a1 = m.group(1)
 assert k1 == '%stA' % a1
 child = '%stvaM' % a1
 children = [child]
 return children

def split_04(k2,k1):
 # example: acApala --lya  -> acApalya
 # example: apApa --pin -> apApin
 m = re.search(r'^([a-zA-Z]+)(.)a,? --(.)([^()]*)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # acApa
 a2 = m.group(2) # l
 assert k1 == '%s%sa' % (a1,a2)
 b1 = m.group(3) # l
 b2 = m.group(4) # ya
 #if k2 == 'apApa --pin': # 'acApala --lya':
 # print(a1,a2,b1,b2)
 if a2 != b1:
  return None
 child = a1 + a2 + b2
 children = [child]
 return children

def split_05(k2,k1):
 # example: aTariH --rI -> aTarI
 m = re.search(r'^([a-zA-Z]+)(.)(iH),? --(.)(I)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # aTa
 a2 = m.group(2) # r
 a3 = m.group(3) # iH
 assert k1 == a1 + a2 + a3
 b1 = m.group(4) # r
 b2 = m.group(5) # I
 if a2 != b1:
  return None
 child = a1 + a2 + b2
 children = [child]
 return children

def split_06(k2,k1):
 # example: aBiBuH --BUH -> aBiBUH
 m = re.search(r'^([a-zA-Z]+)(.)(uH),? --(.)(UH)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # abi
 a2 = m.group(2) # B
 a3 = m.group(3) # uH
 assert k1 == a1 + a2 + a3
 b1 = m.group(4) # B
 b2 = m.group(5) # UH
 if a2 != b1:
  return None
 child = a1 + a2 + b2
 children = [child]
 return children

def split_07(k2,k1):
 # example: vErocanaH, vErocaniH, vErociH -> [vErocaniH, vErociH]
 m = re.search(r'^([a-zA-Z]+), *([a-zA-Z]+), *([a-zA-Z]+)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # vErocanaH
 a2 = m.group(2) # vErocaniH
 a3 = m.group(3) # vErociH
 assert k1 == a1 
 children = [a2,a3]
 return children

def split_08(k2,k1):
 # 'JallarA --rI' -> JallarI
 m = re.search(r'^([a-zA-Z]+)(.)(A),? --(.)(I)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # Jalla
 a2 = m.group(2) # r
 a3 = m.group(3) # A
 if k1 != (a1 + a2 + a3):
  print('split_08 WARNING',k2)
  return None
 b1 = m.group(4) # r
 b2 = m.group(5) # I
 if a2 != b1:
  return None
 child = a1 + a2 + b2
 children = [child]
 return children

def split_09(k2,k1):
 # apasAraRaM --RA -> apasAraRA
 m = re.search(r'^([a-zA-Z]+)(.)(aM),? --(.)(A)$',k2)
 if m == None:
  return None
 a1 = m.group(1) # apasAra
 a2 = m.group(2) # R
 a3 = m.group(3) # aM
 if k1 != (a1 + a2 + a3):
  print('split_WARNING',k2)
  return None
 b1 = m.group(4) # R
 b2 = m.group(5) # A
 if a2 != b1:
  return None
 child = a1 + a2 + b2
 children = [child]
 return children


def split_98(k2,k1):
 # manual
 if k2 in althw_2_man_1_data:
  return althw_2_man_1_data[k2]
 return None

altin_adjust_data = [
  ('98',split_98), # manual
  ('01',split_01),
  ('02',split_02),
  ('03',split_03),
  ('04',split_04),  # acApala --lya
  ('05',split_05),  # aTariH --rI
  ('06',split_06),  # aBiBuH --BUH
  ('07',split_07),  # vErocanaH, vErocaniH, vErociH
  ('08',split_08),  # JallarA --rI
  ('09',split_09),  # apasAraRaM --RA
  # ('10',split_10),  # kaMkaRaH --RaM
  ]

def altin_adjust(altin):
 if altin.children != []:
  # already adjusted
  return

 for fcode,f in altin_adjust_data:
  result = f(altin.k2,altin.k1)
  if result != None:
   children = result
   altin.children = children
   altin.rest = ', '.join(children)
   altin.nc = str(len(children))
   altin.code = fcode
   return
   
def altin_lines(altins):
 altins1 = sorted(altins,key = lambda x: x.code)
 outlines = []
 n1 = 0 # number done
 n2 = 0 # number not done
 for a in altins1:
  fields = [a.code,a.Lparent,a.k2,a.k1,a.nc,a.rest]
  outline = ' : '.join(fields)
  outlines.append(outline)
  if a.rest == '?':
   n2 = n2 + 1
  else:
   n1 = n1 + 1
 print('%s done, %s todo' %(n1,n2))
 return outlines

def helper1(fileout,altins):
 outlines = []
 outlines.append('workdata=[')
 regexk2 = r'^([a-zA-Z]+),? --([a-zA-Z]+)$'
 for altin in altins:
  if altin.nc != '0':
   continue
  k1 = altin.k1
  k2 = altin.k2
  m = re.search(regexk2,k2)
  if m == None:
   continue
  assert k1 == m.group(1)
  k2a = m.group(2)
  out = "  '%s' : ['%s %s']," % (k2,k1,k2a)
  outlines.append(out)
 outlines.append(' ]')
 write_lines(fileout,outlines)

def helper2(fileout,altins):
 outlines = []
 outlines.append('workdata=[')
 #regexk2 = r'^([a-zA-Z]+),? --([a-zA-Z]+)$'
 nrec = 0 # number of altin records written
 for altin in altins:
  if altin.nc != '0':
   continue
  k1 = altin.k1
  k2 = altin.k2
  if not ('(' in k2):
   continue
  nrec = nrec + 1
  parts = k2.split(' ')
  q = '"'
  key = k2
  indent = '  '
  outlines.append(q + k2 + q + ':' + '[')
  for ipart,part in enumerate(parts):
   part1 = re.sub(r'[,-]','',part)
   if ipart == 0:
    outlines.append(indent + '# k1 = ' + k1)
    if '(' in part1:
     outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
   else:
    outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
    if '(' in part1:  # repeat
     outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
  outlines.append(' ],')
 outlines.append(' ]')
 print('helper2 outputs %s cases' % nrec)
 write_lines(fileout,outlines)

def helper3(fileout,altins):
 outlines = []
 outlines.append('workdata=[')
 #regexk2 = r'^([a-zA-Z]+),? --([a-zA-Z]+)$'
 nrec = 0 # number of altin records written
 for altin in altins:
  #if altin.nc != '0':
  if altin.rest != '?':
   continue
  k1 = altin.k1
  k2 = altin.k2
  nrec = nrec + 1
  parts = k2.split(' ')
  q = '"'
  key = k2
  indent = '  '
  outlines.append(q + k2 + q + ':' + '[')
  for ipart,part in enumerate(parts):
   part1 = re.sub(r'[,-]','',part)
   if ipart == 0:
    outlines.append(indent + '# k1 = ' + k1)
    if '(' in part1:
     outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
   else:
    outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
    if '(' in part1:  # repeat
     outlines.append(indent + q + k1 + ' ' + part1 + q + ',')
  outlines.append(' ],')
 outlines.append(' ]')
 print('helper3 outputs %s cases' % nrec)
 if nrec == 0:
  # so output is empty when no examples
  outlines = []
 write_lines(fileout,outlines)

if __name__=="__main__":
 filein = sys.argv[1]  # 
 fileout = sys.argv[2] # output file  adjusted xxx
 altins = init_altins(filein)
 for altin in altins:
  altin_adjust(altin)
 outlines = altin_lines(altins)
 write_lines(fileout,outlines)
 fileout1 = 'tempwork.txt'
 #helper1(fileout1,altins)
 #helper2(fileout1,altins)
 helper3(fileout1,altins)
 
