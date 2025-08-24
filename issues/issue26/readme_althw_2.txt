
readme_althw_2.txt
Starting with temp_ap90_3.txt
Plan to construct temp_ap90_4.txt

python althw_census.py temp_ap90_3.txt althw_census_3.txt
267700 lines read from temp_ap90_3.txt
32877 Entry records, 0 nonEntry records
2727 parents
1157 children
2727 lines written to althw_census_3.txt
--------------------------------------------------
cp temp_ap90_3.txt temp_ap90_3a.txt
# for manual changes

--------------------------------------
changes based on 'case_pending._AB.comments.txt
-----
542 : atiGa : Worth : Wrath : print change to ap90
329 : acitvas : acitvas : acikitvas : print change to ap90, headword change

Also to make print change for acitvas in AP.

--------------------------------------

python althw_census.py temp_ap90_3a.txt althw_census_3a.txt
2714 parents
1157 children

-------
# althw_2_prep.py uses althw_2_man_1.py, which contains a dictionary 
  mapping k2 strings to lists of alternate headwords
  For example: "aMganaM --RaM" : ["aMgaRaM"]

python althw_2_prep.py althw_2_prep.py althw_census_3a.txt  althw_2_input.txt
2714 lines from althw_census_3a.txt
2714 done, 0 todo
2714 lines written to althw_2_input.txt

------------------------------------
# markup the alternate headwords in temp_ap90_4.txt
python althw_2.py temp_ap90_3a.txt althw_2_input.txt temp_ap90_4.txt
1961 althw entries constructed from 1589 parents

grep '^<L>' temp_ap90_3a.txt | wc -l
32877
grep '^<L>' temp_ap90_4.txt | wc -l
34838

(- 34838 32877) = 1961 new entries

--------------
# redo the census using version 4
python althw_census.py temp_ap90_4.txt althw_census_4.txt
2714 parents
3118 children

# compare to  althw_census_3a.txt above,
 2714 althw-parent-entries, and 1157 althw-child-entries
 (- 3118 1157) = 1961  [As expected].
 

python althw_census_diff.py althw_census_3a.txt althw_census_4.txt tempout.txt

The two files have the same set of L-values


====================================================
Finishing up
---------------------
# some documentation

python diff_to_changes_dict.py temp_ap90_3.txt temp_ap90_3a.txt change_3a.txt
116 changes written to change_3a.txt

diff temp_ap90_3a.txt temp_ap90_4.txt > diff_3a_4.txt

---------------------
# remake displays from temp_ap90_3a.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_3a.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------
# remake local displays from temp_ap90_4.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_4.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------
# remake local displays for modified ap.txt (for 2 print changes above)
# changes manual in /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt

cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap  ../../ap
sh xmlchk_xampp.sh ap
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------
# commit change of ap.txt to github
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap 2 changes. Refer readme_althw_2.txt 'print change'
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------
# commit changes to github: csl-orig
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
diff temp_ap90_4.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0 expected
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap90 corrections  (althw_2)
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------
# commit changes to github: csl-corrections
changes to ap90_printchange.txt and ap_printchange.txt

cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "ap90 print changes. 
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26
Ref readme_althw_2.txt 'print change'
"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

-----------------
# sync cologne
csl-orig  # git pull
csl-corrections # git pull
# regenerate displays for ap90, ap

