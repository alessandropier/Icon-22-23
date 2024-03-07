from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from math import *
from prediction import *

def reformat_name(row, name):
    for key in name_dic:
        if name_dic[key] == row[name]:
            row[name] = key
            return row[name]

def reformat_platform(conversion, platforms):
    k = 0
    l = platforms
    for p in platforms:
        l[k] = conversion.loc[conversion['Chiave'] == p, 'Valore'].item()
        k = k+1
    return l

def similarity_with_cosine(row_a, row_b):
    element = cosine_similarity([row_a], [row_b])
    row_a["similarity"] = element[0][0]
    return row_a["similarity"]

def set_recommender(name, platform, publisher, rating, type, year, classification, platforms):
    cluster_dataset = pd.read_csv("./Dataset/giochi_preprocessato.csv")
    conversion = pd.read_csv("./Dataset/dizionario.csv")
    cluster_dataset = cluster_dataset.drop(columns=["Classification_format"])

    conversion.apply(lambda row: set_dictionary(row), axis = 1)

    row_user = []
    
    if name == "":
        cluster_dataset = cluster_dataset.drop(columns=["Name"])
    else:    
        row_user.append(float(search_format(name)))

    row_user.append(float(search_format(platform)))

    row_user.append(float(rating))

    if publisher == "":
        cluster_dataset = cluster_dataset.drop(columns=["Publisher"])
    else:    
        row_user.append(float(search_format(publisher)))

    if year == "":
        cluster_dataset = cluster_dataset.drop(columns=["Year"])
    else:    
        row_user.append(float(search_format(year)))

    if classification == "":
        cluster_dataset = cluster_dataset.drop(columns="Classification")
    else:
        row_user.append(float(search_format_classification(classification)))

    if type == "":
        cluster_dataset = cluster_dataset.drop(columns=["Type"])
    else:    
        row_user.append(float(search_format(type)))

    row_user_normalized = preprocessing.normalize([row_user])

    #Clustering
    kmeans = KMeans(n_clusters = 3).fit(preprocessing.normalize(cluster_dataset))
    cluster_dataset["cluster"] = kmeans.labels_

    prediction = kmeans.predict(row_user_normalized)

    user_cluster = prediction[0]
    split_cluster = cluster_dataset[cluster_dataset["cluster"].apply(lambda x: x == user_cluster)]
    split_cluster = split_cluster.drop(columns=["cluster"])
    split_cluster["similarity"] = split_cluster.apply(lambda row: similarity_with_cosine(row, row_user), axis = 1)
    split_cluster.sort_values(["similarity"], ascending=False, inplace=True)

    set_name()

    ten_sim = split_cluster.head(500)
    ten_sim = ten_sim.loc[:, ["Name", "Platform", "similarity"]]
    ten_sim["Name"] = ten_sim.apply(lambda row: reformat_name(row, "Name"), axis=1)
    platforms = reformat_platform(conversion, platforms)
    platforms.append('-2')
    print("I giochi suggeriti in base alle tue preferenze sono: \n")
    i = 0
    j = 0
    ten_sim_output = []
    while i < 10:
        if j < len(ten_sim.index):
            if (ten_sim["Platform"].iloc[j] in platforms):
                if ten_sim["Name"].iloc[j] not in ten_sim_output:
                    ten_sim_output.append(ten_sim["Name"].iloc[j])
                    print(f"{i+1}) {ten_sim_output[i]}")
                    i = i+1
        if j == len(ten_sim.index):
            split_cluster = split_cluster.loc[:, ["Name", "Platform", "similarity"]]
            split_cluster["Name"] = split_cluster.apply(lambda row: reformat_name(row, "Name"), axis=1)

        if j >= len(ten_sim.index):
            if (split_cluster["Platform"].iloc[j] in platforms):
                if split_cluster["Name"].iloc[j] not in ten_sim_output:
                    ten_sim_output.append(split_cluster["Name"].iloc[j])
                    print(f"{i+1}) {ten_sim_output[i]}")
                    i = i+1
        j=j+1
