import tkinter as tk
from PIL import Image, ImageTk
from rand import generate_data
from tabu_search import tabu_search, starting_solution
import matplotlib.pyplot as plt
ilosc_stud, ilosc_aka, ilosc_wydz, ogr = 0,0,0,0
import tkinter.messagebox as messagebox
import datetime
import re
import os
from datetime import datetime

def show_algorytm(window, canvas):
    remove_back_button(window)
    clear_frame(window)

    napis_tytul = tk.Frame(window)
    label_algorytm = tk.Label(napis_tytul, text="Wybierz sposób dostarczenia danych", font=("Arial", 20))
    label_algorytm.pack(pady=30)
    napis_tytul.pack(fill="both", expand=True)

    przycisk_recznie = tk.Button(window, text="Ręcznie", font=("Arial", 18), width=20, height=2, command=lambda: algorytm_with_data_from_program(window, canvas))
    przycisk_z_pliku = tk.Button(window, text="Z pliku", font=("Arial", 18), width=20, height=2, command=lambda: algorytm_with_data_from_file(window))

    przycisk_recznie.place(x=400, y=150)
    przycisk_z_pliku.place(x=400, y=250)

    add_back_button(window, 1)

  # Importuj datetime


def algorytm_with_data_from_program(window, canvas):

    def set_ogr(value):
        ogr.set(value)  # Ustawienie wartości dla zmiennej ogr
        print(f"Ograniczenie ustawione na: {ogr.get()}")

    def zmien_wartosc():
        global czy_uruchom
        czy_uruchom = True  # Zmieniamy wartość na True
        print(f"Wartość zmiennej: {czy_uruchom}")

    def resetuj_wartosc():
        global czy_uruchom
        czy_uruchom = False  # Zmieniamy wartość na False
        print(f"Wartość zmiennej po resecie: {czy_uruchom}")

    def save_all_numbers():
        # Pobieranie wartości z IntVar i wyświetlanie ich w konsoli
        print(f"Ilość studentów: {ilosc_stud.get()}")
        print(f"Ilość wydziałów: {ilosc_wydz.get()}")
        print(f"Ilość akademików: {ilosc_aka.get()}")
        print(f"Ograniczenie: {ogr.get()}")

        # Aktualizacja wyświetlanych danych
        ilosc_stud2.config(text=f"Ilość studentów - {ilosc_stud.get()}")
        ilosc_wyd2z.config(text=f"Ilość wydziałów - {ilosc_wydz.get()}")
        ilosc_aka1.config(text=f"Ilość akademików - {ilosc_aka.get()}")
        aktualne_ogr.config(text=f"Wybór sąsiedstwa - {ogr.get()}")

    def uruchom_algorytm():
        global best_solution_glob, best_objective_glob, iterations_glob, objectives_glob
        if ilosc_stud.get() == 0 or ilosc_aka.get() == 0 or ilosc_wydz.get() == 0 or ogr.get() == 0:
            messagebox.showerror("Błąd", "Proszę wprowadzić wszystkie dane przed uruchomieniem algorytmu!")
        else:
            [students_years,
            students_disability,
            students_priority_lists,
            students_departments,
            students_sex,
            dormitorys_capacity,
            dormitory_position,
            departments_position] = generate_data(ilosc_stud.get(), ilosc_aka.get(), ilosc_wydz.get())

            start_solution = starting_solution(students_priority_lists, students_disability, students_sex, dormitorys_capacity)

            if ogr.get() == 1:
                best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                                        students_priority_lists, students_sex, students_departments, 
                                        dormitorys_capacity, dormitory_position, departments_position, 
                                        'change_dorm')
            elif ogr.get() == 2:
                best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                                        students_priority_lists, students_sex, students_departments, 
                                        dormitorys_capacity, dormitory_position, departments_position, 
                                        'swap_students')
            elif ogr.get() == 3:
                best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                                        students_priority_lists, students_sex, students_departments, 
                                        dormitorys_capacity, dormitory_position, departments_position, 
                                        'move_group')
            elif ogr.get() == 4:
                best_solution, best_objective, iterations, objectives = tabu_search(start_solution, students_years, students_disability, 
                                        students_priority_lists, students_sex, students_departments, 
                                        dormitorys_capacity, dormitory_position, departments_position, 
                                        'both')
            
            
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            plt.figure(figsize=(10, 5))
            plt.plot(iterations, objectives, marker='o', label='Funkcja celu')
            plt.xlabel('Iteracja')
            plt.ylabel('Wartość funkcji celu')
            plt.title(f'Liczba studentów: {ilosc_stud.get()}, Liczba akademików: {ilosc_aka.get()}, Liczba wydziałów: {ilosc_wydz.get()}\n Sąsiedztwo: {ogr.get()}')
            plt.legend()
            plt.grid()
            plt.savefig(f"zapis_{formatted_date}.png")
            plt.show()
            plt.close()

            #ilosc_stud.get(), ilosc_aka.get(), ilosc_wydz.get()
            zapisz_wynik_algorytmu_do_wyswietlania(ilosc_stud.get(),ilosc_wydz.get() ,ilosc_aka.get() , ogr.get(),best_solution,  best_objective, iterations, objectives )
            
            ods_last(window)

        resetuj_wartosc()

    remove_back_button(window)
    clear_frame(window)


    frame_algorytm = tk.Frame(window)
    label_algorytm = tk.Label(frame_algorytm, text="Podaj dane potrzebne do skompilowania algorytmu", font=("Arial", 20))
    label_algorytm.place(x=200, y=10)
    
    frame_algorytm.pack(fill="both", expand=True)
    
    ilosc_stud = tk.IntVar()
    ilosc_aka = tk.IntVar()
    ilosc_wydz = tk.IntVar()
    ogr = tk.IntVar()

    entry1 = tk.Entry(window, textvariable=ilosc_stud)
    entry1.place(x=200, y=100)  # Pozycjonowanie pola tekstowego

    label1 = tk.Label(window, text="Ilość studentów ", font=("Arial", 14))
    label1.place(x=60, y=95)  # Pozycjonowanie opisu pola

    entry2 = tk.Entry(window, textvariable=ilosc_aka)
    entry2.place(x=200, y=200)  # Pozycjonowanie pola tekstowego

    label2 = tk.Label(window, text="Ilość wydziałów ", font=("Arial", 14))
    label2.place(x=60, y=195)  # Pozycjonowanie opisu pola

    entry3 = tk.Entry(window, textvariable=ilosc_wydz)
    entry3.place(x=220, y=300)  # Pozycjonowanie pola tekstowego

    label3 = tk.Label(window, text="Ilość akademików ", font=("Arial", 14))
    label3.place(x=60, y=295)  # Pozycjonowanie opisu pola

    choose_label = tk.Label(window, text="Wybór sąsiedstwa:", font=("Arial", 14))
    choose_label.place(x=50, y=420)

    button1 = tk.Button(window, text="Zmiana akademika", font=("Arial", 14), command=lambda: set_ogr(1))
    button1.place(x=50, y=450)

    button2 = tk.Button(window, text="Zamiana studentów", font=("Arial", 14), command=lambda: set_ogr(2))
    button2.place(x=50, y=490)

    button3 = tk.Button(window, text="Przeniesienie grupy studentów", font=("Arial", 14), command=lambda: set_ogr(3))
    button3.place(x=50, y=530)

    button4 = tk.Button(window, text="Wszystkie jednocześnie", font=("Arial", 14), command=lambda: set_ogr(4))
    button4.place(x=50, y=570)

    save_button = tk.Button(window, text="Zapisz wartosci",font=("Arial", 15), width=12, height=3, command=save_all_numbers)  # Przekazanie funkcji bez nawiasów
    save_button.place(x=230, y=350)  # Pozycjonowanie przycisku zapisz wszystkie liczby

    aktualne_dane_do_algorytmu = tk.Label(window, text="Aktualne dane do algorytmu", font=("Arial", 14))
    aktualne_dane_do_algorytmu.place(x=400, y=350)

    ilosc_stud2 = tk.Label(window, text="Ilość studentów - ", font=("Arial", 14))
    ilosc_stud2.place(x=400, y=390)

    ilosc_wyd2z = tk.Label(window, text="Ilość wydziałów - ", font=("Arial", 14))
    ilosc_wyd2z.place(x=400, y=430)

    ilosc_aka1 = tk.Label(window, text="Ilość akademików - ", font=("Arial", 14))
    ilosc_aka1.place(x=400, y=470)

    aktualne_ogr = tk.Label(window, text="Wybór sąsiedstwa - ", font=("Arial", 14))
    aktualne_ogr.place(x=400, y=510)
    
    przycisk_alg = tk.Button(window, text="Uruchom algorytm", font=("Arial", 20), width=20, height=3, command=uruchom_algorytm)
    przycisk_alg.place(x=500, y=550)
    
    ods_last(window)

    przycisk_wykres = tk.Button(window, text="Zobacz wykres", font=("Arial", 20), width=12, height=3, command=lambda: ods_last_wykres(window))
    przycisk_wykres.place(x=600, y=100)


    
    add_back_button(window, 2)

