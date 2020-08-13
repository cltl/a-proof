# a-proof
Tools for the text classification of clinical note in electronic patient records

The text classification assing the WHO ICF labels for the functional recovery of patients.

The following steps are needed for analysing the annotations:

1. Export of the individual project in Inception using the in WebAnno TSV v3.2 (webAnnot v3.x) format

2. Run the script: python3 updates_join_annotations.py with the exported folders as the input

This script creates a token level Pandas data frame from all the annotation exported in TSV format. The data frame is saved as: token_level_df.pkl

3. Run the script: python3 main_get_scores_v2.py taking the token_level_df.pkl as input

This script derives a label level dataframe by joining all token annotations from different annotators that assigned the same label to the same token. The data frame is saved as label_level_df.pkl and as label_level_df.xlsx

After creating the label_level_df.xlsx, we need to do a few additional things:

- we need to split the identifiers using "_" as a separator. This allows us to sort the columns by: 1) label, 2) file id, 3) start token id. 
- Unfortunately also the label itself is split, so we need to concatenate the labels again using an excel formula. 

This can all be improved by exporting the dataframe to label_level_df.xlsx in the right way.


4. Run the script: python3 Softboundaries_updated_analysis_code.ipynb

The sorted excel file is used as as input for the soft boundary analysis


