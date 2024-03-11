from sklearn import preprocessing
from classification_function import *
from dizionario import *

giochi = pd.DataFrame()

data = pd.read_csv('./Dataset/dataset_dizionario.csv')

#data = data.iloc[:, [0, 1, 2, 3, 5, 6]]

giochi = data.copy()

giochi = clean_dataframe(giochi)
giochi = giochi[giochi['Classification'] != "+9"]
giochi.apply(lambda row: creation_frequency_dictionary(row, dictionary_frequency_classification, "Classification"), axis=1)
giochi["Classification_format"] = giochi.apply(lambda row: set_columns_giochi(row, dictionary_frequency_classification, "Classification"), axis = 1)

giochi.sort_values(["Classification_format"], ascending=True, inplace=True)

#Format name
giochi.apply(lambda row: creation_frequency_dictionary(row, names_dictionary, "Name"), axis=1)

#Format publisher
giochi.apply(lambda row: creation_frequency_dictionary(row, publishers_dictionary, "Publisher"), axis=1)

#Format platform
giochi.apply(lambda row: creation_frequency_dictionary(row, platforms_dictionary, "Platform"), axis=1)

#Format type
giochi.apply(lambda row: creation_frequency_dictionary(row, genres_dictionary, "Genre"), axis=1)

# Applica il metodo "conversion_string" su giochi
giochi.apply(
    lambda column: conversion_string(giochi["Name"], giochi["Genre"], giochi["Publisher"], giochi["Platform"], giochi['Year']), axis=0)

conversionDataset = pd.DataFrame()

conversionDataset["Chiave"] = conversion_dictionary.keys()
conversionDataset["Valore"] = conversion_dictionary.values()

conversionDataset.to_csv("./Dataset/dizionario.csv", index=False)


#from categorical to numeric
giochi["Name"] = giochi.apply(lambda row: convert_by_column(row, "Name"), axis=1)

giochi["Publisher"] = giochi.apply(lambda row: convert_by_column(row, "Publisher"), axis=1)

giochi["Platform"] = giochi.apply(lambda row: convert_by_column(row, "Platform"), axis=1)

giochi["Genre"] = giochi.apply(lambda row: convert_by_column(row, "Genre"), axis=1)

giochi["Year"] = giochi.apply(lambda row: convert_by_column(row, "Year"), axis=1)

giochi["Classification"] = giochi.apply(lambda row: convert_by_classification(row, "Classification"), axis=1)

giochi = giochi.astype("int")

giochi.to_csv("./Dataset/giochi_preprocessato.csv", index=False)
giochi = giochi.drop(columns=["Classification_format"])

#Begin classification

target = giochi["Classification"]
training = giochi.drop(columns=["Classification"])

scaler = preprocessing.StandardScaler()
scaled_df = scaler.fit_transform(training)
training = pd.DataFrame(scaled_df)

print("\nKNN:")
knn = knn_classification(training, target)

print("\nGaussian Naive Bayes:")
gau = gaussian_nb_classification(training, target)

print("\nRandom Forest:")
rf = random_forest_classification(training, target)

#End classification