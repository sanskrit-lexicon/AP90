# coding=utf-8
""" althw_census_diff.py
"""
from __future__ import print_function
import sys, re,codecs
from althw_2_prep import init_altins

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

def altin_dict_L(altins):
 d = {}
 for altin in altins:
  L = altin.Lparent
  if L in d:
   print('ERROR: altin_dict_L: unexpected duplicate Lparent=%s' % L)
   exit(1)
  d[L] = altin
 return d

def altin_diff1(altins1,altins2,filein1,filein2):
 d1 = altin_dict_L(altins1)
 d2 = altin_dict_L(altins2)
 s1 = set(d1.keys())
 s2 = set(d2.keys())
 s1only = s1.difference(s2)
 s2only = s2.difference(s1)
 print(len(s1only),"only in",filein1)
 for L in s1only:
  a = d1[L]
  print(a.line)
 print(len(s2only),"only in",filein2)
 for L in s2only:
  a = d2[L]
  print(a.line)
 
  
if __name__=="__main__":
 filein1 = sys.argv[1]  #
 filein2 = sys.argv[2] 
 fileout = sys.argv[3] # 
 altins1 = init_altins(filein1)
 altins2 = init_altins(filein2)
 diffsa = altin_diff1(altins1,altins2,filein1,filein2)
 
 exit(1)
 for altin in altins:
  altin_adjust(altin)
 outlines = altin_lines(altins)
 write_lines(fileout,outlines)
 fileout1 = 'tempwork.txt'
 #helper1(fileout1,altins)
 #helper2(fileout1,altins)
 helper3(fileout1,altins)
 
