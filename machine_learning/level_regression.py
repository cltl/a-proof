import pickle
from pathlib import Path
import torch
from datetime import datetime
import pandas as pd
import openpyxl
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error
from utils import completeDataframe, filterDataframe

def createDataframe(filepath_train, filepath_test, domain, type_dataset):
    """
    Creates dataframe with encodings and annotations per sentence
    (Encodings = last 4 layers of BERTje representation)
    Returns pandas dataframe

    :param domain: str: lopen, stemming, beroep, inspanningstolerantie
    :param type_dataset: str: covid, noncovid
    """
    
    print("Reading pickle files...")
    #read pickle files
    with open(filepath_train, "rb") as pkl_file:
        traindata = pickle.load(pkl_file)
 
    with open(filepath_test, "rb") as pkl_file:
        testdata = pickle.load(pkl_file)
    
    if domain == 'lopen':
        d = '.D450: Lopen en zich verplaatsen'
        l = 'FAC '
    elif domain == 'stemming':
        d = '.B152: Stemming'
        l = 'STM '
    elif domain == 'beroep':
        d = '.D840-859: Beroep en werk'
        l = 'BER '
    elif domain == 'inspanningstolerantie':
        d = '.B455: Inspanningstolerantie'
        l = 'INS '
    
    df_train, df_list_tr = completeDataframe(traindata)
    df_test, df_list_te = completeDataframe(testdata)
    
    #get note id's from keys in dataframe
    if type_dataset == 'covid':
        ids= []
        list_keys = df_test['key'].tolist()
        for key in list_keys:
            y = key.split('--')[3]
            ids.append(y)
        df_test['note_id'] = ids
    
    if type_dataset == 'noncovid':
        ids = []
        for instance in df_list_te:
            le = len(str(instance[2]))
            if instance[3] == "['']":
                ids.append(instance[0].split('---')[1])
            else:
                ids.append(instance[0].split('---')[1][:-le])
        df_test['note_id'] = ids
        
    
    df_train[domain] = 0
    df_train['level'] = 'None'
    df_test[domain] = 0
    df_test['level'] = 'None'
    
    #Add domain labels to a seperate column
    df_train['domain'][df_train['labels'].apply(lambda x: d in x)] = d
    df_train['level'][df_train['labels'].apply(lambda x: l+'0'in x)] = 0
    df_train['level'][df_train['labels'].apply(lambda x: l+'1'in x)] = 1
    df_train['level'][df_train['labels'].apply(lambda x: l+'2'in x)] = 2
    df_train['level'][df_train['labels'].apply(lambda x: l+'3'in x)] = 3
    df_train['level'][df_train['labels'].apply(lambda x: l+'4'in x)] = 4
    df_train['level'][df_train['labels'].apply(lambda x: l+'5'in x)] = 5
    
    df_test['domain'][df_test['labels'].apply(lambda x: d in x)] = d
    df_test['level'][df_test['labels'].apply(lambda x: l+'0'in x)] = 0
    df_test['level'][df_test['labels'].apply(lambda x: l+'1'in x)] = 1
    df_test['level'][df_test['labels'].apply(lambda x: l+'2'in x)] = 2
    df_test['level'][df_test['labels'].apply(lambda x: l+'3'in x)] = 3
    df_test['level'][df_test['labels'].apply(lambda x: l+'4'in x)] = 4
    df_test['level'][df_test['labels'].apply(lambda x: l+'5'in x)] = 5

    df_train.loc[df_train['domain'] == d, domain] = 1
    df_test.loc[df_test['domain'] == d, domain] = 1
    
        
    print("Filtering dataframes...")
    #filter dataframe
    del_rows_tr, filtered_df_train = filterDataframe(df_train)
    #only select instances where there is an entry for level
    df_selection_train = filtered_df_train[(filtered_df_train[domain] == 1) & (filtered_df_train['level'] != 'None')]

    #test1
    del_rows_te, filtered_df_test = filterDataframe(df_test)
    #gold output
    df_selection_test = filtered_df_test[(df_test[domain] == 1) & (filtered_df_test['level'] != 'None')]
        
    return(df_selection_train, df_selection_test)
    
    
def prepro(df_train, df_test):

    print("Extract train features and labels...")
    encodings_tr = df_train['encoding'].tolist()
    sen_reps_tr = []
    for entry in encodings_tr:
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_tr.append(array)
    labels_tr = df_train['level'].tolist()
    
    print("Length training data: ", len(sen_reps_tr))
    print("Length labels training data:", len(labels_tr))
    
    print("Extract test features and labels...")
    encodings_te = df_test['encoding'].tolist()
    sen_reps_te = []
    for entry in encodings_te:
        entry2 = entry[-4:]
        #take mean of last 4 layers to create sentence representation
        entry3 = torch.mean(entry2, dim=0)
        #convert in numpy array
        array = entry3.numpy()
        sen_reps_te.append(array)
    labels_te = df_test['level'].tolist()
    
    return(sen_reps_tr, labels_tr, sen_reps_te, labels_te)

