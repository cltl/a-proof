import pickle
from class_definitions import Annotation, BertContainer
from pathlib import Path
import torch
from datetime import datetime


def create_annot_set(data):
    annot_set = set()
    for BertContainer in data:
        for annot in BertContainer.annot:
            annot_set.add(annot.label)
            if annot.label == "disregard\_file":
                break
    return annot_set
        

if __name__ == '__main__':
    # From directory creates single pkl file containing all containers of directory and skips disregarded files
    input_foldername = '../../Non_covid_data_15oct/traindata_batch1/' 
    output_filename = '../../Non_covid_data_15oct/train_data_batch1_disregard_removed.pkl'
    
    #input_foldername = "../sample_data/BERTContainers/"

    print(datetime.now())


    input_foldername = Path(input_foldername)
    output_filename = Path(output_filename)
    
    file_list = input_foldername.glob("*.pkl")
    
    
    light_Containers_list = []
    
    for input_file in file_list:
        with input_file.open("rb") as pkl_file:
            data = pickle.load(pkl_file)
        
        annot_set = create_annot_set(data)
            
        if "disregard\_file" in annot_set:
            continue
        
        for BertContainer in data:
            full_encoding = BertContainer.encoding
            last_4_layers = full_encoding[-4:][0]
            
            #sentence_embedding = torch.mean(last_4_layers, dim=0)
            
            
            # Rewrite BertContainer
            BertContainer.encoding = last_4_layers
            
            light_Containers_list.append(BertContainer)
            
    with output_filename.open("ab") as outfile:
       pickle.dump(light_Containers_list, outfile)
                
    print(datetime.now())
     
    # To read out file produced
    #with output_filename.open("rb") as infile:
    #    sample_data = pickle.load(infile)
        
    #for BertContainer in sample_data:
    #    print(BertContainer.annotator)
    #    print(BertContainer.key)

    
