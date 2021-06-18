# %%
import re
from numpy import unicode_ 
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
# It might generate an error if the student talks about the genre at the start of a new line.
def tagSelfRef(text):
    if re.findall(r'genre="Abs"',text):
        if re.findall(r'\n[Aa]bstract|ABSTRACT|Abs|ABS', text):
            text = re.sub(r'\n([Aa]bstract|ABSTRACT|Abs|ABS)',r'<selfref>\1</selfref>', text)

    if re.findall(r'genre="SoP"',text):
       if re.findall(r'\n[Ss]tatement [Oo]f [Pp]urpose|STATEMENT OF PURPOSE|SOP|SoP', text):
           text = re.sub(r'\n([Ss]tatement [Oo]f [Pp]urpose|STATEMENT OF PURPOSE|SOP|SoP)',r'<selfref>\1</selfref>', text)
    
    if re.findall(r'genre="AEss"',text):
        if re.findall(r'\n[Ee]ssay|ESSAY|[Aa]rgumentative [Ee]ssay|ARGUMENTATIVE ESSAY', text):
            text = re.sub(r'\n([Ee]ssay|ESSAY|[Aa]rgumentative [Ee]ssay|ARGUMENTATIVE ESSAY)',r'<selfref>\1</selfref>', text)

    if re.findall(r'genre="LiR"',text):
        if re.findall(r'\n[Ll]iterature [Rr]eview|LITERATURE REVIEW', text):
            text = re.sub(r'\n([Ll]iterature [Rr]eview|LITERATURE REVIEW)',r'<selfref>\1</selfref>', text)
    
    if re.findall(r'genre="ReA"',text):
        if re.findall(r'\n[Rr]esearch [Aa]rticle|RESEARCH ARTICLE', text):
            text = re.sub(r'\n([Rr]esearch [Aa]rticle|RESEARCH ARTICLE',r'<selfref>\1</selfref>', text)

    
    return text
# %%
"""Tag canonical sections of an academic text"""
def tagCan(text):
    if re.findall(r"[Ii]ntroduction|INTRODUCTION|[Mm]ethods?|METHODS?|[Mm]ethodology|METHODOLOGY|[Rr]Results and [Dd]iscussion|[Rr]Results &amp; [Dd]iscussion|RESULTS AND DISCUSSION|RESULTS &amp; DISCUSSION|[Rr]esults|RESULTS|[Dd]iscussion|DISCUSSION|[Cc]onclusions?|CONCLUSIONS?|[Rr]eferences?|REFERENCES?|[Kk]eywords?|KEYWORDS?(\n| \n|:)", text):
        text = re.sub(r"([Ii]ntroduction|INTRODUCTION|[Mm]ethods?|METHODS?|[Mm]ethodology|METHODOLOGY|[Rr]Results and [Dd]iscussion|[Rr]Results &amp; [Dd]iscussion|RESULTS AND DISCUSSION|RESULTS &amp; DISCUSSION|[Rr]esults|RESULTS|[Dd]iscussion|DISCUSSION|[Cc]onclusions?|CONCLUSIONS?|[Rr]eferences?|REFERENCES?|[Kk]eywords?|KEYWORDS?)(\n| \n|:| :)", r'<sec type="\1">\1</sec>', text)

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
    text = re.sub(r'(\w*[\u00C0-\u01DA]\w*)', r'<foreign>\1</foreign>', text)
    
    return text

# %%
"""remove references"""
#Only works when the text has a section called "References"
def removeRef(text):
    if re.findall(r'(([Rr]eferences?|REFERENCES?)</sec>)',text):
        text = re.sub(r'(([Rr]eferences?|REFERENCES?)</sec>)[^</text>]*(</text>)', r'\1\2', text)
    
    return text
# %%
