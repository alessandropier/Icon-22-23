#!/usr/bin/env python
# coding: utf-8

# In[33]:


import numpy as np
import pandas as pd
from deep_translator import GoogleTranslator


# In[34]:


jvc = pd.read_csv("../Dataset/jvc.csv")
vgsales = pd.read_csv("../Dataset/vgsales.csv")


# In[35]:


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# In[36]:


jvc.rename(columns={"game_en": "Name", "platform": "Platform"}, inplace=True)


# In[37]:


jvc = jvc.merge(vgsales, on=["Name", "Platform"])


# In[38]:


jvc.shape


# In[39]:


jvc.info()


# In[40]:


jvc = jvc[["Name", "Platform", "website_rating", "Publisher", "Year", "classification", "description", "Genre"]]
jvc.rename(columns={"website_rating": "RatingOutOf20", "classification": "Classification", "description": "Description"}, inplace=True)


# In[41]:


jvc


# In[42]:


jvc.isnull().sum()


# In[43]:


jvc.dropna(inplace=True)


# In[44]:


jvc.duplicated().sum()


# In[45]:


jvc=jvc.drop_duplicates()


# In[46]:


jvc.isnull().sum()


# In[47]:


jvc.shape


# In[48]:


jvc = jvc.reset_index()


# In[49]:


for i in range(0, 4059):
    tradotto = GoogleTranslator(source="auto", target="en").translate(jvc.Description[i])
    jvc.Description[i] = tradotto


# In[50]:


jvc.head()


# In[51]:


jvc.to_csv('dataset.csv', index=False)


# In[ ]:




