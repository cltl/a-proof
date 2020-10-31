import pickle
from class_definitions import Annotation, BertContainer
from pathlib import Path
import torch
from datetime import datetime
import pandas as pd
import openpyxl
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report

def lightweightDataframe(data):
    """
    Creates dataframe with encodings and annotations per sentence
    (Encodings = last 4 layers of BERTje representation)
    Returns pandas dataframe
    
    :param data: pickle file
    """
    df_list = []   
    encodings = []
    for instance in data:
        #add encodings
        list_instance = []
        list_instance.append(instance.encoding)
        #make seperate list with encodings
        encodings.append(instance.encoding)
        
        #add lsit of labels per sentence
        list_labels = []
        annot = instance.annot
        for anno in annot:
            label = anno.label
            list_labels.append(label)
        list_instance.append(list_labels)
        df_list.append(list_instance)
        
    #create dataframe    
    df = pd.DataFrame(df_list, columns = ['encoding' , 'labels'])
    # create seperate columns for seperate labels
    df['disregard'] = 0
    df['background'] = 0
    df['target'] = 0
    df['viewthird'] = 0
    df['viewpatient'] = 0
    df['implicit'] = 0
    df['infothird']
    df['domain'] = 0
    df['delete'] = 0
    
    #Add 1 to certain columns
    df['disregard'][df['labels'].apply(lambda x: 'disregard\_file' in x)] = 1
    df['background'][df['labels'].apply(lambda x: 'type\_Background' in x)] = 1
    df['target'][df['labels'].apply(lambda x: 'target' in x)] = 1
    df['viewthird'][df['labels'].apply(lambda x: 'view\_Third party' in x)] = 1
    df['infothird'][df['labels'].apply(lambda x: 'info\_Third party' in x)] = 1
    df['viewpatient'][df['labels'].apply(lambda x: 'view\_Patient' in x)] = 1
    df['implicit'][df['labels'].apply(lambda x: 'type\_Implicit' in x)] = 1
    
    #Add domain labels to a seperate column
    df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'

    #Add 1's to any row you want to delete
    df.loc[df['disregard'] == 1, 'delete'] = 1
    df.loc[df['background'] == 1, 'delete'] = 1
    df.loc[df['target'] == 1, 'delete'] = 1
    df.loc[df['viewthird'] == 1, 'delete'] = 1
    df.loc[df['infothirf'] == 1, 'delete'] = 1
    df.loc[df['viewpatient'] == 1, 'delete'] = 1

    return(encodings, df)

def completeDataframe(data):
    """
    Creates dataframe with key, annoator, sentence id, sentence in natural language, sentence representation in BERTje encoding, and annotations
    Returns pandas dataframe
    
    :param data: pickle file
    """
    df_list = []    
    for instance in data:
        list_instance = []
        list_instance.append(instance.key)
        list_instance.append(instance.annotator)
        list_instance.append(instance.sen_id)
        list_instance.append(instance.sen)
        list_instance.append(instance.encoding)
        #add labels
        list_labels = []
        annot = instance.annot
        for anno in annot:
            label = anno.label
            list_labels.append(label)
        list_instance.append(list_labels)
        df_list.append(list_instance)
    df = pd.DataFrame(df_list, columns = ['key', 'annotator', 'sen_id', 'sen', 'encoding', 'labels'])
      
    df['disregard'] = 0
    df['background'] = 0
    df['target'] = 0
    df['viewthird'] = 0
    df['viewpatient'] = 0
    df['implicit'] = 0
    df['domain'] = 0
    df['delete'] = 0

    df['disregard'][df['labels'].apply(lambda x: 'disregard\_file' in x)] = 1
    df['background'][df['labels'].apply(lambda x: 'type\_Background' in x)] = 1
    df['target'][df['labels'].apply(lambda x: 'target' in x)] = 1
    df['viewthird'][df['labels'].apply(lambda x: 'view\_Third party' in x)] = 1
    df['infothird'][df['labels'].apply(lambda x: 'info\_Third party' in x)] = 1
    df['viewpatient'][df['labels'].apply(lambda x: 'view\_Patient' in x)] = 1
    df['implicit'][df['labels'].apply(lambda x: 'type\_Implicit' in x)] = 1
    df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'
    
    df.loc[df['disregard'] == 1, 'delete'] = 1
    df.loc[df['background'] == 1, 'delete'] = 1
    df.loc[df['target'] == 1, 'delete'] = 1
    df.loc[df['viewthird'] == 1, 'delete'] = 1
    df.loc[df['infothird'] == 1, 'delete'] = 1
    df.loc[df['viewpatient'] == 1, 'delete'] = 1
    
    return(df)

