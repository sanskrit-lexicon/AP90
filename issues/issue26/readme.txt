Begun 07-02-2025

This directory
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26

cp /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90/ap90_correctionform.txt issue26/ap90_correctionform.txt

This file will be edited as items are processed.

ap90.txt version that will be edited:
at commit c3cbf0b171cdeab39ff241be27575270535c4cea of csl-orig

cd /c/xampp/htdocs/cologne/csl-orig
git show c3cbf0b1:v02/ap90/ap90.txt > /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26/temp_ap90.txt
# note 

----------------------------------------------------
=======================================================
Part 1 08-15-2025
=======================================================
ap90_correctionform_scott_usha.txt
  Notes by Usha, Jim based on ap90_correctionform.txt
---
temp_ap90_scott_usha.txt  revision of ap90.

'usha' = Usha Sanka = Github user @Shalu411  
Next step: Jim to install.
----------------------------------------------------
diff temp_ap90.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
# 0 --  Good! no changes to csl-orig/../ap90.txt since 07-02-2025.

python diff_to_changes_dict.py temp_ap90.txt temp_ap90_scott_usha.txt change_1.txt
432 changes written to change_1.txt

----------------------------------------------------
Separate ap90_correctionform_scott_usha.txt into 'types'

case_curlynum.txt:   10
case_eng_hyphen.txt: 62
case_nochange.txt:   21
case_simple.txt:     26

case_LBdash.txt:     11
case_althw.txt:       8
case_pending.txt:     7
                     Total = 143, as expected

# remake displays from temp_ap90_scott_usha.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_scott_usha.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

# commit changes to github
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
diff temp_ap90_scott_usha.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0 expected
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap90 corrections.
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

# this repo
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
git pull
git add .
git commit -m "#26 - part 1"
git push

comment in https://github.com/sanskrit-lexicon/AP90/issues/26
End of part 1

=======================================================
Part2: LBdash  temp_ap90_2.txt
=======================================================
Example: ({#--jaM#}) -> {#--(jaM)#}
In ap90, the markup {#--X#} of ap90.txt is changed
by make_xml.py in two steps:
 {#--X#} -> <s>--X</s>  -> <div n="1"/><b>—</b> <s>X</s>
 In displays, <div n="1"/> gemerates a line break.
When parens are added we end up with
 ({#--X#})  ->  (<div n="1"/><b>—</b> <s>X</s>)
 So in display '(' is followed by line break, not good.

A simple change in ap90.txt solves this problem
 ({#--X#}) -> {#--(X)#}
-----------------------
python LBdash.py temp_ap90_scott_usha.txt temp_ap90_2.txt

python diff_to_changes_dict.py temp_ap90_scott_usha.txt temp_ap90_2.txt change_2.txt
1790 changes written to change_2.txt

# remake displays from temp_ap90_2.txt
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
cp temp_ap90_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

# commit changes to github
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
diff temp_ap90_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0 expected
cd /c/xampp/htdocs/cologne/csl-orig
git pull
git add .
git commit -m "ap90 corrections  (LBdash)
Ref: https://github.com/sanskrit-lexicon/AP90/issues/26"
git push
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26

# this repo
cd /c/xampp/htdocs/sanskrit-lexicon/ap90/issues/issue26
git pull
git add .
git commit -m "#26 - part 2"
git push

=======================================================

----------------------------------
Jim TODO global
-------------------
case_LBdash.txt
 ({#--jaM#}) -> {#--(jaM)#}  ref LBdash.png
1825 matches for "({#--[^#]+#})" in buffer: temp_ap90_scott_usha.txt
-------------------
case_curlynum.txt
Some {N} were changed.  Probably some remain
-------------------

