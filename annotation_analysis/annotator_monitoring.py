import pandas as pd
import glob
from pathlib import Path



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

def main():

    # ADAPT EACH TIME
    folder_path = "./batch1_11_09_2020/"
    date = "11_09_2020"

    # Create output file name
    output_filename = folder_path+"annotator_monitoring_"+date+".csv"

    # Write new file. Fill in header
    with open(output_filename, 'w') as outfile:
            line = "Naam,Aantal documenten,Aantal labels, Gemiddeld aantal labels per document"
            outfile.write(line+"\n")

    # For annotator append info to file
    for annotator_folder in glob.glob(folder_path+"*"):
        annotator_name, file_count, label_count, lab_per_doc = get_counts_for_annotator(annotator_folder)
        
        # Bug fix
        if annotator_name == "unknown":
            continue
        
        with open(output_filename, 'a') as outfile:
            line = ",".join([annotator_name, str(file_count), str(label_count), str(lab_per_doc)])
            outfile.write(line+"\n")
            
if __name__ == "__main__":
    main()
