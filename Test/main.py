from rand import generate_data
from tabu_search import tabu_search, starting_solution
import os

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
        print('3. Zmiana akademika i zamiana studentów')
        neighbourhood_choice = int(input('Wybierz (1, 2, 3): '))

        if neighbourhood_choice not in [1, 2, 3]:
            print('Wrong input!')
        
        elif neighbourhood_choice == 1:
            print('')
            best_solution, best_objective = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'change_dorm')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            
            input()

        elif neighbourhood_choice == 2:
            print('')
            best_solution, best_objective = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'swap_students')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            
            input()

        elif neighbourhood_choice == 3:
            print('')
            best_solution, best_objective = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'both')
            
            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)

            input()
        
        while True:
            clear()
            generate_new_data_choice = int(input('Czy chcesz wygenerować nowe dane (0: NIE; 1: TAK)?'))
            if generate_new_data_choice == 0:
                generate_data_flag = False
                break

            elif generate_new_data_choice == 1:
                generate_data_flag = True
                break

            else:
                print('Wrong input!')
        
        
if __name__ == '__main__':
    main_loop()