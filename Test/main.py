from rand import generate_data
from tabu_search import tabu_search, starting_solution
import os
import matplotlib.pyplot as plt
import time 
clear = lambda: os.system('cls')

def generate_new_data():
    print('---GENEROWANIE DANYCH---')
    N = int(input('Podaj liczbę studentów: '))
    num_dorm = int(input('Podaj liczbę akademików: '))
    num_dep = int(input('Podaj liczbę wydziałów: '))
    print('')

    for elem in [N, num_dorm, num_dep]: 
        if not isinstance(elem, int): 
            print('Wrong input!')
            break

    [students_years,
    students_disability,
    students_priority_lists,
    students_departments,
    students_sex,
    dormitorys_capacity,
    dormitory_position,
    departments_position] = generate_data(N, num_dorm, num_dep)

    start_solution = starting_solution(students_priority_lists, students_disability, students_sex, dormitorys_capacity)

    return (students_years,
            students_disability,
            students_priority_lists,
            students_departments,
            students_sex,
            dormitorys_capacity,
            dormitory_position,
            departments_position,
            start_solution)


def main_loop():
    generate_data_flag = True

    while True:
        if generate_data_flag == True:
            (students_years,
            students_disability,
            students_priority_lists,
            students_departments,
            students_sex,
            dormitorys_capacity,
            dormitory_position,
            departments_position,
            start_solution) = generate_new_data()

        print('---SPOSOBY DEFINIOWANIA SĄSIEDZTWA---')
        print('1. Zmiana akademika')
        print('2. Zamiana studentów')
        print('3. Przeniesienie grupy studentów')
        print('4. Wszystkie jednocześnie')
        neighbourhood_choice = int(input('Wybierz (1, 2, 3, 4): '))

        if neighbourhood_choice not in [1, 2, 3, 4]:
            print('Wrong input!')
        
        elif neighbourhood_choice == 1:
            print('')
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'change_dorm')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            
            input()

        elif neighbourhood_choice == 2:
            print('')
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'swap_students')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            
            input()

        elif neighbourhood_choice == 3:
            print('')
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'move_group')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)

            input()
        
        elif neighbourhood_choice == 4:
            print('')
            start_time = time.time()
            N = 200
            num_dorm = 5 #liczba akadmiekow
           # num_dep = 4 #liczba wydzialow []
            num=0
            wekt_rozw_do_wykresu_kamil=[]
            for num_dep in [1, 2,3, 4,5, 6, 8]:
                [students_years,
                students_disability,
                students_priority_lists,
                students_departments,
                students_sex,
                dormitorys_capacity,
                dormitory_position,
                departments_position] = generate_data(N, num_dorm, num_dep)
                start_solution = starting_solution(students_priority_lists, students_disability, students_sex, dormitorys_capacity)

                best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                                students_priority_lists, students_sex, students_departments, 
                                dormitorys_capacity, dormitory_position, departments_position, 
                                'both')
                end_time = time.time()
                wekt_rozw_do_wykresu_kamil.append(((end_time - start_time), N, num_dorm, num_dep, best_solution, iterations, iterations[-1]))


                print("Najlepsze rozwiązanie:", best_solution)
                print("Wartość funkcji celu:", best_objective)
                print(f"Czas wykonania:", end_time - start_time, "sekundy")

            
                plt.figure(figsize=(10, 5))
                plt.plot(iterations, objectives, marker='o', label='Funkcja celu')
                
                plt.xlabel('Iteracja')
                plt.ylabel('Wartość funkcji celu')
                plt.title(f'Wartość funkcji celu dla liczba studentów = {N}, liczby akademików = {num_dorm} i liczby wydziałów = {num_dep}')
                plt.legend()
                plt.grid()
                folder_path = 'C:\\Users\\kamil\\Desktop\\Badanie_algorytmu_BO'  
                file_name = f'liczba_wydziałów{num_dep}.png'
                full_path = folder_path + '\\' +file_name
                plt.savefig(full_path)
                plt.show()

            wektor_do_wykresu_czas=[ x[0] for x in wekt_rozw_do_wykresu_kamil]
            wektor_do_wykresu_liczba_aka=[ x[3] for x in wekt_rozw_do_wykresu_kamil]

            plt.figure(figsize=(10, 5))
            plt.plot(wektor_do_wykresu_liczba_aka, wektor_do_wykresu_czas, marker='o', label='Funkcja celu')
            plt.xlabel('Liczba wydziałów')
            plt.ylabel('Czas trwania algorytmu [s]')
            plt.title('Czas działania algorytmu, liczba studentów = {N}, liczba akademików = 5 i liczba wydziałów = [1, 2, 3, 4, 5, 6, 8]')
            plt.legend()
            plt.grid()
            folder_path = 'C:\\Users\\kamil\\Desktop\\Badanie_algorytmu_BO'  
            file_name = 'wykre_czasu_od_liczby_wydzialow.png'
            full_path = folder_path + '\\' +file_name
            plt.savefig(full_path)
            plt.show()

            
           
if __name__ == '__main__':
    main_loop()