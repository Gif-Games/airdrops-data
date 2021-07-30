import subprocess
import json

def getUsername(address: str):
    command = f'''
    curl -s 'https://catchmyserver-mainnet.kalamint.io:8443/getUsername' \
    -H 'authority: catchmyserver-mainnet.kalamint.io:8443' \
    -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
    -H 'accept: application/json, text/plain, */*' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
    -H 'content-type: application/json;charset=UTF-8' \
    -H 'origin: https://kalamint.io' \
    -H 'sec-fetch-site: same-site' \
    -H 'sec-fetch-mode: cors' \
    -H 'sec-fetch-dest: empty' \
    -H 'referer: https://kalamint.io/' \
    -H 'accept-language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
    --data-raw '{{"walletAddress":"{address}"}}' \
    --compressed
    '''

    a = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    d = json.loads(a)
    return d['username']
