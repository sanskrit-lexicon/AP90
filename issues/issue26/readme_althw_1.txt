
readme_althw_1.txt 
32176 matches for "^<L>" in buffer: temp_ap90_2.txt
29441 matches for "<k2>[a-zA-Z]+$" in buffer: temp_ap90_2.txt
    9 matches for "<h>"  homonym metalines, no alt headwords.
(- 32176 (+ 29441 9)) = 2726  probable alt headword metalines

456 matches for "{{Lbody=" in buffer: temp_ap90_2.txt
  The pattern here in metaline for L is an alternate expressed with
  parentheses in <k2> of metaline.
  Example:
  <L>602<pc>0032-b<k1>atipAdanicft<k2>atipAdanicf(vf)t
   ...
  <LEND>
  <L>602.01<pc>0032-b<k1>atipAdanivft<k2>atipAdanivft
  {{Lbody=602}}
  <LEND>

(- 2726 456) = 2270  probable alternate headwords UNMARKED.
----------------
Many additional alternates are expressed with commas in k2
1614 matches for "k2>.*," in buffer: temp_ap90_2.txt
  Some of these k2's are complex.
Here is one simple pattern 
702 matches for "<k2>[a-zA-Z]+, *[a-zA-Z]+$"
  Example:
  <L>294<pc>0020-c<k1>aMgiraH<k2>aMgiraH, aMgiras
  Insert lines after <LEND>of 294:
  <L>294.1<pc>0020-c<k1>aMgiras<k2>aMgiras
  {{Lbody=294}}
  <LEND>

  These 702 instances  should be doable by a program.

-------------------------------
Construct temp_ap90_3.txt for these 702 cases.

python althw_1.py temp_ap90_2.txt temp_ap90_3.txt
265597 lines read from temp_ap90_scott_usha.txt
32176 Entry records, 0 nonEntry records
ERROR meta_next= <L>11180.01<pc>0411-c<k1>kuraMgamaH<k2>kuraMgamaH
701 althw entries constructed
write_recs output to temp_ap90_3.txt
32176 Entry records, 2103 nonEntry records

Note 1:  The ERROR line above is not a problem.
Note 2: (+ 32176  701) = 32877
grep -E '<L>' temp_ap90_3.txt | wc -l
32877   # so 701 new (alternate) headwords

-----------------
# remake displays from temp_ap90_3.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_3.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

-------------------------------------------
# commit changes to github
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
diff temp_ap90_3.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0 expected
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap90 corrections  (althw_1)
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
-----------------

# sync cologne
csl-orig  # git pull
# regenerate displays

--------------------------------------
# document changes
diff temp_ap90_2.txt temp_ap90_3.txt > diff_2_3.txt

