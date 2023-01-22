import asyncio
import json
import os
from dotenv import load_dotenv
import re
import base64
import pip._vendor.requests 
import logging
from datetime import datetime

# Configure the logging
logging.basicConfig(filename='./errors.log', level=logging.ERROR)

from near_lake_framework import near_primitives, LakeConfig, streamer

async def handle_streamer_message(streamer_message: near_primitives.StreamerMessage):
    #print("LOADED")

    for shard in streamer_message.shards:
        for receipt_execution_outcome in shard.receipt_execution_outcomes:
                if receipt_execution_outcome.receipt.receiver_id == "social.near":
                    #print("found something")
                    #print(receipt_execution_outcome.receipt.receipt)
                    json_obj = receipt_execution_outcome.receipt.receipt
                    if json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("args") is not None:
                        args = json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("args")
                        decodedResults = base64.b64decode(args).decode()  
                        #print(base64.b64decode(args).decode())              
                    if json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("method_name") is not None:
                        methodName = json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("method_name")
                        #print(methodName)
                        if methodName == 'set':
                            parsed_data = json.loads(decodedResults)
                            #print(parsed_data)
                            for key in parsed_data['data']:
                                if key.endswith('near'):
                                    print('ended with near')
                                    try:
                                        if parsed_data['data'][key]['index']:
                                            if parsed_data.get("data", {})[key].get("index", {}).get("notify") is not None:
                                                print(parsed_data.get("data", {})[key].get("index", {}).get("notify"))
                                                try:
                                                    notify_type = json.loads(parsed_data.get("data", {})[key].get("index", {}).get("notify"))
                                                    notify_type = notify_type['value'].get("type")  
                                                    print(notify_type)
                                                    like_value = None
                                                    follow_value = None
                                                    poke_value = None
                                                    if notify_type == "like":
                                                        like_value = notify_type
                                                        print(like_value)
                                                    if notify_type == "follow":
                                                        follow_value = notify_type
                                                        print(follow_value)
                                                    if notify_type == "poke":
                                                        poke_value = notify_type
                                                        print(poke_value) 
                                                    from_data = parsed_data['data']
                                                    from_data = list(from_data.keys())
                                                    from_data = from_data[0]
                                                
                                                    notify_value = parsed_data['data'][key]['index']['notify']
                                                    print(notify_value)
                                                
                                                    ## parsing the json string to json object
                                                    notify_json = json.loads(notify_value)
                                                    print("Data is from: ",from_data)
                                                    print("Value of 'key': ",notify_json['key'])
                                                    #print("Value of 'blockHeight': ",notify_json['value']['item']['blockHeight'])
                                                    with open("./tgUsers.json", "r") as user_file:
                                                        userArray = json.load(user_file)
                                                    value_to_check = notify_json['key']
                                                    matching_item = None
                                                    for key, value in userArray.items():
                                                        if value == value_to_check:
                                                            matching_item = key
                                                            break
                                                    print(matching_item)
                                                    if matching_item is not None:
                                                        if like_value is not None:
                                                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=markdown&chat_id="+str(matching_item)+"&text=New __LIKE__ from "+from_data+" on Near Social! [View Post](https://near.social/%23/mob.near/widget/MainPage.Post.Page%3FaccountId="+notify_json['key']+"%26blockHeight="+str(notify_json['value']['item']['blockHeight'])+")"
                                                            print(url)
                                                            payload={}
                                                            headers = {}
                                                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                                            matching_item = None
                                                        if follow_value is not None:
                                                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id="+str(matching_item)+"&text=New <b>FOLLOW</b> from "+from_data+" on Near Social!"
                                                            print(url)
                                                            payload={}
                                                            headers = {}
                                                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                                            matching_item = None
                                                        if poke_value is not None:
                                                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id="+str(matching_item)+"&text=You just got <b>POKED</b> by "+from_data+" on Near Social!"
                                                            print(url)
                                                            payload={}
                                                            headers = {}
                                                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                                            matching_item = None
                                                except:
                                                        # code to handle the error
                                                        # get current timestamp
                                                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                        logging.error("### "+timestamp)
                                                        logging.error(parsed_data)
                                                        logging.error("An error occurred", exc_info=True)
                                                        matching_item = None
                                                        continue
                                            else:
                                                matching_item = None
                                                continue  
                                        else:
                                            continue    
                                    except:
                                         # code to handle the error
                                         # get current timestamp
                                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        logging.error("### "+timestamp)
                                        logging.error(parsed_data)
                                        logging.error("An error occurred", exc_info=True)
                                        matching_item = None
                                        continue        
                                else:
                                    continue
                else:
                    continue

async def main():
    blockurl = "https://api.nearblocks.io/v1/blocks/latest?limit=1"
    blockresponse = pip._vendor.requests.request("GET", blockurl)
    blockresponse = json.loads(blockresponse.text)
    startblock = blockresponse["blocks"][0]["block_height"]
    print(startblock)
    config = LakeConfig.mainnet()
    #config.start_block_height = 79913687
    startblock = int(startblock)-10
    print(startblock)
    if startblock > 0:
        #config.start_block_height = startblock
        config.start_block_height = 83556700
        load_dotenv()
        config.aws_access_key_id =  os.getenv('AWS_ACCESS_KEY_ID')
        config.aws_secret_key =  os.getenv('AWS_SECRET_ACCESS_KEY')

        stream_handle, streamer_messages_queue = streamer(config)
        while True:
            streamer_message = await streamer_messages_queue.get()
            await handle_streamer_message(streamer_message)
            print(
                f"Received Block #{streamer_message.block.header.height} from Lake Framework"
            )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())