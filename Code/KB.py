import pandas as pd
import time as t
from pyswip import Prolog
from prediction import *

pegi_dic = {}
genre_dic = {}
year_dic = {}
platforms_dic = {}
publishers_dic = {}

def print_query_format(query):
    vett = []
    for key in query:       
        vett.append(key["X"])

    if(vett == []):
        print("Nessun elemento trovato per questa query.\n")

    i = 0
    for key in vett:
        print([key for key, val in name_dic.items() if val == vett[i]])
        i = i + 1

def set_publishers():
    i = 0
    for key in conversion_dic:
        if key != "fine_publishers" and i == 1:
            publishers_dic[key] = conversion_dic[key]
        elif key == "fine_publishers":
            return
        elif key == "fine_names":
            i = 1

def set_genres():
    i = 1
    for key in conversion_dic:
        if key != "fine_genres" and i == 1:
            genre_dic[key] = conversion_dic[key]
        elif key == "fine_genres":
            return
        

#Carico il dataset giochi_preprocessato.csv
dataset = pd.read_csv("./Dataset/giochi_preprocessato.csv")
dataset = dataset.drop(columns=["Classification_format"])

conversion = pd.read_csv("./Dataset/dizionario.csv")    #Carico il dizionario per le conversioni
conversion.apply(lambda row: set_dictionary(row), axis = 1)     #Carico la lista conversion_dic con tutto il contenuto di dizionario.csv
set_name()      #Carico name_dic con il dizionario dei nomi
set_publishers()
set_genres()

#Apri il file KB.pl in modalità scrittura
with open("./Code/KB.pl", "w") as prolog_file:
    prolog_file.write(":- discontiguous genre/2.\n")
    prolog_file.write(":- discontiguous giochi_pegi/3.\n")
    prolog_file.write(":- discontiguous val_publisher/2.\n")
    prolog_file.write(":- discontiguous genre_publisher/2.\n")
    prolog_file.write(":- discontiguous name_publisher_val/3. \n")

    #Itera attraverso le righe del dataset
    for index, row in dataset.iterrows():
        name = row[0]
        genre = row[6]
        pegi = row[5]
        publisher = row[3]
        rating = row[2]

        #Scrivo il fatto prolog con il gioco associato al genere
        prolog_fact = f"genre({name}, {genre}).\n"  #Scrivo i fact nella forma: genre(name, genre) indicando che il gioco "name" appartiene al genere "genre"
        prolog_file.write(prolog_fact)  #Scrivo nel file prolog il fact

        prolog_fact = f"giochi_pegi({name}, {genre}, {pegi}).\n"
        prolog_file.write(prolog_fact)

        prolog_fact = f"val_publisher({publisher}, {rating}).\n"
        prolog_file.write(prolog_fact)

        prolog_fact = f"genre_publisher({genre}, {publisher}).\n"
        prolog_file.write(prolog_fact)

        prolog_fact = f"name_publisher_val({name}, {publisher}, {rating}).\n"
        prolog_file.write(prolog_fact)