def filterDataframe(df):
    """
    Takes out the rows that need to be deleted from df
    Returns filtered df and list of indexes of rows that were deleted
    
    :param df: pandas dataframe
    """
    rows_to_delete = []
    for index, item in enumerate(df['delete']):
        if item == 1:
            rows_to_delete.append(index)
    df = df.drop(rows_to_delete)
    return(rows_to_delete, df)
    
        
def main():
    """
    Reads train and test data, prepares data, trains SVM, predicts on test data, prints sklearn classification classification_report
    """
    print(datetime.now())
    #define paths to train and test pickles
    input_train = '../../Non_covid_data_15oct/train_data_batch1_disregard_removed.pkl' 
    input_test =  '../../Non_covid_data_15oct/test_data_batch1_disregard_removed.pkl' 
    
    print("Reading pickle files...")
    #read pickle files
    with open(input_train, "rb") as pkl_file:
        traindata = pickle.load(pkl_file)
        
    with open(input_test, "rb") as pkl_file:
        testdata = pickle.load(pkl_file)
        
    print("Creating and filtering dataframes...")
    #prepare training dataframe
    encodings_tr, df_tr = lightweightDataframe(traindata)
    rows_to_delete_tr, filtered_df_tr = filterDataframe(df_tr)
    #extract training labels
    filtered_labels_tr = filtered_df_tr['domain'].to_list()

    #prepare test dataframe
    encodings_te, df_te = lightweightDataframe(testdata)
    rows_to_delete_te, filtered_df_te = filterDataframe(df_te)
    #extract test labels
    filtered_labels_te = filtered_df_te['domain'].to_list()
    
    print("Filtering and converting encodings...")
    
    #prepare training features
    filtered_encodings_tr = [i for j, i in enumerate(encodings_tr) if j not in rows_to_delete_tr]
    sen_reps_tr = []
    for entry in filtered_encodings_tr:
        #take mean of last 4 layers to create sentence representation
        entry2 = torch.mean(entry, dim=0)
        #convert in numpy array
        array = entry2.numpy()
        sen_reps_tr.append(array)
    
    #prepare test features
    filtered_encodings_te = [i for j, i in enumerate(encodings_te) if j not in rows_to_delete_te]
    sen_reps_te = []
    for entry in filtered_encodings_te:
        #take mean of last 4 layers to create sentence representation
        entry2 = torch.mean(entry, dim=0)
        #convert in numpy array
        array = entry2.numpy()
        sen_reps_te.append(array)

    #traindata = []
    #for x in filtered_encodings_tr:
    #    traindata.append(x[0].flatten())

    #traindata = np.vstack(traindata)
    
    #testdata = []
    #for x in filtered_encodings_te:
    #    testdata.append(x[0].flatten())

    #testdata = np.vstack(testdata)
    
    print("Start training...")
    traindata = [x[0] for x in sen_reps_tr] 
    lin_clf = svm.LinearSVC(class_weight = 'balanced')
    lin_clf.fit(traindata, filtered_labels_tr)
    
    
    print("Start predicting...")
    testdata = [x[0] for x in sen_reps_te]
    predictions = lin_clf.predict(testdata)
    
    eval_report = classification_report(filtered_labels_te, predictions, digits = 3) 
    print(eval_report)
    
    print(datetime.now())
    
    
if __name__ == '__main__':
    main()
