
Ref: https://github.com/sanskrit-lexicon/AP90/issues/7
Markup re hyphenated Devanagari text at end of lines.
This word was done in a temporary subdirectory of local installation
of csl-orig/v02/ap90/.


# Begin with ap90.txt at commit 8c0e6e90f14b82792361c7e014376d3346c38b8a
cp ../ap90.txt ap90_0.txt

13601 matches for "-#}$" in buffer: ap90_0.txt

Objective: resolve these hyphenations.
Because '--' has special significance in the digitization,
the changes are best done in stages.
The last stage is Stage 3.

redo.sh does all the changes , ending with ap90_3.txt.
This is then installed as csl-orig/v02/ap90/ap90.txt
The new csl-orig commit is 29e18e69b49f79d8b2411df35d79bcdea6bf6195.



#-----------------------------------------------------
Stage 0a. Manual changes
changes0_edit.txt
python updateByLine.py ap90_0.txt changes0_edit.txt ap90_0a.txt
53 change transactions from changes0_edit.txt

#-----------------------------------------------------
Stage 0b. ' #}{#' -> '#} {#'  AND '#}{# ' -> '#} {#'
python spacechg.py ap90_0a.txt changes_0b.txt
986 written to changes_0b.txt
  730 space end deva
  256 space begin deva

python updateByLine.py ap90_0a.txt changes0b.txt ap90_0b.txt

#-----------------------------------------------------
Stage 1.
Example:
OLD:
<>are traceable to 1. above. {@--Comp.@} {#--aM-#}
<>{#SaH#} [{#za#}. {#ta#}.] a secondary incarnation;
NEW:
<>are traceable to 1. above. {@--Comp.@} <lbinfo n="--aM#SaH"/>
<>{#--aMSaH#} [{#za#}. {#ta#}.] a secondary incarnation;

python hyphen1.py ap90_0b.txt changes1.txt questions1.txt
1232 potential changes found
1232 written to changes1.txt
0 written to questions1.txt

python updateByLine.py ap90_0b.txt changes1.txt ap90_1.txt
2464 change transactions from changes1.txt

#-----------------------------------------------------
Stage 2.
Example:
OLD:
<>to be supplied; {%e. g.;%} {#ºratnapraBa-#}
<>{#vasya yasya#} under {#anaMta#} means
NEW:
<>to be supplied; {%e. g.;%} <lbinfo n="ratnapraBa#vasya"/>
<>{#ºratnapraBavasya yasya#} under {#anaMta#} means


python hyphen2.py ap90_1.txt changes2.txt questions2.txt
12298 potential changes found
12298 written to changes2.txt
0 written to questions2.txt

python updateByLine.py ap90_1.txt changes2.txt ap90_2.txt

#-----------------------------------------------------
Stage 3. There are 35 or so cases ending in '{#--#}'
generate prototype changes for these, with lbinfo
Example:
OLD:
<>of light. {#--DaraH,#} {#--patiH --Bft, --bARaH--Bartf#}. {#--#}
<>{#svAmI#} the sun, (bearer of rays or
NEW:
<>of light. {#--DaraH,#} {#--patiH --Bft, --bARaH--Bartf#}. 
<>{#--svAmI#} the sun, (bearer of rays or
NOTE: This leaves a space at the end of first line.

python hyphen3.py ap90_2.txt changes3.txt questions3.txt

python updateByLine.py ap90_2.txt changes3.txt ap90_3.txt


#-----------------------------------------------------
It may be useful to know how to restore the hyphens.

# program to restore the hyphens from ap90_1.txt
python restore1.py ap90_1.txt restore1.txt

python updateByLine.py ap90_1.txt restore1.txt ap90_0_restore1.txt
diff ap90_0b.txt ap90_0_restore1.txt
# no difference, as expected
rm ap90_0_restore1.txt

# program to restore the hyphens from ap90_2.txt
python restore2.py ap90_2.txt restore2.txt

python updateByLine.py ap90_2.txt restore2.txt ap90_1_restore2.txt
diff ap90_1.txt ap90_1_restore2.txt
# no difference, as expected
rm ap90_1_restore2.txt

# program to restore the hyphens from ap90_3.txt
python restore3.py ap90_3.txt restore3.txt

python updateByLine.py ap90_3.txt restore3.txt ap90_2_restore.txt
diff ap90_2.txt ap90_2_restore.txt
# no difference, as expected
rm ap90_2_restore.txt
