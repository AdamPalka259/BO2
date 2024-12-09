from typing import List, Union, Dict, Tuple
from math import sqrt
from rand import generate_data
import os

disability_priority: Dict[int, int] = {1: 100, 2: 75, 3: 50, 0: 25}  # Priorytet na podstawie stopnia niepełnosprawności używany w funkcji celu

clear = lambda: os.system('cls')

def calculate_distances(dorm_pos: List[tuple[float]], dep_pos: List[tuple[float]]) -> List[List[float]]:
    '''Zwraca macierz odległości między akademikami a wydziałami.
    Wiersze to akademiki, a kolumny to wydziały.'''
    dist_matrix = []  # Macierz odległości w km
    for dorm in dorm_pos:
        dorm_dist = []
        for dep in dep_pos:
            # Obliczanie odległości między akademikiem, a wydziałem w km
            dist = round(sqrt((dorm[0] - dep[0])**2 + (dorm[1] - dep[1])**2),3)
            dorm_dist.append(dist)
        dist_matrix.append(dorm_dist)
    return dist_matrix


def starting_solution(
    prior_list: List[List[int]], 
    dorm_capacity: List[int], 
    students_sex: List[int],    # 0 - mężczyzna, 1 - kobieta
    min_fill: float = 0,        # Minimalny poziom wypełnienia (tylko dla choice == 2)
    choice: int = 1             # Tryb rozwiązania (1 - bez ograniczeń, 2 - minimalny poziom wypełnienia, 3 - usunięcie niechcianego, 4 - proporcja płci)
) -> List[int]:
    '''Zwraca początkowe rozwiązanie do algorytmu Tabu Search z uwzględnieniem wyboru trybu działania (choice).'''
    result = [None] * len(prior_list)  # Wstępne przypisanie "brak akademika" każdemu studentowi
    dorm_counter = {i: {'male': 0, 'female': 0} for i in range(len(dorm_capacity))}  # Licznik płci w akademikach
    bad_students = []  # Studenci, których nie udało się przypisać w pierwszej pętli

    # Jeśli choice == 4, obliczamy globalną proporcję płci
    if choice == 4:
        total_males = sum(1 for s in students_sex if s == 0)
        total_females = sum(1 for s in students_sex if s == 1)
        global_gender_ratio = total_females / total_males if total_males > 0 else 1

    # Jeśli choice == 2, obliczamy maksymalny możliwy min_fill
    if choice == 2:
        total_capacity = sum(dorm_capacity)
        max_possible_fill = min(1, len(prior_list) / total_capacity)

        # Jeśli podany min_fill jest wyższy niż maksymalny możliwy, zastąp go
        if min_fill > max_possible_fill:
            min_fill = max_possible_fill

    # Pierwsza pętla: Przypisanie zgodnie z listą priorytetów
    for i, student_prior in enumerate(prior_list):
        assigned = False  # Flaga określająca, czy student został przypisany
        for dorm in student_prior:
            if dorm is not None:
                current_total = dorm_counter[dorm]['male'] + dorm_counter[dorm]['female']
                if current_total < dorm_capacity[dorm]:
                    # Przydział dla choice == 4 z zachowaniem proporcji płci
                    if choice == 4:
                        # Obliczamy lokalną proporcję płci w akademiku
                        local_males = dorm_counter[dorm]['male']
                        local_females = dorm_counter[dorm]['female']
                        local_ratio = (local_females / local_males) if local_males > 0 else float('inf')

                        # Sprawdzenie, czy przydział zachowuje proporcję
                        if students_sex[i] == 1 and local_ratio < global_gender_ratio:  # Kobieta
                            dorm_counter[dorm]['female'] += 1
                            result[i] = dorm
                            assigned = True
                            break
                        elif students_sex[i] == 0 and local_ratio > global_gender_ratio:  # Mężczyzna
                            dorm_counter[dorm]['male'] += 1
                            result[i] = dorm
                            assigned = True
                            break
                    else:  # Przydział dla innych trybów
                        dorm_counter[dorm]['female' if students_sex[i] == 1 else 'male'] += 1
                        result[i] = dorm
                        assigned = True
                        break

        if not assigned:
            bad_students.append(i)  # Student bez przypisania w pierwszej pętli

    # Druga pętla: Przypisanie pozostałych studentów
    for student in bad_students:
        for dorm in range(len(dorm_capacity)):
            current_total = dorm_counter[dorm]['male'] + dorm_counter[dorm]['female']
            if current_total < dorm_capacity[dorm]:
                # Sprawdzenie proporcji płci dla choice == 4
                if choice == 4:
                    local_males = dorm_counter[dorm]['male']
                    local_females = dorm_counter[dorm]['female']
                    local_ratio = (local_females / local_males) if local_males > 0 else float('inf')

                    if students_sex[student] == 1 and local_ratio < global_gender_ratio:  # Kobieta
                        dorm_counter[dorm]['female'] += 1
                        result[student] = dorm
                        break
                    elif students_sex[student] == 0 and local_ratio > global_gender_ratio:  # Mężczyzna
                        dorm_counter[dorm]['male'] += 1
                        result[student] = dorm
                        break
                else:  # Standardowe przydziały
                    dorm_counter[dorm]['female' if students_sex[student] == 1 else 'male'] += 1
                    result[student] = dorm
                    break

    return result



