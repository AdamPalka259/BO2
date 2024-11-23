import random
from typing import List, Union, Tuple, Dict

def generate_data(N: int, num_dormitories: int, num_departments: int) -> Tuple[
    List[int], List[Union[0, 1, 2, 3]], List[List[int]], List[int],
    List[int], List[Tuple[float, float]], List[Tuple[float, float]]
]:
    # Students data
    students_years = [random.randint(1, 5) for _ in range(N)]  # Losowy rok studiów od 1 do 5
    students_disability = random.choices([0, 1, 2, 3], weights=[70, 15, 10, 5], k=N) # Stopień niepełnosprawności
    students_priority_lists = [random.sample(range(1, num_dormitories + 1), num_dormitories) for _ in range(N)]  # Priorytety akademików
    students_departments = [random.randint(1, num_departments) for _ in range(N)]  # Losowy wydział dla każdego studenta

    # Dormitories data
    dormitory_position = []
    dormitorys_capacity = []
    for y in range(1, num_dormitories + 1):
        dormitory_position.append((round(random.uniform(1, 50), 2), round(random.uniform(1, 50), 2)))  # Losowa pozycja akademika (x, y)
        dormitorys_capacity.append(random.randint(50, 100))  # Losowa pojemność akademika
        
    print('dormitorys_capacities')
    print(dormitorys_capacity)
    print('dormitorys_positions')
    print(dormitory_position)

    # Departments data
    departments_position = []
    for y in range(1, num_departments + 1):
        departments_position.append((round(random.uniform(1, 50), 2), round(random.uniform(1, 50), 2)))
    print('departments_positions')
    print(departments_position)

    # Student_data
    print("stud_data id rok niepel priorytet_akademikow   wydzial kordy_wydzialu")
    for i in range(N):
        x = students_departments[i]
        print("student_id",i,"->",students_years[i],students_disability[i],students_priority_lists[i],students_departments[i],departments_position[x-1])

    return (
        students_years,
        students_disability,
        students_priority_lists,
        students_departments,
        dormitorys_capacity,
        dormitory_position,
        departments_position
    )

# Przykład użycia
N = 50  # Liczba studentów
num_dormitories = 10  # Liczba akademików
num_departments = 4  # Liczba wydziałów
data = generate_data(N, num_dormitories, num_departments)

# dane
(students_years, students_disability, students_priority_lists,
 students_departments, dormitorys_capacity, dormitory_position,
 departments_position) = data





