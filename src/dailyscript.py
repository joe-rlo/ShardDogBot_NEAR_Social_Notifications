import http.client
import pip._vendor.requests 
import json

conn = http.client.HTTPSConnection("nearblocks.io")
payload = ''
headers = {}
conn.request("GET", "/api/account/balance?address=sharddog.near", payload, headers)
res = conn.getresponse()
data = res.read()
balanceData = data.decode("utf-8")
obj = json.loads(balanceData)
print(data.decode("utf-8"))
balance = obj.get("balance")

url = "https://api.telegram.org/APIKEY/sendMessage?chat_id=-602480598&text=ShardDog.near current balance is: "+balance+"N"

payload={}
headers = {}

response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)

print(response.text)

conn = http.client.HTTPSConnection("nearblocks.io")
payload = ''
headers = {}
conn.request("GET", "/api/account/balance?address=readylayerone_staking.poolv1.near", payload, headers)
res = conn.getresponse()
data = res.read()
balanceData = data.decode("utf-8")
obj = json.loads(balanceData)
print(data.decode("utf-8"))
balance = obj.get("balance")

url = "https://api.telegram.org/APIKEY/sendMessage?chat_id=-602480598&text=RLO validator current balance is: "+balance+"N"

payload={}
headers = {}

response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)

print(response.text)
