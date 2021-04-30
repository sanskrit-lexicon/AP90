
The files in this directory can be used to
start with a copy of ap90.txt at one commit,
apply a sequence of changes, and result in the next version of ap90.txt.

In a local installation of csl-orig repository,
1. extract ap90.txt at commit 19c7ee9c3f1edc04e8975b00bf55f04b3825caea
git show 19c7ee9c3f1edc04e8975b00bf55f04b3825caea:ap90.txt > temp_ap90_5.txt
2. Move temp_ap90_5.txt to this abls1 directory
3. apply all the changes in sequence. Uses change6.txt,...,change15.txt
sh redo2.sh
4. The end result is temp_ap90_15.txt.
  This is same as ap90.txt at commit 37f98f8bb07a0dc1579ad03706637ddc9093e327

The change files were partially or completely constructed by programs.
A sampling of these programs is in filtercode directory, in case they may
be useful elsewhere.

ls_summary1.txt provides some statistics of occurrence of the various literary source abbreviations. It is recreated from:
python ls_summary1.py temp_ap90_15.txt tooltip.txt ls_summary1.txt
