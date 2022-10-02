import re
import pandas as pd

def lowercase(text):
    new_text = text.lower()
    return new_text


def remove_unnecessary_char(text):
    text = re.sub(r'\\n',' ', text)
    text = re.sub('rt','', text)
    text = re.sub('user','', text)
    text = re.sub('url','', text)
    text = re.sub(';','', text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)
    text = re.sub('  +',' ', text)
    text = re.sub('\d+\.\s',' ', text)
    text = re.sub(r'x[a-z0-9][a-z0-9]','',text)
    return text


def remove_nonaplhanumeric(text):
    text = re.sub(r'[^0-9a-zA-Z\?!,.]+', ' ', text)
    text = re.sub('"','', text)
    text = re.sub('\s\s+' , ' ', text)
    text = re.sub('^\s','', text)
    return text


def remove_duplicateexclamation(text):
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[\?]{2,}', '?', text)
    text = re.sub(r'(! ){2,}', '!', text)
    text = re.sub(r'(\? ){2,}', '?', text)
    text = re.sub(r',{2,}', ',', text)
    text = re.sub(r'\.{2,}', ',', text)
    return text


 
def normalize_alay(text):
    kamus_alay = pd.read_csv('source/kamusalay.csv')
    alay_dict_map = dict(zip(kamus_alay['alay'], kamus_alay['arti']))
    for word in alay_dict_map:
        normalized_word = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])
        return normalized_word



def process_word(text):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_nonaplhanumeric(text)
    text = remove_duplicateexclamation(text)
    text = normalize_alay(text)
    return text




# text = 'USER USER USER USER BANCI KALENG" MAL"U GA BISA JAWAB PERTANYAAN KAMI DARI 2 HARI LALU.... NYUNGSEP KOE USER URL'
# print(process_word(text))

# list_text = ['"saya adl abid"', 'u suka *((*(*makan', 'kata mamah : "kamuh hebat"']
# clean_list =[]
# for text in list_text:
#     # print(text)
#     text = process_word(text)
#     # print(text)
#     clean_list.append(text)
# print(clean_list)

# df = pd.DataFrame(list_text)
# df


# first_column = df.iloc[:,0]

# cleaned_list = []
# for text in first_column:
#     print(text)
#     text = process_word(text)
#     print(text)
#     cleaned_list.append(text)

# print(cleaned_list)