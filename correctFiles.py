import os

path = ".//data//quaterly//cashflowS"
dir_list = os.listdir(path)
stockList = dir_list

for i in stockList:
    file = open("data/quaterly/cashflowS/" + i)
    string_list = file.readlines()
    file.close()
    if not string_list[0].startswith("Date; "):
        string_list[0] = "Date; " + string_list[0]
    for j, row in enumerate(string_list):
        if row.endswith("; \n"):
            string_list[j] = row[:-3] + "\n"
            
    file = open("data/quaterly/cashflowS/" + i, "w")
    new_file_contents = "".join(string_list)
    file.write(new_file_contents)
    file.close()