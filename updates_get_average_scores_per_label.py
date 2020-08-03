'''
This code takes a dataframe with annotations and returns a dataframe with annotation spans and scores per annotator and average scores for each label. 
@author: Stella Verkijk
'''

import pandas as pd

class Span:
    """
    class containing information about the Span
    """

    def __init__(self,
                 begin, end, token):
        self.begintoken = begin
        self.endtoken = end
        self.token = token

def get_span_for_tag (df, annotator, filename, nametag):
    list_range = []
    token = ''
    for row_index, row in df.iterrows():
        if row['file_id'] != filename:
            continue
        else:
            if nametag in str(row[annotator]):
                token += ' '+row['token']
                list_range.append(row_index[5:])
    #get span
    if len(list_range)>1:
        begintoken = int(list_range[0])
        endtoken = int(list_range[-1])

    else:
        begintoken = int(list_range[0])
        endtoken = int(list_range[0])
    span = Span(begintoken, endtoken, token)
    return span

def make_keyname (df, filename, keynametag, span):
    #create list with info (label, file_id, begin_span, end_span)
    keyname = keynametag + '_' + filename + '_' + str(span.begintoken) + '_' + str(span.endtoken)
    return keyname
             

def get_annotator_dict(df, annotator):
    '''
    Create a dictionary with all the labels and their spans with token index for one annotator
    :param df: a pandas dataframe 
    :param annotator: str (annotator's last name)
    '''
    #create empty dict
    annotator_dict = dict()
    
    for index, tag in enumerate(df[annotator]):
        try:
        #check where label is
            tag = str(tag)
            if tag != '_':
                #save file_id of that location
                filename = df.iloc[index]['file_id']
                new_list = []
                if ('|') in tag:
                    #begin extracting first tag for cells with double tags
                    nametag = tag.split('|')[0]
                    keynametag = tag[:-3]
                    span = get_span_for_tag(df, annotator, filename, nametag)
                    keyname = make_keyname(df, filename, keynametag, span)
                    new_list.append(keynametag)
                    new_list.append(filename)
                    new_list.append(span.begintoken)
                    new_list.append(span.endtoken)
                    new_list.append(span.token)
                    #add list to dict with identifier as key
                    if keyname not in annotator_dict:
                        annotator_dict[keyname] = new_list
                    else:
                        continue
                        
                    #begin extracting second tag for cells with double tags
                    nametag = tag.split('|')[1]
                    keynametag = tag[:-3]
                    span = get_span_for_tag(df, annotator, filename, nametag)
                    keyname = make_keyname(df, filename, keynametag, span)
                    new_list.append(keynametag)
                    new_list.append(filename)
                    new_list.append(span.begintoken)
                    new_list.append(span.endtoken)
                    new_list.append(span.token)
                    #add list to dict with identifier as key
                    if keyname not in annotator_dict:
                        annotator_dict[keyname] = new_list
                    else:
                        continue
                        
                #extracting tag when there is just one tag in a cell:
                else:
                    keynametag = tag[:-3]
                    span = get_span_for_tag(df, annotator, filename, tag)
                    keyname = make_keyname(df, filename, keynametag, span)
                    new_list.append(keynametag)
                    new_list.append(filename)
                    new_list.append(span.begintoken)
                    new_list.append(span.endtoken)
                    new_list.append(span.token)
                    if keyname not in annotator_dict:
                        annotator_dict[keyname] = new_list
                    else:
                        continue
                        
        except KeyError:
            print('KeyError: {} does not exist in the table.'.format(annotator))
            continue
    
    return(annotator_dict)


def get_dataframe(df, annotator_names): 
    '''
    Create a dataframe with all possible labels and spans from all annotators 
     :param df: a pandas dataframe
     :param annotator_names: a list with strings which are in accordance with the columnnames of the df (annotators' last names)
    '''
    mergeddict = dict()
    # get dictionaries per annotator
    for annotator in annotator_names:
        try:
            dicta = get_annotator_dict(df, 'labels_'+annotator)
            if len(dicta)>0:
                for key, value in dicta.items():
                    if key not in mergeddict:
                        mergeddict[key] = value 
            else:
                print('no labels for annotator:', annotator)
        except KeyError:
            print('KeyError: {} does not exist in the table.'.format(annotator))
            continue                

    new_df = pd.DataFrame.from_dict(mergeddict, orient = 'index')
    new_df.columns = ['label', 'file_id', 'begin_span', 'end_span', 'token', '2nd_label', '2nd_file_id', 'begin_2nd_label', 'end_2nd_label', 'unknown']
    
    for annotator in annotator_names:
        # create a dataframe from the dictionaries
        new_df[annotator] = 0

    new_df.info()
    return(new_df)

def find_matches(df, annotator, dictionary):
    '''
    Score labels that a certain annotator annotated with 1 in the df by finding matches between the identifiers in the df and the identifiers in the personal dictionary of the annotator
    '''

    for key, value in dictionary.items():
        for row_index, row in df.iterrows():
            if key == row_index:
                df.at[row_index, annotator] = 1                
    
    return(df)

def get_average_score_per_label(df, label):
    '''
    Get average scores per label by summing all scores in the 'score' column from the df and dividing it with the amount of total scores
    :param df: a pandas dataframe
    :param label: str
    '''
    score_list = []
    for index, tag in enumerate(df['label']):
        if label in tag:
            score_list.append(df.iloc[index]['score'])

    sum_scores = sum(score_list)
    average_score = sum_scores / len(score_list)
    return(average_score)
