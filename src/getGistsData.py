import ast, socket, re, sys, argparse, os, subprocess, time, orderedset
from pprint import pprint
from urllib.parse import urlparse
import requests, json
from requests.auth import HTTPBasicAuth

username = '***'
password = '***'

count = 0
list = []
for dirName, subdirList, fileList in os.walk('/home/brokenquark/Workspace/ICSME19/gist-src'):
    for fileName in fileList:
        list.append(fileName)

ix = [44,45,75,76,83,2361,3364,4970]

# for index in ix:
#     try:
#         dump = open('dump2.csv', 'a')
#         url = f'https://api.github.com/gists/{list[index][0:-3]}'
#         response = requests.get(url, auth=HTTPBasicAuth(username, password))
#         try:
#             author = response.json()['owner']['login']
#         except:
#             continue
#         url = f'https://api.github.com/users/{author}'
#         response = requests.get(url, auth=HTTPBasicAuth(username, password))
#         publicRepoCount = response.json()['public_repos']
#         publicGistCount = response.json()['public_gists']
#         followers = response.json()['followers']
#         following = response.json()['following']
#         createdAt = response.json()['created_at']
#         dump.write(f'{index},{list[index]},{author},{publicRepoCount},{publicGistCount},{followers},{following},{createdAt[0:10]}\n')
#         dump.close()
#     except:
#         print(index, end=',')
#         time.sleep(300)


dump = open('dump2.csv', 'r')
list = []
for line in dump:
    list.append(line)

set = orderedset.OrderedSet(list)

dump2 = open('author2.csv', 'w')

for item in set:
    dump2.write(item)

dump2.close()