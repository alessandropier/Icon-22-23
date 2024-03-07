import pandas as pd
import numpy as np
from warnings import simplefilter
from dizionario import classification_dictionary
from classification_function import random_forest_classification
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

simplefilter(action="ignore", category=FutureWarning)   #Ignora tutti i prossimi warning

name_dic = {}
conversion_dic = {}

#Predizione genere

def set_name():
    i = 0
    for key in conversion_dic:
        if key != "fine_names" and i == 1:
            name_dic[key] = conversion_dic[key]
        elif key == "fine_names":
            return
        elif key == "fine_genres":
            i = 1

def search_format(e):
    if e in conversion_dic:
        return conversion_dic[e]
    else:
        i = 0
        for name in conversion_dic:
            i = i + 1
        conversion_dic[e] = i
        return conversion_dic[e]
    
def search_format_classification(e):
    if e in classification_dictionary:
        return classification_dictionary[e]
    
def set_dictionary(row):
    conversion_dic[row["Chiave"]] = row["Valore"]


def predict_classification(name, genre, publisher, platform, rating, year):
    giochi = pd.read_csv("./Dataset/giochi_preprocessato.csv")
    conversion = pd.read_csv("./Dataset/dizionario.csv")
    giochi = giochi.drop(columns=["Classification_format"])
    conversion.apply(lambda row: set_dictionary(row), axis = 1)

    target = giochi["Classification"]
    training = giochi.drop(columns=["Classification"])  

    #Assegna indici ai valori inseriti dall'utente
    name_format = search_format(name)
    genre_format = search_format(genre)
    publisher_format = search_format(publisher)
    platform_format = search_format(platform)
    year_format = search_format(year)
    row_user = [name_format, genre_format, publisher_format, platform_format, year_format, rating]
    rf = random_forest_classification(training, target)
    classification_predict = rf.predict([row_user])
    final_val = [key for key, val in classification_dictionary.items() if val == classification_predict[0]]
    print(f"La classificazione del gioco {name} e': ", final_val[0])
