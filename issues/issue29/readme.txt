
Begin 05-15-2026 Activate link targets for ap90

 
cd /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29 #home

* tempwork/ap90.txt
cd /c/xampp/htdocs/cologne/csl-orig/
git log | head -n 1
# commit 47891de24fdc8cd9e5acdf494d563bbaa33e7a46

git show 47891de2:v02/ap90/ap90.txt > /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29/tempwork/ap90.txt

cd /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29/

* tempwork/ap.txt
cd /c/xampp/htdocs/cologne/csl-orig/
git log | head -n 1
# commit 47891de24fdc8cd9e5acdf494d563bbaa33e7a46

git show 47891de2:v02/ap/ap.txt > /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29/tempwork/ap.txt

cd /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29/


* tooltips for ap
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/ap/pywork/apauth/tooltip.txt ap_tooltip.txt

* tooltips for ap90
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/ap90/pywork/ap90auth/tooltip.txt ap90_tooltip.txt

* tempwork/lsextract_all_ap.txt, lsunknowns_ap.txt
python lsextract_all.py ap tempwork/ap.txt ap_tooltip.txt lsextract_all_ap.txt lsunknowns_ap.txt

* lsextract_all_ap90.txt, lsunknowns_ap90.txt
python lsextract_all.py ap90 tempwork/ap90.txt ap90_tooltip.txt lsextract_all_ap90.txt lsunknowns_ap90.txt

* lsdump_all.txt
python lsdump_all.py ap90 tempwork/ap90.txt ap90_tooltip.txt tempdump/lsdump_all_ap90.txt
330 tooltips from ap90_tooltip.txt
44212 lines written to tempdump/lsdump_all_ap90.txt

* link_target_work_ap.txt
 The link targets for ap.
 copied from from 
    /c/xampp/htdocs/sanskrit-lexicon/AP/issues/issue19/link_target_work.txt
There are 29 active AP link targets.
Mark those that agree in spelling with ap90_tooltip.txt
The first field is the number of instances from lsextract_all_ap90.txt
The first field is the number of instances. 
 For a few, the different ap90 abbrev is noted

