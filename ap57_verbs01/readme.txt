
Analysis of ap57 verbs
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/ap57/.

The shell script redo.sh reruns 5 python programs, from mwverb.py to verb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* ap57_verb_filter.
ap57 has prefixed verbs as separate entries (like MW, in contrast to pwg, etc.).

python ap57_verb_filter.py temp_ap57.txt ap57_verb_exclude.txt ap57_verb_include.txt ap57_verb_filter.txt

ap57_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  
ap57_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns.
These files are derived empirically.

Patterns for roots:  
 D = 'Den[.] [AĀUP][.]'   # Denominative
 € = '€[0-9, ]*[AĀUP][.]' # class pada  standard form with €
 C = '[0-9, ]*[AĀUP][.]', # class pada  standard form without €
 T = ' To '   # some have only this English definition pattern
 X = other (from ap57_verb_include.txt)

Counts of total patterns:
0316 D
2979 €
0469 C
0286 T
0123 X

Total 3978 entries identified as verbs.
These can be verbs or prefixed verbs.

Format of file ap57_verb_filter.txt by ecample:
;; Case 0006: L=214, k1=agadyati, k2=agadyati, code=D, mw=agadya
;; Case 0001: L=3, k1=aMS, k2=aMS, code=€, mw=aMS
;; Case 0007: L=267, k1=aG, k2=aG, code=C, mw=aG
;; Case 0090: L=1737, k1=anuGaww, k2=anuGaww, code=T, mw=anuGaww anu+Gaww
;; Case 0192: L=2515, k1=apakfz, k2=apakfz, code=X, mw=apakfz apa+kfz


Note that for Denominatives, the headword is a 3rd singular form.

* ap57_verb_filter_map
python ap57_verb_filter_map.py ap57_verb_filter.txt mwverbs1.txt ap57_verb_filter_map.txt

Correspondences between ap57 verb spellings and
 - ap57 verb spellings
 - mw verb spellings

Uses some empirically derived rules, and some empirically derived mappings.

Format of ap57_verb_filter_map.txt:
 Adds a field mw=xxx to each line of ap57_verb_filter.txt,
indicating the MW root believed to correspond to the AP57 root.
For example, agadyati in AP57 is believed to correspond to agadya in MW.
;; Case 0006: L=214, k1=agadyati, k2=agadyati, code=D, mw=agadya

In 98 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0049: L=1011, k1=aDarIkf, k2=aDarIkf, code=D, mw=?

In case the matched verb is a prefixed verb in MW,  the parse of MW preverb
is also present. For example:
;; Case 0052: L=1048, k1=aDikram, k2=aDikram, code=X, mw=aDikram aDi+kram

1926 of the verbs found in ap57 are matched to prefixed verbs in MW.
  98 of the ap57 verbs are not currently matched to MW verbs.
1954 of the verbs are considered non-prefixed verbs in MW.
3978 count of all ap57 verb entries found.

3595 of the matching verbs are spelled the same by AP57 and MW.
 383 of the matching verbs are spelled differently by AP57 and MW.

* ap57_verb1.txt and ap57_verb1_deva.txt
python verb1.py slp1 temp_ap57.txt ap57_verb_filter_map.txt ap57_verb1.txt
python verb1.py deva temp_ap57.txt ap57_verb_filter_map.txt ap57_verb1_deva.txt

These two files display the underlying ap57 text for all the verbs.
One shows Sanskrit text in SLP1, and the other shows Sanskrit text in
Devanagari.

* ap57_ap90_compare.txt
python compare_filter_map.py ap57_verb_filter_map.txt ../../ap90/temp_verbs01/ap90_verb_filter_map.txt ap57_ap90_compare.txt

The output shows all ap57 and ap90 verbs in two columns:
.......ap57..........     .......ap90..........
     3 aMS                   3 aMS         identical spellings
   280 aNk                 247 aMk         identical NORMALIZED spellings
  1737 anuGaww           ---------------   verb in ap57 not in ap90
 ---------------      14004 juq            verb in ap90 not in ap57

Based on this analysis:
There are 8 verbs in ap90 but not in ap57.
There are 300 verbs in ap57 but not in ap90.
