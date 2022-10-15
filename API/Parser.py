import csv


def get_number_list(file_name, key="number"):
    unformated_number_list = []
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unformated_number_list.append(row[key])
    number_list = ['+'+''.join(filter(str.isdigit, tel)) for tel in unformated_number_list]
    return number_list

