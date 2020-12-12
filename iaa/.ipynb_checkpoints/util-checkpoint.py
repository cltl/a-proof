import numpy as np
import pandas as pd
import os, random, glob, json, re
from sklearn.metrics import cohen_kappa_score


def get_token_ids (df):
    tokens=[]
    for token in df['sen_id-tok_id']:
        tokens.append(token)
    return tokens

def clean_value (annotation):
    if type(annotation)!=str:
        clean="_"
    else:
        clean = annotation
    ind = clean.find('[')
    if ind>0:
        clean=clean[:ind]
    return clean

def clean_df(df):
    for index, label in enumerate(df['annotation']):
        value = clean_value(label)
        df['annotation'].iloc[index]=value
    print('Length:', len(get_token_ids(df)))
    return df
 
def get_token_anno (df):
    labels=[]
    for index, token in enumerate(df['sen_id-tok_id']):
        label=df['annotation'].iloc[index]
        labels.append(label)
    return labels

def get_sentence_anno (sentence_dict):
    annos=[]
    for key, value in sentence_dict.items():
        #print(key, '->', value)
        minus = value.count("_")
        if minus==len(value):
            annos.append("_")
        else:
            for item in value:
                if item!="_":
                    annos.append(item)
                    print(item)
                    break
            ### we take the first value that is not "_"
    return annos    


def get_sentence_set_anno_dict (sentence_dict):
    annos={}
    for key, value in sentence_dict.items():
        #print(key, '->', value)
        unique_values = set(value)
        annos[key]=unique_values
    return annos

def sentence_anno(df):
    sentence_label_dict={}
    for index, sen_tok in enumerate(df['sen_id-tok_id']):
        sen_id = sen_tok[:sen_tok.find('-')]
        label = df['annotation'].iloc[index]
        note_id = df['note_id'].iloc[index]
        sen_id = note_id+"_"+sen_id
        if sen_id in sentence_label_dict:
            sentence_label_dict[sen_id].append(label)
        else:
            sentence_label_dict[sen_id]=[label]
    return sentence_label_dict


def init_row (key):
    #'Label', 'G1', 'G2', 'G3', 'G4', 'G5'
    new_row = {'Label':key, 'G1':-1, 'G2':-1, 'G3':-1, 'G4':-1, 'G5':-1}
    return new_row

def add_new_row_with_value (df, key, score, group):
    row = df.loc[df['Label'] == key]
    if not row.empty:
        df.loc[row.index, group]=score
    else:
        row = init_row(key)
        row[group]=score
        df = df.append(row, ignore_index=True)
    return df


def get_kappa_for_label (dict1, dict2, label, group):
    no_anno_cnt=0
    linemismatch_cnt = 0
    labels1=[]
    labels2=[]
    groups=[]
    keys=[]
    ### key = the note_sentence_id, values = aggregated set of values from all tokens in that sentence
    for key, values1 in dict1.items():
        try:
            values2=dict2[key]
            if (values1=={'_'} and values2=={'_'}):
                labels1.append(label1)
                labels2.append(label2)
                continue
            ### we initialise with the first value
            label1 = list(values1)[0]
            label2 = list(values2)[0]
            ### we check if the target label is listed in either set of values
            for value in values1:
                if (value==label):
                    label1=value
            for value in values2:
                if (value==label):
                    label2=value
            ## We only append if either of the annotators annotated this sentence with the target label
            if (label1==label) or label2==label:
                no_anno_cnt+=1
                labels1.append(label1)
                labels2.append(label2)
                keys.append(key)
                groups.append(group)
        except:
            linemismatch_cnt+=1
            #print('Line mismatch error:', key)
    #print('No annoations by both:', no_anno_cnt, ' Proportion of sentences:', no_anno_cnt/len(dict1.items()))          
    kappa=-2
    try:
        kappa=cohen_kappa_score(labels1, labels2)
    except:
        print('kappa error')
        
    return kappa, no_anno_cnt, labels1, labels2, keys, groups


 
def get_doc_labels (df):
    doc_label_dict1={}
    doc_label_dict2={}
    for index, key in enumerate(df['Key']):
        doc = key[:key.find('_')]
        group = df['Group'].iloc[index]
        label1 = df['label1'].iloc[index]
        label2 = df['label2'].iloc[index]
        if doc in doc_label_dict1:
            doc_label_dict1[doc].append(label1)
        else:
            doc_label_dict1[doc]=[label1]
        
        if doc in doc_label_dict2:
            doc_label_dict2[doc].append(label2)
        else:
            doc_label_dict2[doc]=[label2]
    return doc_label_dict1, doc_label_dict2
 