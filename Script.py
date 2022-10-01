#Importing libraries
import re
<<<<<<< HEAD
import pandas as pd


#Func for lowering text
def lowercase(text):
    new_text = text.lower()
    return new_text


#Func for remove unnecessary_char
def remove_unnecessary_char(text):
    text = re.sub(r'\\n',' ', text)
    text = re.sub('rt','', text)
    text = re.sub('user','', text)
    text = re.sub(';','', text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)
    text = re.sub('  +',' ', text)
    text = re.sub('\d+\.\s',' ', text)
    text = re.sub(r"x[a-z0-9][a-z0-9]",'',text)
    return text


#Func for remove nonalphanumeric
def remove_nonaplhanumeric(text):
    text = re.sub(r'[^0-9a-zA-Z\?!]+', ' ', text)
    text = re.sub("\s\s+" , " ", text)
    text = re.sub('^\s','', text)
    return text


#Func for remove duplicate exclamation mark
def remove_duplicateexclamation(text):
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    text = re.sub(r'(! ){2,}', '?', text)
    text = re.sub(r'(? ){2,}', '?', text)
    return text


#Func to normalize "alay" word to formal word
kamus_alay = pd.read_csv('Source/kamusalay.csv')
alay_dict_map = dict(zip(kamus_alay['alay'], kamus_alay['arti'])) 
def normalize_alay(text):
    for word in alay_dict_map:
        normalized_word = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])
        return normalized_word


#Final function
def process_word(text):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_nonaplhanumeric(text)
    text = remove_duplicateexclamation(text)
    text = normalize_alay(text)
    return text
=======
>>>>>>> parent of bf7a170 (Merge pull request #3 from muhammadabidd/Making-Regex-Function)
