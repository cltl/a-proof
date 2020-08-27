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
    output_filepath = '../sample_data/Covid_notities.csv'
    # Read files
    df_diagnoses = pd.read_excel("../sample_data/raw_data/Diagnoses.xlsx", header=None)
    df_notities = pd.read_excel("../sample_data/raw_data/Notities.xlsx", header=None)
    # df_diagnoses = pd.read_csv("FILEPATH_DIAGNOSES.csv", sep=';', header=None)
    # df_notities = pd.read_csv("FILEPATH_NOTITIES.csv", sep=';', header=None)

    # Search queries
    search_5 = ['acute respiratoire aandoening door SARS-CoV-2',
                'acute respiratoire aandoening vermoedelijk door SARS-CoV-2']
    search_7 = ["COVID-19, virus geïdentificeerd [U07.1]", "COVID-19, virus niet geïdentificeerd [U07.1]"]

    MDN_ids = select_ids(df_diagnoses, search_5=search_5, search_7=search_7)

    # Create df with selected MDN ids
    df_selection = df_notities.loc[df_notities[0].isin(MDN_ids)]

    # Write to csv
    df_selection.to_csv(output_filepath, sep=';')

if __name__ == "__main__":
    main()
