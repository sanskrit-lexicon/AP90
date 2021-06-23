
the Apte Student ed. S2H (a translation of Apte Student's S2E 1890 into Hindi in 1965)

apte_s2h_works.txt contains a transliteration of the pdf into SLP1.
See comment in this file for details of formatting.

Slightly edited in preparation for transcoding.

Transcoding:
python transcode.py slp1 deva apte_s2h_works.txt apte_s2h_works_deva.txt
 The 'period' is changed to lAGava cihna (Devanagari abbreviation sign),
  \u0970.   Usually, period in slp1 represents danda.
 <X> is used for English text X, which is not to be transcoded
 
python transcode.py slp1 roman apte_s2h_works.txt apte_s2h_works_iast.txt
  The 'words' (both in abbreviation and name fields) are capitalized.
  