def objective_func(
        input_vector: List[int], 
        years: List[int], 
        disabilities: List[Union[0, 1, 2, 3]], 
        prior_list: List[List[int]], 
        departments: List[int], 
        distances: List[List[float]], 
        alpha: float = 0.5
) -> float:
    '''Zwraca wartość funkcji celu dla wejścia input_vector'''
    result = 0
    for i in range(len(input_vector)):
        dorm = input_vector[i]
        department = departments[i]
        prior_rank = prior_list[i].index(dorm) if dorm in prior_list[i] else 0
        result += (disability_priority[disabilities[i]] * (1 - years[i]/10) - distances[dorm][department] + alpha * prior_rank)
    
    return round(result,3)


def tabu_search(
    years: List[int],
    disabilities: List[Union[0, 1, 2, 3]],
    prior_list: List[List[int]],
    departments: List[int],
    dorm_capacity: List[int],
    dorm_pos: List[Tuple[float, float]],
    dep_pos: List[Tuple[float, float]],
    students_sex: List[int],  # 0 - mężczyzna, 1 - kobieta
    choice: Union[1, 2, 3, 4],
    min_fill: float = 0,  # Minimalny poziom wypełnienia (tylko dla choice == 2)
    max_iterations: int = 200,
    tabu_list_size: int = 100,
    alpha: float = 0.5
):
    '''Implementacja algorytmu Tabu Search dla przypisania akademików.'''

    distances = calculate_distances(dorm_pos, dep_pos)

    # Rozwiązanie początkowe
    current_solution = starting_solution(prior_list, dorm_capacity, students_sex, min_fill, choice)
    best_solution = current_solution[:]
    best_objective = objective_func(current_solution, years, disabilities, prior_list, departments, distances, alpha)

    # Inicjowanie listy tabu
    tabu_list = []

    # Licznik odwiedzonych rozwiązań
    visited_solutions = 0

    # Jeśli choice == 2, obliczamy maksymalny możliwy min_fill
    if choice == 2:
        total_capacity = sum(dorm_capacity)
        max_possible_fill = min(1, len(prior_list) / total_capacity)

        # Jeśli podany min_fill jest wyższy niż maksymalny możliwy, zastąp go
        if min_fill > max_possible_fill:
            print(f"Uwaga: min_fill {min_fill:.2f} jest niemożliwe do osiągnięcia. "
                  f"Zmieniono na maksymalne możliwe min_fill = {max_possible_fill:.2f}.")
            min_fill = max_possible_fill

    # Oblicz globalną proporcję płci dla choice == 4
    if choice == 4:
        total_males = sum(1 for sex in students_sex if sex == 0)
        total_females = sum(1 for sex in students_sex if sex == 1)
        global_gender_ratio = total_females / total_males if total_males > 0 else float('inf')

    for _ in range(max_iterations):
        neighbors = []

        # Generowanie sąsiedztwa
        for student in range(len(current_solution)):
            for dorm in prior_list[student]:
                # Dla choice == 3 pomijamy ostatni akademik z listy priorytetów
                if choice == 3 and dorm == prior_list[student][-1]:
                    continue

                if dorm != current_solution[student]:
                    new_solution = current_solution[:]
                    new_solution[student] = dorm

                    # Warunek ograniczonej pojemności akademików
                    dorm_counts = {d: {'male': 0, 'female': 0} for d in range(len(dorm_capacity))}
                    for s, assigned_dorm in enumerate(new_solution):
                        if assigned_dorm is not None:
                            dorm_counts[assigned_dorm]['male' if students_sex[s] == 0 else 'female'] += 1

                    # Proporcja płci dla choice == 4
                    if choice == 4:
                        valid = True
                        for d in range(len(dorm_capacity)):
                            local_males = dorm_counts[d]['male']
                            local_females = dorm_counts[d]['female']
                            local_ratio = (local_females / local_males) if local_males > 0 else float('inf')

                            # Sprawdzamy, czy proporcja w akademiku nie odbiega zbytnio od globalnej
                            if abs(local_ratio - global_gender_ratio) > 0.1 * global_gender_ratio:  # Tolerancja 10%
                                valid = False
                                break
                        if not valid:
                            continue

                    if dorm_counts[dorm]['male'] + dorm_counts[dorm]['female'] <= dorm_capacity[dorm]:
                        # Sprawdzenie dla choice == 2: Minimalny poziom wypełnienia akademików
                        if choice == 2:
                            min_fill_counts = [(dorm_counts[d]['male'] + dorm_counts[d]['female']) / dorm_capacity[d]
                                               for d in range(len(dorm_capacity))]
                            if min(min_fill_counts) >= min_fill:
                                neighbors.append(new_solution)
                                visited_solutions += 1  # Zlicz rozwiązanie

                        # Sprawdzenie dla pozostałych trybów
                        elif choice in [1, 3, 4]:
                            neighbors.append(new_solution)
                            visited_solutions += 1  # Zlicz rozwiązanie

        # Ocena sąsiednich rozwiązań
        best_neighbor = None
        best_neighbor_objective = float('-inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list: 
                neighbor_objective = objective_func(neighbor, years, disabilities, prior_list, departments, distances, alpha)
                visited_solutions += 1  # Zlicz każde sprawdzone rozwiązanie
                if neighbor_objective > best_neighbor_objective:
                    best_neighbor = neighbor
                    best_neighbor_objective = neighbor_objective

        # Jeśli brak sąsiedztwa, zakończ
        if best_neighbor is None:
            break

        # Aktualizacja najlepszego rozwiązania
        if best_neighbor_objective > best_objective:
            best_solution = best_neighbor[:]
            best_objective = best_neighbor_objective

        current_solution = best_neighbor

        # Dodanie rozwiązania do listy tabu
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

    return best_solution, best_objective #, visited_solutions


def main_loop():
    while True:
        os.system('cls')
        print('---GENEROWANIE DANYCH---')
        N = int(input('Podaj liczbę studentów: '))
        num_dorm = int(input('Podaj liczbę akademików: '))
        num_dep = int(input('Podaj liczbę wydziałów: '))
        print('')

        for elem in [N, num_dorm, num_dep]: 
            if not isinstance(elem, int): 
                print('Wrong input!')

        [students_years,
        students_disability,
        students_priority_lists,
        students_departments,
        students_sex,
        dormitorys_capacity,
        dormitory_position,
        departments_position] = generate_data(N, num_dorm, num_dep)

        print('---OGRANICZENIA---')
        print('1. Brak')
        print('2. Minimalny poziom wypełnienia akademików')
        print('3. Usunięcie najbardziej niechcianego akademika')
        print('4. Równe rozmieszczenie ze względu na płeć')
        restriction_choice = int(input('Wybierz (1, 2, 3, 4): '))

        if restriction_choice not in [1, 2, 3, 4]:
            print('Wrong input!')
        
        elif restriction_choice == 1:
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            students_sex, restriction_choice))
            input()

        elif restriction_choice == 2:
            print('')
            min_fill = float(input('Podaj minimalny poziom wypełnienia (zakres od 0 do 1): '))
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            students_sex, restriction_choice, min_fill))
            input()

        elif restriction_choice == 3:
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            students_sex, restriction_choice))
            input()

        elif restriction_choice == 4:
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            students_sex, restriction_choice))
            input()


if __name__ == '__main__':
    # Główna pętla programu
    main_loop()
