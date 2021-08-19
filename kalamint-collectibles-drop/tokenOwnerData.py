import json
from os import error
import requests
import aiohttp
import asyncio
import sys
sys.path.append('../')
from utils.kalamintUsername import getUsername
from utils.json2csv import json2csv

# tokenDataUrl = "https://catchmyserver-mainnet.kalamint.io:8443/km/conseil/tokenData?tokenId="
tokenDataUrl = "https://api.tzkt.io/v1/bigmaps/861/keys/"

tokens = []
tokenData = []

with open("token_ids.json") as f:
    tokens = json.load(f)


async def fetch(session, tokenId):
    while True:
        try:
            async with session.get(tokenDataUrl+str(tokenId)) as response:
                text = await response.text()
                data = json.loads(text)
                print(f"Got data - {tokenId}")
                token_id = data['value']['token_id']
                owner_address = data['value']['owner']
                print(data['value']['extras']['name'])
                kalamint_username = getUsername(owner_address)
                tokenData.append({
                    'token_id': str(token_id),
                    'name': data['value']['extras']['name'],
                    'UNO amount': "33" if token_id == "3162" else "6",
                    'owner_address': owner_address,
                    'kalamint_username': kalamint_username
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

# tokenData.append({
#     'token_id': str(1),
#     'UNO amount': "6",
#     'owner_address': "owner_address",
#     'kalamint_username': "kalamint_username"
# })
def getKey(data):
    return data['token_id']

tokenData.sort(key=getKey)

with open('data.json', 'w') as f:
    json.dump(tokenData, f, indent=4)

json2csv(tokenData, 'data.csv')
