
Analysis of ap90 verbs
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/ap90/.

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

* ap90_verb_filter.
ap90 has prefixed verbs as separate entries (like MW, in contrast to pwg, etc.).

python ap90_verb_filter.py ../ap90.txt ap90_verb_exclude.txt ap90_verb_include.txt ap90_verb_filter.txt

ap90_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  
ap90_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns.
These files are derived empirically.

Patterns for roots:  
 C = '[0-9][.]? [AUP][.]'  class-pada.  Examples: 1 A., 2 P., 1 U.
 D = 'Den[.] [AUP][.]'   Den.-pada  (Denominative)
 P = ' [AUP][.]'   Pada only 

Counts of total patterns:
3338 C
0286 D
0008 P

Total 3632 entries identified as verbs.
These can be verbs or prefixed verbs.

Format of file ap90_verb_filter.txt by ecample:
;; Case 0001: L=3, k1=aMS, k2=aMS, code=C
;; Case 0007: L=238, k1=aGAyati, k2=aGAyati, code=D
;; Case 0012: L=310, k1=aMG, k2=aMG, code=P

Note that for Denominatives, the headword is a 3rd singular form.

* ap90_verb_filter_map
python ap90_verb_filter_map.py ap90_verb_filter.txt mwverbs1.txt ap90_verb_filter_map.txt

Correspondences between ap90 verb spellings and
 - ap90 verb spellings
 - mw verb spellings

Uses some empirically derived rules, and some empirically derived mappings.

Format of ap90_verb_filter_map.txt:
 Adds a field mw=xxx to each line of ap90_verb_filter.txt,
indicating the MW root believed to correspond to the AP90 root.
For example, aMSay in AP90 is believed to correspond to aMS in MW.
;; Case 0001: L=13, k1=aMSay, k2=aMSay, code=N, mw=aMS

In 70 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0044: L=3913, k1=apary, k2=apary, code=N, mw=?

In case the matched verb is a prefixed verb in MW,  the parse of MW preverb
is also present. For example:
;; Case 0026: L=520, k1=atikram, k2=atikram, code=C, mw=atikram ati+kram

1740 of the verbs found in ap90 are matched to prefixed verbs in MW.
1822 of the verbs are considered non-prefixed verbs in MW.
  70 of the ap90 verbs are not currently matched to MW verbs.
3632 count of all ap90 verb entries found.

2987 of the matching verbs are spelled the same by AP90 and MW.
 575 of the matching verbs are spelled differently by AP90 and MW.

* ap90_verb1.txt and ap90_verb1_deva.txt
python verb1.py slp1 ../ap90.txt ap90_verb_filter_map.txt ap90_verb1.txt
python verb1.py deva ../ap90.txt ap90_verb_filter_map.txt ap90_verb1_deva.txt

These two files print the underlying ap90 text for all the verbs.
One prints Sanskrit text in SLP1, and the other prints Sanskrit text in
Devanagari.
