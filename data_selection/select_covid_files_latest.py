import pandas as pd

def select_ids(df_diagnoses, search_5=[], search_7=[]):

    MDN_ids = set()
    for query in search_5:
        temp_set = set(df_diagnoses.loc[df_diagnoses[5] == query][0])
        MDN_ids.update(temp_set)

    for query in search_7:
        temp_set = set(df_diagnoses.loc[df_diagnoses[7] == query][0])
        MDN_ids.update(temp_set)

    return MDN_ids


def main():
    output_filepath = '../../../data/Covid_notities_AMC_2020_q1_q2_q3_Search1.csv'
    
    # ../../../../../../bestanden 2020/
    # Change to AMC or VUmc
    hospital = "AMC"
    
    # Read files
    if hospital == "AMC":
        # AMC
        diagnoses_filepath = "../../../../../../bestanden 2020/Diagnoses AMC 2020 sept.csv"
        notities_filepath_1 = "../../../../../../bestanden 2020/Notities AMC 2020 Q1.csv"
        notities_filepath_2 = "../../../../../../bestanden 2020/Notities AMC 2020 Q2.csv"
        notities_filepath_3 = "../../../../../../bestanden 2020/Notities AMC 2020 Q3.csv"
    else:
        #VUmc
        diagnoses_filepath = "../../../../../../bestanden 2020/Diagnoses VUMC 2020 sept.csv"
        notities_filepath_1 = "../../../../../../bestanden 2020/Notities VUMC 2020 Q1.csv"
        notities_filepath_2 = "../../../../../../bestanden 2020/Notities VUMC 2020 Q2.csv"
        notities_filepath_3 = "../../../../../../bestanden 2020/Notities VUMC 2020 Q3.csv"
    
    
    # Define patient id pat_id_column
    pat_id_column = 0
    # pat_id_column = 'Pat_id'
    
    # Read in files as pd.DataFrame types
    df_diagnoses = pd.read_csv(diagnoses_filepath, sep=';', header=None, encoding = 'utf-8')
    
    df_notities_1 = pd.read_csv(notities_filepath_1, sep=';', header=None, encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
    df_notities_2 = pd.read_csv(notities_filepath_2, sep=';', header=None, encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
    df_notities_3 = pd.read_csv(notities_filepath_3, sep=';', header=None, encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
    # Join notes to one df
    df_notities = pd.concat([df_notities_1, df_notities_2, df_notities_3])
    

    # Search queries
    #Comment out two of three searches
    search_5 = []# ['acute respiratoire aandoening door SARS-CoV-2', 'infectie met SARS-CoV-2', 
                # 'dyspnoe bij infectie met SARS-CoV-2']
    search_7 =  ["COVID-19, virus geïdentificeerd [U07.1]"]

    # MDN_ids is patient id
    MDN_ids = select_ids(df_diagnoses, search_5=search_5, search_7=search_7)

    # Create df with selected MDN ids
    df_selection = df_notities.loc[df_notities[pat_id_column].isin(MDN_ids)]
    
    
    # Print statements for counts
    print(search_5, search_7)
    print("Aantal patient ids in search", len(MDN_ids))
    print("Patient ids die ook in notities staan", len(MDN_ids & set(df_notities[pat_id_column])))
    print("Aantal notities van die patienten", df_selection.shape[0])
    print("Gemiddeld aantal documenten per patient", df_selection.shape[0]/len(MDN_ids & set(df_notities[pat_id_column])))

    # Write to csv
    df_selection.to_csv(output_filepath, sep=';')

if __name__ == "__main__":
    main()



#Search1 = COVID-19, virus geïdentificeerd [U07.1]
#Search2 = acute respiratoire aandoening door SARS-CoV-2
#Search3 = acute respiratoire aandoening vermoedelijk door SARS-CoV-2
# infectie met SARS-CoV-2
# dyspnoe bij infectie met SARS-CoV-2
