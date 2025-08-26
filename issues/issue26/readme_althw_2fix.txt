
readme_althw_2fix.txt
cp temp_ap90_4.txt temp_ap90_5.txt

Apply changes per althw_2_fix2_ab_jim.txt

print change for ap90
10094 : kaRAwInaH : kaRAwArakaH : kaRAwIrakaH : printchange : also AP
15164 : datta : dataka : dattaka : printchange

---------------------
# remake local displays from temp_ap90_5.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_5.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

---------------------------
python althw_census.py temp_ap90_5.txt althw_census_5.txt
2714 parents
3162 children
2714 lines written to althw_census_5.txt

diff althw_census_4.txt althw_census_5.txt > diff_althw_census_4_5.txt

diff temp_ap90_4.txt temp_ap90_5.txt > diff_ap90_4_5.txt

==========================================
comments from althw_2_fix2_ab_jim.txt 
* DONE 4935  aba-hitTA and aba-hitTam are unique to ap90, ap 
old: 4935 : ava(ba)hitTA --tTaM : avahitTA : 2 : abahitTA avahitTaM
new: 4935 : ava(ba)hitTA --tTaM : avahitTA : 2 : abahitTA avahitTaM abahitTaM
status: ok Note:
ABn: 4935 : ava(ba)hitTA --tTaM : avahitTA : 3 : abahitTA avahitTaM abahitTaM ;;count change

----------------------
* DONE 10964  ABQUESTION: Why drop kIdfSI, kIdfkzI?
old: 10964 : kIdfSa, kIdfSa : kIdfSa : 1 : kIdfSa
new: 10964 : kIdfS, kIdfSa, --SI, kIdfkza, --kzI : kIdfS : 1 : kIdfSa kIdfSI kIdfkza kIdfkzI
status: ok Note: typo and markup. k2 -> kIdfS, kIdfSa, --SI, kIdfkza, --kzI
ABn: 10964 : kIdfS, kIdfSa, kIdfkza : kIdfS : 2 : kIdfSa kIdfkza

----------------------
* DONE 15861 ABEXception. 
old: 15861 : dvAja, dvAtriMSat, dvAdaSa : dvAja : 2 : dvAtriMSat dvAdaSa
new: 15861 : dvAja, dvAtriMSat, dvAdaSa : dvAja : 2 : dvAtriMSat dvAdaSa
status: nochange Note: Jim thinks no change needed
AB: dvAja (which in no way can be found under ‘dvi’) has to be dvija ;;print change
JIM: dvAja appears in l4v, mw, pw, pwg, vcp. in AP90(AP) these dvA words appear as 'dvi' compounds
     
-----------------------
* DONE 21718  ABException
old: 21718 : bAlhakAH, bAlhikAH, bAlhIkAH : bAlhakAH : 2 : bAlhikAH bAlhIkAH
new: 21718 : bAlhakAH, bAlhikAH, bAlhIkAH : bAlhakAH : 2 : bAlhikAH bAlhIkAH
status: nochange Note: ap: has 'hl'. mw, pw, pwg, vcp have bAlhaka etc.
ABn: 21718 : bAhlakAH, bAhlikAH, bAhlIkAH : bAhlakAH : 2 : bAhlikAH bAhlIkAH ;;In Skt. there is no 'lh' (which, of course, is in Prakrit!); see the entry 25323 below as the corresp. counterpart!
JIM:  This is too complicated! 
      For example, entry 25323 says '{#vahlika, --vahlIka#},¦ see {#bahlika, bahlIka#}.'
      but there is No bahlika or bahlIka (according to ap90).


==========================================
install to github

---------------------
# commit changes to github: csl-orig
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
diff temp_ap90_5.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0 expected
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap90 corrections  (althw_2fix)
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

------------------------------
ap90_printchange.txt edit for 2 print changes above

# commit changes to github: csl-corrections
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "ap90 print changes
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

-----------------
# sync cologne
csl-orig  # git pull
csl-corrections # git pull
# regenerate displays for ap90, ap

==========================================

==========================================
OLD  DELETE
==========================================

====================================================


----------------
# sync cologne
csl-orig  # git pull
csl-corrections # git pull
# regenerate displays for ap90

---------------------

# sync this repo to github
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
git pull
git add .
git commit -m "#26 - althw_2fix"
git push
