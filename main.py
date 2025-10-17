from config import parameters
from utils import clear

param = parameters()


def main():
    #print(param.display())
        
    while True:
        clear()
        print(param.display())
        choice = str(input("1 - Изменение параметров\n2 - Запуск во всех режимах\n3 - Запуск однопоточного режима\n4 - Запуск многопоточного режима\n5 - Запуск многопроцессорного режима\n6 - Выход\n"))

        if choice == '1':
            param.change_if()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        else:
            print("[!] Завершение работы программы")
            exit()
        

if __name__ == '__main__':
    main()