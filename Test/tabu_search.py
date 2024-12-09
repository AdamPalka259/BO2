from typing import List, Union, Dict, Tuple
from math import sqrt


disability_priority: Dict[int, int] = {1: 100, 2: 75, 3: 50, 0: 25}  # Priorytet na podstawie stopnia niepełnosprawności używany w funkcji celu

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
    disabilities: List[Union[0, 1, 2, 3]], 
    students_sex: List[int],    # 0 - kobieta, 1 - mężczyzna
    dorm_capacity: List[int], 
) -> List[Union[int, None]]:
    '''Zwraca początkowe rozwiązanie do algorytmu Tabu Search z uwzględnieniem wyboru trybu działania (choice).'''
    result = [None] * len(prior_list)
    current_capacity = [0] * len(dorm_capacity)

    # Sortujemy indeksy studentów według priorytetu na podstawie `disabilities` 
    # (1 -> najwyższy priorytet, 0 -> najniższy).
    sorted_students = sorted(range(len(prior_list)), key=lambda x: -disabilities[x])

    # Przypisujemy studentów do akademików według kolejności
    for student in sorted_students:
        for dorm in prior_list[student]:
            if current_capacity[dorm] < dorm_capacity[dorm]:  # Sprawdzamy pojemność akademika
                result[student] = dorm
                current_capacity[dorm] += 1
                break

    return result



