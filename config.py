import json
import os
from utils import load_data, save_data, iface_hashes, interface_ssumbols, clear, validate_txt_filename
from hardcode import MENU
import time

class parameters:
    def __init__(self):
        self.FILENAME = 'init.json'
        self.cores = None
        self.password_length = None
        self.output = None
        self.symbols = None
        self.targets = None
        self.data = None
        self.load_parameters(self.FILENAME)

    def zzz(self):
        clear()
        print(self.display())
        
    
    def load_parameters(self, FILENAME, reset = False):
        script_dir = os.path.dirname(__file__)
        filepath = os.path.join(script_dir, FILENAME)

        data = load_data(filepath)
        
        if not data or reset == True:
            print("[-] Файл с конфигурацией не найден или пустой")
            self.targets = ['1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad', 
                            '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b',
                            '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f']
            self.symbols = [{"start": 97,
                             "end": 123 }]
            self.cores = os.cpu_count()
            self.output = 'output.txt'
            self.password_length = 5
            self.data = {"cores":self.cores, "password_length":self.password_length, "output":self.output, "symbols":self.symbols,"targets":self.targets}
            save_data(FILENAME, self.data)
        else:
            
            cores_from_data = data.get('cores')
            self.cores = cores_from_data if cores_from_data is not None else os.cpu_count()
            
            password_length_from_data = data.get('password_length')
            self.password_length = password_length_from_data if password_length_from_data is not None else 5
            
            output_from_data = data.get('output')
            self.output = output_from_data if output_from_data is not None else 'output.txt'
            
            symbols_from_data = data.get('symbols')
            self.symbols = symbols_from_data if symbols_from_data else [{"start": 97, "end": 123}]
            
            targets_from_data = data.get('targets')
            self.targets = targets_from_data if targets_from_data else [
                '1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad', 
                '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b',
                '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f'
            ]
            self.data = {"cores": self.cores, "password_length": self.password_length, "output": self.output, "symbols": self.symbols, "targets": self.targets}
            save_data(FILENAME, self.data)
            
    def display(self):
        return f'{"-"*50}\nПараметры: \nКоличество процессов: {self.cores}\nДлина целевой строки: {self.password_length}\nФайл вывода: {self.output}\nПул символов: {interface_ssumbols(self.symbols)}\nТаргеты: {iface_hashes(self.targets)}\n{"-"*50}'
    
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
                pass
            elif choice == 'remove symbol':
                pass
            elif choice == 'add target':
                pass
            elif choice == 'remove target':
                pass
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
        

    def change_symbols(self):
        symbols = []
        while True:
            self.zzz()
            try:
                print("[Изменение всех символов для перебора]\nВведите символы или нажмите любую клавишу для выхода.\n1 число начало границы\n2 число конец границы\n")
                left = int(input("Начало границы: "))
                right = int(input("Конец границы: "))
                symbols.append({"start": left, "end": right})
                self.symbols = symbols
                continue
            except ValueError:
                break
            
        self.data["symbols"] = symbols
        save_data(self.FILENAME, self.data)
    
    def change_targets(self):
        hashes = []
        while True:
            self.zzz()
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

