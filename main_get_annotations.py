import pandas as pd
from pathlib import Path
from updates_join_annotations import open_df_from_tsv
#import updates_get_average_scores_per_label as scores

            
def main():
    # DEFINE PATHS
    # folder_path = './sample_data'           # Folder path from which to find the annotated tsv files
    # output_pkl_path = 'token_level_df.pkl'  # Output path to which to write the df in pkl format
    
    folder_path = './../../data/raw_data/week_30'           # Folder path from which to find the annotated tsv files
    output_pkl_path = './../../data/processed_data/week_30/token_level_df.pkl'  # Output path to which to write the df in pkl format

    for index, filename in enumerate(Path(folder_path).glob('**/*.tsv')):
        """
        Creates pd.DataFrame by joining files from different annotators and different documents to one
        large df
        """
    
        print(filename)
        # Extract annotator name from doc
        annotator = filename.stem
    
        # Use the first file to create df
        if index == 0:
            df = open_df_from_tsv(filename)
        
        # Update df with new files
        else: 
            # Create temporary df
            df_temp = open_df_from_tsv(filename)
            if df_temp.empty:
                #no content
                continue
            try:
                # if file is already in rows, and annotator is already in colmumns, then update
                # if empty ['file_id'][1] does not exist, crash?
                if df_temp['file_id'][1] in set(df['file_id']) and 'labels_{}'.format(annotator) in df.columns:
                    df.update(df_temp)
                # Elif file is in rows (and annotator not yet in columns), then concat with axis=1
                elif df_temp['file_id'][1] in set(df['file_id']):
                    df_temp.drop(['token_d_id', 'token', 'file_id', 'sent_id', 'token_s_id'], axis=1, inplace=True)
                    df = pd.concat([df, df_temp], axis=1, sort=False)
                # Else
                else:
                    df = pd.concat([df, df_temp], join='inner')
            except:
                continue
                
    df.to_pickle(output_pkl_path)


if __name__ == "__main__":
    main()


