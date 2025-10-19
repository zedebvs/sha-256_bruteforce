from config import param, parameters
from utils import parse_char_pool, hash_, clear, parse_char_pool, log_hash
from itertools import product
from hardcode import line_, print_, settings
import datetime


class brute_single_thread:
    def __init__(self, config: parameters):
        self.config = config
        self.symbols_pool = "".join(parse_char_pool(self.config.symbols))

    def bruteforce(self):
        targets_to_find = set(self.config.targets)
        found_results = []
        log_entries = []

        clear()
        line_("Начало атаки на хэши полным перебором")

        start = datetime.datetime.now()
        log_entries.append(f"Начало атаки: {start}")
        log_entries.append(settings(self.config.cores, self.config.password_length, self.config.output, "".join(parse_char_pool(self.config.symbols)), log_hash(self.config.targets), "Однопоточный режим"))

        for i in range(1, self.config.password_length + 1):
            for j in product(self.symbols_pool, repeat=i):
                string = ''.join(j)
                _hash = hash_(string)
                if _hash in targets_to_find:
                    targets_to_find.remove(_hash)
                    found_results.append({_hash: string})
                    log_line = print_(f"Спустя {datetime.datetime.now() - start} был найден хэш: {_hash} из строки: {string}")
                    log_entries.append(log_line.strip())

                    if not targets_to_find:
                        break
            if not targets_to_find:
                break

        clear()
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
