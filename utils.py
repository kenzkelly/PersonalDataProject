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

df = pd.read_json('post_comments.json')
df = make_temp(df)
df = make_full_temp(df)
df = make_dataframe(df)
print(df)

tmp = df['string_map_data']
keys = get_keys(tmp)
keys = keys[0]
comment = [] 
creation = []
media_owner = []
i = 0 
while i < len(tmp):
    j = 0 
    while j < len(keys):
        if keys[j] == "Comment":
            comment.append(tmp[i][keys[j]]['value'])
        elif keys[j] == "Comment creation time": 
            creation.append(tmp[i][keys[j]]['timestamp'])
        elif keys[j] == 'Media owner':
            media_owner.append(tmp[i][keys[j]]['value'])
        else: 
             print(1)
        j += 1
    i += 1

df['Comment'] = comment 
df['Timestamp'] = creation 
df['Media Owner'] = media_owner

print(df)

del df['media_map_data']
del df['string_map_data']

df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit = 's')

year = []
time = []

for row in df['Timestamp']:
    year.append(str(row)[:4])
    thing = str(row)[11:].split(':')
    time.append(thing[0] + thing[1] + thing[2])


df['year'] = year 
df['time'] = time
del df['Timestamp']
del df['Media Owner']

print(df)
df.to_csv('post_comments_instagram.csv')