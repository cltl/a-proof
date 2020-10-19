import os
from glob import glob
import itertools
import pathlib
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split


def get_list_per_annotator(input_dir):
    """
    Loops through folder with all .pkl files from all annotators and returns a list of lists which sorts files on annotator names
    :param input_dir str: filepath to folder with all .pkl files that get outputten by Generate_BertContainersPickle.py
    """
    
    suffix = ".pkl"

    # create list with names of all folders in input directory
    list_filenames = []
    for pkl in glob(f'{input_dir}/*{suffix}'):
        filename = os.path.basename(pkl)
        list_filenames.append(filename)
        
        
    list_sorted = sorted(list_filenames)   
    list_per_annotator = [list(g) for _, g in itertools.groupby(list_sorted, lambda x: x.split('__')[1])]

    return(list_per_annotator)



def copy_files(input_dir, output_dir):
    """
    copies all files from 1 annotator to 1 folder
    :param input_dir str: filepath to folder with all .pkl files that get outputten by Generate_BertContainersPickle.py
    :param output_dir str: filepath to the folder which you want to copy the files per annotator to. This folder should have subfolders per annotator.
    """
    
    list_per_annotator = get_list_per_annotator(input_dir)
    
    for l in list_per_annotator:
        for item in l:
            shutil.copy(input_dir+'/'+item, output_dir+"/"+item.split('__')[1][:-4]) 
            
            
def split_files(source_dir, trainsize):
    """
    Splits train/test per annotator randomly and then adds all train filepaths together in one list and all test filepaths in a different list. 
    :param source_dir str: filepath that is the same as output_dir in dopy_files()
    :param trainsize int: percentage of data you want as training data. Should be 0.80 for final data.
    """
    
    datadir=Path(source_dir)

    all_trains, all_tests = [], []
    for annotator in datadir.glob('*'):
            files = list(annotator.glob('*.pkl'))
            train, test = train_test_split(files, train_size=trainsize, shuffle=True, random_state=42)
            all_trains.extend(train)
            all_tests.extend(test)
            
    return(all_trains, all_tests)
            
            
if __name__ == '__main__':
    copy_files(''All_Info_Batch1', ''All_Info_Batch1_Sorted')
    print("Completed sorting and copying, start splitting...")
    
    result = split_files('All_Info_Batch1_Sorted', 0.80)
    print("Completed splitting")
    print(result[0])
    print(result[1])
    

    
