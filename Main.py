# %%
import glob
import pandas as pd
import re
from TextFormating import anon
from Helpers import prep, addmainTag, tagSelfRef, tagQuot, tagCan, tagFor, removeRef
# %%
"""Import and sort data"""
students_data = pd.read_excel('Data\students_data_base.xlsx', sheet_name=0)
names_collection = students_data["Name"]
names_collection = names_collection.sort_values(key= lambda x:x.str.len(), ascending=False)

#%% 
texts_path = glob.glob('Sample_Bank\Textos-CorIFA-2020-1-não-limpo\Batch_[1-9]\*.txt')

# %%

for i in texts_path:
    """open sample"""
    with open( i , "r", encoding="utf-8") as fd:
        text = fd.read()

    text = prep(text)
    text = anon(names_collection, text)
    text = addmainTag(text)
    text = tagSelfRef(text)
    text = tagCan(text)
    text = removeRef(text)
    text = tagQuot(text)
    text = tagFor(text)   

    with open(i, "w", encoding="utf-8") as fd:
         fd.write(text)


# %%
