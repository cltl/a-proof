import os

list_1= os.listdir("Test_Data_Filteren/Map 1")
list_2 = os.listdir("Test_Data_Filteren/Map 2")

list_to_delete = []
for item in list_1:
    for item2 in list_2:
        if item[:15] == item2[:15]:
            list_to_delete.append(item2)
            
for item in list_to_delete:
    os.remove("Test_Data_Filteren/Map 2/" + item)