def ods_last_wykres(window):
    sciezka_do_najnowszego_wyk=find_latest_file(r'C:/Users/kamil/Documents/GitHub/BO2', "zapis_", 2)
    image = Image.open(sciezka_do_najnowszego_wyk)
    image = image.resize((1050, 500))  # Opcjonalnie zmień rozmiar obrazu
    photo = ImageTk.PhotoImage(image)
   
    # Tworzenie nowego okna
    new_window = tk.Toplevel(window)
    new_window.title("Wykres")
    new_window.geometry("1000x500")  # Rozmiar nowego okna

    # Wyświetl obraz w nowym oknie
    label = tk.Label(new_window, image=photo)
    label.image = photo  # Zachowaj referencję
    label.pack(pady=20)

def ods_last(window):
    sciezka_do_najnowszego_eksperymentu=find_latest_file(r'C:/Users/kamil/Documents/GitHub/BO2', "zapis_",1)
    data=extract_values_from_file(sciezka_do_najnowszego_eksperymentu)

    students = data['students']
    dormitories = data['dormitories']
    faculties = data['faculties']
    neighborhood = data['neighborhood']
    best_solution = data['best_solution']
    best_objective = data['best_objective']
    iterations = data['iterations']

    Ostatnio_wykonany_algorytm = tk.Label(window, text="Parametry ostatnio wykonanego algorytmu", font=("Arial", 14))
    Ostatnio_wykonany_algorytm.place(x=350, y=40)

    Ostatnio_wykonany_algorytm_student = tk.Label(window, text=f"liczba studentow - {students}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_student.place(x=350, y=65)

    Ostatnio_wykonany_algorytm_dormitories = tk.Label(window, text=f"liczba akademików - {dormitories}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_dormitories.place(x=350, y=90)

    Ostatnio_wykonany_algorytm_faculties = tk.Label(window, text=f"liczba wydziałów - {faculties}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_faculties.place(x=350, y=115)

    Ostatnio_wykonany_algorytm_neighborhood = tk.Label(window, text=f"Wybór sąsiedswa - {neighborhood}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_neighborhood.place(x=350, y=140)

   # Ostatnio_wykonany_algorytm_best_solution = tk.Label(window, text=f"najlepsze rozwiązanie - {best_solution}", font=("Arial", 14))
   # Ostatnio_wykonany_algorytm_best_solution.place(x=350, y=165)

    Ostatnio_wykonany_algorytm_best_objective = tk.Label(window, text=f"najlepszy cel - {best_objective}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_best_objective.place(x=350, y=165)

    Ostatnio_wykonany_algorytm_iterations = tk.Label(window, text=f"liczba iteracji - {max(iterations)}", font=("Arial", 14))
    Ostatnio_wykonany_algorytm_iterations.place(x=350, y=190)
def extract_values_from_file(file_path):
    extracted_values = {}

    with open(file_path, 'r') as file:
        content = file.read()

        extracted_values['students'] = int(re.search(r'Ilość studentów:\s*(\d+)', content).group(1))

        extracted_values['dormitories'] = int(re.search(r'Ilość akademików:\s*(\d+)', content).group(1))

        extracted_values['faculties'] = int(re.search(r'Ilość wydziałów:\s*(\d+)', content).group(1))

        extracted_values['neighborhood'] = int(re.search(r'Wybór sąsiedztwa:\s*(\d+)', content).group(1))

        best_solution_match = re.search(r'najlepsze rozw:\s*\[([^\]]+)\]', content)
        if best_solution_match:
            extracted_values['best_solution'] = [int(x) for x in best_solution_match.group(1).split(',')]

        extracted_values['best_objective'] = float(re.search(r'best objectives\s*([\d\.]+)', content).group(1))

        iterations_match = re.search(r'iteracje:\s*\[([^\]]+)\]', content)
        if iterations_match:
            extracted_values['iterations'] = [int(x) for x in iterations_match.group(1).split(',')]

        objectives_match = re.search(r'objectives co kolwiek to jest\[(.*?)\]', content, re.DOTALL)
        if objectives_match:
            extracted_values['objectives'] = [float(x) for x in objectives_match.group(1).split(',')]

    return extracted_values


def find_latest_file(directory, pattern, war):
    if war==1:
        extension=".txt"
    elif war==2:
        extension=".png"
    latest_file = None
    latest_time = None
    
    for filename in os.listdir(directory):
        if filename.startswith(pattern) and filename.endswith(extension):
            try:
                date_str = filename[len(pattern):-len(extension)]  # Exclude the extension from the date part
                file_date = datetime.strptime(date_str, "%Y_%m_%d_%H_%M_%S")
                
                # Check if this file's date is the latest one (based on hour, minute, then second if needed)
                if latest_time is None:
                    latest_time = file_date
                    latest_file = filename
                else:
                    # Compare by hour first, then minute, then second
                    if (file_date.hour > latest_time.hour) or \
                       (file_date.hour == latest_time.hour and file_date.minute > latest_time.minute) or \
                       (file_date.hour == latest_time.hour and file_date.minute == latest_time.minute and file_date.second > latest_time.second):
                        latest_time = file_date
                        latest_file = filename
            except ValueError:
                # Ignore files that don't match the expected format
                continue

    return latest_file
def add_back_button(window, w_glebi):
    if w_glebi==2:
       if not hasattr(window, 'back_button'):
            canvas = tk.Canvas(window, width=1000, height=700)

            window.back_button = tk.Button(window, text="Cofnij", font=("Arial", 14), width=10, height=2, command=lambda: show_algorytm(window, canvas))
            window.back_button.place(x=10, y=10)
    else:
        if not hasattr(window, 'back_button'):
            window.back_button = tk.Button(window, text="Cofnij", font=("Arial", 14), width=10, height=2, command=lambda: back_to_main(window))
            window.back_button.place(x=10, y=10)

def zapisz_wynik_algorytmu_do_wyswietlania( ilosc_stud, ilosc_aka, ilosc_wydz, ograniczenia,best_solution, best_objective, iterations, objectives ):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
    with open(f"zapis_{formatted_date}.txt", "w") as file:
        file.write(f"Ilość studentów: {ilosc_stud}\n")
        file.write(f"Ilość akademików: {ilosc_aka}\n")
        file.write(f"Ilość wydziałów: {ilosc_wydz}\n")
        file.write(f"Wybór sąsiedztwa: {ograniczenia}\n")
        file.write(f"najlepsze rozw: {best_solution}\n")
        file.write(f"best objectives {best_objective}\n")
        file.write(f"iteracje: {iterations}\n")
        file.write(f"Wartość funkcji celu dla kolejnych rozw{objectives}") 
        
def algorytm_with_data_from_file(window):
    remove_back_button(window)
    clear_frame(window)

    label_dane = tk.Label(window, text="Wprowadź dane w folerze 'dane' plik w formacie xls", font=("Arial", 20))
    label_dane.place(x=200, y=10)

    add_back_button(window, 2)
    
def zapisz_wyk_algorytmu(ilosc_studentow, ilosc_wydzialow, ilosc_akademikow, sasiedstwo,wygenerowane_dane, rozwiazanie):
    import datetime
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")

    with open(f"zapis_{formatted_date}.txt", "w") as file:
        file.write(f"Ilość studentów: {ilosc_studentow}\n")
        file.write(f"Ilość akademików: {ilosc_akademikow}\n")
        file.write(f"Ilość wydziałów: {ilosc_wydzialow}\n")
        file.write(f"Wybór sąsiedztwa: {sasiedstwo}\n")
        file.write(f"Wybór sąsiedztwa: {wygenerowane_dane}\n")
        file.write(f"rozwiązanie{rozwiazanie}")

def remove_back_button(window):
    if hasattr(window, 'back_button'):
        window.back_button.destroy()
        del window.back_button

def back_to_main(window):
    remove_back_button(window)
    clear_frame(window)
    show_main_menu(window)

def back_to_algorytm_with_data_from_program(window):
    remove_back_button(window)
    clear_frame(window)
    show_algorytm(window)

def show_main_menu(window):
    clear_frame(window)
    canvas = tk.Canvas(window, width=1000, height=700)
    canvas.pack(fill="both", expand=True)
    canvas.delete("all")  # Usuwamy wszystkie istniejące elementy na canvasie
    image = Image.open("zdjecia/kapitol.png")
    image = image.resize((1000, 700))

    bg_image = ImageTk.PhotoImage(image)

    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    title_label = tk.Label(window, text="Algorytm optymalnego rozmieszczania studentów w akademikach", font=("Arial", 18, 'bold'), bg="white", width=50, height=2)
    canvas.create_window(500, 50, window=title_label)

    przycisk_algorytm = tk.Button(window, text="Algorytm", font=("Arial", 18), width=22, height=2, command=lambda: show_algorytm(window, canvas))
    przycisk_ostatnie = tk.Button(window, text="Ostatnie Działanie algorytmu", font=("Arial", 18), width=22, height=2, command=lambda: show_ostatnie_dzialanie(window, canvas))
    przycisk_dokumentacja = tk.Button(window, text="Dokumentacja", font=("Arial", 18), width=22, height=2, command=lambda: show_dokumentacja(window, canvas))
    przycisk_tworcze = tk.Button(window, text="Twórcy ", font=("Arial", 18), width=22, height=2, command=lambda: show_tworcze(window, canvas))

    canvas.create_window(500, 150, window=przycisk_algorytm)
    canvas.create_window(500, 250, window=przycisk_ostatnie)
    canvas.create_window(500, 350, window=przycisk_dokumentacja)
    canvas.create_window(500, 450, window=przycisk_tworcze)

from tkinter import ttk 
def show_ostatnie_dzialanie(window, canvas):
    clear_frame(window)
    
    frame_ostatnie = tk.Frame(window)
    frame_ostatnie.pack(fill="both", expand=True)

    label_ostatnie = tk.Label(frame_ostatnie, text="Ostatnie Działanie: Pliki tekstowe w katalogu", font=("Arial", 20))
    label_ostatnie.pack(pady=20)

    # Tabela
    columns = ("Nazwa pliku", "Liczba studentów", "Akademiki", "Wydziały", "Sąsiedztwa", "Najlepszy cel")
    table = ttk.Treeview(frame_ostatnie, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=150)

    table.pack(fill="both", expand=True, padx=20, pady=10)

    directory = r'C:/Users/kamil/Documents/GitHub/BO2'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                data = extract_values_from_file(file_path)
                table.insert("", "end", values=(
                    filename,
                    data.get('students', 'N/A'),
                    data.get('dormitories', 'N/A'),
                    data.get('faculties', 'N/A'),
                    data.get('neighborhood', 'N/A'),
                    data.get('best_objective', 'N/A')
                ))
            except Exception as e:
                print(f"Błąd przetwarzania pliku {filename}: {e}")
    
    add_back_button(window, 1)

import webbrowser

def show_dokumentacja(window, canvas):
    clear_frame(window)  # Funkcja do czyszczenia ramki (pozostawiona bez zmian)
    
    # Tworzenie nowej ramki dla dokumentacji
    frame_dokumentacja = tk.Frame(window)
    frame_dokumentacja.pack(fill="both", expand=True)

    # Tworzenie etykiety z tekstem
    label_dokumentacja = tk.Label(frame_dokumentacja, text="Dokumentacja znajduje się pod poniższym linkiem:", font=("Arial", 20))
    label_dokumentacja.pack(pady=20)

    # Tworzenie linku jako etykiety
    link = tk.Label(
        frame_dokumentacja,
        text="GitHub Repository: BO2",
        font=("Arial", 16),
        fg="blue",
        cursor="hand2"
    )
    link.pack(pady=10)

    # Funkcja otwierająca link w przeglądarce
    def open_github():
        webbrowser.open("https://github.com/AdamPalka259/BO2")
    
    # Przypisanie akcji kliknięcia
    link.bind("<Button-1>", lambda e: open_github())

    # Dodanie przycisku powrotu
    add_back_button(window, 1)
import itertools

def show_tworcze(window, canvas):
    clear_frame(window)
    
    # Tworzenie ramki
    frame_tworcze = tk.Frame(window)
    frame_tworcze.pack(fill="both", expand=True)

    # Nagłówek
    label_tworcze = tk.Label(frame_tworcze, text="Twórcy programu:", font=("Arial", 25))
    label_tworcze.pack(pady=40)

    # Informacja o twórcach
    creators_label = tk.Label(frame_tworcze, text="Kamil, Bartek i Adam", font=("Arial", 25))
    creators_label.pack(pady=40)

    # Animacja migającego tekstu
    animated_label = tk.Label(frame_tworcze, text="😂😂😂😂😂😂😂", font=("Arial", 25), fg="red")
    animated_label.pack(pady=40)

    # Funkcja animacji
    def animate_text():
        colors = itertools.cycle(["red", "blue", "green", "orange", "purple"])
        def change_color():
            animated_label.config(fg=next(colors))
            animated_label.after(300, change_color)  # Zmiana co 300 ms
        change_color()

    animate_text()

    add_back_button(window, 1)

def clear_frame(window):
    for widget in window.winfo_children():
        widget.pack_forget()

# Główna funkcja programu
def main():
    window = tk.Tk()
    window.title("Menu")
    window.geometry('1000x700')

    # Tworzymy canvas raz, aby był używany przez wszystkie widoki
    canvas = tk.Canvas(window, width=1000, height=700)
    canvas.pack(fill="both", expand=True)

    show_main_menu(window)  # Wywołanie funkcji pokazującej główne menu po uruchomieniu programu

    window.mainloop()

# Uruchomienie głównej funkcji
if __name__ == "__main__":
    main()
