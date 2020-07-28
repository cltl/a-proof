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
    with open(filename, 'r') as infile:
        for row in infile:
            # Skip rows starting with #
            if row.startswith('#'):
                continue
            # Remove '\n' at end of row
            row = row[:-1]
            # Split on tab
            split_row = row.split('\t')  
            # Skip if empty row
            if split_row[0] == '':
                continue
            # If length is not 5 (some files had only 3 columns), append columns with '_'
            if len(split_row) != 5:
                split_row.extend(['_', '_'])
                
            data.append(split_row)
    data 
    
    # Create pd.DataFrame
    df = pd.DataFrame(data=data, columns=['sent_token_id', 'char_id', "token", f"labels_{annotator}", f"relation_{annotator}"])
    # Add column containing file_id
    df = df.assign(file_id=doc_id)
    
    # Split sent_id and token_id (in sentence) and drop orginal and char_id
    df['sent_id'] = df.apply(lambda row: row['sent_token_id'].split('-')[0], axis=1)
    df['token_s_id'] = df.apply(lambda row: row['sent_token_id'].split('-')[1], axis=1)
    df.drop(['sent_token_id', 'char_id'], axis=1, inplace=True)
    
    # Create column containing token id (from start of doc)
    df.reset_index(drop=False, inplace=True)
    df.rename({'index': 'token_d_id'}, axis=1, inplace=True)
    
    # Create index from file id and token id (from start of doc)
    df['doc_token_id'] = df.apply(lambda row: str(row['file_id']) + '_'+ str(row['token_d_id']), axis=1)
    df.set_index('doc_token_id', inplace=True)

    return df


def main(): 
    for index, filename in enumerate(Path('sample_data').glob('**/*.tsv')):
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
            if df_temp['file_id'][1] in set(df['file_id']) and f'labels_{annotator}' in df.columns:
                df.update(df_temp)
            # Elif file is in rows (and annotator not yet in columns), then concat with axis=1
            elif df_temp['file_id'][1] in set(df['file_id']):
                df_temp.drop(['token_d_id', 'token', 'file_id', 'sent_id', 'token_s_id'], axis=1, inplace=True)
                df = pd.concat([df, df_temp], axis=1, sort=False)
            # Else
            else:
                df = pd.concat([df, df_temp], join='inner')

                
    df.to_pickle('/data/homedirs/stella/IAA_code/token_level_df.pkl')
    
if __name__ == "__main__":
    main()

    