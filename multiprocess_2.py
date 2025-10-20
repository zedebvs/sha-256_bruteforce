from config import param
from utils import parse_char_pool, hash_, clear, log_hash
from itertools import product
import numpy as np
from hardcode import line_, print_, settings
import datetime, time
from multiprocessing import Process, Manager, Queue
import os


class brute_multi_process_:
    def __init__(self):
        self.config = None
        self.symbols_pool = None
        
    def bruteforce(self):
        self.config = param
        self.symbols_pool = "".join(parse_char_pool(self.config.symbols))
        found_results = []
        log_entries = []
        targets_ = set(self.config.targets)
        
        
        clear()
        line_("Начало атаки на хэши поолным перебором в многопроцессорном режиме")
        start = datetime.datetime.now()
        log_entries.append(f"Начало атаки: {start}")
        log_entries.append(settings(self.config.cores, self.config.password_length, self.config.output, "".join(parse_char_pool(self.config.symbols)), log_hash(self.config.targets), "Многопроцессорный режим 2 версия"))
        prefix_chunks = np.array_split(list(self.symbols_pool), self.config.cores)

        try:
            with Manager() as manager:
                shared_targets = manager.list(self.config.targets)
                log_queue = manager.Queue()
                
                proc = [Process(target=process_prefix_chunk, args=(chunk, self.symbols_pool, self.config.password_length, shared_targets, log_queue, self.config.chunk_size, self.config.verbose)) for chunk in prefix_chunks]
                for p in proc: p.start()

                while any(p.is_alive() for p in proc) or not log_queue.empty():
                    while not log_queue.empty():
                        found_item = log_queue.get()
                        found_results.append(found_item)
                        hash_val, pwd = list(found_item.items())[0]
                        log_line = print_(f"Спустя {datetime.datetime.now() - start} был найден хэш: {hash_val} из строки: {pwd}")
                        log_entries.append(log_line.strip())
                        targets_.discard(hash_val)

                    if not shared_targets: 
                        for p in proc:
                            if p.is_alive():
                                p.terminate() 
                        break
                    time.sleep(0.1) 

                for p in proc: p.join() 

        except KeyboardInterrupt:
            print("[-] Принудительное завершение атаки.")
                
        end_time = datetime.datetime.now()
            
        if not found_results or len(found_results) < len(self.config.targets):
            log = f"Атака закончилась, не все хэши найдены\nВремя выполнения: {end_time - start} секунд\nОставшиеся хэши: {log_hash(targets_)}"
            log_entries.append(log)
            line_(log)
        else:
            log = f"Атака закончилась успешно, все хэши найдены\nВремя выполнения: {end_time - start} секунд"
            log_entries.append(log)
            line_(log)
        
        log_entries.append(f"Конец атаки: {end_time}\n\n\n\n\n")
        self.save_result("\n".join(log_entries))
        input("Для продолжения нажмите Enter...")
        
    def save_result(self, output_):
        with open(self.config.output, 'a') as f:
            f.write(output_)
        print(f"[+] Результат сохранен в файл: {self.config.output}")




def process_prefix_chunk(prefix_chunk, full_alphabet, max_len, shared_targets, log_queue, chunk_size, verbose=False):
    if verbose: print(f"Процесс: {os.getpid()} работает с символами: {''.join(prefix_chunk)}")
    
    targets_local = set(shared_targets)
    batch = []
                
    for prefix in prefix_chunk:
        for i in range(max_len):
            for p in product(full_alphabet, repeat=i):
                password = prefix + "".join(p)
                _hash = hash_(password)
                if _hash in targets_local:
                    try:
                        shared_targets.remove(_hash)
                        log_queue.put({_hash: password})
                        targets_local.discard(_hash)
                    except ValueError:
                        pass
                batch.append(password)
                if len(batch) >= chunk_size:
                    batch.clear()
                    targets_local = set(shared_targets)
                if not targets_local:
                    return 
    return
