""" 
To run on linux server first enter bert environment: source bert/bin/activate
"""

import torch
from transformers import BertTokenizer, BertModel # change
import numpy as np
import pickle
from class_definitions import Annotation, BertContainer
from pathlib import Path


def read_tsv(filepath):
    """
    Reads tsv file. Skips lines starting with '#' (except for '#Text=') and empty lines.
    :param filepath: filepath to tsv file
    :return: data in list of list.
    """
    with filepath.open(mode='r') as infile:
        data = []
        for line in infile:
            # Remove unnecessary lines
            if line.startswith('#') and not line.startswith('#Text='):
                continue
            if line.startswith('\t'):
                continue
            # Remove '\n' at end of line
            line = line[:-1]
            # Split line on tab
            line = line.split('\t')

            data.append(line)
    return data

def get_sentence_lvl(data):
    """
    Creates list of lists on sentence level. Each element of resulting list is a list where the first element
    is a str of the sentence. The second element is a list of the rows of tokens. 
    :param data: List of list with sentence elements starting with '#Text='
    :return: List of list. Text separated by sentence.
    """
    text_list = []
    sentence_list = []

    for index, line_list in enumerate(data):
        # If line is whole sentence
        if line_list[0].startswith('#'):
            # If not the first sentence
            if index != 0:
                # Add info from previous sentence
                text_list.append(sentence_list)
            # Create empty sentence list and append string
            sentence_list = []
            sentence_list.append(line_list[0][6:])
        # If line is last in text
        elif index == len(data) - 1:
            sentence_list.append(line_list)
            text_list.append(sentence_list)

        # Else append token level info
        else:
            sentence_list.append(line_list)
    return text_list

def get_labels_tokens(sentence_obj):
    """
    Collects tokens related to same label. First loops through all tokens in sentence to collect all labels in a set. 
    Then loops through labels and through all tokens in a sentence to gather the tokens with that label. 
    This code could be made more efficient.
    :param sentence: List containing rows which belong to a single sentence.
    :return: dictionary of labels with matching tokens {'label_id': [('t1', 'token_1'), ('t2', 'token_2')], ...}
    """
    # Define set to collect labels in this sentence
    label_set = set()
    # For token in sentence
    for index, row in enumerate(sentence_obj):
        # Continue only if row contains single token (so is not the full sentence) and has a label
        if type(row) == list and len(row) >= 4 and row[3] != '_':
            # Split if there are multiple labels for token. If-statement is for bug fix
            if type(row[3]) == str:
                row[3] = row[3].split('|')
            # Add label to set
            label_set.update(row[3])
    
    # Create dictionary to match label to tokens
    label_token_dict = dict()
    # Loop through labels and create dictionary entry
    for label in label_set:
        label_token_dict[label] = []
        # Loop through sentence, if the row has the label, then create token tuple and add to dict
        for index, row in enumerate(sentence_obj):
            if len(row) > 3 and label in row[3]:
                token_tuple = ('t' + str(index), row[2])
                label_token_dict[label].append(token_tuple)

    return label_token_dict


def get_key_and_annotator(filepath):
    """
    Extract key and annotator name from file name
    :param filepath:
    :return:
    """

    annotator = filepath.stem
    file_id = filepath.parent.stem

    return file_id, annotator


def get_BERTje_encoding(sentence):
    #import model
    bertje='wietsedv/bert-base-dutch-cased'
    bertje_tokenizer = BertTokenizer.from_pretrained(bertje)
    bertje_model = BertModel.from_pretrained(bertje, output_hidden_states = True)
    
    #get progressed inputs
    marked_text = '[CLS] ' + sentence + ' [SEP]'
    tokenized_text = bertje_tokenizer.tokenize(marked_text)
    token_ids = bertje_tokenizer.convert_tokens_to_ids(tokenized_text)
    segment_ids = [1] * len(tokenized_text)
    
    #convert inputs to PyTorch tensors
    segments_tensors = torch.tensor([segment_ids])
    tokens_tensor = torch.tensor([token_ids])
  
    #run sentence through BERTje and collect all hidden states from all 12 layers
    with torch.no_grad():
        outputs = bertje_model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]
    
    #sum last 4 layers to get sentence embedding 
    #token_vecs = hidden_states[-4:][0]
    #sentence_embedding = torch.mean(token_vecs, dim=0)
    
    return(hidden_states)

    

if __name__ == '__main__':
    """    
    writes a list with dictionaries per sentence to pkl file
    """
    # Define folder path to data
    #folderpath_in = "../sample_data/INCEpTION_output/"
    #folderpath_out = "../sample_data/BERTContainers/"
    
    folderpath_in = "../../Non_covid_data_15oct/Inception_Output_Batch1/"
    folderpath_out = "../../Non_covid_data_15oct/BertContainers_Batch1/"

    folderpath_in = Path(folderpath_in)
    file_list = folderpath_in.rglob('*.tsv')

    for filepath in file_list:
        # Read in data and get it in correct format
        data = read_tsv(filepath)
        text_list = get_sentence_lvl(data)
        file_id, annotator = get_key_and_annotator(filepath)

        all_dicts = []
        # For every sentence in the text
        for sentence_obj in text_list:
            # Extract sentence, sentence_id and encoding
            if sentence_obj[0] != str:
                sen='-'
            else:
                sen = sentence_obj[0]
            sen_id = sentence_obj[1][0].split('-')[0]
            key = file_id + sen_id
            encoding = get_BERTje_encoding(sen) # change
            #encoding = 12345

            # Define BertContainer instance
            instance = BertContainer(key, annotator, sen_id, sen, encoding)

            # Create label dictionary and loop through it

            label_dict = get_labels_tokens(sentence_obj)
            for label, token_list in label_dict.items():
                label_clean = label.split('[')[0]
                # Add the labels to the BertContainer instance
                anno = Annotation(token_list, label_clean)
                instance.add_anno(anno)


            all_dicts.append(instance)


        filename_out = folderpath_out +"Container_"+key+"__"+annotator+".pkl"
        fil = open(filename_out, 'wb')
        pickle.dump(all_dicts, fil)
        fil.close()
