import pandas as pd
from pathlib import Path
from updates_join_annotations import open_df_from_tsv
import updates_get_average_scores_per_label as scores

            
def main(): 
    for index, filename in enumerate(Path('./sample_data').glob('**/*.tsv')):
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
                if df_temp['file_id'][1] in set(df['file_id']) and f'labels_{annotator}' in df.columns:
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
                
    df.info()
    annotator_names = ['avelli', 'bos', 'meskers']
    #annotator_names = ['avelli', 'bos', 'katsburg', 'meskers', 'opsomer', 'swartjes', 'vanderpas', 'vervaart']

    new_df = scores.get_dataframe(df, annotator_names)

    score = 0
    for annotator in annotator_names:
        try:
            print(annotator)
            dicta = dict()
            # get personal dicts per annotator
            dicta = scores.get_annotator_dict(df, 'labels_'+annotator)
            print('Nr. of annotations', len(dicta))
            # score the annotations in the df
            new_df = scores.find_matches(new_df, annotator, dicta)
            score += new_df[annotator]
        except KeyError:
            print('KeyError: {} does not exist in the table.'.format(annotator))
            continue

    # sum the scores and put in new column
    new_df['score'] = score
    new_df.to_excel('excel_with_scores.xlsx')


if __name__ == "__main__":
    main()

