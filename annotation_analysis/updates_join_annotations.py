#import numpy
import pandas as pd
from pathlib import Path

def open_df_from_tsv(filename):
    """
    Creates pd.DataFrame from tsv file in conll format.
    """
    # Make pathlib type

    filename = Path(filename)

    # Get document id and annotator name from filename
    doc_id = filename.parent.stem[-4:]
    annotator = filename.stem

    # Read file
    data = []
    #ata2= []
    with (filename).open() as infile:
        #with open(filename, 'r', encoding = 'utf-8') as infile:
        for row in infile:
            # Skip rows starting with #
            if row.startswith('#'):
                continue
            # Remove '\n' at end of row and traling whitespaces
            row = row[:-1].strip()
            # Split on tab
            split_row = row.split('\t')  
            # Skip if empty row
            if split_row[0] == '':
                continue

            # If length is not 5 (some files had only 3 columns), append columns with '_'
            if len(split_row) == 5:
                split_row.extend(['_'])
            elif len(split_row) == 4:
                #print(len(split_row))
                #print(filename)
                split_row.extend(['_', '_'])
            
            elif len(split_row) == 3:
                #print(split_row)
                split_row.extend(['_', '_', '_'])
                #continue
            elif len(spit_row!=6):
                # print(len(split_row))
                # print(split_row)
                continue
            data.append(split_row)

    #print(data)
    
    # Create pd.DataFrame
    df = pd.DataFrame(data=data, columns=['sent_token_id', 'char_id', "token", "labels_" +annotator, "relation_" +annotator,'temp'])
    #print(df)
    # Add column containing file_id
    df = df.assign(file_id=doc_id)
    
    # Split sent_id and token_id (in sentence) and drop orginal and char_id
    df['sent_id'] = 0
    df['token_s_id'] = 0
    df['doc_token_id'] = 0 
    df['sent_id'] = df.apply(lambda row: row['sent_token_id'].split('-')[0], axis=1)
    df['token_s_id'] = df.apply(lambda row: row['sent_token_id'].split('-')[1], axis=1)
    df.drop(['sent_token_id', 'char_id'], axis=1, inplace=True)
    #df.drop(['temp1', 'temp2', 'temp3'], axis=1, inplace=True)
    
    # Create column containing token id (from start of doc)
    df.reset_index(drop=False, inplace=True)
    df.rename({'index': 'token_d_id'}, axis=1, inplace=True)
    
    # Create index from file id and token id (from start of doc)
    df['doc_token_id'] = df.apply(lambda row: str(row['file_id']) + '_'+ str(row['token_d_id']), axis=1)
    df.set_index('doc_token_id', inplace=True)

    return df


def main():
    # DEFINE PATHS
    folder_path = '../sample_data/INCEpTION_output'
    output_pkl_path = '../sample_data/token_level_df.pkl'


    for index, filename in enumerate(Path(folder_path).glob('**/*.tsv')):
        """
        Creates pd.DataFrame by joining files from different annotators and different documents to one
        large df
        """
        # Extract annotator name from doc
        annotator = filename.stem

        # Use the first file to create df
        if index == 0:
            df = open_df_from_tsv(filename)

        # Update df with new files
        else: 
            # Create temporary df
            df_temp = open_df_from_tsv(filename)
            
            # if file is already in rows, and annotator is already in colmumns, then update
            if df_temp['file_id'][1] in set(df['file_id']) and ('labels_'+annotator) in df.columns:
                df.update(df_temp)
            # Elif file is in rows (and annotator not yet in columns), then concat with axis=1
            elif df_temp['file_id'][1] in set(df['file_id']):
                df_temp.drop(['token_d_id', 'token', 'file_id', 'sent_id', 'token_s_id'], axis=1, inplace=True)
                df = pd.concat([df, df_temp], axis=1, sort=False)
            # Else
            else:
                df = pd.concat([df, df_temp], join='inner')

                
    df.to_pickle(output_pkl_path)
    
if __name__ == "__main__":
    main()
