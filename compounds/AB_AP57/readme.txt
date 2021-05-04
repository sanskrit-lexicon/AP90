
# transcode AP57entries from devanagari to slp1

python deva_slp1.py deva slp1 AP57entries.txt AP57entries_slp1.txt

remove certain 'comment' lines:
 Those comprising two tabs
# ap57a.txt
 (minor cleanup of file)
# parseprep
python parseprep.py AP57entries_slp1.txt ap57a.txt
85168 in AP57entries_slp1.txt
82383 lines after removing 'empty' lines (those starting with 2 tabs)

# parse
python parse.py ap57a.txt ap57b.txt ap57b_ptrs.txt
82363 in ap57a.txt
82072 records with status = True
36589 entries

4365 entries with compounds
4365 records written to ap57b.txt
37649 Total number of compounds
