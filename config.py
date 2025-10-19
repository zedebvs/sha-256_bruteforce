import json
import os
from utils import load_data, save_data, iface_hashes, interface_ssumbols, clear, validate_txt_filename, elements
from hardcode import *
import time
from multiprocessing import current_process

class parameters:
    def __init__(self):
        self.FILENAME = 'init.json'
        self.cores = None
        self.password_length = None
        self.output = None
        self.symbols = None
        self.targets = None
        self.chunk_size = None
        self.data = None
        self.load_parameters(self.FILENAME)

    def zzz(self):
        clear()
        print(self.display())
        
    def _get_default_config(self):
        return {
            "cores": os.cpu_count(),
            "password_length": 5,
            "output": "output.txt",
            "chunk_size": 10000,
            "symbols": [{"start": 97, "end": 123}],
            "targets": [
                "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
                "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
                "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f"
            ]
        }
        
    def load_parameters(self, FILENAME, reset = False):
        script_dir = os.path.dirname(__file__)
        filepath = os.path.join(script_dir, FILENAME)

        data = load_data(filepath)
        
        if reset:
            print("[-] Сброс конфигурации к стандартным значениям.")
            data = None

        if not data:
            data = self._get_default_config()

        defaults = self._get_default_config()
        self.cores = data.get('cores', defaults['cores'])
        self.password_length = data.get('password_length', defaults['password_length'])
        self.output = data.get('output', defaults['output'])
        self.chunk_size = data.get('chunk_size', defaults['chunk_size'])
        self.symbols = data.get('symbols', defaults['symbols'])
        self.targets = data.get('targets', defaults['targets'])

        self.data = {"cores": self.cores, "password_length": self.password_length, "output": self.output, "chunk_size": self.chunk_size, "symbols": self.symbols, "targets": self.targets}
        
        if current_process().name == "MainProcess":
            try:
                save_data(FILENAME, self.data)
            except Exception:
                pass
        else:
            pass
            
    def display(self):
        return f'{"-"*50}\nПараметры: \nКоличество процессов: {self.cores}\nДлина целевой строки: {self.password_length}\nФайл вывода: {self.output}\nРазмер чанка: {self.chunk_size}\nПул символов: {interface_ssumbols(self.symbols)}\nТаргеты: {iface_hashes(self.targets)}\n{"-"*50}'
    
    def change_if(self):
        while True:
            self.zzz()
            print(f"\n[!] Вы можете поменять параметры вручную в файле: {self.FILENAME}\n")

            menu_text = MENU
            choice = str(input(f"{menu_text}\nВаш выбор: ")).lower().strip()
            
            if choice == 'reset':
                self.load_parameters(self.FILENAME, reset=True)
            elif choice == '1':
                self.change_cores()
            elif choice == '2':
                self.change_password_length()
            elif choice == '3':
                self.change_output()
            elif choice == '4':
                self.change_symbols()
            elif choice == '5':
                self.change_targets()
            elif choice == 'add symbol':
                self.change_symbols(pool = True)
            elif choice == 'remove symbol':
                self.delete_( self.symbols)
                self.data["symbols"] = self.symbols
                save_data(self.FILENAME, self.data)
            elif choice == 'add target':
                self.change_targets(pool = True)
            elif choice == 'remove target':
                self.delete_( self.targets)
                self.data["targets"] = self.targets
                save_data(self.FILENAME, self.data)
            elif choice == 'exit':
                return
            
    def change_cores(self):
        while True:
            self.zzz()
            print(f"Оптимальное количество ядер: {os.cpu_count()}")
            try:
                cores = int(input("Введите количество ядер: "))
            except ValueError:
                clear()
                print("Введите число!")
                time.sleep(1)
                continue
            self.cores = cores
            self.data["cores"] = cores
            save_data(self.FILENAME, self.data)
            break
        
    def change_password_length(self):
        while True:
            self.zzz()
            try:
                password_length = int(input("Введите длину строки: "))
            except ValueError:
                clear()
                print("Введите число!")
                time.sleep(1)
                continue
            self.password_length = password_length
            self.data["password_length"] = password_length
            save_data(self.FILENAME, self.data)
            break
        
    def change_output(self):
        while True:
            self.zzz()
            output = str(input("Введите название файла: "))
            if validate_txt_filename(output):
                self.output = output
                self.data["output"] = output
                save_data(self.FILENAME, self.data)
                break
            else:
                time.sleep(1)
                continue
        

    def change_symbols(self, pool = False):
        if pool:
            symbols = self.symbols
            text = ADD_POLL
        else:
            symbols = []
            text = ADD_FULL_POOL
        while True:
            self.zzz()
            try:
                print(f"{text}\nВведите exit для сохранения или выхода\nВведите начальный символ, а потом конечный. В пул будет загружен весь диапазон!\n")
                left = str(input("Начальный символ: "))
                if left == 'exit':
                    break
                left = left[0]
                right = str(input("Конечный символ: "))
                if right == 'exit':
                    break
                right = right[0]
                
                symbols_ = elements([left, right])
                if not symbols_:
                    continue
                if symbols_ in symbols:
                    clear()
                    print("Данные символы уже загружены в пул!")
                    time.sleep(1)
                    continue
                 
                symbols.append(symbols_)
                self.symbols = symbols
                time.sleep(2)
                continue
            except Exception:
                break
            
        self.data["symbols"] = symbols
        save_data(self.FILENAME, self.data)
    
    def change_targets(self, pool = False):
        if pool:
            hashes = self.targets
            text = ADD_POLL_HASH
        else:
            hashes = []
            text = ADD_FULL_POOL_HASH
        while True:
            self.zzz()
            print(text)
            hash_ = str(input("Для выхода нажмите - exit\nВведите sha-256 хэш в hex формате: "))
            if hash_ == 'exit':
                break
            elif len(hash_) != 64:
                print("Введите 32-байтный хэш в hex формате!")
                time.sleep(1)
                continue
            elif hash_ in hashes: 
                print("Не должно быть 2 одинаковых хэшей!")
                time.sleep(1)
                continue
            hashes.append(hash_)
            self.targets = hashes
        self.data["targets"] = hashes
        save_data(self.FILENAME, self.data)
    
    def delete_(self, for_delete):
        while True:
            self.zzz()
            print(DELETE_HASH)
            
            choice = input(DELETE)
            if choice == 'exit':
                break
            try:
                choice = int(choice)
                if choice < 0 or choice >= len(self.targets):
                    print("Вы ошиблись при выборе элемента для удаления!")
                    time.sleep(1)
                    continue
                del for_delete[choice-1]
            except ValueError:
                clear()
                print("Введите число!")
                time.sleep(1)
                continue
    
    def delete_symbols(self):
        pass

param = parameters()
