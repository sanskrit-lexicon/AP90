import os

def count_case_lines():
    # List all files in the current directory starting with 'case_'
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('case_')]

    for filename in files:
        count = 0
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('* Case'):
                    count += 1
        print(f"{filename}: {count} line(s) starting with '* Case'")

if __name__ == "__main__":
    count_case_lines()
    
