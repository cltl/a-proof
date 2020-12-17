import pandas as pd
import pickle
from collections import Counter
from utils import lightweightDataframe, completeDataframe
from preprocessing import prepareDataC, prepareDataNC
from eval_domain_agg import eval_per_domain
from pathlib import Path
import torch
from datetime import datetime
import openpyxl
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report


def get_predictions(train, trainlabels, test):
    
    print("Start training...")
    traindata = [x[0] for x in train] 
        

    #Change parameters for different experiments
    lin_clf = svm.SVC(kernel='poly', degree=9, probability=False)
    #lin_clf = svm.LinearSVC(dual = False, class_weight = 'balanced')
    #train model
    lin_clf.fit(traindata, trainlabels)
    
    #save model 
    #filename = 'best_model_lopen.sav'
    #pickle.dump(lin_clf, open(filename, 'wb'))
    
    print("Start predicting...")
    testdata = [x[0] for x in test]
    predictions = lin_clf.predict(testdata)

    return(predictions)


def make_note_df(note_ids, labels):

    data = {'note_id': note_ids,
                'labels': labels}

    df = pd.DataFrame(data)

    return(df)

def noteLabels(df):

    all_labels = []
    labels = []
    ids = []
    all_ids = []
    i = 0
    for index, row in df.iterrows():
        #append labels and note id's 
        labels.append(df.iloc[i]['labels'])
        ids.append(df.iloc[i]['note_id'])
        try:
            #see if note id changes in df
            if df.iloc[i]['note_id'] != df.iloc[i+1]['note_id']:
                #if so, append the list in which you collected labels and note id's earlier to a bigger list
                all_labels.append(labels)
                all_ids.append(ids)
                #and empty the lists in which you collect seperate labels and note id's
                labels = []
                ids = []
            i += 1
        except IndexError:
            #make sure you can append the last list as well
            all_labels.append(labels)
            all_ids.append(ids)
            labels = []
            ids = []

    
    print("all_labels: ", len(all_labels))
    print("all_ids: ", len(all_ids))


    labels_per_note = []
    for entry in all_labels:
        #eliminate double labels
        s = set(entry)
        l = list(s)
        labels_per_note.append(l)
        
    unique_ids = []
    for entry in all_ids:
        i_d = entry[0]
        unique_ids.append(i_d)
        
    print("labels per note: ", len(labels_per_note))
    print("unique_ids: ", len(unique_ids))

    final_list = []
    for l in labels_per_note:
        if len(l) > 1:
            #remove 'None' labels in notes where there is a domain label
            l.remove('None')
            final_list.append(l)
        else:
            final_list.append(l)
            
    print("final list: ", len(final_list))
            
    return(final_list, unique_ids)


def main():

    #Get train and test data and note id's
    labels_tr_c, labels_te_c, tr_c, te_c, ids_c = prepareDataC(completeDataframe) # splitting = True, percentage = 25)
    labels_tr_nc, labels_te_nc, tr_nc, te_nc, ids_nc = prepareDataNC(completeDataframe)


    #Uncomment to extend training and/or test set
    #tr_c += tr_nc
    #labels_tr_c += labels_tr_nc
    #te_c += te_nc
    #labels_te_c += labels_te_nc
    #ids_c += ids_nc

    #get predictions and eval on sentence level: feed selected traindata
    predictions = get_predictions(tr_c, labels_tr_c, te_c)
    eval_report = classification_report(labels_te_c, predictions, digits = 3) 
    print(eval_report)

    #make dataframe of note id's and labels for annotations: change variables according to traindata you selected
    df_annotations = make_note_df(ids_c, labels_te_c)
    #get annotations per note 
    annotations_per_note, unique_ids_man = noteLabels(df_annotations)

    #make dataframe of note id's and labels for predictions
    df_predictions = make_note_df(ids_c, predictions)
    #get predicted labels per note
    predictions_per_note, unique_ids_sys = noteLabels(df_predictions)

    #make dictionaries for evaluation
    dict_predict = dict(zip(unique_ids_sys, predictions_per_note))
    dict_ann = dict(zip(unique_ids_man, annotations_per_note))

    #Write eval per domain on note level to tsv file
    eval_per_domain(dict_predict, dict_ann, "../machine_learning/test.tsv")

    #Check lenghts
    #print(len(df_annotations))
    #print(len(df_predictions))
    #print(len(annotations_per_note))
    #print(len(predictions_per_note))
    #print(len(unique_ids_man))
    #print(len(unique_ids_sys))
    #print(len(dict_predict))
    #print(len(dict_ann))
    
    
if __name__ == '__main__':
    main()



        










