# %%
import re
import unidecode

"""Anonymization""" 

def anon(serie, text):
    names = serie
    for name in names:
        if re.findall(name, text, flags=re.IGNORECASE):
            text = re.sub(name, "<anon/>", text, flags=re.IGNORECASE)

        else:
            name = unidecode.unidecode(name)
            text = re.sub(name, "<anon/>", text, flags=re.IGNORECASE)

    return text


# %%
