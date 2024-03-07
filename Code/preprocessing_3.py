import numpy as np
import pandas as pd

dataset = pd.read_csv("./Dataset/dataset_dizionario.csv")

dataset = dataset.apply(lambda x: x.astype(str).str.lower())

dataset.to_csv("dataset_dizionario.csv", index=False)