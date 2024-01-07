import requests
import json


f = open("data/SandPSymbols.txt", "r")
Lines = f.readlines()
stockList = []
for i in Lines:
    stockList.append(i.strip())

fo = open("data/SandPNames.txt", "a")
for s in stockList:
    x = requests.get('https://www.macrotrends.net/stocks/charts/' + s)
    html = x.content.decode("utf-8")
    fo.writelines(x.url + "\n")