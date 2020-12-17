import pickle
from class_definitions import Annotation, BertContainer
from pathlib import Path
import torch
from datetime import datetime
import pandas as pd
import openpyxl
import numpy as np
from utils import lightweightDataframe, completeDataframe, filterDataframe

def prepareDataC(function, splitting = False, percentage = 100):   
    """
    Reads train and test data, prepares data, trains SVM, predicts on test data, prints sklearn classification classification_report
    """
    print(datetime.now())
    #define paths to train and test pickles    
    input_train_covid = '../../Covid_data_11nov/traindata_covidbatch.pkl'
    input_test_covid =  '../../Covid_data_11nov/testdata_covidbatch.pkl' 
    
    print("Reading pickle files...")
    #read pickle files
    with open(input_train_covid, "rb") as pkl_file:
        traindata_c = pickle.load(pkl_file)
        
    with open(input_test_covid, "rb") as pkl_file:
        testdata_c = pickle.load(pkl_file)
        
        
    print("Creating and filtering dataframes...")
    #prepare training dataframes
    df_tr_c = function(traindata_c)[0]
    #take out sentences with labels that we should ignore (background, target, view_patient, view_thirdparty, info_thirdparty)
    rows_to_delete_tr_c, filtered_df_tr_c = filterDataframe(df_tr_c)

    #prepare test dataframes
    df_te_c = function(testdata_c)[0]
    rows_to_delete_te_c, filtered_df_te_c = filterDataframe(df_te_c)
    #extract test labels
    filtered_labels_te_c = filtered_df_te_c['domain'].to_list()
    filtered_encodings_te_c = filtered_df_te_c['encoding'].tolist()

    print("Retrieve note id's...")
    #get note id's for aggregation
    try:    
        ids_c = []
        list_keys_c = filtered_df_te_c['key'].tolist()
        for key in list_keys_c:
            y = key.split('--')[3]
            ids_c.append(y)
    except KeyError:
        ids_c = []
        
        
    print("Downsampling training labels...")
    #Original to randomly select indices of negative examples for downsampling
    #Get original support 0 class
    #seriesObj = filtered_df_tr.apply(lambda x: True if x['domain'] == 'None' else False , axis=1)
    # Count number of True in series
    #numOfRows = len(seriesObj[seriesObj == True].index)
    #print('Number of Rows in dataframe in which domain is None =', numOfRows)
    
    #per_50 = (numOfRows/2)
    #per_25 = (per_50/2)
    #per_125 = (per_25/2)
    #per_625 = (per_625/2)
    #per_3125 = (per_3125/2)
    #N = int(per_50) #+ int(per_25) + int(per_125) + int(per_625) + int(per_3125)
    
    #down_df_tr, indices = downsample(filtered_df_tr, N)
    
    with open("down_indices_covid2.pkl", "rb") as f:
        indices = pickle.load(f)
    down_df_tr_c = filtered_df_tr_c.drop(indices)
    
    
    if splitting == False:
        downsampled_filtered_labels_tr_c = down_df_tr_c['domain'].to_list()
        downsampled_filtered_encodings_tr_c = down_df_tr_c['encoding'].tolist()
        
    if splitting == True:
        #splitting final dataframw
        shuffled = down_df_tr_c.sample(frac = 1)
        parts = np.array_split(shuffled, 4)
                               
        df_25 = parts[0]
        df_50 = df_25.append(parts[1])
        df_75 = df_50.append(parts[2])
        
        if percentage == 25:
            #extract training labels
            downsampled_filtered_labels_tr_c = df_25['domain'].to_list()
            downsampled_filtered_encodings_tr_c = df_25['encoding'].tolist()
        if percentage == 50:
            downsampled_filtered_labels_tr_c = df_50['domain'].to_list()
            downsampled_filtered_encodings_tr_c = df_50['encoding'].tolist()            
        if percentage == 75:
            downsampled_filtered_labels_tr_c = df_75['domain'].to_list()
            downsampled_filtered_encodings_tr_c = df_75['encoding'].tolist() 
        
    
    print('Converting encodings...')
    
    sen_reps_tr_c = []
    for entry in downsampled_filtered_encodings_tr_c:
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_tr_c.append(array)
        
    #prepare test features
    #filtered_encodings_te = [i for j, i in enumerate(encodings_te) if j not in set(rows_to_delete_te)]        
    sen_reps_te_c = []
    for entry in filtered_encodings_te_c:
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_te_c.append(array)


    return(downsampled_filtered_labels_tr_c, filtered_labels_te_c, sen_reps_tr_c, sen_reps_te_c, ids_c)


