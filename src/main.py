import asyncio
import json
import os
from dotenv import load_dotenv
import re
import base64
import pip._vendor.requests 

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
                                    if parsed_data['data'][key]['index']:
                                        like_value = parsed_data['data'][key]['index'].get("like", None)
                                        if like_value is not None:
                                            like_value = json.loads(like_value)
                                        follow_value = parsed_data['data'][key]['index'].get("follow", None)
                                        if follow_value is not None:
                                            follow_value = json.loads(follow_value)
                                        poke_value = parsed_data['data'][key]['index'].get("poke", None)  
                                        if poke_value is not None:
                                            poke_value = json.loads(poke_value)  
                                        from_data = parsed_data['data']
                                        from_data = list(from_data.keys())
                                        from_data = from_data[0]
                                        notify_value = parsed_data['data'][key]['index']['notify']
                                        #print(notify_value)
                                       
                                        ## parsing the json string to json object
                                        notify_json = json.loads(notify_value)
                                        #print("Data is from: ",from_data)
                                        #print("Value of 'key': ",notify_json['key'])
                                        #print("Value of 'blockHeight': ",notify_json['value']['item']['blockHeight'])
                                        if like_value is not None:
                                            if notify_json['key'] == 'orangejoe.near':
                                                url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id=5222409941&text=New <b>LIKE</b> from "+from_data+" on near.social! View at https://near.social/#/mob.near/widget/MainPage.Post.Page?accountId="+notify_json['key']+"&blockHeight="+str(notify_json['value']['item']['blockHeight'])
                                                payload={}
                                                headers = {}
                                                response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                        if follow_value is not None:
                                            if notify_json['key'] == 'orangejoe.near':
                                                url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id=5222409941&text=New <b>FOLLOW</b> from "+from_data+" on near.social!"
                                                payload={}
                                                headers = {}
                                                response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                        if poke_value is not None:
                                            if notify_json['key'] == 'orangejoe.near':
                                                url = "https://api.telegram.org/botID:APIKEY/sendMessage?parse_mode=html&chat_id=5222409941&text=You just <b>POKED</b> by "+from_data+" on near.social!"
                                                payload={}
                                                headers = {}
                                                response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                                    else:
                                        continue
                else:
                    continue

async def main():
    config = LakeConfig.mainnet()
    #config.start_block_height = 79913687
    config.start_block_height = 83401102
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