def get_predictions(train, trainlabels, test):

    print("Start training...")
    traindata = [x[0] for x in train] 
    print("train: ", len(traindata))
        
    #reg_model = linear_model.LinearRegression()
    reg_model = svm.SVR(kernel = 'poly')
    reg_model.fit(traindata, trainlabels)
    
    #save model 
    #filename = 'best_model_FAC.sav'
    #pickle.dump(reg_model, open(filename, 'wb'))
        
    print("Start predicting...")
    testdata = [x[0] for x in test]
    print("test: ", len(testdata))
    predictions = reg_model.predict(testdata)
    
    return(predictions)
    

def evaluation(labels_te, predictions):
    
    MSE = mean_squared_error(labels_te, predictions)
    MAE = mean_absolute_error(labels_te, predictions)
    RMSE = mean_squared_error(labels_te, predictions, squared=False)
    
    return(MSE, MAE, RMSE)


def make_note_df(df_test, labels):
    
    note_ids = df_test['note_id'].tolist() 
    data = {'note_id': note_ids,
                'level': labels}
    df = pd.DataFrame(data)
    return(df)


def means(df):

    #Create one list of lists containing levels per note
    #Create one list of lists containing note id's per note
    all_levels = []
    levels = []
    ids = []
    all_ids = []
    i = 0
    for index, row in df.iterrows():
        #append levels and note id's 
        levels.append(df.iloc[i]['level'])
        ids.append(df.iloc[i]['note_id'])
        try:
            #see if note id changes in df
            if df.iloc[i]['note_id'] != df.iloc[i+1]['note_id']:
                #if so, append the list in which you collected levels and note id's earlier to a bigger list
                all_levels.append(levels)
                all_ids.append(ids)
                #and empty the lists in which you collect seperate levels and note id's 
                levels = []
                ids = []
            i += 1
        except IndexError:
            #make sure you can append the last list as well
            all_levels.append(levels)
            all_ids.append(ids)
            levels = []
            ids = []

    
    print("list_of_lists: ", len(all_levels))
    print("list_all_ids: ", len(all_ids))
    
    #Check levels per note
    print(all_levels)
    
    list_means = []
    for item in all_levels:
        mean = sum(item)/len(item)
        list_means.append(mean)
        
    unique_ids = []
    for entry in all_ids:
        i_d = entry[0]
        unique_ids.append(i_d)
    
    #Check if same length    
    print("means: ", len(list_means))
    print("unique_ids: ", len(unique_ids))
    
    return(list_means)


def main(domain):
    """
    Change this code to test different datasets
    :param domain: str
    
    """

    filepath_train1 = '../../Non_covid_data_15oct/train_data_batch1_disregard_removed.pkl'
    filepath_test1 = '../../Non_covid_data_15oct/test_data_batch1_disregard_removed.pkl'
    filepath_train2 = '../../Covid_data_11nov/traindata_covidbatch.pkl'
    filepath_test2 = '../../Covid_data_11nov/testdata_covidbatch.pkl'

    df_train_nc, df_test_nc = createDataframe(filepath_train1, filepath_test1, domain, 'noncovid')
    df_train_c, df_test_c = createDataframe(filepath_train2, filepath_test2, domain, 'covid')
    #print(df_train)
    sen_reps_tr_nc, labels_tr_nc, sen_reps_te_nc, labels_te_nc = prepro(df_train_nc, df_test_nc)
    sen_reps_tr_c, labels_tr_c, sen_reps_te_c, labels_te_c = prepro(df_train_c, df_test_c)
    #print(labels_te)

    #Uncomment to combine training datasets 
    #sen_reps_tr_c += sen_reps_tr_nc
    #labels_tr_c += labels_tr_nc

    #Uncomment to combine test datasets and test labels if necessary (if you do so, also combine test df's)
    #sen_reps_te_c += sen_reps_te_nc
    #labels_te_c += labels_te_nc
    #df_test = pd.concat([df_test_c, df_test_nc])

    #Feed selected train and test data to regression model
    predictions = get_predictions(sen_reps_tr_c, labels_tr_c, sen_reps_te_c)

    #Make dataframes of note id's and labels
    df_ann = make_note_df(df_test_c, labels_te_c)
    df_pred = make_note_df(df_test_c, predictions)

    #Evaluate on sentence level
    MSE, MAE, RMSE = evaluation(labels_te_c, predictions)

    print("MSE "+domain, MSE)
    print("MAE "+domain, MAE)
    print("RMSE "+domain, RMSE)

    #Aggregate per note
    means_ann = means(df_ann)
    means_pred = means(df_pred)

    #Evaluate on note level
    MSE, MAE, RMSE = evaluation(means_ann, means_pred)

    print("MSE agg"+domain, MSE)
    print("MAE agg"+domain, MAE)
    print("RMSE agg"+domain, RMSE)


if __name__ == '__main__':
    #change to 'stemming', 'beroep' or 'inspanningstolerantie's
    main('lopen')
    






    