def prepareDataNC(function):
    """
    Reads train and test data, prepares data, trains SVM, predicts on test data, prints sklearn classification classification_report
    """
    print(datetime.now())
    #define paths to train and test pickles    
    input_train_noncovid = '../../Non_covid_data_15oct/train_data_batch1_disregard_removed.pkl'
    input_test_noncovid = '../../Non_covid_data_15oct/test_data_batch1_disregard_removed.pkl'
    
    print("Reading pickle files...")
    #read pickle files        
    with open(input_train_noncovid, "rb") as pkl_file:
        traindata_nc = pickle.load(pkl_file)
        
    with open(input_test_noncovid, "rb") as pkl_file:
        testdata_nc = pickle.load(pkl_file)
        
    print("Creating and filtering dataframes...")
    #prepare training dataframes
    df_tr_nc = function(traindata_nc)[0]
    #take out sentences with labels that we should ignore (background, target, view_patient, view_thirdparty, info_thirdparty)
    rows_to_delete_tr_nc, filtered_df_tr_nc = filterDataframe(df_tr_nc)

    #prepare test dataframes
    df_te_nc = function(testdata_nc)[0]
    rows_to_delete_te_nc, filtered_df_te_nc = filterDataframe(df_te_nc)
    #extract test labels
    filtered_labels_te_nc = filtered_df_te_nc['domain'].to_list()
    filtered_encodings_te_nc = filtered_df_te_nc['encoding'].tolist()
    
    print("Retrieve note id's...")
    #get keys for aggregation
    try: 
        ids_nc = []
        df_list = function(testdata_nc)[1]
        df_list_new =  [i for j, i in enumerate(df_list) if j not in set(rows_to_delete_te_nc)]
        for instance in df_list_new:
            l = len(str(instance[2]))
            if instance[3] == "['']":
                ids_nc.append(instance[0].split('---')[1])
            else:
                ids_nc.append(instance[0].split('---')[1][:-l])
    except IndexError:
        ids_nc = []
                    
    
    print("Downsampling training labels...")
    #Original to randomly select indices of negative examples for downsampling
    #Get original support 0 class
    #seriesObj = filtered_df_tr.apply(lambda x: True if x['domain'] == 'None' else False , axis=1)
    # Count number of True in series
    #numOfRows = len(seriesObj[seriesObj == True].index)
    #print('Number of Rows in dataframe in which domain is None =', numOfRows)
    
    #per_50 = (numOfRows/2)
    #per_25 = (per_50/2)
    #per_125 = (per_25/2)
    #per_625 = (per_625/2)
    #per_3125 = (per_3125/2)
    #N = int(per_50) #+ int(per_25) + int(per_125) + int(per_625) + int(per_3125)
    
    #down_df_tr, indices = downsample(filtered_df_tr, N)
    
    #down_df_tr, indices = downsample(filtered_df_tr, N)
    with open("down_indices3.pkl", "rb") as f:
        indices = pickle.load(f)
    down_df_tr_nc = filtered_df_tr_nc.drop(indices)
    downsampled_filtered_labels_tr_nc = down_df_tr_nc['domain'].to_list()
    downsampled_filtered_encodings_tr_nc = down_df_tr_nc['encoding'].tolist()

    print('Converting encodings...')
    sen_reps_tr_nc = []
    for entry in downsampled_filtered_encodings_tr_nc:
        #select last four layers
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_tr_nc.append(array)
        
   
    #prepare test features
    #filtered_encodings_te = [i for j, i in enumerate(encodings_te) if j not in set(rows_to_delete_te)]        
    sen_reps_te_nc = []
    for entry in filtered_encodings_te_nc:
        #select last four layers
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_te_nc.append(array)


    return(downsampled_filtered_labels_tr_nc, filtered_labels_te_nc, sen_reps_tr_nc, sen_reps_te_nc, ids_nc)
