import glob
from pathlib import Path
import pandas as pd

def get_data_from_tsv(filename):
    """
    Creates list of data from tsv file in conll format.
    Adapted from updates_join_annotators.py
    """
    # Make pathlib type
    filename = Path(filename)

    # Get document id and annotator name from filename
    doc_id = filename.parent.stem[-4:]
    annotator = filename.stem

    # Read file
    data = []
    with (filename).open() as infile:
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
                split_row.extend(['_', '_'])
            
            elif len(split_row) == 3:
                split_row.extend(['_', '_', '_'])
            elif len(spit_row!=6):
                continue
            data.append(split_row)
            
    return data, annotator


def label_counter(data):
    """
    Counts unique labels in data. Requires labels to be in column 3.
    Returns count
    """
    # Define set
    labels_set = set()

    # Add all labels in 3rd column to set
    for row in data:
        labels_set.add(row[3])
        
    # Return len of set -1 to account for no label ('_')
    return len(labels_set)-1


def get_counts_for_annotator(annotator_folder):
    """
    Get several counts for one annotator. Calculates amount of docs, labels and labels per doc.
    Returns tuple containing annotator name, document count, total label count and average amount of labels per doc. 
    """
    # Redirect to correct sub_folder
    sub_folder = annotator_folder+"/annotation/"

    # Set annotator and total_label_count variables
    annotator = "unknown"
    total_label_count = 0
    
    # Get list of folders containing annotations
    sub_folder_list = glob.glob(sub_folder+"*")
    # Length of folder is amount of files annotated
    file_count = len(sub_folder_list)
    
    # Loop through folder to get all files for this annotator
    for annotations_folder in sub_folder_list:
        
        filename = glob.glob(annotations_folder + "/*")[0]
        # Extract data and annotator name
        data, annotator = get_data_from_tsv(filename)
        # Get label counts for this file and sum to total label_count
        count_file = label_counter(data)
        total_label_count += count_file
    
    # Bug fix for division by 0 when sub_folder_list is empty
    if file_count != 0:
        lab_per_doc = round(total_label_count/file_count, 2)
    else: 
        lab_per_doc = 0
    
    return annotator, file_count, total_label_count, lab_per_doc


def extract_total_annotations_file(folder_path, output_filename):

    # Write new file. Fill in header
    with open(output_filename, 'w') as outfile:
            line = "Naam\tAantal documenten\tAantal labels\tGemiddeld aantal labels per document"
            outfile.write(line+"\n")

    # For annotator append info to file
    for annotator_folder in glob.glob(folder_path+"*"):
        annotator_name, file_count, label_count, lab_per_doc = get_counts_for_annotator(annotator_folder)
        
        # Bug fix
        if annotator_name == "unknown":
            continue
        
        with open(output_filename, 'a') as outfile:
            line = "\t".join([annotator_name, str(file_count), str(label_count), str(lab_per_doc)])
            outfile.write(line+"\n")

def main():
    """
    Calculates annotator progress since last update.
    Counts labeled and locked documents and labels up to now, and writes to file.
    Reads in previous file (from last week).
    Calculates difference between last weeks counts and this weeks counts. Writes that to second file.
    :return:
    """
    # ADAPT EACH TIME
    folder_path = "./batch1_18_09_2020/"
    date = "18-09-2020"
    last_weeks_total_filepath = "./analysis_files/annotator_monitoring_total_11-09-2020.txt"

    # Create output file name
    total_annotations_filename = "./analysis_files/annotator_monitoring_total_" + date + ".txt"
    difference_filename = "./analysis_files/annotator_monitoring_difference_" + date + ".txt"

    extract_total_annotations_file(folder_path, total_annotations_filename)

    df_previous_total = pd.read_csv(last_weeks_total_filepath, sep='\t', index_col="Naam").add_prefix('previous_')
    df_current_total = pd.read_csv(total_annotations_filename, sep='\t', index_col="Naam").add_prefix('Totaal ')

    # Remove duplicated annotator
    df_previous_total = df_previous_total[~df_previous_total.index.duplicated(keep='first')]
    df_current_total = df_current_total[~df_current_total.index.duplicated(keep='first')]

    # Join dfs
    df = pd.concat([df_previous_total, df_current_total], axis=1, sort=False)

    # Calculate difference between last week and this week
    df['Aantal documenten deze week'] = df['Totaal Aantal documenten'] - df['previous_Aantal documenten']
    df['Aantal labels deze week'] = df['Totaal Aantal labels'] - df['previous_Aantal labels']

    # Write file
    df.to_csv(difference_filename, sep='\t', columns=['Totaal Aantal documenten', 'Totaal Aantal labels',
                                                      'Aantal documenten deze week', 'Aantal labels deze week'])


if __name__ == "__main__":
    main()
