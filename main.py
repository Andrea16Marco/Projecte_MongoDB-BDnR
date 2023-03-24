from pymongo import MongoClient
import pandas as pd
import ast

conn = MongoClient('localhost', 27017)

conn.drop_database('tenda')
db = conn['tenda']

data = pd.read_excel('Dades.xlsx', sheet_name=None)

def string_to_list(string):
    if isinstance(string, str) and string.startswith('['):
        string = string.replace('[', "['").replace(']', "']")
        string = string.replace(', ', "', '")
        string = tuple(ast.literal_eval(string))

    return string


data['Colleccions-Publicacions'] = data['Colleccions-Publicacions'].applymap(string_to_list)


data['Editorials'] = data['Colleccions-Publicacions'].iloc[:, :4]
data['Colleccions'] = data['Colleccions-Publicacions'].iloc[:, 4:11]
data['Publicacions'] = data['Colleccions-Publicacions'].iloc[:, 11:]


del data['Colleccions-Publicacions']

for coll_name, coll_df in data.items():
    coll = db.create_collection(coll_name)
    coll_dict = coll_df.drop_duplicates().to_dict('records')
    coll.insert_many(coll_dict)

conn.close()