Haima 00001 : AP  : 00017	Abh. Cin.	Abhidhāna Cintāmaṇi Kośa.
00037 : AP  : 00079	Ait. Br.	Aitareya Brāhmaṇa, (Bombay).
00125 : AP  : 00187	Ak.	Amarakoṣa, (Bombay).
00004 : AP  : 00422	Av.	Atharva-Veda. 
01037 : AP  : 01541	Bg.	Bhagavadgītā (Tilak Edition).
00930 : AP  : 01051	Bh.	Bhartṛhariʼs three śatakas
00051 : AP  : 02978	Bhāg.	Bhāgavata, (V. Ramaswamy Sastrulu & Sons, Madras).
01311 : AP  : 01634	Bk.	Bhaṭṭikāvya, (Nirṇaya Sāgara, 1928).
00034 : AP  : 00154	Bṛ. S.	Varāhamihiraʼs Bṛhatsamhitā
Ch. P. 00059 : AP  : 00062	C. P.	Caurapañcāśikā.
00476 : AP  : 00506	Gīt.	Gītagovinda.
00613 : AP  : 00688	H.	Hitopadeśa, (आर्यभूषण प्रेस, पुणें, १९३३).
00053 : AP  : 00057	H. Pr.	हितोपदेश-प्रस्ताविका
00021 : AP  : 00059	Hariv.	Harivaṃśa, (चित्रशाळा, पुणें, १९३६).
01388 : AP  : 01871 Ki.	Kirātārjunīya, (Nirṇaya Sāgara, 1922).
00052 : AP  : 00299	Ks.	Kathāsaritsāgara.
02547 : AP  : 02613	Ku.	Kumārasambhava, (Nirṇaya Sāgara, 1916).
00636 : AP  : 00646	M.	Mālavikāgnimitra, (Prin. R. D. Karmarkar, 1933).
00008 : AP  : 00028	Mārk. P.	Mārkaṇḍeya Purāṇa.
00407 : AP  : 04102	Mb.	Mahābhārata, (चित्रशाळा, पुणें , १९२९-३३).
01160 : AP  : 01188	Me.	Meghadūta, (R. D. Karmarkar, 1938).
00004 : AP  : 00056	Med.	Medinīkośa.
03509 : AP  : 05195	Ms.	Manusmṛti, (J. M. Gurjar, Bombay, 1894).
00018 : AP  : 00025	Nala.	Nalopākhyāna, (Bombay).
00077 : AP  : 00100	Nir.	Nirukta.
00725 : AP  : 01338	P.	Pāṇiniʼs Aṣṭādhyāyī.
? 00000 : AP  : 00027	Pañc.	Pañcarātra 
01570 : AP  : 01653	Pt.	Pañcatantra. Chap, I, IV, V, (आर्यभूषण प्रेस, पुणें  १८९३); Chap. II and III, (Oriental Publishing Company, Bombay, 1912).
06981 : AP  : 07182	R.	Raghuvaṃśa, (R. A. Sagoon, Bombay 1897).
00012 : AP  : 00182	Rāj. T.	Rājataraṅgiṇī.
00356 : AP  : 02430	Rām.	Rāmāyaṇa, (Nirṇaya Sāgara, 1888).
00218 : AP  : 01493	Rv.	Ṛgveda, .
02487 : AP  : 02539	Ś.	Śakuntalam, (Shiralkar & Co. Poona, 1902).
00383 : AP  : 00430	S. D.	Sāhityadarpaṇa.
00030 : AP  : 00032	Ś. Til.	Śṛṅgāratilaka.
00063 : AP  : 00099	Śat. Br.	Śatapatha Brāhmaṇa.
02361 : AP  : 02857	Śi.	Śiśupālavadha, (Nirṇaya Sāgara, 1902).
? 00000 : AP  : 00006	T. Br.	Taittirīya Brāhmaṇa.
00010 : AP  : 00013	Trik.	Trikāṇḍaśeṣa.
? 00000 : AP  : 00020	Ts.	Taittirīya Saṃhitā.
00827 : AP  : 00869	V.	Vikramorvaśīyam, (R. D. Karmarkar, 1932).
00002 : AP  : Vāj.	Vājasaneyi Saṃhitā,
00877 : AP  : 01064	Y.	Yājñavalkya Smṛti, (Nirṇaya Sāgara, 1926).


* link_target_work_ap90.txt
Start with copy of ap version
cp link_target_work_ap.txt link_target_work_ap90.txt
and edit for ap90

* basicadjust_new.php
cp  /c/xampp/htdocs/cologne/csl-apidev/basicadjust.php basicadjust_new.php

* redo_new.sh
 1. copies basicadjust_new.php to basicadjust.php in csl-websanlexicon and csl-apidev
 2. regenerates local displays from csl-pywork/v02
 3. restores basicadjust.php in csl-websanlexicon

* revisions to basicadjust_new.php
 Confirm via examples in link_target_work_ap90.txt
 13 link targets activated (** DONE YESx).

* ===========================================
* installation Github
cd /c/xampp/htdocs/sanskrit-lexicon/AP90/issues/issue29 #home
cp basicadjust_new.php /c/xampp/htdocs/cologne/csl-websanlexicon/v02/makotemplates/web/webtc/basicadjust.php
cp basicadjust_new.php /c/xampp/htdocs/cologne/csl-apidev/basicadjust.php

# make local displays for ap90, and check xml
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
# csl-websanlexicon to github
cd /c/xampp/htdocs/cologne/csl-websanlexicon/
git pull
git add .
git commit -m "AP90: link targets. 
Ref: https://github.com/sanskrit-lexicon/AP90/issues/29"
git push
# csl-apidev to github
cd /c/xampp/htdocs/cologne/csl-apidev/
git pull
git add .
git commit -m "AP90: link targets. 
Ref: https://github.com/sanskrit-lexicon/AP90/issues/29"
git push
* installation cologne  : Cannot connect to cologne!   <<<< TODO
# connect to cologne and change to scans directory
cd csl-orig
git pull
cd ../csl-websanlexicon
git pull
cd ../csl-apidev
git pull
cd
* csl-lslink update ap90
cd /c/xampp/htdocs/cologne/csl-lslink
sh redo_one_xampp.sh ap90
18741  links found
zip/ap90_lslinks.sqlite.zip  

* push this repo
