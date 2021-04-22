
Start with csl-orig/v02/ap90/ap90.txt
   at commit 29e18e69b49f79d8b2411df35d79bcdea6bf6195

cp ../ap90.txt ap90_0.txt

Changes were made to ap90_0.txt in several steps, ending with ap90_5.txt.
The 'redo.sh' script goes through all the steps.
Then ap90_5.txt was used to revise csl-orig/v02/ap90/ap90.txt
  at commit 19c7ee9c3f1edc04e8975b00bf55f04b3825caea.

Following are discussions of the steps taken by redo.sh

ap90_0a.txt
python change0a.py ap90_0.txt change0a.txt
   16 {%As%}val. -> Āśval.
  236 {%S.%} -> Ś.
    4 {%S.%} Til. -> Ś. Til.
python updateByLine.py ap90_0.txt change0a.txt ap90_0a.txt

ap90_0b.txt
 Miscellaneous manual changes
change0b.txt  manual
 [Help with additional changes.
  The output is edited manually and merged into change0b.txt
  python change_misc.py ap90_0a.txt temp_changes.txt
  python change_misc2.py ap90_0a.txt temp_changes.txt
 ]
python updateByLine.py ap90_0a.txt change0b.txt ap90_0b.txt

abbr_1.txt and auth_1.txt are from header part of ap90.txt.
Added A. D.  and B. C.  to abbr_1.txt
python abbrauth.py abbr_1.txt auth_1.txt abbrauth_1.txt
python abbrauth.py abbr_1a.txt auth_1.txt abbrauth_1a.txt

269 total abbreviations
269 written to abbrauth_1.txt
dup 1 N.:ab:49:Name.
dup 2 N.:ls:100:Naiṣadhacarita.

dup 1 P.:ab:54:Parasmaipada.
dup 2 P.:ls:107:Pāṇini's Aṣṭādhyāyī.

dup 1 U.:ab:70:Ubhayapada (Parasmai. and Ātmane.)
dup 2 U.:ls:158:Uttararāmacarita.

15 type 2 duplicates
dup 1 A.:ab:0:Ātmanepada.
dup 2 A. S.:ab:8:Anglo-Saxon.
dup 3 A. D.:ab:75:Anno Domini = CE (Common Era)
dup 4 A. L.:ls:2:Ānandalaharī.
dup 5 A. R.:ls:5:Anargharāghava (published in the Kāvyamālā).

dup 1 N.:ab:49:Name.
dup 2 N.:ls:100:Naiṣadhacarita.

dup 1 P.:ab:54:Parasmaipada.
dup 2 P.:ls:107:Pāṇini's Aṣṭādhyāyī.
dup 3 P. P.:ls:109:Pārvatīpariṇaya.
dup 4 P. R.:ls:110:Prasannarāghava.

dup 1 U.:ab:70:Ubhayapada (Parasmai. and Ātmane.)
dup 2 U.:ls:158:Uttararāmacarita.

dup 1 Dāy.:ls:35:Dāyabhāga.
dup 2 Dāy. B.:ls:36:Dāyabhāga.

dup 1 H.:ls:51:Hitopadeśa (Nirṇaya Sāgara Edition).
dup 2 H. D.:ls:55:Haṃsadūta.

dup 1 K.:ls:59:Kādambarī (Bombay).
dup 2 K. P.:ls:73:Kāvyaprakāśa.

dup 1 N.:ls:100:Naiṣadhacarita.
dup 2 N.:ab:49:Name.

dup 1 P.:ls:107:Pāṇini's Aṣṭādhyāyī.
dup 2 P.:ab:54:Parasmaipada.
dup 3 P. P.:ls:109:Pārvatīpariṇaya.
dup 4 P. R.:ls:110:Prasannarāghava.

dup 1 R.:ls:115:Raghuvaṃśa (Bombay).
dup 2 R. G.:ls:121:Rasagaṅgādhara (published in the Kāvyamālā).

dup 1 Ś.:ls:124:Śakuntalā (Bombay).
dup 2 Ś. Til.:ls:146:Śṛṅgāratilaka.

dup 1 Subh.:ls:147:Subhāṣitaratnākara (Bombay).
dup 2 Subh. Ratn.:ls:149:Subhāṣitaratnabhāṇḍāgāra (Bombay)

dup 1 U.:ls:158:Uttararāmacarita.
dup 2 U.:ab:70:Ubhayapada (Parasmai. and Ātmane.)

