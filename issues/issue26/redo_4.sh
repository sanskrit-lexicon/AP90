echo "althw_census_3a"
python althw_census.py temp_ap90_3a.txt althw_census_3a.txt
echo ""

echo "althw_2_input"
python althw_2_prep.py althw_census_3a.txt  althw_2_input.txt
echo ""

echo "temp_ap90_4"
python althw_2.py temp_ap90_3a.txt althw_2_input.txt temp_ap90_4.txt
echo ""

echo "althw_census_4"
python althw_census.py temp_ap90_4.txt althw_census_4.txt
echo ""

echo "althw_census_diff 3a 4"
python althw_census_diff.py althw_census_3a.txt althw_census_4.txt tempout.txt

