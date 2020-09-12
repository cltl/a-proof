"""
This is an adaptation of Marten Postma's convert_text_to_conll.py script in his Keyword Matcher module (github.com/cltl/KeywordMatcher)

Before you start:
    # install spacy in python3
    # install docopt
    # run in terminal:
        # python3 -m spacy download "nl_core_news_sm" 
    # clone Marten's TextToConll git:
        #in terminal:
        # cd lib
        # git clone https://github.com/cltl/TextToConll
        # cd TextToConll
        # pip install -r requirements.txt
        

"""
from docopt import docopt
import json
import os

import pandas as pd
import spacy


from TextToCoNLL import text_to_conll


nlp = spacy.load('nl_core_news_sm' )

#load df
df = pd.read_csv('Data 2020/Covid_notities_VUmc_2020_q3q4_Search3.csv', sep = ';')

#iterate through df and selecr text and doc name info from rows
for index, row in df.iterrows():

    if int(index) >= 10000:
        break
    
    text = row[5]

    basename = str(row[0])+'--'+str(row[1])+'--'+str(row[2])+'--'+str(row[4])

    if type(text) != str:
        continue

    if len(text) >= 10000:
        continue

#convert to conll
#change output_dir per half year and per search
    text_to_conll(text=text,
                    nlp=nlp,
                    delimiter=" ",
                    output_dir="Output_VUmc_q3q4__Search3",
                    basename=f'{"VUmc"}--{basename}--{"q3q4"}--{"Search3"}.conll',
                    spacy_attrs=["text", "ent_type_"],
                    exclude=["is_space"],
                    default_values={"ent_type_" : "O"},
                    start_with_index= False,
                    verbose=1)