dup 1 V.:ls:166:Vikramorvaśīyam (Bombay).
dup 2 V. May.:ls:181:Vyavahāramayūkha (Mr. Mandlik's Edition).
dup 3 V. P.:ls:184:Viṣṇu Purāṇa.
dup 4 V. Ratn.:ls:185:Vṛttaratnākara.
dup 5 V. Sah.:ls:187:Viṣṇusahasranāman.

dup 1 Vaiś.:ls:168:Vaiśeṣika.
dup 2 Vaiś. Sūt.:ls:169:Vaiśeṣikasūtras.


Example:
dup 1 A.:ab:0:Ātmanepada.
dup 2 A. S.:ab:8:Anglo-Saxon.
dup 3 A. L.:ls:2:Ānandalaharī.
dup 4 A. R.:ls:5:Anargharāghava (published in the Kāvyamālā).

A. is both an abbreviation,and the start of other abbreviations.
Thus, A. at the end of a line could be any of the 4 possibilities.

For any abbreviation other than those above, finding the text (other
than in {#...#}, should be safe to mark.

Some (20) abbreviations occur in italics: Example: {%m.%}
These can be marked as '{%<ab>m.</ab>%}'.

For literary source abbreviations,  we want to include verse references
Rv. 1. 191. 7. -> <ls>Rv. 1. 191. 7.</ls>  146 are 'like' this.
But some such are split across lines; 20 occur at end of lines like:

<>Unconscious {#(ajYAna);#} {#ketuM kfRvannaketave#} Rv.
<>1. 6. 3. ({#ajYAnAya#}); shapeless (?)

And there are a few with incomplete references.


prep1 deals only with general abbreviations (code=='ab' in abbrauth_1)
python prep1.py ap90_0b.txt abbrauth_1.txt ap90_1.txt abbr_2.txt
python prep1.py ap90_0b.txt abbrauth_1a.txt ap90_1a.txt abbr_2a.txt

38022 lines changed
write 267150 lines to ap90_1.txt
77 records written to abbr_2.txt
abbr_2.txt has counts of number of lines for each abbreviation.
Known deficiencies:
  ' A.', ' P'

prep2 deals only with literary source abbreviations (code == 'ls')
python prep2.py ap90_1.txt abbrauth_1.txt ap90_2.txt auth_2.txt
Open questions:
Bhāv. P.  typo line 57474 -> Bhāva. P.
auth_2.txt contains 'numnums' data for each.
Example: Rv.:ls:123:Ṛgveda (Max Müller's Edition).:203:20,22,15,146:3
 203 = total number of instances.
  20 = number of instances with no ' [0-9]+' following (such as at end of line)
  22 = number followed by only 1 ' [0-9]+'
  15 = number followed by only 2 ' [0-9]+[.] [0-9]+'
 146 = number of instances  followed by ' [0-9]+[.] [0-9]+[.] [0-9]+'
 (+ 146 15 22 20) == 203
 3 = the most frequent number of number sequences after the abbreviation.

Note:  The <ls> elements include all number sequences which
a. follow the abbreviation, and
b. are in the same line as the abbreviation.

Example 1:  completely marked
OLD: (ap90_1.txt)
<>{#vizRurvicakrame#} Rv. 1. 22. 16; {#kimu paramato narta-#} 
NEW: (ap90_2.txt)
<>{#vizRurvicakrame#} <ls>Rv. 1. 22. 16</ls>; {#kimu paramato narta-#} 

Example 2: incompletely marked
OLD:
<>Unconscious {#(ajYAna);#} {#ketuM kfRvannaketave#} Rv.
<>1. 6. 3. ({#ajYAnAya#}); shapeless (?)
NEW: 
<>{#vizRurvicakrame#} <ls>Rv. 1. 22. 16</ls>; {#kimu paramato narta-#} 
<>1. 6. 3. ({#ajYAnAya#}); shapeless (?)

The next step, prep3, will deal with completing such ls markup.

prep3. ap90_2.txt

python prep3.py ap90_2.txt auth_2.txt ap90_3.txt changes3.txt

changes3.txt contains the lines changed in ap90_3.txt. For reference only.

Most (146) Rv. references have 3 following numbers:



Ku.:ls:75:Kumārasambhava (Bombay).:2289:239,213,1833,4:3  -> :2
Māl.:ls:83:Mālatīmādhava (Bombay).:1274:152,405,716,1:3  -> :2
Ms.:ls:95:Manusmṛti.:2675:288,266,2115,6:3
R.:ls:115:Raghuvaṃśa (Bombay).:5297:503,517,4264,13:3
Ś.:ls:124:Śakuntalā (Bombay).:2357:168,1005,1183,1:3
Śi.:ls:136:Śiśupālavadha.:2070:198,174,1695,3:3
Y.:ls:188:Yājñavalkya (Mr. Mandlik's Edition).:808:63,83,661,1:3

['Ku.' ,'Māl.' ,'Ms.' ,'R.' ,'Ś.' ,'Śi.' ,'Y.' ]  max = 2 (from 3)

Dk.:ls:41:Daśakumāracarita (Bombay).:506:130,373,3,0:2
Gīt.:ls:47:Gītagovinda.:444:48,395,1,0:2
K.:ls:59:Kādambarī (Bombay).:1069:210,858,1,0:2
Me.:ls:89:Meghadūta (Bombay).:1043:116,925,2,0:2
A. R.:ls:5:Anargharāghava .:10:2,6,2,0:2

['Dk.', 'Gīt.', 'K.' , 'Me.' , 'A. R.' ]   max = 1 (from 2)


ap90_4.txt
Additional hyphenations, where there is a ' ' at end of line.
python hyphen_eng1.py ap90_3.txt hyphen_eng.txt hyphen_eng_questions.txt

python updateByLine.py ap90_3.txt hyphen_eng.txt ap90_4.txt

ap90_5.txt
Additional devanagari hyphenations: line ends with '-#} ' (space at eol).
hyphen_deva1.py is minor variant of ../hyphen_deva/hyphen2.py

python hyphen_deva1.py ap90_4.txt hyphen_deva.txt hyphen_deva_questions.txt

python updateByLine.py ap90_4.txt hyphen_deva.txt ap90_5.txt
