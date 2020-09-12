import os

#KWARTAAL 1 EN 2
#output_no_doubles = een folder met een kopie van de 6 mapjes met output van convert_text_to_conll.py
list_1= os.listdir("Output_No_Doubles/Output_VUmc_q1q2__Search1")
list_2 = os.listdir("Output_No_Doubles/Output_VUmc_q1q2__Search2")
list_3 = os.listdir("Output_No_Doubles/Output_VUmc_q1q2__Search3")

#print(len(list_1))
#print(len(list_2))
#print(len(list_3))

list_to_delete_search2 = []
for item in list_1:
    #print(item[:40])
    for item2 in list_2:
        if item[:40] == item2[:40]:
            list_to_delete_search2.append(item2)

list_to_delete_search3 = []
for item in list_1:
    #print(item[:40])
    for item3 in list_3:
        if item[:40] == item3[:40]:
            list_to_delete_search3.append(item3)
            
for item2 in list_2:
    #print(item[:40])
    for item3 in list_3:
        if item2[:40] == item3[:40]:
            list_to_delete_search3.append(item3)

#print(len(list_to_delete_search2))
#print(len(list_to_delete_search3))
#print()

            
for item in list_to_delete_search2:
    os.remove("Output_No_Doubles/Output_VUmc_q1q2__Search2/" + item)
    
for item in list_to_delete_search3:
    os.remove("Output_No_Doubles/Output_VUmc_q1q2__Search3/" + item)

#KWARTAAL 3 EN 4
list_1q= os.listdir("Output_No_Doubles/Output_VUmc_q3q4__Search1")
list_2q = os.listdir("Output_No_Doubles/Output_VUmc_q3q4__Search2")
list_3q = os.listdir("Output_No_Doubles/Output_VUmc_q3q4__Search3")

#print(len(list_1q))
#print(len(list_2q))
#print(len(list_3q))

list_to_delete_search2_q = []
for item in list_1q:
    #print(item[:40])
    for item2 in list_2q:
        if item[:40] == item2[:40]:
            list_to_delete_search2_q.append(item2)

list_to_delete_search3_q = []
for item in list_1q:
    #print(item[:40])
    for item3 in list_3q:
        if item[:40] == item3[:40]:
            list_to_delete_search3_q.append(item3)
            
for item2 in list_2q:
    #print(item[:40])
    for item3 in list_3q:
        if item2[:40] == item3[:40]:
            list_to_delete_search3_q.append(item3)

#print(len(list_to_delete_search2_q))
#print(len(list_to_delete_search3_q))

            
for item in list_to_delete_search2_q:
    os.remove("Output_No_Doubles/Output_VUmc_q3q4__Search2/" + item)
    
for item in list_to_delete_search3_q:
    if item in os.listdir("Output_No_Doubles/Output_VUmc_q3q4__Search3"):
        os.remove("Output_No_Doubles/Output_VUmc_q3q4__Search3/" + item)
