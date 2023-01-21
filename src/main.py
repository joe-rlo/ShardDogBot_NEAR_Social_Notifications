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
                if receipt_execution_outcome.receipt.predecessor_id == "sharddog.near" or receipt_execution_outcome.receipt.predecessor_id == "v1.keypom.near" or receipt_execution_outcome.receipt.receiver_id == "readylayerone_staking.poolv1.near":
                    print("found something")
                    print(receipt_execution_outcome.receipt.receipt)
                    json_obj = receipt_execution_outcome.receipt.receipt
                    if json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("args") is not None:
                        args = json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("args")
                        decodedResults = base64.b64decode(args).decode()
                        print(base64.b64decode(args).decode())
                    if json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("method_name") is not None:
                        methodName = json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("method_name")
                        print(methodName)
                        if methodName == 'create_drop':
                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?chat_id=-602480598&text=WOOF! New drop created from ShardDog on Mainnet!"
                            payload={}
                            headers = {}
                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                        if methodName == 'create_account':
                            accountName = json.loads(decodedResults).get("new_account_id")
                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?chat_id=-602480598&text=WOOF! "+accountName+ " was just created using KeyPom! Check https://explorer.near.org/?query=" + receipt_execution_outcome.execution_outcome.id+ " to see if it came from ShardDog!"
                            payload={}
                            headers = {}
                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                        #NEEDS TO CATCH THE CORRECT ADDRESS AND TEST
                        if methodName == 'deposit_and_stake':
                            depositamount = int(json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("deposit"))/1000000000000000000000000
                            depositbywho = json_obj.get("Action", {}).get("signer_id")
                            print(depositamount)
                            print(depositbywho)
                            url = "https://api.telegram.org/botID:APIKEY/sendMessage?chat_id=-602480598&text=WOOF! WOOF! New deposit on validator (" + str(depositamount) +" by "+depositbywho+")"
                            payload={}
                            headers = {}
                            response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                    if json_obj.get("Action", {}).get("actions", [{}])[0].get("Stake", {}).get("stake") is not None:
                        print("found stake total")
                        newTotal = int(json_obj.get("Action", {}).get("actions", [{}])[0].get("Stake", {}).get("stake"))/1000000000000000000000000
                        print(newTotal)
                        url = "https://api.telegram.org/botID:APIKEY/sendMessage?chat_id=-602480598&text=WOOF! WOOF! Validator staked amount updated: "+str(newTotal)+"N"
                        payload={}
                        headers = {}
                        response = pip._vendor.requests.request("GET", url, headers=headers, data=payload)
                    else: 
                        methodName = json_obj.get("Action", {}).get("actions", [{}])[0].get("FunctionCall", {}).get("method_names")
                        print(methodName)
                else:
                    continue

async def main():
    config = LakeConfig.mainnet()
    #config.start_block_height = 79913687
    config.start_block_height = 80392968
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