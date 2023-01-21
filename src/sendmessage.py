import pip._vendor.requests 

url = "https://api.telegram.org/botID:APIKEY/sendMessage?chat_id=-602480598&text=WOOF! New drop created from ShardDog mainnet!"

payload={}
headers = {}

response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)

print(response.text)