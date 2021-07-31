import json
import requests
import aiohttp
import asyncio
import sys
sys.path.append('../')
from utils.kalamintUsername import getUsername
from utils.json2csv import json2csv

tokenDataUrl = "https://catchmyserver-mainnet.kalamint.io:8443/km/conseil/tokenData?tokenId="

tokens = {}
tokenData = []

with open("token_ids.json") as f:
    tokens = json.load(f)


async def fetch(session, blockId, tokenId):
    while True:
        try:
            async with session.get(tokenDataUrl+tokenId) as response:
                text = await response.text()
                data = json.loads(text)
                print(f"Got data - {blockId}")
                token_id = data['value']['token_id']
                owner_address = data['value']['owner']
                kalamint_username = getUsername(owner_address)
                tokenData.append({
                    'block_id': blockId,
                    'token_id': token_id,
                    'owner_address': owner_address,
                    'kalamint_username': kalamint_username
                })
        except:
            print("e", blockId)
            continue
        break


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for blockId in tokens:
            tokenId = tokens[blockId]
            tasks.append(asyncio.create_task(fetch(session, blockId, tokenId)))
        await asyncio.gather(*tasks)
            
asyncio.run(main())


def getKey(data):
    return data['block_id']

tokenData.sort(key=getKey)

with open('tokenData.json', 'w') as f:
    json.dump(tokenData, f, indent=4)

json2csv(tokenData, 'data.csv')
