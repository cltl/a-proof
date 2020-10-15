import pickle
from class_definitions import Annotation, BertContainer
import pandas as pd
import glob
from collections import Counter


# pkl_filepath = '../sample_data/BERTContainers/Container_notities_2017_deel1_cleaned.csv---25032_avelli.pkl'
def main():
    #pkl_folderpath = '../sample_data/BERTContainers/'
    pkl_folderpath = "../../Non_covid_data_15oct/BertContainers_Batch1/"
    output_file = '../sample_data/general_stats.txt'

    domain_set = {'.B152: Stemming', '.D450: Lopen en zich verplaatsen'}

    gradation_stm = {'STM 0', 'STM 1', 'STM 2', 'STM 3', 'STM 4'}
    gradation_ins = {'INS 0', 'INS 1', 'INS 2', 'INS 3', 'INS 4', 'INS 5'}
    gradation_lop = {'FAC 0', 'FAC 1', 'FAC 2', 'FAC 3', 'FAC 4', 'FAC 5'}
    gradation_ber = {'BER 0', 'BER 1', 'BER 2', 'BER 3', 'BER 4'}

    gradation_set = gradation_stm | gradation_ins | gradation_ber | gradation_lop

    sentences_count = 0
    doc_count = 0
    domain_and_gradation_same_sentence = 0
    sentences_with_labels = 0
    domain_and_gradation = 0
    sentences_with_domain = 0
    double_labels = 0
    double_domain_label = 0
    document_with_background = 0
    document_with_target = 0
    disregard_file = 0
    label_count_dict = dict()

    for pkl_filepath in glob.glob(pkl_folderpath + '*'):
        doc_count += 1
        pkl_file = open(pkl_filepath, "rb")
        document = pickle.load(pkl_file)

        document_annotation_set = set()

        # One BertContainer contains info of one sentence
        for BertContainer in document:
            # gather annotations
            annotation_list = []
            if len(BertContainer.annot) != 0:
                for annotation in BertContainer.annot:
                    annotation_list.append(annotation.label)
                    if annotation.label in label_count_dict:
                        label_count_dict[annotation.label] += 1
                    else:
                        label_count_dict[annotation.label] = 1
            annotation_set = set(annotation_list)
            document_annotation_set = document_annotation_set | annotation_set

            # get counts
            sentences_count += 1

            if len(annotation_list) != 0:
                sentences_with_labels += 1

            if len(annotation_list) != len(annotation_set):
                double_labels += 1
                annotation_counter = Counter(annotation_list)
                for domain in domain_set:
                    if annotation_counter[domain] > 1:
                        double_domain_label += 1
                        break

            # check domain label
            if len(annotation_set & domain_set) != 0:
                sentences_with_domain += 1
                if len(annotation_set & gradation_set) != 0:
                    if '.B152: Stemming' in annotation_set and len(annotation_set & gradation_stm) != 0:
                        domain_and_gradation_same_sentence += 1
                    elif '.D450: Lopen en zich verplaatsen' in annotation_set and len(
                            annotation_set & gradation_lop) != 0:
                        domain_and_gradation_same_sentence += 1
                    elif '.B455: Inspanningstolerantie' in annotation_set and len(
                            annotation_set & gradation_lop) != 0:
                        domain_and_gradation_same_sentence += 1
                    elif '.D840-859: Beroep en werk' in annotation_set and len(
                            annotation_set & gradation_lop) != 0:
                        domain_and_gradation_same_sentence += 1

        if 'type\\_Background' in document_annotation_set:
            document_with_background += 1

        if 'target' in document_annotation_set: 
            document_with_target += 1
            
        if 'disregard\\_file' in document_annotation_set:
            disregard_file += 1
        

    domain_labels_count = 0
    for label in domain_set:
        domain_labels_count += label_count_dict[label]

    with open(output_file, 'a') as outfile:
        outfile.write('Total amount of documents: ' + str(doc_count) +'\n')
        outfile.write('Total amount of sentences: ' + str(sentences_count) +'\n')
        outfile.write('Total amount of labels: ' + str(sum(label_count_dict.values())) +'\n')

        outfile.write('Amount of documents to disregard: ' + str(disregard_file) +'\n')

        outfile.write('Amount of domain_labels: ' + str(domain_labels_count) +'\n')
        outfile.write('Total amount of sentences that contain labels: ' + str(sentences_with_labels) +'\n')
        outfile.write('Amount of sentences that contain domain labels: ' + str(sentences_with_domain) +'\n')
        outfile.write('Amount of sentences that contain domain and gradation label in same sentence: ' + str(domain_and_gradation_same_sentence) +'\n')

        outfile.write('Amount of sentences with repeated labels: ' + str(double_labels) +'\n')
        outfile.write('Amount of sentences with repeated domain labels: ' + str(double_domain_label) +'\n')

        outfile.write(str(label_count_dict))


if __name__ == '__main__':
    main()
