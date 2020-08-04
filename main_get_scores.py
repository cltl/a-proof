import pandas as pd
from pathlib import Path
from updates_join_annotations import open_df_from_tsv
import updates_get_average_scores_per_label as scores

            
def main(): 

    df = pd.read_pickle('token_level_df.pkl')
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

