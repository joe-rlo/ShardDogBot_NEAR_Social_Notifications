import json
import pip._vendor.requests 
import pickle

filename = 'offset.pk'
with open(filename, 'rb') as fi:
    offset = pickle.load(fi)
    print(offset)
url = "https://api.telegram.org/APIKEY/getUpdates"

payload={'offset': offset}
headers = {}

response = pip._vendor.requests.request("POST", url, headers=headers, data=payload)

print(response.text)

data = json.loads(response.text)

tgUsers = {}

for message in data['result']:
    if 'my_chat_member' not in message.keys():
        if message['message']['chat']['type'] == 'private':
            chat_id = message['message']['chat']['id']
            if 'text'in message['message'].keys():
                text = message['message']['text']
                tgUsers[text] = str(chat_id)
                if text.endswith('.near'):
                    if text.startswith("remove"):
                        print("The string starts with 'remove'.")
                        substrings = text.split(" ")
                        with open("tgUsers.json", "r") as file:
                            current_data = json.load(file)
                        # Remove the key-value pair
                        # Search for the key-value pair
                        keys_to_remove = []
                        for key, value in current_data.items():
                            print(substrings[1])
                            if key == substrings[1]:
                                keys_to_remove.append(key)
                                matching_item = value
                                break

                        # Remove the key-value pair
                        if keys_to_remove:
                            # Choose the key to remove based on some criteria, e.g. the first key
                            url = "https://api.telegram.org/APIKEY/sendMessage?parse_mode=html&chat_id="+str(matching_item)+"&text=Account has been removed from notifications."
                            print(url)
                            payload={}
                            headers = {}
                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                            matching_item = None
                            key_to_remove = keys_to_remove[0]
                            del current_data[key_to_remove]

                        # Save the updated JSON file
                            with open("tgUsers.json", "w") as file:
                                json.dump(current_data, file)
                    else:
                    # Read the existing data from the file
                        with open("tgUsers.json", "r") as f:
                            existing_data = json.load(f)

                        # Add the new data to the existing data
                            existing_data.update(tgUsers)

                        # Write the combined data back to the file
                        with open("tgUsers.json", "w") as f:
                            json.dump(existing_data, f, ensure_ascii=False)
                        url = "https://api.telegram.org/APIKEY/sendMessage?parse_mode=html&chat_id="+str(chat_id)+"&text=Account has been added to notifications."
                        print(url)
                        payload={}
                        headers = {}
                        response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
 
if data['result'] != []:                        
    offset = int(message['update_id'])+1
    print(offset)
    with open(filename, 'wb') as fi:
        # dump your data into the file
        pickle.dump(offset, fi)
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
