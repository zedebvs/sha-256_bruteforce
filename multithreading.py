from config import param
from utils import parse_char_pool, hash_, clear, log_hash
from itertools import islice, product
from hardcode import line_, print_, settings
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class brute_multi_thread:
    def __init__(self):
        self.config = None
        self.symbols_pool = None
    
    def chunks(self):
        for i in range(1, self.config.password_length + 1):
            prod = product(self.symbols_pool, repeat=i)
            while True:
                chunk = list(islice(prod, self.config.chunk_size))
                if not chunk:
                    break
                yield chunk
    
    def bruteforce(self):
        self.config = param
        self.symbols_pool = "".join(parse_char_pool(self.config.symbols))
        targets_to_find = set(self.config.targets)
        found_results = []
        log_entries = []
        
        clear()
        line_("Начало атаки на хэши поолным перебором в многопоточном режиме")
        start = datetime.datetime.now()
        log_entries.append(f"Начало атаки: {start}")
        log_entries.append(settings(self.config.cores, self.config.password_length, self.config.output, "".join(parse_char_pool(self.config.symbols)), log_hash(self.config.targets), "Многопоточный режим"))
        try:
            with ThreadPoolExecutor(max_workers=self.config.cores) as executor:
                chunk_iterator = self.chunks()
                futures = {executor.submit(process_chunk, next(chunk_iterator), targets_to_find) for _ in range(self.config.cores)}
                
                while futures:
                    for future in as_completed(futures):
                        found_in_chunk = future.result()
                        if found_in_chunk:
                            for item in found_in_chunk:
                                found_results.append(item) 
                                hash_val, _ = list(item.items())[0] 
                                log_line = print_(f"Спустя {datetime.datetime.now() - start} был найден хэш: {hash_val} из строки: {_}")
                                log_entries.append(log_line.strip())
                                targets_to_find.discard(hash_val)
                        futures.remove(future)
                        try:
                            new_chunk = next(chunk_iterator)
                            futures.add(executor.submit(process_chunk, new_chunk, targets_to_find))
                        except StopIteration:
                            pass
                        break 
                    if not targets_to_find:
                        for f in futures:
                            f.cancel()
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

def process_chunk(chunk, targets_to_find):
    found_in_chunk = []
    for password_tuple in chunk:
        password = ''.join(password_tuple)
        _hash = hash_(password)
        if _hash in targets_to_find:
            found_in_chunk.append({_hash: password})
    return found_in_chunk