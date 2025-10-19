import json
import os
from pathlib import Path
from hashlib import sha256, sha1, md5


def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не найден")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка чтения или парсинга файла '{file_path}': {e}")
        return None


def save_data(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[+] Файл {file_path} успешно сохранен")
    except Exception as e:
        print(f"Ошибка записи в файл '{file_path}': {e}")
        
def parse_char_pool(symbol_ranges):
    chars = []
    for r in symbol_ranges:
        chars.extend([chr(i) for i in range(r['start'], r['end']) if chr(i) not in chars])
    return chars

def interface_ssumbols(symbol_ranges):
    result = []
    result_string = ''
    for r in symbol_ranges:
        result.append(f'{r["start"]} - {r["end"]}')
        result_string = ", ".join(result)
    return f"Cимволы для перебора: {result_string}"
    
def iface_hashes(hashes):
    str_ = ''
    for i in hashes:
        str_ +=f'{i}, '
    return str_[:-2]

def log_hash(hashes):
    f_ = '\n'
    for i in hashes:
        f_ += f'{i}\n'
    return f_

def clear():
    os.system('cls || clear')
    
def validate_txt_filename(filename):

    path = Path(filename)

    if path.suffix.lower() != '.txt':
        print(f" Неправильное расширение файла! Повторите попытку")
        return False

    invalid_chars = '/\\?%*:|"<> '
    if any(char in path.name for char in invalid_chars):
        print("Имя файла содержит недопустимые символы.")
        return False
    
    return True

def elements(arr):
    symbols = [chr(i) for i in range (ord(min(arr)), ord(max(arr))+1)]
    if len(symbols) > 200:
        choice = str(input("Вы уверены, что хотите загрузить столько символов в пул? y/n")).lower().strip()
        if choice != 'y':
            return None
    print(f'Символы загружены в пул: {symbols}')
    return {"start": ord(min(arr)), "end": ord(max(arr))+1}


def hash_(string):
    return sha256(string.encode('utf-8')).hexdigest()