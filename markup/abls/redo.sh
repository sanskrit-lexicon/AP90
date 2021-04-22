echo "change0a.txt"
which python
python change0a.py ap90_0.txt change0a.txt
echo "ap90_0a.txt"
python updateByLine.py ap90_0.txt change0a.txt ap90_0a.txt
echo "ap90_0b.txt"
python updateByLine.py ap90_0a.txt change0b.txt ap90_0b.txt
echo "abbrauth_1.txt"
python abbrauth.py abbr_1.txt auth_1.txt abbrauth_1.txt
echo "ap90_1.txt and abbr_2.txt"
python prep1.py ap90_0b.txt abbrauth_1.txt ap90_1.txt abbr_2.txt
echo "ap90_2.txt and auth_2.txt"
python prep2.py ap90_1.txt abbrauth_1.txt ap90_2.txt auth_2.txt
echo "ap90_3.txt"
python prep3.py ap90_2.txt auth_2.txt ap90_3.txt changes3.txt
echo "hyphen_eng.txt"
python hyphen_eng1.py ap90_3.txt hyphen_eng.txt hyphen_eng_questions.txt
echo "ap90_4.txt"
python updateByLine.py ap90_3.txt hyphen_eng.txt ap90_4.txt
echo "hyphen_deva.txt"
python hyphen_deva1.py ap90_4.txt hyphen_deva.txt hyphen_deva_questions.txt
echo "ap90_4.txt"
python updateByLine.py ap90_4.txt hyphen_deva.txt ap90_5.txt
