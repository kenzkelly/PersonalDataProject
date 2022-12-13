import numpy as np
import pandas as pd
import json


#first round of abstraction -- goes through each row and appends the series' to a list
def make_temp(df): 
    tmp_list = [] 

    i = 0 
    while i < len(df): 
        tmp_list.append(df.iloc[i].tolist()[0])
        i += 1
    return tmp_list

def get_keys(list): 
    all_keys = []

    for item in list:
        all_keys.append([*item])
    return all_keys 

def make_full_temp(list_og):
    keys = get_keys(list_og)
    new_list = [] 

    i = 0 
    while i < len(keys):
        to_add = {}
        for item in list_og[i]:
            if isinstance((list_og[i][item]), list) == False:
                to_add[item] = list_og[i][item]
            else: 
                for dict in list_og[i][item]:
                    j = 0 
                    while j < len(dict):
                        to_add[[*dict][j]] = [*dict.values()][j]
                        j += 1
        new_list.append(to_add)
        i += 1
    return new_list

def make_dataframe(list):
    keys = [*list[0]]
    final_dict = {}
    for key in keys: 
        final_dict[key] = []
    for dictionary in list: 
        for key in keys: 
            final_dict[key].append(dictionary[key])
    df = pd.DataFrame(final_dict)
    return df

df2 = pd.read_csv('post_comments_instagram.csv')
df2['type'] = 'comment'
del df2['Unnamed: 0']
del df2['Comment']
print(df2)
df2.to_csv("post_comments_instagram.csv")