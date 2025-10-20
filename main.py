from config import param
from utils import clear
from single_thread import brute_single_thread
from multithreading import brute_multi_thread
from multiprocess import brute_multi_process
from multiprocess_2 import brute_multi_process_


brut = brute_single_thread()
brut_2 = brute_multi_thread()
brut_3 = brute_multi_process()
brut_4 = brute_multi_process_()


def main():
    #print(param.display())
        
    while True:
        clear()
        print(param.display())
        choice = str(input("1 - Изменение параметров\n2 - Запуск во всех режимах\n3 - Запуск однопоточного режима\n4 - Запуск многопоточного режима\n5 - Запуск многопроцессорного режима\n6 - Запуск многопроцессорного режима 2\n7 - Выход\n"))
        if choice == '1':
            param.change_if()
        elif choice == '2':
            pass
        elif choice == '3':
            brut.bruteforce()
        elif choice == '4':
            brut_2.bruteforce()
        elif choice == '5':
            brut_3.bruteforce()
        elif choice == '6':
            brut_4.bruteforce()
        else:
            print("[!] Завершение работы программы")
            exit()
        

if __name__ == '__main__':
    main()