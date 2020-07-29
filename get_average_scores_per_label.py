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
    #create empty dict
    annotator_dict = dict()
    for index, tag in enumerate(df[columname]):
        #check where label is
        if tag != '_':
            #save file_id of that location
            filename = df.iloc[index]['file_id']
            new_list = []
            #begin extracting first tag for cells with double tags
            if ('|') in tag:
                nametag = tag.split('|')[0]
                keynametag = nametag[:-3]
                list_range = []
                for row_index,row in df.iterrows():
                    if row['file_id'] != filename:
                        continue
                    else:
                        if nametag in str(row[columname]):
                            list_range.append(row_index[5:])
                #get span
                if len(list_range)>1:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[-1])

                else:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[0])
                
                #create list with info (label, file_id, begin_span, end_span)
                keyname = keynametag + '_' + str(df.iloc[index]['file_id']) + '_' + str(begintoken) + '_' + str(endtoken)
                new_list.append(keynametag)
                new_list.append(df.iloc[index]['file_id'])
                new_list.append(begintoken)
                new_list.append(endtoken)
                
                #add list to dict with identifier as key
                if keyname not in annotator_dict:
                    annotator_dict[keyname] = new_list
                else:
                    continue
            
            #begin extracting second tag for cells with double tags
            if ('|') in tag:
                nametag = tag.split('|')[1]
                keynametag = nametag[:-3]
                
                list_range = []
                for row_index,row in df.iterrows():
                    if row['file_id'] != filename:
                        continue
                    else:
                        if nametag in str(row[columname]):
                            list_range.append(row_index[5:])
                    
                if len(list_range)>1:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[-1])

                else:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[0])
                    
                keyname = keynametag + '_' + str(df.iloc[index]['file_id']) + '_' + str(begintoken) + '_' + str(endtoken)
                new_list.append(keynametag)
                new_list.append(df.iloc[index]['file_id'])
                new_list.append(begintoken)
                new_list.append(endtoken)
                
                if keyname not in annotator_dict:
                    annotator_dict[keyname] = new_list
                else:
                    continue
                    
            #extracting tag when there is just one tag in a cell:
            else:
                keynametag = tag[:-3]
                list_range = []
                for row_index,row in df.iterrows():
                    if row['file_id'] != filename:
                        continue
                    else:
                        if row[columname] == tag:
                            list_range.append(row_index[5:])

                if len(list_range)>1:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[-1])

                else:
                    begintoken = int(list_range[0])
                    endtoken = int(list_range[0])

                keyname = keynametag + '_' + str(df.iloc[index]['file_id']) + '_' + str(begintoken) + '_' + str(endtoken)
                new_list.append(keynametag)
                new_list.append(df.iloc[index]['file_id'])
                new_list.append(begintoken)
                new_list.append(endtoken)

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
    dict4 = get_annotator_dict(df, 'labels_'+annotator_names[3])
    dict5 = get_annotator_dict(df, 'labels_'+annotator_names[4])
    dict6 = get_annotator_dict(df, 'labels_'+annotator_names[6])
    dict7 = get_annotator_dict(df, 'labels_'+annotator_names[7])
    dict8 = get_annotator_dict(df, 'labels_'+annotator_names[8])
    
    # merge all dictionaries without taking any double ones
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value
    for key, value in dict3.items():
        if key not in dict1:
            dict1[key] = value
    for key, value in dict4.items():
        if key not in dict1:
            dict1[key] = value
     for key, value in dict5.items():
        if key not in dict1:
            dict1[key] = value
     for key, value in dict7.items():
        if key not in dict1:
            dict1[key] = value 
     for key, value in dict8.items():
        if key not in dict1:
            dict1[key] = value           
            
    # create a dataframe from the dictionaries
    new_df = pd.DataFrame.from_dict(dict1, orient = 'index')
    new_df.columns = ['label', 'file_id', 'begin_span', 'end_span', '2nd_label', '2nd_file_id', 'begin_2nd_label', 'end_2nd_label']
    new_df[annotator_names[0]] = 0
    new_df[annotator_names[1]] = 0
    new_df[annotator_names[2]] = 0
    new_df[annotator_names[3]] = 0
    new_df[annotator_names[4]] = 0
    new_df[annotator_names[5]] = 0
    new_df[annotator_names[6]] = 0
    new_df[annotator_names[7]] = 0
    
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
    annotator_names = ['avelli', 'bos', 'katsburg', 'meskers', 'opsomer', 'swartjes', 'vanderpas', 'vervaart']
    
    # read in Quirine's df
    df = pd.read_pickle('token_level_df_all_annotators_all_docs.pkl')
    new_df = get_dataframe(df, annotator_names)
    
    # get personal dicts per annotator
    dict_a1 = get_annotator_dict(df, 'labels_'+annotator_names[0])
    dict_a2 = get_annotator_dict(df, 'labels_'+annotator_names[1])
    dict_a3 = get_annotator_dict(df, 'labels_'+annotator_names[2])
    dict_a4 = get_annotator_dict(df, 'labels_'+annotator_names[3])
    dict_a5 = get_annotator_dict(df, 'labels_'+annotator_names[4])
    dict_a6 = get_annotator_dict(df, 'labels_'+annotator_names[5])
    dict_a7 = get_annotator_dict(df, 'labels_'+annotator_names[6])
    dict_a8 = get_annotator_dict(df, 'labels_'+annotator_names[7])
    
    # score the annotations in the df
    new_df = find_matches(new_df, annotator_names[0], dict_a1)
    new_df = find_matches(new_df, annotator_names[1], dict_a2)
    new_df = find_matches(new_df, annotator_names[2], dict_a3)
    new_df = find_matches(new_df, annotator_names[3], dict_a4)
    new_df = find_matches(new_df, annotator_names[4], dict_a5)
    new_df = find_matches(new_df, annotator_names[5], dict_a6)
    new_df = find_matches(new_df, annotator_names[6], dict_a7)
    new_df = find_matches(new_df, annotator_names[7], dict_a8)
    
    # sum the scores and put in new column
    new_df['score'] = new_df[annotator_names[0]]+new_df[annotator_names[1]]+new_df[annotator_names[2]]+new_df[annotator_names[3]]+new_df[annotator_names[4]]+new_df[annotator_names[5]]+new_df[annotator_names[6]]+new_df[annotator_names[7]]+new_df[annotator_names[8]]
    new_df.to_excel('excel_with_scores.xlsx')
    
    # extract average scores per label
    print('average scores domains:')
    print('average score Stemming: '+ str(get_average_score_per_label(new_df, 'Stemming')))
    print('average score Lopen: '+ str(get_average_score_per_label(new_df, 'Lopen')))
    print('average score Beroep en Werk: '+str(get_average_score_per_label(new_df, 'Beroep')))
    print('average score Inspanningstolerantie: '+str(get_average_score_per_label(new_df, 'Inspanningstolerantie')))
    print()
    print('average scores levels:')
    print('average score FAC 0: '+ str(get_average_score_per_label(new_df, 'FAC 2')))
    print('average score FAC 1: '+ str(get_average_score_per_label(new_df, 'FAC 1')))
    print('average score FAC 2: '+ str(get_average_score_per_label(new_df, 'FAC 2')))
    print('average score FAC 3: '+ str(get_average_score_per_label(new_df, 'FAC 2')))
    print('average score FAC 4: '+ str(get_average_score_per_label(new_df, 'FAC 4')))
    print('average score FAC 5: '+ str(get_average_score_per_label(new_df, 'FAC 5')))
    print()
    print('average score STM 0: '+ str(get_average_score_per_label(new_df, 'STM 0')))
    print('average score STM 1: '+ str(get_average_score_per_label(new_df, 'STM 1')))
    print('average score STM 2: '+ str(get_average_score_per_label(new_df, 'STM 2')))
    print('average score STM 3: '+ str(get_average_score_per_label(new_df, 'STM 3')))
    print('average score STM 4: '+ str(get_average_score_per_label(new_df, 'STM 4')))
    print('average score STM 5: '+ str(get_average_score_per_label(new_df, 'STM 5')))
    print()
    print('average score INS 0: '+ str(get_average_score_per_label(new_df, 'INS 0')))
    print('average score INS 1: '+ str(get_average_score_per_label(new_df, 'INS 1')))
    print('average score INS 2: '+ str(get_average_score_per_label(new_df, 'INS 2')))
    print('average score INS 3: '+ str(get_average_score_per_label(new_df, 'INS 3')))
    print('average score INS 4: '+ str(get_average_score_per_label(new_df, 'INS 4')))
    print()
    print('average score BER 0: '+ str(get_average_score_per_label(new_df, 'BER 0')))
    print('average score BER 1: '+ str(get_average_score_per_label(new_df, 'BER 1')))
    print('average score BER 2: '+ str(get_average_score_per_label(new_df, 'BER 2')))
    print('average score BER 3: '+ str(get_average_score_per_label(new_df, 'BER 3')))
    print('average score BER 4: '+ str(get_average_score_per_label(new_df, 'BER 4')))
    print()
    print('average score remaining labels')
    print('average score stm\_reaction: '+ str(get_average_score_per_label(new_df, 'reaction')))
    print('average score type\_Background: '+ str(get_average_score_per_label(new_df, 'Background')))
    print('average score view\_Patient: '+ str(get_average_score_per_label(new_df, 'Patient')))
    print('average score view\_Thirdparty: '+ str(get_average_score_per_label(new_df, 'Third')))
    print('average score type\_Implicit: '+ str(get_average_score_per_label(new_df, 'Implicit')))
    
if __name__ == "__main__":
    main()

    


