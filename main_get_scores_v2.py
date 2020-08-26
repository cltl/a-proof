import pandas as pd
#from pathlib import Path
#from updates_join_annotations import open_df_from_tsv
#import updates_get_average_scores_per_label as scores

def change_labels_to_list_format(df):
    for column_name in df.columns:
        if column_name.startswith('labels_'):
            # to avoid the function repeating itself:
            if type(df[column_name][0]) == list:
                continue
            original_labels = df[column_name]

            cleaned_labels = []
            for label in original_labels:
                if '|' in str(label):
                    label_split = label.split('|')
                else:
                    label_split = [label]
                cleaned_labels.append(label_split)

            df[column_name] = cleaned_labels
    return df


def get_dict_per_file_per_annotator(df, annotator, filename):
    df_filtered = df.loc[df['file_id'] == filename][['token_d_id', 'token', 'labels_{}'.format(annotator)]]

    labels_per_doc_per_annotator_dict = dict()

    for index, row in df_filtered.iterrows():
        if row['labels_{}'.format(annotator)] != ['_']:

            for label_and_id in row['labels_{}'.format(annotator)]:
                if label_and_id in labels_per_doc_per_annotator_dict:
                    labels_per_doc_per_annotator_dict[label_and_id]['indices'].append(row['token_d_id'])
                    labels_per_doc_per_annotator_dict[label_and_id]['tokens'].append(row['token'])
                else:
                    labels_per_doc_per_annotator_dict[label_and_id] = {'indices': [row['token_d_id']],
                                                                       'tokens': [row['token']],
                                                                       'file_id': filename,
                                                                       'annotator': annotator}

    return labels_per_doc_per_annotator_dict

def join_dicts_on_label_and_index(dict_of_dicts):

    gathered_dict = dict()

    for uncleaned_dict in dict_of_dicts.values():
        for key, inner_dict in uncleaned_dict.items():

            start = inner_dict['indices'][0]
            if inner_dict['indices'] == 1:
                end = inner_dict['indices'][0]
            else:
                end = inner_dict['indices'][-1]


            cleaned_inner_dict = {'file_id': inner_dict['file_id'],
                                    'start_index': start,
                                  'end_index': end,
                                 'tokens': inner_dict['tokens'],
                                 'annotators': set([inner_dict['annotator']])}
            splitkey = str(key).split('[')[0]
            cleaned_key = '_'.join([inner_dict['file_id'], str(start), str(end), splitkey])

            if cleaned_key in gathered_dict:
                gathered_dict[cleaned_key]['annotators'].add(inner_dict['annotator'])
            else:
                gathered_dict[cleaned_key] = cleaned_inner_dict

    return gathered_dict

def main():
    # DEFINE PATHS
    input_file = './sample_data/token_level_df.pkl'       # Input pkl containing df of tokens with labels for all annotators
    output_file = './sample_data/label_level_df.pkl'      # Output pkl
    output_file_xlsx = './sample_data/label_level_df.xlsx' # Output xlsx
    
    # input_file = './../../data/processed_data/week_30/token_level_df.pkl'      # Input pkl containing df of tokens with labels for all annotators
    # output_file = './../../data/processed_data/week_30/label_level_df.pkl'      # Output pkl
    # output_file_xlsx = './../../data/processed_data/week_30/label_level_df.xlsx'      # Output xlsx

    df = pd.read_pickle(input_file)
    annotator_names = ['avelli', 'bos', 'meskers']
    # annotator_names = ['avelli', 'bos', 'katsburg', 'meskers', 'opsomer', 'swartjes', 'vanderpas', 'vervaart']

    # Change format of labels in f'labels_{name}' columns to list format
    df = change_labels_to_list_format(df)

    # Creates dictionary for each file and each annotator and joins in a dictionary with keys in format 'avelli_2503'
    # Filters df on filename for each annotator, then loops through all rows.
    dict_of_dicts_per_file_annotator = dict()
    for annotator in annotator_names:
        for file_id in set(df['file_id']):
            dict_of_dicts_per_file_annotator['{}_{}'.format(annotator, file_id)] = get_dict_per_file_per_annotator(df, annotator, file_id)

    # Join the dictionaries to form one cleaned dictionary with identifiers containing file_id and start, end index
    data = join_dicts_on_label_and_index(dict_of_dicts_per_file_annotator)

    # Creates df to write to pkl
    df_new = pd.DataFrame.from_dict(data, orient='index')
    df_new['annotator_count'] = df_new.apply(lambda row: len(row['annotators']), axis=1)

    df_new.sort_values(by=['file_id', 'start_index', 'end_index'])

    df_new.to_pickle(output_file)
    df_new.to_excel(output_file_xlsx)

if __name__ == '__main__':
    main()
