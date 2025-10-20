from config import param
from utils import parse_char_pool, hash_, clear, log_hash
from itertools import product
import numpy as np
from hardcode import line_, print_, settings
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import os


class brute_multi_process:
    def __init__(self):
        self.config = None
        self.symbols_pool = None
        
    def bruteforce(self):
        self.config = param
        self.symbols_pool = "".join(parse_char_pool(self.config.symbols))
        targets_to_find = set(self.config.targets)
        found_results = []
        log_entries = []
        
        clear()
        line_("Начало атаки на хэши поолным перебором в многопроцессорном режиме")
        start = datetime.datetime.now()
        log_entries.append(f"Начало атаки: {start}")
        log_entries.append(settings(self.config.cores, self.config.password_length, self.config.output, "".join(parse_char_pool(self.config.symbols)), log_hash(self.config.targets), "Многопроцессорный режим"))
        try:
            with ProcessPoolExecutor(max_workers=self.config.cores) as executor:

                prefix_chunks = np.array_split(list(self.symbols_pool), self.config.cores)
                
                futures = {executor.submit(process_prefix_chunk, chunk, self.symbols_pool, self.config.password_length, targets_to_find, verbose=self.config.verbose) for chunk in prefix_chunks}
                
                for future in as_completed(futures):
                    found_list = future.result()
                    if found_list:
                        for item in found_list:
                            found_results.append(item) 
                            hash_val, pwd = list(item.items())[0] 
                            log_line = print_(f"Спустя {datetime.datetime.now() - start} был найден хэш: {hash_val} из строки: {pwd}")
                            log_entries.append(log_line.strip())
                            targets_to_find.discard(hash_val)
                    
                    if not targets_to_find:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
        except KeyboardInterrupt:
            print("[-] Принудительное завершение атаки.")
                
        end_time = datetime.datetime.now()
        if not targets_to_find:
            log = f"Атака закончилась успешно, все хэши найдены\nВремя выполнения: {end_time - start} секунд"
            log_entries.append(log)
            line_(log)
        else:
            log = f"Атака закончилась, не все хэши найдены\nВремя выполнения: {end_time - start} секунд\nОставшиеся хэши: {log_hash(targets_to_find)}"
            log_entries.append(log)
            line_(log)
        
        log_entries.append(f"Конец атаки: {end_time}\n\n\n\n\n")
        self.save_result("\n".join(log_entries))
        input("Для продолжения нажмите Enter...")
        
    def save_result(self, output_):
        with open(self.config.output, 'a') as f:
            f.write(output_)
        print(f"[+] Результат сохранен в файл: {self.config.output}")

def process_prefix_chunk(prefix_chunk, full_alphabet, max_len, targets_to_find, verbose=False):
    if verbose: print(f"Процесс: {os.getpid()} работает с символами: {''.join(prefix_chunk)}")
    found_in_chunk = []
    for prefix in prefix_chunk:
        if hash_(prefix) in targets_to_find:
            found_in_chunk.append({hash_(prefix): prefix})
            
        for i in range(1, max_len):
            for p in product(full_alphabet, repeat=i):
                password = prefix + "".join(p)
                _hash = hash_(password)
                if _hash in targets_to_find:
                    found_in_chunk.append({_hash: password})
    return found_in_chunk