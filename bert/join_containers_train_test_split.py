import pickle
from class_definitions import Annotation, BertContainer
from pathlib import Path
import torch



if __name__ == '__main__':
    input_foldername = '../../Non_covid_data_15oct/traindata_batch1/' 
    output_filename = '../../Non_covid_data_15oct/train_data.pkl'


    input_foldername = Path(input_foldername)
    output_filename = Path(output_filename)
    
    file_list = input_foldername.glob("*.pkl")
    
    
    light_Containers_list = []
    
    for input_file in file_list:
        with input_file.open("rb") as pkl_file:
            data = pickle.load(pkl_file)
        
        counter = 0
        for BertContainer in data:
            counter += 1
            full_encoding = BertContainer.encoding
            last_4_layers = full_encoding[-4:][0]
            
            #sentence_embedding = torch.mean(last_4_layers, dim=0)
            
            
            # Rewrite BertContainer
            BertContainer.encoding = last_4_layers
            
            light_Containers_list.append(BertContainer)
            
    with output_filename.open("ab") as outfile:
        pickle.dump(light_Containers_list, outfile)
                
     
    # To read out file produced
    #with output_filename.open("rb") as infile:
    #    sample_data = pickle.load(infile)
        
    #for BertContainer in sample_data:
    #    print(BertContainer.annotator)
    #    print(BertContainer.key)

    
