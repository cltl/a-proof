import pickle
from annotation import Annotation


pkl_file = open("Container_notities_2017_deel1_cleaned.csv---2503.conll_avelli.pkl", "rb")
info = pickle.load(pkl_file)
pkl_file.close()
print(info)
