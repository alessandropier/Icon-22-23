import pandas as pd

conversion_dictionary = {} # Dizionario da cui si ricava la tabella

publishers_dictionary = {}
platforms_dictionary = {}
ratings_dictionary = {}
names_dictionary = {}
genres_dictionary = {}
years_dictionary = {}

dictionary_classification_format = {}
dictionary_frequency_classification = {}
classification_dictionary = {'+3': 0, '+7': 1, '+12': 2, '+16': 3, '+18': 4}

def conversion_string(column_names, column_genres, column_publishers, column_platforms, column_years):
    i = 0
    for genres in column_genres:
        if genres not in conversion_dictionary:
            conversion_dictionary[genres] = i
            i = i + 1
    conversion_dictionary["fine_genres"] = -1
    i = 0
    for names in column_names:
        if names not in conversion_dictionary:
            conversion_dictionary[names] = i
            i = i + 1
    conversion_dictionary["fine_names"] = -1
    i = 0
    for publishers in column_publishers:
        if publishers not in conversion_dictionary:
            conversion_dictionary[publishers] = i
            i = i + 1
    conversion_dictionary["fine_publishers"] = -1
    i = 0
    for platforms in column_platforms:
        if platforms not in conversion_dictionary:
            conversion_dictionary[platforms] = i
            i = i + 1
    conversion_dictionary["fine_platforms"] = -1
    i = 0
    for years in column_years:
        if years not in conversion_dictionary:
            conversion_dictionary[years] = i
            i = i + 1
    conversion_dictionary["fine_years"] = -1
    
def clean_dataframe(dataset):
    dataset = dataset[dataset['Classification'].apply(lambda x: x != 'unknown')]
    dataset = dataset[dataset['Publisher'].apply(lambda x: x != 'unknown')]
    dataset.reset_index(drop = True)
    dataset["Genre"] = dataset["Genre"].replace("unknown", 'indie')
    dataset["Genre"] = dataset["Genre"].replace("others", 'indie')
    return dataset

# Metodo per trasformare i dati categorici in dati numerici
def convert_by_column(row, column_name):
    if row[column_name] in conversion_dictionary:
        element = row[column_name]
        row[column_name] = conversion_dictionary[element]
    return row[column_name]

# Metodo per trasformare i dati categorici in dati numerici
def convert_by_classification(row, column_name):
    if row[column_name] in classification_dictionary:
        element = row[column_name]
        row[column_name] = classification_dictionary[element]
    return row[column_name]

def creation_frequency_dictionary(row, dictionary, column_name):
    list_ = str(row[column_name]).split(', ')
    for element in list_:
        if element not in dictionary:
            dictionary[element] = 1
        else:
            dictionary[element] = dictionary[element] + 1

def set_columns_giochi(row, dictionary, column_name):
    list_ = str(row[column_name]).split(', ')
    classification_frequency = 0
    final_genre = ''
    for name in list_:
        if dictionary[name] > classification_frequency:
            classification_frequency = dictionary[name]
            final_genre = name
    row[column_name] = final_genre
    return row[column_name]
