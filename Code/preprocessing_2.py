#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


dataset = pd.read_csv("./Dataset/dataset.csv")


# In[3]:


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# In[4]:


dataset


# In[6]:


dataset = dataset[["Name", "Platform", "RatingOutOf20", "Publisher", "Year", "Classification", "Description", "Genre"]]


# In[7]:


dataset.head()


# In[8]:


import ast
dataset["Description"] = dataset["Description"].apply(lambda x:x.split())


# In[9]:


dataset.head()


# In[10]:


dataset["Publisher"] = dataset["Publisher"].apply(lambda x:x.split())


# In[13]:


for i in range(0, 4059):
    dataset.Year[i] = str(dataset.Year[i])


# In[14]:


for i in range(0, 4059):
    dataset.Year[i] = dataset.Year[i].replace(".0", "")


# In[15]:


dataset.head()


# In[16]:


for i in range(0, 4059):
    dataset.Classification[i] = dataset.Classification[i].replace(" ans", "")


# In[17]:


dataset


# In[18]:


for i in range(0, 4059):
    dataset.RatingOutOf20[i] = dataset.RatingOutOf20[i].replace("/20", "")


# In[19]:


dataset.head()


# In[20]:


dataset["Genre"] = dataset["Genre"].apply(lambda x:x.split())


# In[24]:


dataset["Tags"] = dataset["Description"] + dataset["Genre"] + dataset["Publisher"]


# In[25]:


dataset.to_csv('dataset_nuovo.csv', index=False)


# In[26]:


new_df = dataset[["Name", "Platform", "Tags"]]


# In[27]:


new_df


# In[28]:


new_df["Tags"] = new_df["Tags"].apply(lambda x: " ".join(x))


# In[29]:


new_df["Tags"] = new_df["Tags"].apply(lambda X:X.lower())


# In[30]:


new_df.to_csv('dataset_recom.csv', index=False)

dataset["Publisher"] = dataset["Publisher"].apply(lambda x: " ".join(x))
dataset["Genre"] = dataset["Genre"].apply(lambda x: " ".join(x))

dataset_dizionario = dataset[["Name", "Platform", "RatingOutOf20", "Publisher", "Year", "Classification", "Genre"]]
dataset_dizionario.to_csv("dataset_dizionario.csv", index = False)