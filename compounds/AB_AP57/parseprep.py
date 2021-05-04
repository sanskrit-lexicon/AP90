#-*- coding:utf-8 -*-
"""
 
 
"""
from __future__ import print_function
import sys, re,codecs

class Raw(object):
 n = 0
 def __init__(self,line):
  parts = line.split('\t')
  self.a,self.b,self.c = parts
  flag = False
  for u,v in (('<p>','<p>'),('<b>','<+>'),('<c>','<c>')):
   if self.b.startswith(u) and self.c.startswith(v):
    flag = True
    break
  if not flag:
   print('error?:',line)
   #exit(1)

  """
  if Raw.n < 10:
   print(len(parts),line)
   print('--%s:%s:%s' %(parts[0],parts[1],parts[2]))
  Raw.n = Raw.n + 1
  assert len(parts) == 3
  """
class Entry(object):
 pass

def replace(lines):
 replacements = {
  'Comp. (apfTak)	<b>-DarmaSIla	 <+>apfTagDarmaSIla':
  'Comp. (apfTak)	<b>-DarmaSIla	<+>apfTagDarmaSIla',
  '0540-15/15	<p>kartarikA, kartarI	':
  '0540-15/15	<p>kartarikA, kartarI	<p>kartarikA, kartarI',
  '0693-15/15	<p>caRqA, -RqI	':
  '0693-15/15	<p>caRqA, -RqI	<p>caRqA, caRqI',
  '0728-4/4	<p>jambu, -mbU	':
  '0728-4/4	<p>jambu, -mbU	<p>jambu, jammbU',
  '0801-3/3	<p>dantAvalaH, dantin	':
  '0801-3/3	<p>dantAvalaH, dantin	<p>dantAvalaH, dantin',
  '1085-21/21		<p>pratyagra':
  '1085-21/21	<p>pratyagra	<p>pratyagra',
  '0462-14/14 (upaSama)	<p>upaSamaH	<p>upaSamaH':
  '0462-14/14	<p>upaSamaH	<p>upaSamaH',
  # under hw 'raH'. not found in ap90
  'Comp. ???	<b>-vipulA	<+>vipulA???':
  '		'

 }
 irepl = 0
 for iline,line in enumerate(lines):
  if line in replacements:
   newline = replacements[line]
   lines[iline]=newline
   irepl = irepl+1
   if True:
    print('old:',line)
    print('new:',line)
    print()
 print(irepl,'lines replaced')
 
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"in",filein)
 replace(lines) # modify lines in place
 # remove empty lines
 lines1 = [x for x in lines if not x.startswith('\t\t')]
 print(len(lines1),"lines after removing 'empty' lines")
 # remove '*-*-' lines  (roughly at 100 pages)
 lines1 = [x for x in lines1 if not x.startswith('*-*-')]
 print(len(lines1),"lines after removing '*-' lines")
 rawrecs = [Raw(x) for x in lines1]
 with codecs.open(fileout,"w","utf-8") as f:
  for x in lines1:
   f.write(x+'\n')
 print(len(lines1),"lines written to",fileout)

