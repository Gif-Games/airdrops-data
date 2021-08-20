import json
from os import error
import requests
import aiohttp
import asyncio
import sys
sys.path.append('../')
from utils.json2csv import json2csv

tokenDataUrl = "https://api.tzkt.io/v1/bigmaps/9923/keys/"

tokens = []
tokenData = []

with open("token_ids.json") as f:
    tokens = json.load(f)


async def fetch(session, tokenId):
    while True:
        try:
            async with session.get(tokenDataUrl+str(tokenId)+"/updates") as response:
                text = await response.text()
                data = json.loads(text)[2]
                print(f"Got data - {tokenId}")
                token_id = data['value']['token_id']
                owner_address = data['value']['owner']
                tokenData.append({
                    'Token ID': str(token_id),
                    'Unit #': data['value']['uid'],
                    "UNO amount": 3,
                    'Owner Address': owner_address,
                })
        except Exception as e:
            print("e", tokenId)
            print(e)
            continue
        break


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for tokenId in tokens:
            tasks.append(asyncio.create_task(fetch(session, tokenId)))
        await asyncio.gather(*tasks)
            
asyncio.run(main())

def getKey(data):
    return data['Token ID']

tokenData.sort(key=getKey)

with open('data.json', 'w') as f:
    json.dump(tokenData, f, indent=4)

json2csv(tokenData, 'data.csv')
