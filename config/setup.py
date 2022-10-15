import os
session_name = 'anon'
api_id = 12250674
api_hash = "447912eb100ed4731789329e7c59d32d"
database = os.path.normpath('E:\\programs\\PycharmProjects\\SpamProgramm\\database.db')


#чтение из файла config.txt
parent_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(parent_dir,'config.txt'), 'r') as config_file:
    config_info = config_file.read()
    onstring = config_info.split("\n")[:-1]
    config_data = {'k':'v'}
    for item in onstring:
        key = item.split(" ")[0]
        value = item.split(" ")[1]
        config_data[key] = value
default_csv = config_data['default_csv']
default_csv_key = config_data['default_csv_key']
messages_file = config_data['messages_file']
default_delay =  config_data['default_delay']
last_client_number = config_data['last_client_number']
default_start = config_data['default_start']


