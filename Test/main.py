import os
import csv
import time
import matplotlib.pyplot as plt
from rand import generate_data
from tabu_search import tabu_search, starting_solution

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


# output_dir = "test1_wykresy"
# os.makedirs(output_dir, exist_ok=True)

# def save_plot(iterations, objectives, num_students, num_dorms, num_departments, neighbourhood, max_iterations, tabu_list_size):
#     plt.figure(figsize=(10, 5))
#     plt.plot(iterations, objectives, marker='o', label='Funkcja celu')
#     plt.xlabel('Iteracja')
#     plt.ylabel('Wartość funkcji celu')
#     plt.title(f'Liczba studentów: {num_students}, Liczba akademików: {num_dorms}, Liczba wydziałów: {num_departments}\n Sąsiedztwo: {neighbourhood}')
#     plt.legend()
#     plt.grid()
#     filename = f"{output_dir}/{num_students}_students_{num_dorms}_dorms_{num_departments}_departments_{neighbourhood}_{max_iterations}_{tabu_list_size}.png"
#     plt.savefig(filename)
#     plt.close()

# def write_to_csv(file_path, row):
#     file_exists = os.path.isfile(file_path)
#     with open(file_path, mode='a', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["Liczba studentów", "Liczba akademików", "Liczba wydziałów", "Typ sąsiedztwa", "Czas wykonania", "Funkcja celu (start)", "Funkcja celu (koniec)"])
#         writer.writerow(row)

# def perform_tests(num_students, num_dorms, num_departments, max_iterations, tabu_list_size):
#     print(f"--- Rozpoczynanie testów dla {num_students} studentów, {num_dorms} akademików, {num_departments} wydziałów ---")

#     # Generowanie danych
#     data = generate_data(num_students, num_dorms, num_departments)
#     start_solution = starting_solution(data[2], data[1], data[4], data[5])
    
#     # Typy sąsiedztw
#     neighbourhoods = ['change_dorm', 'swap_students', 'move_group', 'both']

#     for neighbourhood in neighbourhoods:
#         start_time = time.time()
#         best_solution, best_objective, iterations, objectives = tabu_search(
#             start_solution, data[0], data[1], data[2], data[4], data[3],
#             data[5], data[6], data[7], neighbourhood, max_iterations, tabu_list_size
#         )
#         end_time = time.time()

#         execution_time = end_time - start_time

#         # Zapis wykresu
#         save_plot(iterations, objectives, num_students, num_dorms, num_departments, neighbourhood, max_iterations, tabu_list_size)

#         # Zapis do pliku CSV
#         csv_path = os.path.join(output_dir, "results.csv")
#         write_to_csv(csv_path, [
#             num_students, num_dorms, num_departments, neighbourhood,
#             round(execution_time, 6), objectives[0], best_objective
#         ])

#         print(f"Zakończono dla sąsiedztwa: {neighbourhood}")


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
            start_time = time.time()
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'change_dorm')
            end_time = time.time()
            execution_time = end_time - start_time

            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            print(f"Czas wykonania: {execution_time:.6f} sekund")
            input()

        elif neighbourhood_choice == 2:
            print('')
            start_time = time.time()
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'swap_students')
            end_time = time.time()
            execution_time = end_time - start_time

            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            print(f"Czas wykonania: {execution_time:.6f} sekund")
            
            input()

        elif neighbourhood_choice == 3:
            print('')
            start_time = time.time()
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'move_group')
            end_time = time.time()
            execution_time = end_time - start_time

            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            print(f"Czas wykonania: {execution_time:.6f} sekund")

            input()
        
        elif neighbourhood_choice == 4:
            print('')
            start_time = time.time()
            best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                            students_priority_lists, students_sex, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            'both')
            end_time = time.time()
            execution_time = end_time - start_time

            print("Najlepsze rozwiązanie:", best_solution)
            print("Wartość funkcji celu:", best_objective)
            print(f"Czas wykonania: {execution_time:.6f} sekund")

            input()
        
        plt.figure(figsize=(10, 5))
        plt.plot(iterations, objectives, marker='o', label='Funkcja celu')
        plt.xlabel('Iteracja')
        plt.ylabel('Wartość funkcji celu')
        plt.title('Wartość funkcji celu w kolejnych iteracjach')
        plt.legend()
        plt.grid()
        plt.show()
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


# if __name__ == '__main__':
#     test_cases = [ 
#         (250, 10, 5, 1000, 100),    #Studenci, Akademiki, Wydziały, max_iterations, tabu_list_size
#         (250, 5, 5, 1000, 100), 
#         (250, 2, 5, 1000, 100),    
#         (250, 10, 10, 1000, 100),  
#         (250, 5, 10, 1000, 100),   
#         (250, 2, 10, 1000, 100),
#         (500, 10, 5, 1000, 100),   
#         (500, 5, 5, 1000, 100),    
#         (500, 2, 5, 1000, 100),    
#         (500, 10, 10, 1000, 100),  
#         (500, 5, 10, 1000, 100),   
#         (500, 2, 10, 1000, 100),   
#         (250, 5, 10, 500, 100), 
#         (250, 5, 10, 500, 50),
#         (250, 5, 10, 1000, 50),
#         (250, 5, 10, 1000, 500),
#         (500, 5, 10, 500, 100),
#         (500, 5, 10, 500, 50),
#         (500, 5, 10, 1000, 50),
#         (500, 5, 10, 1000, 500)
#     ]

#     for num_students, num_dorms, num_departments, max_iterations, tabu_list_size in test_cases:
#         perform_tests(num_students, num_dorms, num_departments, max_iterations, tabu_list_size)

#     print("--- Wszystkie testy zakończone ---")