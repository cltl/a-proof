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
    df_list = []   
    encodings = []
    for instance in data:
        #add sentence vector represenation
        list_instance = []
        list_instance.append(instance.encoding)
        encodings.append(instance.encoding)

        #sentence_rep = torch.mean(instance.encoding, dim=0)
        #sentence_array = sentence_rep.numpy()
        
        #add labels
        list_labels = []
        annot = instance.annot
        for anno in annot:
            label = anno.label
            list_labels.append(label)
        list_instance.append(list_labels)
        df_list.append(list_instance)
        
    df = pd.DataFrame(df_list, columns = ['encoding' , 'labels'])
    df['disregard'] = 0
    df['background'] = 0
    df['target'] = 0
    df['thirdparty'] = 0
    df['viewpatient'] = 0
    df['implicit'] = 0
    df['domain'] = 0
    df['delete'] = 0
    #df['lopen'] = 0
    #df['inspanning'] = 0
    #df['werk'] = 0
    #df['stemming'] = 0

    df['disregard'][df['labels'].apply(lambda x: 'disregard\_file' in x)] = 1
    df['background'][df['labels'].apply(lambda x: 'type\_Background' in x)] = 1
    df['target'][df['labels'].apply(lambda x: 'target' in x)] = 1
    df['thirdparty'][df['labels'].apply(lambda x: 'view\_Third party' in x)] = 1
    df['viewpatient'][df['labels'].apply(lambda x: 'view\_Patient' in x)] = 1
    df['implicit'][df['labels'].apply(lambda x: 'type\_Implicit' in x)] = 1
    df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'
    #df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' not in x)]  = 'None'
    #df['stemming'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'
    #df['lopen'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    #df['inspanning'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    #df['werk'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    
    df.loc[df['disregard'] == 1, 'delete'] = 1
    df.loc[df['background'] == 1, 'delete'] = 1
    df.loc[df['target'] == 1, 'delete'] = 1
    df.loc[df['thirdparty'] == 1, 'delete'] = 1
    df.loc[df['viewpatient'] == 1, 'delete'] = 1

    return(encodings, df)

def completeDataframe(data):
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
    df['thirdparty'] = 0
    df['viewpatient'] = 0
    df['implicit'] = 0
    df['domain'] = 0
    df['delete'] = 0
    #df['lopen'] = 0
    #df['inspanning'] = 0
    #df['werk'] = 0
    #df['stemming'] = 0

    df['disregard'][df['labels'].apply(lambda x: 'disregard\_file' in x)] = 1
    df['background'][df['labels'].apply(lambda x: 'type\_Background' in x)] = 1
    df['target'][df['labels'].apply(lambda x: 'target' in x)] = 1
    df['thirdparty'][df['labels'].apply(lambda x: 'view\_Third party' in x)] = 1
    df['viewpatient'][df['labels'].apply(lambda x: 'view\_Patient' in x)] = 1
    df['implicit'][df['labels'].apply(lambda x: 'type\_Implicit' in x)] = 1
    df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'
    #df['domain'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: '.B152: Stemming' not in x)]  = 'None'
    #df['domain'][df['labels'].apply(lambda x: ['.D450: Lopen en zich verplaatsen', '.B455: Inspanningstolerantie', '.D840-859: Beroep en werk', '.B152: Stemming'] not in x)]  = 'None'
    #df['stemming'][df['labels'].apply(lambda x: '.B152: Stemming' in x)] = '.B152: Stemming'
    #df['lopen'][df['labels'].apply(lambda x: '.D450: Lopen en zich verplaatsen' in x)] = '.D450: Lopen en zich verplaatsen'
    #df['inspanning'][df['labels'].apply(lambda x: '.B455: Inspanningstolerantie' in x)] = '.B455: Inspanningstolerantie'
    #df['werk'][df['labels'].apply(lambda x: '.D840-859: Beroep en werk' in x)] = '.D840-859: Beroep en werk'
    
    df.loc[df['disregard'] == 1, 'delete'] = 1
    df.loc[df['background'] == 1, 'delete'] = 1
    df.loc[df['target'] == 1, 'delete'] = 1
    df.loc[df['thirdparty'] == 1, 'delete'] = 1
    df.loc[df['viewpatient'] == 1, 'delete'] = 1
    
    return(df)

def filterDataframe(df):
    rows_to_delete = []
    for index, item in enumerate(df['delete']):
        if item == 1:
            rows_to_delete.append(index)
    df = df.drop(rows_to_delete)
    return(rows_to_delete, df)

def train_svm(traindata, labels):
    lin_clf = svm.LinearSVC()
    lin_clf.fit(traindata, labels)

    
        
def main():
    print(datetime.now())
    input_train = '../../Non_covid_data_15oct/train_data_batch1_disregard_removed.pkl' 
    input_test =  '../../Non_covid_data_15oct/test_data_batch1_disregard_removed.pkl' 
    
    print("Reading pickle files...")
    with open(input_train, "rb") as pkl_file:
        traindata = pickle.load(pkl_file)
        
    with open(input_test, "rb") as pkl_file:
        testdata = pickle.load(pkl_file)
        
    print("Creating and filtering dataframes...")
    #train
    encodings_tr, df_tr = lightweightDataframe(traindata)
    rows_to_delete_tr, filtered_df_tr = filterDataframe(df_tr)
    filtered_labels_tr = filtered_df_tr['domain'].to_list()
    #for item in filtered_labels_tr:
    #    if item == 0:
    #        item = str(item)
    #        item.replace('0', 'None')
    #test
    encodings_te, df_te = lightweightDataframe(testdata)
    rows_to_delete_te, filtered_df_te = filterDataframe(df_te)
    filtered_labels_te = filtered_df_te['domain'].to_list()
    #for item in filtered_labels_te:
    #    if item == 0:
    #        item = str(item)
    #        item.replace('0', 'None')
    
    print("Filtering and converting encodings...")
    
    filtered_encodings_tr = [i for j, i in enumerate(encodings_tr) if j not in rows_to_delete_tr]
    sen_reps_tr = []
    for entry in filtered_encodings_tr:
        entry2 = torch.mean(entry, dim=0)
        #entry4 = entry3.squeeze().detach().numpy()
        array = entry2.numpy()
        array2 = array.flatten()
        sen_reps_tr.append(array)
        
    filtered_encodings_te = [i for j, i in enumerate(encodings_te) if j not in rows_to_delete_te]
    sen_reps_te = []
    for entry in filtered_encodings_te:
        entry2 = torch.mean(entry, dim=0)
        #entry4 = entry3.squeeze().detach().numpy()
        array = entry2.numpy()
        array2 = array.flatten()
        sen_reps_te.append(array)

    #traindata = []
    #for x in filtered_encodings_tr:
    #    traindata.append(x[0].flatten())

    #traindata = np.vstack(traindata)
    
    #testdata = []
    #for x in filtered_encodings_te:
    #    testdata.append(x[0].flatten())

    #testdata = np.vstack(testdata)
    
    #train_features = np.vectorize(sen_reps_tr)
    #print(train_features[:5])
    #print(len(filtered_labels))
    #print(len(sen_reps))
    
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
