# from Copilot 04-12-2026
#
import unicodedata

def strip_diacritics(s):
    # Normalize to NFD: decomposes ā → a + ̄
    decomposed = unicodedata.normalize("NFD", s)
    # Remove combining marks
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))
def sort_iast_key(w):
    return strip_diacritics(w.lower())
def test():
 words = ['X', 'Āry. S.','Śalihotra']
 sorted_list = sorted(words, key=lambda w: strip_diacritics(w.lower()))
 print(sorted_list)  # ['Āry. S.', 'Śalihotra', 'X']
 sorted_list1 = sorted(words,key=lambda w : sort_iast_key(w))
 print(sorted_list1)
 
          
if __name__=="__main__":
 test()
 
                         
