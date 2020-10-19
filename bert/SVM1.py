"""
First SVM implementation
"""

from glob import glob
import pickle
from class_definitions import Annotation, BertContainer
import torch
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score



def completeReader(input_dir):
    """
    Takes pkl files, extract features and creates dict
    """
    suffix = ".pkl"
    paths = []
    for path in glob(f'{input_dir}/*{suffix}'):
        paths.append(path)
    
    list_dicts = []
    list_labels = []
    for path in paths:
        pkl_file=open(path, "rb")
        info_note = pickle.load(pkl_file)
        for container in info_note:
            feature_dict = {}
            key = container.key 
            feature_dict['key'] = key
            annotator = container.annotator
            feature_dict['annotator'] = annotator
            sen_id = container.sen_id
            feature_dict['sen_id']= sen_id
            sen = container.sen
            feature_dict['sen'] = sen
            encoding = container.encoding
            hs = encoding[-4:][0]
            sen_embedding = torch.mean(hs, dim=0)
            feature_dict['encoding'] = sen_embedding
            list_dicts.append(feature_dict)
            
            list_annos = []
            annot = container.annot
            if len(annot) == 0:
                list_annos.append('NULL')
            else:
                for anno in annot:
                    tokens = anno.tokens
                    label = anno.label
                    list_annos.append(tokens,label)
            list_labels.append(list_annos)

        
    return(list_dicts, list_labels)

def lightWeightReader(input_dir):
    """
    Takes pkl files, extract features and creates dict
    """
    suffix = ".pkl"
    paths = []
    for path in glob(f'{input_dir}/*{suffix}'):
        paths.append(path)
    
    list_dicts = []
    list_labels = []
    for path in paths:
        pkl_file=open(path, "rb")
        info_note = pickle.load(pkl_file)
        for container in info_note:
            feature_dict = {}
            encoding = container.encoding
            hs = encoding[-4:][0]
            sen_embedding = torch.mean(hs, dim=0)
            feature_dict['encoding'] = sen_embedding
            list_dicts.append(feature_dict)
            
            list_annos = []
            annot = container.annot
            if len(annot) == 0:
                list_annos.append('NULL')
            else:
                for anno in annot:
                    label = anno.label
                    #Maybe try to only append "type\\_Background" for binary classification?
                    list_annos.append(label)
            list_labels.append(list_annos)
        
    return(list_dicts, list_labels)

def crossvalSVM(train_dict, train_labels):  
    """
    This function is just a dummy it does NOT WORK
    """
    clf = svm.SVC(kernel='linear', C=1)
    scores = cross_val_score(clf, train_dict, train_labels, cv=10)
    return(scores)


def main():
    
    #train_dir = ".."
    #test_dir = ".."
    #train_dict = extract_features_labels(train_dir)[0]
    #train_labels = extract_features_labels(train_dir)[1]
    #test_data = extract_features_labels(test_dir)[0]
    #gold_labels = extract_features_labels(test_dir[1]

    small_test_dir = "test_subset" # = folder with 6 pkl files
    train_dictionary = lightWeightReader(small_test_dir)[0]
    train_labels = lightWeightReader(small_test_dir)[1]

    scores = crossvalSVM(train_dictionary, train_labels)
    print(scores)

if __name__ == "__main__":
    main()
    
    
    #TO DO:
    #Eliminate docs with the label "disregard\_file"
    

