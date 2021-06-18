# %%
import pandas as pd
import re

"""Anonymization""" 

def anon(serie, text):
    names = serie
    for name in names:
        if re.findall(name, text):
            text = re.sub(name, "<anon/>", text)
    
    return text

