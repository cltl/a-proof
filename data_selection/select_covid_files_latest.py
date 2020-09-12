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
    # Read files

    df_diagnoses = pd.read_csv("Data 2020/Diagnoses VUmc.csv", sep=';', header=None, encoding = 'utf-8')
    df_notities = pd.read_csv("Data 2020/Datamining valrisico - Edwin Geleijn - Covid project - q3&q4.csv", sep=';', encoding = 'utf-8-sig', engine='python', error_bad_lines=False)

    # Search queries
    #Comment out two of three searches
    search_5 = ['acute respiratoire aandoening vermoedelijk door SARS-CoV-2']
                #['acute respiratoire aandoening door SARS-CoV-2']
    search_7 = [] # ["COVID-19, virus geïdentificeerd [U07.1]"]

    MDN_ids = select_ids(df_diagnoses, search_5=search_5, search_7=search_7)

    # Create df with selected MDN ids
    df_selection = df_notities.loc[df_notities['Pat_id'].isin(MDN_ids)]

    # Write to csv
    df_selection.to_csv(output_filepath, sep=';')

if __name__ == "__main__":
    main()



#Search1 = virus geidentificeerd 
#Search2 = acute respiratoire aandoening door SARS-CoV-2
#Search3 = acute respiratoire aandoening vermoedelijk door SARS-CoV-2
