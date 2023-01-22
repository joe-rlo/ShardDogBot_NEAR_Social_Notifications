import json
with open("./tgUsers.json", "r") as user_file:
    userArray = json.load(user_file)

value_to_check = 'readylayerone.near'
matching_item = None
for key, value in userArray.items():
    if value == value_to_check:
        matching_item = key
        break
print(matching_item)
