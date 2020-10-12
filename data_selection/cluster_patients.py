import os
from glob import glob
import itertools

#choose filepath for input dir
input_dir = "output_for_inception_VUmc" 
#input_dir = "output_for_inception_AMC"
suffix = ".conll"

# create list with names of all folders in input directory
list_basenames = []
for conll_path in glob(f'{input_dir}/*{suffix}'):
    basename = os.path.basename(conll_path)
    list_basenames.append(basename)
    
# make list of lists which sorts on patient id    
list_sorted = sorted(list_basenames)    
x = [list(g) for _, g in itertools.groupby(list_sorted, lambda x: x.split('--')[2])]

#only select lists with 8 or more items, i.e. only when there are at least 8 files with the same patient id do they get included
final_list = []
for item in x:
    if len(item) > 7:
        final_list.append(item)
 
#make list of all files that can be deleted 
for l in final_list:
    for item in l:
        list_basenames.remove(item)
to_remove = list_basenames
      
#remove files you don't want from your input folder or a copy of it
for item in to_remove:
    os.remove("output_for_inception_VUmc_sorted/" + item)
    #os.remove("output_for_inception_AMC_sorted/" + item)
    
