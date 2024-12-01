from typing import List, Union, Dict, Tuple
from math import sqrt
from rand import generate_data
import os

# students data
'''Id studenta to jego indeks w listach'''
'''students_years: List[int] = []                       # Rok, na którym studiują studenci
students_disability: List[Union[0, 1, 2, 3]] = []       # Stopień niepełnosprawności studentów
students_priority_lists: List[List[int]] = [[]]         # Lista priorytetów studentów
students_departments: List[int] = []                    # Lista wydziałów studentów'''

# dormitories data
'''Id akademika to jego indeks w listach'''
'''dormitorys_capacity: List[int] = []                  # Pojemność akademików
dormitory_position: List[Tuple[float, float]] = []      # Pozycja akademików (x, y) w km

departments_position: List[Tuple[float, float]] = []    # Pozycja wydziałów studentów (x, y) w km'''
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


def starting_solution(prior_list: List[List[int]], dorm_capacity: List[int], min_fill: float = 0) -> List[int]:
    '''Zwraca początkowe rozwiązanie do algorytmu Tabu Search z uwzględnieniem warunku min_fill.'''
    result = [None] * len(prior_list)  # Wstępne przypisanie "brak akademika" każdemu studentowi
    dorm_counter = {i: 0 for i in range(len(dorm_capacity))}  # Licznik miejsc w akademikach
    bad_students = []  # Studenci, których nie udało się przypisać w pierwszej pętli

    # Obliczenie maksymalnego możliwego min_fill
    total_capacity = sum(dorm_capacity)
    max_possible_fill = min(1, len(prior_list) / total_capacity)

    # Jeśli podany min_fill jest wyższy niż maksymalny możliwy, zastąp go
    if min_fill > max_possible_fill:
        min_fill = max_possible_fill

    # Pierwsza pętla: Przypisanie zgodnie z listą priorytetów
    for i, student_prior in enumerate(prior_list):
        assigned = False  # Flaga określająca, czy student został przypisany
        for dorm in student_prior:
            if dorm is not None and dorm_counter[dorm] < dorm_capacity[dorm]:
                dorm_counter[dorm] += 1
                result[i] = dorm  # Przypisanie akademika
                assigned = True
                break  

        if not assigned:
            bad_students.append(i)  # Student bez przypisania w pierwszej pętli

    # Druga pętla: Przypisanie pozostałych studentów z uwzględnieniem min_fill
    for student in bad_students:
        for dorm in range(len(dorm_capacity)):
            # Sprawdzenie warunku minimalnego wypełnienia
            current_fill = dorm_counter[dorm] / dorm_capacity[dorm] if dorm_capacity[dorm] > 0 else 0
            if dorm_counter[dorm] < dorm_capacity[dorm] and current_fill >= min_fill:
                dorm_counter[dorm] += 1
                result[student] = dorm  # Przypisanie studenta
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
    choice: Union[1, 2, 3],
    min_fill: float = 0,  # Minimalny poziom wypełnienia (dla choice == 2)
    max_iterations: int = 200,
    tabu_list_size: int = 100,
    alpha: float = 0.5
):
    '''Implementacja algorytmu Tabu Search dla przypisania akademików.'''

    distances = calculate_distances(dorm_pos, dep_pos)

    # Obliczenie maksymalnego możliwego min_fill
    total_capacity = sum(dorm_capacity)
    max_possible_fill = min(1, len(prior_list) / total_capacity)

    # Jeśli podany min_fill jest wyższy niż maksymalny możliwy, zastąp go
    if min_fill > max_possible_fill:
        print(f"Uwaga: min_fill {min_fill:.2f} jest niemożliwe do osiągnięcia. "
              f"Zmieniono na maksymalne możliwe min_fill = {max_possible_fill:.2f}.")
        min_fill = max_possible_fill

    # Rozwiązanie początkowe
    current_solution = starting_solution(prior_list, dorm_capacity, min_fill)
    best_solution = current_solution[:]
    best_objective = objective_func(current_solution, years, disabilities, prior_list, departments, distances, alpha)

    # Inicjowanie listy tabu
    tabu_list = []

    # Licznik odwiedzonych rozwiązań
    visited_solutions = 0

    for _ in range(max_iterations):
        neighbors = []

        # Generowanie sąsiedztwa
        for student in range(len(current_solution)):
            for dorm in prior_list[student]:
                if dorm != current_solution[student]:
                    new_solution = current_solution[:]
                    new_solution[student] = dorm

                    # Warunek ograniczonej pojemności akademików
                    dorm_counts = {d: new_solution.count(d) for d in range(len(dorm_capacity))}
                    if dorm_counts[dorm] <= dorm_capacity[dorm]:
                        if choice == 2:
                            # Minimalny poziom wypełnienia akademików
                            min_fill_counts = [dorm_counts[d] / dorm_capacity[d] for d in range(len(dorm_capacity))]
                            if min(min_fill_counts) >= min_fill:  # Akademiki muszą spełniać minimalny poziom wypełnienia
                                neighbors.append(new_solution)
                                visited_solutions += 1  # Zlicz rozwiązanie
                        else:
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
        dormitorys_capacity,
        dormitory_position,
        departments_position] = generate_data(N, num_dorm, num_dep)

        print('---OGRANICZENIA---')
        print('1. Brak')
        print('2. Minimalny poziom wypełnienia akademików')
        print('---------------')
        restriction_choice = int(input('Wybierz (1, 2, 3, 4): '))

        if restriction_choice not in [1, 2, 3, 4]:
            print('Wrong input!')
        
        elif restriction_choice == 1:
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            restriction_choice))
            input()

        elif restriction_choice == 2:
            print('')
            min_fill = float(input('Podaj minimalny poziom wypełnienia (zakres od 0 do 1): '))
            print('')
            print(tabu_search(students_years, students_disability, 
                            students_priority_lists, students_departments, 
                            dormitorys_capacity, dormitory_position, departments_position, 
                            restriction_choice, min_fill))
            input()


if __name__ == '__main__':
    # Główna pętla programu
    main_loop()
