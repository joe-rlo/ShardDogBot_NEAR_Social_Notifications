import pip._vendor.requests 

url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id=5222409941&text=<i>Test</i> From NEAR Social!"

payload={}
headers = {}

response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)

print(response.text)