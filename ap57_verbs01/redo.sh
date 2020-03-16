echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake ap57_verb_filter.txt"
python ap57_verb_filter.py temp_ap57.txt ap57_verb_exclude.txt ap57_verb_include.txt ap57_verb_filter.txt
echo "remake ap57_verb_filter_map.txt"
python ap57_verb_filter_map.py ap57_verb_filter.txt  mwverbs1.txt ap57_verb_filter_map.txt

echo "ap57_verb1.txt"
python verb1.py slp1 temp_ap57.txt ap57_verb_filter_map.txt ap57_verb1.txt
echo "ap57_verb1_deva.txt"
python verb1.py deva temp_ap57.txt ap57_verb_filter_map.txt ap57_verb1_deva.txt
