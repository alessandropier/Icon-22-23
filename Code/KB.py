import pandas as pd
from pyswip import Prolog
from prediction import *

pegi_dic = {}
genre_dic = {}
year_dic = {}
platforms_dic = {}
publishers_dic = {}

#Carico il dataset giochi_preprocessato.csv
dataset = pd.read_csv("./Dataset/giochi_preprocessato.csv")
dataset = dataset.drop(columns=["Classification_format"])

conversion = pd.read_csv("./Dataset/dizionario.csv")    #Carico il dizionario per le conversioni
conversion.apply(lambda row: set_dictionary(row), axis = 1)     #Carico la lista conversion_dic con tutto il contenuto di dizionario.csv
set_name()      #Carico name_dic con il dizionario dei nomi

#Apri il file KB.pl in modalità scrittura
with open("./Code/KB.pl", "w") as prolog_file:
    prolog_file.write(":- discontiguous genre/2.\n")
    prolog_file.write(":- discontiguous giochi_pegi/3.\n")

    #Itera attraverso le righe del dataset
    for index, row in dataset.iterrows():
        name = row[0]
        genre = row[6]
        pegi = row[5]

        #Scrivo il fatto prolog con il gioco associato al genere
        prolog_fact = f"genre({name}, {genre}).\n"  #Scrivo i fact nella forma: genre(name, genre) indicando che il gioco "name" appartiene al genere "genre"
        prolog_file.write(prolog_fact)  #Scrivo nel file prolog il fact

        prolog_fact = f"giochi_pegi({name}, {genre}, {pegi}).\n"
        prolog_file.write(prolog_fact)

prolog = Prolog()
prolog.consult("./Code/KB.pl")

#Conversione il genere inserito dall'utente nel corrispondente indice nel dizionario
genre = input("Inserisci il genere che vuoi cercare: ").lower()
genre_format = search_format(genre)

#print(list(prolog.query(f"genre(X, {genre_format}).")))
#print(bool(prolog.query("genre(5, 5).")))

query = list(prolog.query(f"genre(X, {genre_format})."))

#Conversione e stampa da indici nel dizionario a nomi dei videogames
vett = []
for key in query:
    vett.append(key["X"])

i = 0
for key in vett:
    print([key for key, val in name_dic.items() if val == vett[i]])
    i = i + 1

#print(list(prolog.query("giochi_pegi(X, 1, 1).")))