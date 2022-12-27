import pickle
import streamlit as st
import malaya
import pandas as pd
import re
import string
bm_dict_df = pd.read_csv('BM_dict.csv')
bm_dict_df = bm_dict_df.reset_index(drop=True)
corrector = malaya.spelling_correction.probability.load()
normalizer = malaya.normalize.normalizer(corrector)
from googletrans import Translator
from cleantext import clean #to remove emoji in text
from googletrans import Translator


def lemmatization_input(userinput):
    token_raw = []
    content_filtered = []
    content_normalized1 = []
    content_normalized2 = []
    content_translated = []
    content_lemma = []
    tokenizer = malaya.tokenizer.Tokenizer()
    translator = Translator()
    corrector = malaya.spelling_correction.probability.load()
    normalizer = malaya.normalize.normalizer(corrector)
    sastrawi = malaya.stem.sastrawi()
    
    def chk_content(token_raw,content_filtered,content_normalized1,content_normalized2,content_translated,content_lemma):
        if len(token_raw) != 0:
            token_raw.clear()
            content_filtered.clear()
            content_normalized1.clear()
            content_normalized2.clear()
            content_translated.clear()
            content_lemma.clear()
    
    def append_token(token):
        for i in token:
            token_raw.append(i)
    
    chk_content(token_raw,content_filtered,content_normalized1,content_normalized2,content_translated,content_lemma)
    append_token(tokenizer.tokenize(userinput))

    for i in token_raw:
        #Covert all letters to lowercase
        i.lower()
        #Remove emoji in text
        i = clean(i, no_emoji=True)
        #Remove all @mention,newlines,hyperlink
        i = re.sub("#[A-Za-z0-9_]+|@[A-Za-z0-9_]+|\n|http\S+|\"","",i)
        #Remove all white space
        #i = i.strip()
        #Remove punctuation
        i = i.translate(str.maketrans("", "", string.punctuation))
        # print(tokenizer.tokenize(i))
        #Remove no tweet content from list
        if i == "":
            continue
        else:
            # print(tokenizer.tokenize(i))
            # token = tokenizer.tokenize(i)
            content_filtered.append(i)
    
   
    for i in content_filtered:
        if (bm_dict_df['rojak'] == i).any():
            str(content_normalized1.append(bm_dict_df[bm_dict_df['rojak'] == i]['actual'].to_string(index=False)))
        else:
            str(content_normalized1.append(i))
                                     
    for i in content_normalized1:
        content_normalized2.append(normalizer.normalize(i)["normalize"])
          
 
    for i in content_normalized2:
        translate = translator.translate(i, src='en', dest = 'id')
        content_translated.append(translate.text)
                
    for i in content_translated:
            content_lemma.append(sastrawi.stem(i))
           
    return content_lemma

def main():
    st.set_page_config(
        page_title="Lemmetizer",
        page_icon="img2.png",
        initial_sidebar_state="expanded"
    )

    # title
    st.image('img1.png', width=700)
    st.title('Lemmatization of Malay Language')

    # input
    lemma = st.text_input(label='Enter a sentence:')


    # prediction code
    if st.button('Analyze'):
        st.success(lemmatization_input(lemma))
        st.snow()
        

if __name__ == '__main__':
    main()
