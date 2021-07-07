# %%
import re
import unidecode

"""Pre-taggin"""
def prep(text):
    prep_text = str(text)
    prep_text = re.sub(r"&", "&amp;", prep_text)
    prep_text = re.sub(r"<", "&lt;", prep_text)
    prep_text = re.sub(r">", "&gt;", prep_text)
    return prep_text

# %%
"""Adding main tag"""
def addmainTag(text):
    tag = str(re.findall(r"&lt;CorIFA.*?&gt;", text))
    tag = re.sub("\['&lt;", "", tag)
    tag = re.sub("&gt;'\]", "", tag)
    tag_corpus, tag_uni, tag_level, tag_type, tag_ed, tag_gen, tag_year, tag_sem, tag_id, tag_stu = re.split("-|\.", tag)
    tag = str('<text id="'+tag_id +'" corpus="'+tag_corpus+'" uni="'+tag_uni+'" level="'+tag_level+'" type="'+tag_type+'" edit="'+tag_ed+'" genre="'+tag_gen+'" year="'+tag_year+'" sem="'+tag_sem+'" student="'+tag_stu+'">')
    text = re.sub(r"&lt;CorIFA.*?&gt;", tag, text)

    text = text + "</text>"

    return text


# %%
"""Removes self reference to the genre"""

def tagSelfRef(text):
    if re.findall(r'genre="Abs"',text):
        if re.findall(r'\nabstract', text, flags=re.IGNORECASE):
            text = re.sub(r'\n(abstract)',r'<selfref>\1</selfref>', text, flags=re.IGNORECASE)

    if re.findall(r'genre="SoP"',text):
       if re.findall(r'\nstatement of purpose|\nsop', text, flags=re.IGNORECASE):
           text = re.sub(r'\n(statement of purpose|\nsop)',r'<selfref>\1</selfref>', text, flags=re.IGNORECASE)
    
    if re.findall(r'genre="AEss"',text):
        if re.findall(r'\nessay|\nargumentative essay', text, flags=re.IGNORECASE):
            text = re.sub(r'(\nessay|\nargumentative essay)',r'<selfref>\1</selfref>', text, flags=re.IGNORECASE)

    if re.findall(r'genre="LiR"',text):
        if re.findall(r'\nliterature review', text, flags=re.IGNORECASE):
            text = re.sub(r'\n(literature review)',r'<selfref>\1</selfref>', text, flags=re.IGNORECASE)

    if re.findall(r'genre="ReA"',text):
        if re.findall(r'\nresearch article', text, flags=re.IGNORECASE):
            text = re.sub(r'\n(research article)',r'<selfref>\1</selfref>', text, flags=re.IGNORECASE)

    
    return text


# %%
"""Tag canonical sections of an academic text"""
def tagCan(text):
    if re.findall(r"(introduction|methods?|methodology|results and discussion|results &amp; discussion|results|discussion|conclusions?|references?|bibliography|keywords?)(?=(\n| \n|:| :))", text, flags=re.IGNORECASE):
        text = re.sub(r"(introduction|methods?|methodology|results and discussion|results &amp; discussion|results|discussion|conclusions?|references?|bibliography|keywords?)(?=(\n| \n|:| :))", r'<sec type="\1">\1</sec>', text, flags=re.IGNORECASE)

    return text

# %%
"""Tagging quotes"""
#It considers a quote anything that has over 5 words between angular quotes. 
def tagQuot(text):
    text = re.sub(r'(“)(?=[^”]+ [^”]+ [^”]+ [^”]+ [^”]+ )', r'<quote>\1', text)
    
    text = re.sub(r'[^“|\s]+ [^“|\s]+ [^“|\s]+ [^“|\s]+ [^“|\s]+(”)', r'\1</quote>', text)

    return text
# %%
"""Tagging accented words"""

def tagFor(text):
    text = re.sub(r'(\w*[\u00C0-\u01DA]\w*)', r'<foreign orig="\1">\1</foreign>', text)

    for i in re.findall(r'>\w*[\u00C0-\u01DA]\w*<', text):
        j = unidecode.unidecode(i)
        text = re.sub(i, j, text)
    
    
    return text

# %%
"""remove references"""
#Only works when the text has a section called "References"
def removeRef(text):
    if re.findall(r'((references?|bibliography)</sec>)',text, flags=re.IGNORECASE):
        text = re.sub(r'(references?</sec>|bibliography</sec>).*</text>', r'\1 </text>', text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    return text

