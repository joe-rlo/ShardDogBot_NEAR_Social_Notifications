import json
import pip._vendor.requests 

url = "https://api.telegram.org/botID%3APIKEY/getUpdates"

payload={}
headers = {}

response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)

print(response.text)


data = json.loads(response.text)

for message in data['result']:
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    print(f"Chat ID: {chat_id}, Text: {text}")

tgUsers = {}
for message in data['result']:
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    tgUsers[chat_id] = text
if text.endswith('.near'):
    with open("tgUsers.json", "w") as outfile:
        json.dump(tgUsers, outfile)

"""
# open file in read mode
with open("tgUsers.json", "r") as file:
    data = json.load(file)

data.update(tgUsers)

# open file in write mode
with open("tgUsers.json", "w") as file:
    json.dump(data, file)


#have wallet:TG pairs
userArray = json.load("./tgUsers.json")

value_to_check = notify_json['key']
#check if match
matching_item = next((item for item in userArray if value_to_check in item.values()), None)
#if match then send notifications based on logic
if matching_item:
    key_var, value_var = list(matching_item.items())[0]
    print(f"{key_var} : {value_var}")



# open file in write mode
with open("chat_text.json", "w") as file:
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
"""