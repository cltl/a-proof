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

# load arguments
#arguments = docopt(__doc__)
#print()
#print('PROVIDED ARGUMENTS')
#print(arguments)
#print()

#settings = json.load(open(arguments['--config_path']))
nlp = spacy.load('nl_core_news_sm' )

# process and convert
#for csv_path in 'Data 2020/Notities AMC.csv':
 #   print(csv_path)
 #   basename = os.path.basename(csv_path)
df = pd.read_csv('Data 2020/Covid_notities_AMC.csv', sep = ';')#, error_bad_lines=False)
   # print(f'loaded {csv_path} containing {len(df)} rows.')
   
#print(df)

for index, row in df.iterrows():

    if int(index) >= 10000:
        break

    basename = row[2]
    text = row[5]

    if type(text) != str:
        continue

    if len(text) >= 10000:
        continue


    text_to_conll(text=text,
                    nlp=nlp,
                    delimiter=" ",
                    output_dir="Output_AMC",
                    basename=f'{'AMC'}--{basename}---{index+1}.conll',
                    spacy_attrs=["text", "ent_type_"],
                    exclude=["is_space"],
                    default_values={"ent_type_" : "O"},
                    start_with_index= False,
                    verbose=1)
