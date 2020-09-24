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
    output_filepath = 'Data 2020/Covid_notities_VUmc_2020_q3q4_Search3.csv'
    
    # Change to AMC or VUmc
    hospital = "VUmc"
    
    # Read files
    if hospital == "AMC":
        # AMC
        diagnoses_filepath = "Data 2020/Diagnoses AMC.csv"
        notities_filepath_1 = "Data 2020/Datamining valrisico - Edwin Geleijnse - Covid project - q1 AMC.csv"
        notities_filepath_2 = "Data 2020/Datamining valrisico - Edwin Geleijnse - Covid project - q2 AMC.csv"
        notities_filepath_3 = "Data 2020/Datamining valrisico - Edwin Geleijnse - Covid project - q3&q4 AMC.csv"
    else:
        #VUmc
        diagnoses_filepath = "Data 2020/Diagnoses VUmc.csv"
        notities_filepath_1 = "Data 2020/Datamining valrisico - Edwin Geleijn - Covid project - q1&q2.csv"
        notities_filepath_2 = "Data 2020/Datamining valrisico - Edwin Geleijn - Covid project - q3&q4.csv"
    
    # Read in files as pd.DataFrame types
    df_diagnoses = pd.read_csv(diagnoses_filepath, sep=';', header=None, encoding = 'utf-8')
    
    df_notities_1 = pd.read_csv(notities_filepath_1, sep=';', encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
    df_notities_2 = pd.read_csv(notities_filepath_2, sep=';', encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
    
    # If AMC then read in third doc too and concat
    if hospital == "AMC":
        df_notities_3 = pd.read_csv(notities_filepath_3, sep=';', encoding = 'utf-8-sig', engine='python', error_bad_lines=False)
        df_notities = pd.concat([df_notities_1, df_notities_2, df_notities_3])
    else:
        df_notities = pd.concat([df_notities_1, df_notities_2])

    # Search queries
    #Comment out two of three searches
    search_5 = [] #['acute respiratoire aandoening vermoedelijk door SARS-CoV-2']
                #['acute respiratoire aandoening door SARS-CoV-2']
    search_7 =  ["COVID-19, virus geïdentificeerd [U07.1]"]

    # MDN_ids is patient id
    MDN_ids = select_ids(df_diagnoses, search_5=search_5, search_7=search_7)

    # Create df with selected MDN ids
    df_selection = df_notities.loc[df_notities['Pat_id'].isin(MDN_ids)]
    
    
    # Print statements for counts
    print("Aantal patient ids in search", len(MDN_ids))
    print("Patient ids die ook in notities staan", len(MDN_ids & set(df_notities['Pat_id'])))
    print("Aantal notities van die patienten", df_selection.shape[0])
    print("Gemiddeld aantal documenten per patient", df_selection.shape[0]/len(MDN_ids & set(df_notities['Pat_id'])))

    # Write to csv
    #df_selection.to_csv(output_filepath, sep=';')

if __name__ == "__main__":
    main()



#Search1 = virus geidentificeerd 
#Search2 = acute respiratoire aandoening door SARS-CoV-2
#Search3 = acute respiratoire aandoening vermoedelijk door SARS-CoV-2
