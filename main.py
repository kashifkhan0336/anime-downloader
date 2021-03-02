#!/usr/bin/python
# -*- coding: utf-8 -*-
from requests import get
from json import dumps, loads
from bs4 import BeautifulSoup
import subprocess
import sys
import time
import os
import pickle

anime_id = '1735'

print(len(sys.argv))
if (len(sys.argv) > 1):
    anime_show = sys.argv[1]
    episode = sys.argv[2]
else:
    episode = str(int(pickle.load(open("config.pk", mode="rb")))+1)
    print("Last downloaded episode : ",str(int(pickle.load(open("config.pk", mode="rb")))))
    print("Episode to download : "+episode)
    pickle.dump(episode, open("config.pk", mode="wb"))
# url = "https://aninow.net/watch/naruto-shippuuden/episode/"+episode+"/"+anime_id

url = 'https://vidstreaming.io/videos/'+ anime_show +'-episode-' + episode
print(url)
response = get(url)

def get_page(url):
    return get(url)

headers = {
    'authority':'vidstreaming.io',
    'accept':'application/json, text/javascript, */*; q=0.01',
    'x-requested-with':'XMLHttpRequest',
    'accept-language':'en-US,en;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'sec-fetch-site':'same-origin',
    'sec-fetch-mode':'cors',
    'sec-fetch-dest':'empty',
    'referer':'https://vidstreaming.io/streaming.php?id=MjIwOQ==&title=Naruto+Shippuden&typesub=SUB&sub=&cover=aW1hZ2VzL2FuaW1lL25hcnV0b19zaGlwcHVkZW4uanBn',
    'cookie':'__cfduid=d254364753ba04fc2538ce40840c1db501598911521; _ga=GA1.2.36461707.1598929636; _gid=GA1.2.1672011179.1599099798; MjIwOQ===1019.61148',
}

if response.status_code == 200:
    print('200 ok \nParsing...')
    parsed = BeautifulSoup(response.content, features='lxml')
    print('Extracting id')
    stream_id = parsed.select('iframe')[0].attrs['src'].split('&')[0].split(
        '?id=')[1]
    if stream_id:
        streams = []
        print('ID => ', stream_id)
        response = get('https://vidstreaming.io/ajax.php',
                       headers=headers,
                       params=(
                           ('id', str(stream_id)),
                           ('title', 'Naruto Shippuden'),
                           ('typesub', 'SUB'),
                           ('sub', ''),
                           ('cover',
                            'aW1hZ2VzL2FuaW1lL25hcnV0b19zaGlwcHVkZW4uanBn'),
                           ('refer', 'none'),
                       ))
        streams_data = loads(response.text)

        # print(dict(streams_data))

        for (k, v) in dict(streams_data).items():
            #print('Key: ' + k)
            if k.startswith('source'):
                #print(v[0]['file'])
                streams.append(v[0]['file'])
            #print('Value: ' + str(v))
        #print(streams[0])
        
        print(len(streams), "streams Found")
        print("Triggering download with 1 stream")
        #system("idman /d "+streams[0]+" /f "+episode+".mp4"+" /n")
        print(streams[0])
        print(streams[1])
        subprocess.call(
            ["C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe", "/d",
             str(streams[0]), "/f", anime_show+'-'+episode + ".mp4", "/n"])
        t = input("Does downloading start?")
        if (t == "y" or t == "yes"):

            print("Yippe")
        else:
            print("Triggering download with 2 stream")
            subprocess.call(
                ["C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe", "/d",
                 str(streams[1]), "/f", anime_show+'-'+episode + ".mp4", "/n"])
            time.sleep(5)

    else:
        print('ERROR')