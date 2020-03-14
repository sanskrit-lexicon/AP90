echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake ap90_verb_filter.txt"
python ap90_verb_filter.py ../ap90.txt ap90_verb_exclude.txt ap90_verb_include.txt ap90_verb_filter.txt
echo "remake ap90_verb_filter_map.txt"
python ap90_verb_filter_map.py ap90_verb_filter.txt  mwverbs1.txt ap90_verb_filter_map.txt

echo "ap90_verb1.txt"
python verb1.py slp1 ../ap90.txt ap90_verb_filter_map.txt ap90_verb1.txt
echo "ap90_verb1_deva.txt"
python verb1.py deva ../ap90.txt ap90_verb_filter_map.txt ap90_verb1_deva.txt