rules = """
% Predicato per contare il numero di elementi in una lista
count_elements([], 0).
count_elements([_|Tail], Count) :-
    count_elements(Tail, TailCount),
    Count is 1 + TailCount.

% Predicato per calcolare la somma degli elementi di una lista
sum_list([], 0).
sum_list([Head|Tail], Sum) :-
    sum_list(Tail, TailSum),
    Sum is Head + TailSum.

% Predicato per calcolare la media di una lista di numeri
average([], 0).
average(List, Average) :-
    sum_list(List, Sum),
    count_elements(List, Count),
    Count > 0, % Evita la divisione per zero
    Average is Sum / Count.

% Predicato per trovare il publisher con più giochi di un genere specifico
publisher_with_most_games_of_genre(Genre, Publisher) :-
    findall(P, genre_publisher(Genre, P), Publishers),
    list_max_occurrences(Publishers, Publisher, _).

% Predicato per trovare il valore massimo e il numero di occorrenze in una lista
list_max_occurrences(List, Max, Occurrences) :-
    msort(List, Sorted), % Ordina la lista
    pack(Sorted, Packed), % Raggruppa gli elementi consecutivi
    find_max_occurrences(Packed, Max, Occurrences). % Trova il valore massimo e le occorrenze

% Predicato per raggruppare gli elementi consecutivi di una lista
pack([], []).
pack([X|Xs], [[X|Packed]|Rest]) :-
    transfer(X, Xs, Ys, Packed),
    pack(Ys, Rest).

% Predicato per trasferire gli elementi uguali consecutivi dalla lista di input
transfer(_, [], [], []).
transfer(X, [Y|Ys], [Y|Ys], []) :- X \\= Y.
transfer(X, [X|Xs], Ys, [X|Packed]) :- transfer(X, Xs, Ys, Packed).

% Predicato per trovare il valore massimo e il numero di occorrenze in una lista
find_max_occurrences([], _, 0).
find_max_occurrences([L|Ls], Max, Occurrences) :-
    length(L, Len),
    find_max_occurrences(Ls, Max1, Occurrences1),
    (Len > Occurrences1 -> Max = L, Occurrences = Len; Max = Max1, Occurrences = Occurrences1).

% Predicato per trovare il gioco di un publisher con il rating più alto
highest_rated_game(Publisher, Game) :-
    name_publisher_val(Game, Publisher, Rating),
    \\+ (name_publisher_val(OtherGame, Publisher, OtherRating), OtherRating > Rating, Game \\= OtherGame).

% Predicato booleano per determinare se age >= pegi e determinare se una persona può giocare ad un gioco 
is_age_appropriate(Age, Pegi) :-
    Age >= Pegi.
"""

with open("./Code/KB.pl", "a") as prolog_file:
    prolog_file.write(rules)

prolog_file.close()

prolog = Prolog()
prolog.consult("./Code/KB.pl")

