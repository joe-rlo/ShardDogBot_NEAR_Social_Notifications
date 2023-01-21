import json

# open file in read mode
with open("data.json", "r") as file:
    data = json.load(file)

data.update({"new_key": "new_value"})

# open file in write mode
with open("data.json", "w") as file:
    json.dump(data, file)

#have wallet:TG pairs
my_array = [{'key1': 'value1'}, {'key2': 'value2'}, {'key3': 'value3'}]

value_to_check = 'value2'
#check if match
matching_item = next((item for item in my_array if value_to_check in item.values()), None)
#if match then send notifications based on logic
if matching_item:
    key_var, value_var = list(matching_item.items())[0]
    print(f"{key_var} : {value_var}")
