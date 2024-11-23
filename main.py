from typing import List, Union, Dict, Tuple
from math import sqrt

# students data
'''Id studenta to jego indeks w listach'''
students_years: List[int] = []  # Rok, na którym studiują studenci
students_disability: List[Union[0, 1, 2, 3]] = []  # Stopień niepełnosprawności studentów
students_priority_lists: List[List[int]] = [[]]  # Lista priorytetów studentów
students_departments: List[int] = [] # Lista wydziałów studentów

# dormitories data
'''Id akademika to jego indeks w listach'''
dormitorys_capacity: List[int] = []  # Pojemność akademików
dormitory_position: List[Tuple[float, float]] = []  # Pozycja akademików (x, y) w km

departments_position: List[Tuple[float, float]] = []  # Pozycja wydziałów studentów (x, y) w km
disability_priority: Dict[int, int] = {1: 100, 2: 75, 3: 50, 0: 25}  # Priorytet na podstawie stopnia niepełnosprawności używany w funkcji celu


def calculate_distances(dorm_pos: List[tuple[float]], dep_pos: List[tuple[float]]):
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


def starting_solution(prior_list: List[List[int]], dorm_capacity: List[int]):
    '''Zwraca początkowe rozwiązanie do algorytmu Tabu Search'''
    result = [None] * len(prior_list) # Wstępne przypisanie "brak akademika" każdemu studentowi
    dorm_counter = {i: 0 for i in range(len(dorm_capacity))} # Licznik miejsc w akademikach
    bad_students = [] # Studenci, których nie udało się przypisać w pierwszej pętli


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

    # Druga pętla: Przypisujemy pozostałych studentów do wolnych miejsc
    for student in bad_students:
        for dorm in range(len(dorm_capacity)):
            if dorm_counter[dorm] < dorm_capacity[dorm]:
                dorm_counter[dorm] += 1
                result[student] = dorm  # Przypisanie studenta
                break  
    return result


def objective_func(input_vector: List[int], years: List[int], disabilities: List[Union[0, 1, 2, 3]], prior_list: List[List[int]], departments: List[int], distances: List[List[float]], alpha: float = 0.5):
    '''Zwraca wartość funkcji celu dla wejścia input_vector'''
    result = 0
    for i in range(len(input_vector)):
        dorm = input_vector[i]
        department = departments[i]
        prior_rank = prior_list[i].index(dorm) if dorm in prior_list[i] else 0
        result += (disability_priority[disabilities[i]] * (1 - years[i]/10) - distances[dorm][department] + alpha * prior_rank)
    
    return result


def tabu_search(years: List[int], disabilities: List[Union[0, 1, 2, 3]], prior_list: List[List[int]], dep_pos: List[Tuple[float, float]], dorm_capacity: List[int], dorm_pos: List[Tuple[float, float]]):
    # Losowe rozwiązanie startowe
    s: List[int] = starting_solution(prior_list, dorm_capacity)

    # Inicjowanie listy tabu
    t: List[List[int]] = [None for i in range(100)]

    for i in range(1000):
        pass


if __name__ == '__main__':
    pass
