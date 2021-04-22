Ref: https://github.com/sanskrit-lexicon/AP90/issues/7

26750 matches for "-$" in buffer: ap90.txt
25544 matches for " [a-zA-Z]+-$" in buffer: ap90.txt

Objective: resolve these hyphenations.

Example:
OLD:
<>{#samadakziRA#} Rām. {@--4@} Not handy, skil-
<>ful or clever; awkward. {@--5@} Un-
<>favourable.

NEW: remove hyphen - a third possibility
<>{#samadakziRA#} Rām. {@--4@} Not handy, <lbinfo n="skil+ful"/>
<>skilful or clever; awkward. {@--5@} <lbinfo n="Un+favourable"/>
<>Unfavourable.


# assume we are in a temp directory of v02/ap90 in csl-orig repository.

cp ../ap90.txt ap90_0.txt
This work was done with ap90.txt at commit d1a09082de43262eb6638a0e33712ce167a17bba of csl-orig.

# Generate change transactions to accomplish the task of the Example:
python hyphen_eng.py ap90_0.txt hyphen_changes.txt hyphen_questions.txt

26749 potential changes found
26652 written to hyphen_changes.txt
97 written to hyphen_questions.txt

Note: In 3000+ instances, there are consecutive lines ending in '-'.

## apply the change transactions to the digitization
python updateByLine.py ap90_0.txt hyphen_changes.txt ap90_1.txt

# program to restore the hyphens.  This is done to be sure we can restore.
python restore_hyphen_eng.py ap90_1.txt hyphen_restore_changes.txt

python updateByLine.py ap90_1.txt hyphen_restore_changes.txt ap90_0_restore.txt
# we expect that ap90_0_restore.txt is what we started with.
diff ap90_0.txt ap90_0_restore.txt
# no difference, as expected
# don't need ap90_0_restore.txt any longer
rm ap90_0_restore.txt

Now install ap90_1.txt
# assume we are in temp subdirectory of csl-orig/v02/ap90
cp ap90_1.txt ../ap90.txt

# regenerate dictionary files via usual csl-pywork/v02 script.
# At cologne, this is

sh generate_dict.sh ap90  ../../AP90Scan/2020/


# suggestions for further improvement.
1. hyphen_questions.txt
  There are about 100 cases of lines in ap90.txt that still end in '-';
  but they were not amenable to the hyphenation removal process.
2. 'type=false' in hyphen_changes.txt
  After resolution of hyphens, the resulting word was checked against
  an English spell check dictionary.  About 3000 of the 26000 cases
  were NOT confirmed.  These could be checked.
  
