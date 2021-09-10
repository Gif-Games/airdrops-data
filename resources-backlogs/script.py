import json
import requests
import sys
import aiohttp
import asyncio
import datetime
sys.path.append('../')
from utils.json2csv import json2csv

tokens = {}
with open("token_ids.json") as f:
    tokens = json.load(f)

tezotopData = {}
with open("tezotopData.json") as f:
    tezotopData = json.load(f)

url = "https://api.tzkt.io/v1/operations/transactions?target=KT1EpGgjQs73QfFJs9z7m1Mxm5MTnpC2tqse&entrypoint=mint&limit=10&parameter.token_id="
tokenData = []

def toTimestamp(time: str):
    return datetime.datetime.timestamp(
        datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    )

def addTezotopData(blockId, time):
    hours = round((toTimestamp("2021-09-10 14:00:00") - toTimestamp(time)) / 3600, 4)
    tokenData.append({
        'Block ID': blockId,
        'Minting time': time,
        'UNO Backlog': round(hours * 0.0005 * tezotopData[blockId]["UNO"], 4),
        'ENR Backlog': round(hours * 0.5 * tezotopData[blockId]["ENR"], 4),
        'MIN Backlog': round(hours * 0.25 * tezotopData[blockId]["MIN"], 4),
        'MCH Backlog': round(hours * 0.25, 4),
    })

async def fetch(session, blockId, tokenId):
    while True:
        try:
            async with session.get(url+str(tokenId)) as response:
                text = await response.text()
                obj = json.loads(text)
                data = {}
                for d in obj:
                    if d['status'] == 'applied':
                        data = d
                if len(data) == 0:
                    print("!!!Error" + tokenId)
                    a = 1/0
                print(f"Got data - {tokenId}")
                time = data['timestamp'].replace('T', ' ')[:-1]
                addTezotopData(blockId, time)
        except Exception as e:
            print("e", tokenId)
            print(e)
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
    return data['Block ID']

tokenData.sort(key=getKey)

for id in range(177, 210):
    blockId = '0' + str(id)
    addTezotopData(blockId, "2021-08-09 16:00:00")

for id in range(210, 213):
    blockId = '0' + str(id)
    addTezotopData(blockId, "2021-08-30 17:00:00")

with open('data.json', 'w') as f:
    json.dump(tokenData, f, indent=4)

json2csv(tokenData, 'data.csv')
