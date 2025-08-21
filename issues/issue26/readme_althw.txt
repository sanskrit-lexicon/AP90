
456 matches for "{{Lbody=L" in buffer: temp_ap90_2.txt
  The pattern here in metaline for L is an alternate expressed with
  parentheses in <k2> of metaline.
  Example:
  <L>602<pc>0032-b<k1>atipAdanicft<k2>atipAdanicf(vf)t
   ...
  <LEND>
  <L>602.01<pc>0032-b<k1>atipAdanivft<k2>atipAdanivft
  {{Lbody=602}}
  <LEND>

Many additional alternates are expressed with commas in k2
1614 matches for "k2>.*," in buffer: temp_ap90_2.txt
  Some of these k2's are complex.
702 matches for "<k2>[a-zA-Z]+, *[a-zA-Z]+$"
  Example:
  <L>294<pc>0020-c<k1>aMgiraH<k2>aMgiraH, aMgiras
  Insert lines after <LEND>of 294:
  <L>294.1<pc>0020-c<k1>aMgiras<k2>aMgiras
  {{Lbody=294}}
  <LEND>

  This should be doable by a program.
  
python althw_1.py temp_ap90_scott_usha.txt temp_ap90_2.txt
265597 lines read from temp_ap90_scott_usha.txt
32176 Entry records, 0 nonEntry records
ERROR meta_next= <L>11180.01<pc>0411-c<k1>kuraMgamaH<k2>kuraMgamaH
701 althw entries constructed
write_recs output to temp_ap90_2.txt
32176 Entry records, 2103 nonEntry records

Note 1:  The ERROR line above is not a problem.
Note 2: (+ 32176  701) = 32877
grep -E '<L>' temp_ap90_2.txt | wc -l
32877

-----------------
# remake displays from temp_ap90_2.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