def objective_func(
        input_vector: List[Union[int, None]], 
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
        if input_vector[i] is not None:
            dorm = input_vector[i]
            department = departments[i]
            prior_rank = prior_list[i].index(dorm) if dorm in prior_list[i] else 0
            result += (disability_priority[disabilities[i]]/100 * (1 - years[i]/10) * distances[dorm][department] + alpha * prior_rank)
    
    return round(result,3)


def generate_neighbourhood(
    current_solution: List[Union[int, None]],
    prior_list: List[List[int]],
    dorm_capacity: List[int],
    neighbourhood_type: str = "both"
) -> List[List[Union[int, None]]]:
    '''Generuje sąsiedztwo przez różne typy ruchów.'''
    neighbourhood = []
    num_students = len(current_solution)

    def is_valid_solution(solution):
        '''Sprawdza, czy rozwiązanie spełnia ograniczenia pojemności akademików.'''
        capacity_usage = [0] * len(dorm_capacity)
        for dorm in solution:
            if dorm is not None:
                capacity_usage[dorm] += 1
        return all(capacity_usage[dorm] <= dorm_capacity[dorm] for dorm in range(len(dorm_capacity)))

    if neighbourhood_type in ("change_dorm", "both"):
        for i in range(num_students):
            if current_solution[i] is not None:
                for dorm in prior_list[i]:
                    if dorm != current_solution[i]:
                        new_solution = current_solution[:]
                        new_solution[i] = dorm
                        if is_valid_solution(new_solution):
                            neighbourhood.append(new_solution)

    if neighbourhood_type in ("swap_students", "both"):
        for i in range(num_students):
            for j in range(i + 1, num_students):
                if current_solution[i] is not None and current_solution[j] is not None:
                    new_solution = current_solution[:]
                    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                    if is_valid_solution(new_solution):
                        neighbourhood.append(new_solution)

    if neighbourhood_type in ("move_group", "both"):
        for dorm_from in range(len(dorm_capacity)):
            for dorm_to in range(len(dorm_capacity)):
                if dorm_from != dorm_to:
                    # Zidentyfikuj studentów przypisanych do dorm_from
                    group = [i for i in range(num_students) if current_solution[i] == dorm_from]
                    if group:
                        new_solution = current_solution[:]
                        for student in group:
                            new_solution[student] = dorm_to
                        if is_valid_solution(new_solution):
                            neighbourhood.append(new_solution)

    return neighbourhood



def tabu_search(
    start_solution: List[Union[int, None]],
    years: List[int],
    disabilities: List[Union[0, 1, 2, 3]],
    prior_list: List[List[int]],
    students_sex: List[int],  # 0 - mężczyzna, 1 - kobieta
    departments: List[int],
    dorm_capacity: List[int],
    dorm_pos: List[Tuple[float, float]],
    dep_pos: List[Tuple[float, float]],
    neighbourhood_type: str = "both",  # Dodanie argumentu typu sąsiedztwa
    max_iterations: int = 1000,
    tabu_list_size: int = 100,
    alpha: float = 0.5
) -> Tuple[List[Union[int, None]], float]:
    '''Implementacja algorytmu Tabu Search dla przypisania akademików z uwzględnieniem kryterium aspiracji i minimalizacji funkcji celu.'''

    distances = calculate_distances(dorm_pos, dep_pos)

    # Inicjalizacja
    if start_solution is None:
        raise ValueError("Rozwiązanie początkowe nie zostało poprawnie wygenerowane!")

    current_solution = start_solution[:]
    best_solution = current_solution[:]
    best_objective = objective_func(
        current_solution, years, disabilities, prior_list, departments, distances, alpha
    )

    # Lista tabu
    tabu_list = []
    iteration = 0
    no_improvement_counter = 0  # Licznik iteracji bez poprawy

    iterations = []
    objectives = []

    def check_aspiration(solution, objective_value):
        '''Sprawdzenie kryterium aspiracji.'''
        if solution in tabu_list:
            if objective_value < best_objective:  # Dostosowano do minimalizacji
                print("Kryterium aspiracji spełnione: ruch poprawia funkcję celu.")
                return True
            else:
                print("Kryterium aspiracji nie spełnione.")
                return False
        return True

    while iteration < max_iterations:
        print(f"Iteracja {iteration}, najlepsze rozwiązanie: {best_solution}, wartość funkcji celu: {best_objective}")

        # Zbieranie danych do wykresu
        iterations.append(iteration)
        print(iterations)
        objectives.append(best_objective)
        print(objectives)
        
        # Generowanie sąsiedztwa z uwzględnieniem typu sąsiedztwa
        neighbourhood = generate_neighbourhood(
            current_solution, prior_list, dorm_capacity, neighbourhood_type
        )
        if not neighbourhood:
            print("Brak dostępnych sąsiadów, kończymy iterację.")
            break

        # Filtrowanie przez listę tabu
        neighbourhood = [solution for solution in neighbourhood if solution not in tabu_list]
        if not neighbourhood:
            print("Brak sąsiedztwa po uwzględnieniu listy tabu, kończymy iterację.")
            break

        # Inicjalizacja najlepszych wartości w bieżącej iteracji
        best_neighbour = neighbourhood[0]
        best_neighbour_objective = objective_func(
            best_neighbour, years, disabilities, prior_list, departments, distances, alpha
        )

        # Wybór najlepszego sąsiada
        for neighbour in neighbourhood:
            objective = objective_func(neighbour, years, disabilities, prior_list, departments, distances, alpha)

            # Sprawdzanie kryterium aspiracji i minimalizacja funkcji celu
            if check_aspiration(neighbour, objective) and objective < best_neighbour_objective:
                best_neighbour = neighbour
                best_neighbour_objective = objective

        # Aktualizacja najlepszego rozwiązania
        if best_neighbour_objective < best_objective:  # Minimalizacja: nowa wartość musi być mniejsza
            best_solution = best_neighbour[:]
            best_objective = best_neighbour_objective
            no_improvement_counter = 0  # Reset licznika przy poprawie
        else:
            no_improvement_counter += 1  # Zwiększanie licznika, jeśli brak poprawy

        # Aktualizacja bieżącego rozwiązania
        current_solution = best_neighbour
        tabu_list.append(current_solution)

        # Usuwanie najstarszego elementu z listy tabu (FIFO)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        # Sprawdzanie warunku przerywania po 10 iteracjach bez poprawy
        if no_improvement_counter >= 10:
            print("Brak poprawy funkcji celu przez 10 iteracji. Kończymy obliczenia.")
            break

        iteration += 1

    return best_solution, best_objective, iterations, objectives

