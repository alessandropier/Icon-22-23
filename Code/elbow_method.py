import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

cluster_dataset = pd.read_csv("./Dataset/giochi_preprocessato.csv")

wcss = []

for i in range(1, 10):
    kmeansOut = KMeans(n_clusters=i, init="k-means++", max_iter=300, n_init=10, random_state=0)
    kmeansOut.fit(cluster_dataset)
    wcss.append(kmeansOut.inertia_)

plt.plot(range(1, 10), wcss, 'bx-')

plt.title('The elbow method')

plt.xlabel('Number of clusters')

plt.xticks(range(1,10))

plt.ylabel('WCSS')  # within cluster sum of squares

plt.grid(True)

plt.show()