esegui = True
while (esegui):
    t.sleep(2) # Attende 'n' secondi prima di proseguire con gli output per permettere all'utente di leggere la risposta del sistema
    print("1: Chiede in input genere e classificazione d'età e da in output la lista dei giochi di quel genere con quel pegi")
    print("2: Chiede in input un genere e stampa quanti giochi di quel genere ci sono")
    print("3: Chiede in input un genere e stampa i titoli dei giochi di quel genere")
    print("4: Chiede in input un publisher e restituisce la media dei rating dei suoi giochi")
    print("5: Chiede in input un genere e restituisce il publisher con più giochi di quel genere")
    print("6: Chiede in input un publisher e restituisce il gioco di quel publisher con il rating più alto")
    print("7: Chiede in input nome gioco ed età di una persona e restituisce true se può giocarlo, false altrimenti")
    print("8: Uscita\n")

    scelta = input("Quale query vuoi eseguire?")

    if scelta == '1':
        #Query 1: Chiede in input genere e classificazione d'età e da in output la lista dei giochi di quel genere con quel pegi
        print("Query 1: Chiede in input genere e classificazione d'età e da in output la lista dei giochi di quel genere con quel pegi\n")

        genre = input("Inserisci il genere che vuoi cercare: ").lower()
        genre_format = search_format(genre)

        pegi = input("Inserisci la classificazione PEGI (Esempio: +3): ").lower()
        pegi_format = search_format_classification(pegi)

        if pegi_format == None:         #Controllo per evitare valore "None" pegi_format che causa errori
            pegi_format = -1

        query = list(prolog.query(f"giochi_pegi(X, {genre_format}, {pegi_format})."))   #Esegue la query
        print(f"\nGiochi con pegi {pegi}:")
        print_query_format(query)                                                       #Stampa il risultato della query

    elif scelta == '2':
        #Query 2: Chiede in input un genere e stampa quanti giochi di quel genere ci sono
        print("Query 2: Chiede in input un genere e stampa quanti giochi di quel genere ci sono\n")

        genre = input("Inserisci il genere che vuoi cercare: ").lower()
        genre_format = search_format(genre)

        lista_ris = list(prolog.query(f"genre(X, {genre_format})."))

        for val in prolog.query(f"count_elements({lista_ris}, Count)"):
            count_result = val["Count"]

        print(f"Ci sono {count_result} giochi del genere {genre}")

    elif scelta == '3':
        #Query 3: Chiede in input un genere e stampa i titoli dei giochi di quel genere
        print("Query 3: Chiede in input un genere e stampa i titoli dei giochi di quel genere\n")

        genre = input("Inserisci il genere che vuoi cercare: ").lower()
        genre_format = search_format(genre)

        query = list(prolog.query(f"genre(X, {genre_format})."))

        print_query_format(query)

    elif scelta == '4':
        #Query 4: Chiede in input un publisher e restituisce la media dei rating dei suoi giochi
        print("Query 4: Chiede in input un publisher e restituisce la media dei rating dei suoi giochi\n")

        publisher = input("Inserisci il publisher che vuoi cercare: ").lower()
        publisher_format = search_format(publisher)

        vett = list(prolog.query(f"val_publisher({publisher_format}, X)."))
        lista_ris = []
        for key in vett:       
            lista_ris.append(key["X"])

        for soln in prolog.query(f"average({lista_ris}, Average)"):
            average_result = soln["Average"]
        print(f"La media dei rating del publisher {publisher} è: {average_result}\n")

    elif scelta == '5':
        #Query 5: Chiede in input un genere e restituisce il publisher con più giochi di quel genere
        print("Query 5: Chiede in input un genere e restituisce il publisher con più giochi di quel genere\n")

        genre = input("Inserisci il genere che vuoi cercare: ").lower()
        genre_format = search_format(genre)

        result = next(prolog.query(f"publisher_with_most_games_of_genre({genre_format}, Publisher)"))

        # Stampa del risultato
        if result and genre_format in genre_dic.values():
            publisher = result["Publisher"][0]
            publisher = [key for key, val in publishers_dic.items() if val == publisher]
            print(f"Il publisher con più giochi del genere {genre} è: {publisher}")
        else:
            print(f"Nessun publisher trovato per il genere {genre}")

    elif scelta == '6':
        #Query 6: Chiede in input un publisher e restituisce il gioco di quel publisher con il rating più alto
        print("Query 6: Chiede in input un publisher e restituisce il gioco di quel publisher con il rating più alto\n")

        publisher = input("Inserisci il publisher che vuoi cercare: ").lower()
        publisher_format = search_format(publisher)

        lista = (list(prolog.query(f"highest_rated_game({publisher_format}, X)")))

        if lista != []:
            print(f"I giochi con il rating più alto del publisher {publisher} sono:")

        print_query_format(lista)

    elif scelta == '7':
        #Query 7: Chiede in input nome gioco ed età di una persona e restituisce true se può giocarlo, false altrimenti
        print("Query 7: Chiede in input nome gioco ed età di una persona e restituisce true se può giocarlo, false altrimenti\n")

        # input nome gioco
        name = input("Inserisci il nome del gioco che vuoi cercare: ").lower()
        name_format = search_format(name)

        # input età
        age = int(input("Inserisci la tua età in formato numerico: "))

        # Ottenimento del pegi dal gioco e conversione in numero per il confronto con l'età
        lista = list(prolog.query(f"giochi_pegi({name_format}, _, Pegi)."))
        pegi_format = lista[0]["Pegi"] # Indice del pegi
        pegi_str = [key for key, val in classification_dictionary.items() if val == pegi_format][0] # Valore del pegi
        pegi = int(pegi_str[1:]) # Pegi Convertito in numero

        flag = list(prolog.query(f"is_age_appropriate({age}, {pegi})."))

        if flag:
            print(f"L'età {age} è adatta per il gioco {name} con pegi {pegi_str}.")
        else:
            print(f"L'età {age} non è adatta per il gioco {name} con pegi {pegi_str}.")

    elif scelta == '8':
        esegui = False
        print("Grazie per aver usato il programma.")
    else: 
        print("Valore non valido! Inserire un numero compreso tra 1 e 8")
