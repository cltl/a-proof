'''
This code takes a dataframe with annotations and returns a dataframe with annotation spans and scores per annotator and average scores for each label. 
@author: Stella Verkijk
'''

import pandas as pd

def get_annotator_dict(df, columname):
    '''
    Create a dictionary with all the labels and their spans with token index for one annotator
    :param df: a pandas dataframe 
    :param columname: str (annotator's last name)
    '''
    annotator_dict = dict()
    for index, tag in enumerate(df[columname]):
        # find location of a label
        if tag != '_':
            #save the file this label belongs to
            filename = df.iloc[index]['file_id']
            new_list = []
            # split the double tags and use the first label
            if ('|') in tag:
                nametag = tag.split('|')[0]
                keynametag = nametag[:-3]
                list_range = []
                # save span
                for row_index,row in df.iterrows():
                    if row['file_id'] != filename:
                        continue
                    else:
                        if nametag in str(row[columname]):
                            list_range.append(row_index[5:])

            else:
                keynametag = tag[:-3]
                list_range = []
                for row_index,row in df.iterrows():
                    if row['file_id'] != filename:
                        continue
                    else:
                        if row[columname] == tag:
                            list_range.append(row_index[5:])
                            
            # get first and last index number from list
            if len(list_range)>1:
                begintoken = int(list_range[0])
                endtoken = int(list_range[-1])

            else:
                begintoken = int(list_range[0])
                endtoken = int(list_range[0])
            
            # create identifier
            keyname = keynametag + '_' + str(df.iloc[index]['file_id']) + '_' + str(begintoken) + '_' + str(endtoken)
            
            # create a list with all information needed
            new_list.append(keynametag)
            new_list.append(df.iloc[index]['file_id'])
            new_list.append(begintoken)
            new_list.append(endtoken)
            
            # avoid double identifiers and add each list to a dictionary with its identifier as its key
            if keyname not in annotator_dict:
                annotator_dict[keyname] = new_list
            else:
                continue
    return(annotator_dict)


def get_dataframe(df, annotator_names): 
    '''
    Create a dataframe with all possible labels and spans from all annotators 
     :param df: a pandas dataframe
     :param annotator_names: a list with strings which are in accordance with the columnnames of the df (annotators' last names)
    '''
    
    # get dictionaries per annotator
    dict1 = get_annotator_dict(df, 'labels_'+annotator_names[0])
    dict2 = get_annotator_dict(df, 'labels_'+annotator_names[1])
    dict3 = get_annotator_dict(df, 'labels_'+annotator_names[2])
    
    # merge all dictionaries without taking any double ones
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value

    for key, value in dict3.items():
        if key not in dict1:
            dict1[key] = value
    
    # create a dataframe from the dictionaries
    new_df = pd.DataFrame.from_dict(dict1, orient = 'index')
    new_df.columns = ['label', 'file_id', 'begin_span', 'end_span']
    new_df[annotator_names[0]] = 0
    new_df[annotator_names[1]] = 0
    new_df[annotator_names[2]] = 0
    
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

def main():
    
    # list annotator names
    annotator_names = ['avelli', 'bos', 'meskers']
    
    # read in Quirine's df
    df = pd.read_pickle('token_level_df_all_annotators_all_docs.pkl')
    new_df = get_dataframe(df, annotator_names)
    
    # get personal dicts per annotator
    dict_a1 = get_annotator_dict(df, 'labels_'+annotator_names[0])
    dict_a2 = get_annotator_dict(df, 'labels_'+annotator_names[1])
    dict_a3 = get_annotator_dict(df, 'labels_'+annotator_names[2])
    
    # score the annotations in the df
    new_df = find_matches(new_df, annotator_names[0], dict_a1)
    new_df = find_matches(new_df, annotator_names[1], dict_a2)
    new_df = find_matches(new_df, annotator_names[2], dict_a3)
    
    # sum the scores and put in new column
    new_df['score'] = new_df[annotator_names[0]]+new_df[annotator_names[1]]+new_df[annotator_names[2]]
    #new_df.to_excel('third_run.xlsx')
    
    # extract average scores per label
    print('average score Stemming: '+ str(get_average_score_per_label(new_df, 'Stemming')))
    print('average score Lopen: '+ str(get_average_score_per_label(new_df, 'Lopen')))
    print('average score FAC 1: '+ str(get_average_score_per_label(new_df, 'FAC 1')))
    print('average score FAC 2: '+ str(get_average_score_per_label(new_df, 'FAC 2')))
    print('average score FAC 4: '+ str(get_average_score_per_label(new_df, 'FAC 4')))
    print('average score stm\_reaction: '+ str(get_average_score_per_label(new_df, 'reaction')))
    print('average score type\_Background: '+ str(get_average_score_per_label(new_df, 'Background')))
    
if __name__ == "__main__":
    main()

    


