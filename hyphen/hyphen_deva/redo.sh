echo "ap90_0a.txt"
python updateByLine.py ap90_0.txt changes0_edit.txt ap90_0a.txt
echo "changes_0b.txt"
python spacechg.py ap90_0a.txt changes0b.txt
echo "ap90_0b.txt"
python updateByLine.py ap90_0a.txt changes0b.txt ap90_0b.txt
echo "changes1.txt"
python hyphen1.py ap90_0b.txt changes1.txt questions1.txt
echo "ap90_1.txt"
python updateByLine.py ap90_0b.txt changes1.txt ap90_1.txt
echo "changes2.txt"
python hyphen2.py ap90_1.txt changes2.txt questions2.txt
echo "ap90_2.txt"
python updateByLine.py ap90_1.txt changes2.txt ap90_2.txt
echo "changes3.txt"
python hyphen3.py ap90_2.txt changes3.txt questions3.txt
echo "ap90_3.txt"
python updateByLine.py ap90_2.txt changes3.txt ap90_3.txt
