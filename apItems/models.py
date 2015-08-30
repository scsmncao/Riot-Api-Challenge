from django.db import models
from riotwatcher import RiotWatcher
import json
import os
import time
import copy
import requests
import os.path
import operator

requests.packages.urllib3.disable_warnings()

collectData = False


with open('apItems/dev_api_key', 'r') as f:
    devApiKey = f.readline()

patchesToCompare = ['5.11', '5.14']
servers = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
gameModes = ['NORMAL_5X5', 'RANKED_SOLO']
riotApi = RiotWatcher(devApiKey)

# Create your models here.
# Wanted to use a database but due to time constraints had to use json objects and static data

# class Item(models.Model):
#   item_name = models.CharField(max_length=200)
#   buy_rate = models.FloatField(default=0)
#   win_rate = models.FloatField(default=0)
#   patch = models.CharField(max_length=200)
#   def __str__(self):
#       itemString = ''
#       itemString += 'Patch: ' + self.patch + '\n'
#       itemString += 'Item Name: ' + self.item_name + '\n'
#       itemString += 'Buy Rate: ' + self.buy_rate + '\n'
#       itemString += 'Win Rate: ' + self.win_rate + '\n'
#       return itemString

# this will take a few days so start it early
def fetchDatafromApi(patch, mode, server):
    listOfGamesAndCount = getListOfGamesAndCount()
    numberOfGamesCountByRegion = listOfGamesAndCount[0]
    listOfGames = listOfGamesAndCount[1]
    dictionaryOfApItems = gatherAllApItems()

    gamesCount = 0

    filePath = 'apItems/static/apItems/data/' + patch + '/' + mode + '/' + server + '.json'
    if os.path.isfile(filePath):
        return
    gameIds = listOfGames[patch][mode][server]
    # need to split off the data to gather the data from the servers faster (if I store everything at once
    # it uses up too much memory)
    currentApItems = copy.deepcopy(dictionaryOfApItems)
    for game in gameIds:
        # riotwatcher has a dev limit so need to try catch to avoid limits
        try:
            matchData = riotApi.get_match(game, region=server.lower())
        except:
            pass
        for summoner in matchData['participants']:
            # get all items for that summoner
            for i in range(0,7):
                itemId = str(summoner['stats']['item' + str(i)])
                if itemId in dictionaryOfApItems:
                    item = currentApItems[itemId]
                    item['useCount'] += 1
                    item['championsUsed'][summoner['championId']] += 1
                    if summoner['stats']['winner']:
                        item['wins'] += 1
        gamesCount += 1
        print 'on game %i for %s in %s region and on patch %s' % (gamesCount, mode, server, patch)
    gamesCount = 0
    with open(filePath, 'w+') as f:
        json.dump(currentApItems, f)
        f.close()

def gatherAllApItems():
    allItems = riotApi.static_get_item_list(region="na", item_list_data='tags')
    itemsData = allItems['data']
    apItemDictionary = {}
    championsDictionary = getAllChampions()
    for itemID in itemsData.keys():
        itemId = itemsData[itemID]
        if 'tags' in itemId:
            if 'SpellDamage' in itemId['tags']:
                if 'Crystal Scar' not in itemId['name'] and 'Showdown' not in itemsData[itemID]['name']:
                    apItemDictionary[itemID] = {
                        'useCount': 0,
                        'championsUsed': copy.deepcopy(championsDictionary),
                        'wins': 0
                    }
    return apItemDictionary

def getAllChampions():
    allChamps = riotApi.get_all_champions(region="na")
    championsDictionary = {}
    for champion in allChamps['champions']:
        championsDictionary[champion['id']] = 0
    return championsDictionary

def getListOfGamesAndCount():
    finalGamesDictionary = {}
    numberOfGamesCountByRegion = {}
    for patch in patchesToCompare:
        finalGamesDictionary[patch] = {}
        numberOfGamesCountByRegion[patch] = {}
        for mode in gameModes:
            finalGamesDictionary[patch][mode] = {}
            numberOfGamesCountByRegion[patch][mode] = {}
            for server in servers:
                intialFilePath = 'apItems/AP_ITEM_DATASET/' + patch + '/' + mode + '/' + server + '.json'
                listOfGames = convertJsonToObject(intialFilePath)
                finalGamesDictionary[patch][mode][server] = listOfGames
                numberOfGamesCountByRegion[patch][mode][server] = len(listOfGames)
    return numberOfGamesCountByRegion, finalGamesDictionary

def convertJsonToObject(file_path):
    with open(file_path) as json_data:
        data = json.load(json_data)
        json_data.close()
        return data

# these will be combined into one method, don't need to do a triple for loop everytime!!!!!!

# we need to add the data from items that build from other items. Right now the data only exists for when the player
# ends the game with that particular item
def normalizeDataByAddingItemTree(patch, mode, server):
    filePath = 'apItems/static/apItems/data/' + patch + '/' + mode + '/' + server + '.json'
    finalPath = 'apItems/static/apItems/modified_data/' + patch + '/' + mode + '/' + server + '.json'
    if os.path.isfile(finalPath):
        return
    dataFile = convertJsonToObject(filePath)
    # first loop through the items with depth 3 since we want to add the rates consecutively from highest depth
    # to lowest (4 is the highest so we don't need to add to that), this isn't efficient since it runs 
    # through the data 4 times when it can be done in 1, but 
    # there's not enough time to store new data so this will have to do for now
    for i in range(3, 0, -1):
        print 'working on depth %i for server %s in mode %s in patch %s' % (i, server, mode, patch)
        for item in dataFile.keys():
            apItem = riotApi.static_get_item(item, item_data='all')
            if 'depth' not in apItem:
                apItem['depth'] = 1
            if apItem['depth'] == i and 'into' in apItem:
                for itemId in apItem['into']:
                    if itemId in dataFile:
                        print 'before use count %i for item %s' % (dataFile[item]['useCount'], item) 
                        dataFile[item]['useCount'] += dataFile[itemId]['useCount']
                        print 'after use count %i' % dataFile[item]['useCount']
                        dataFile[item]['wins'] += dataFile[itemId]['wins']
                        for champion in dataFile[itemId]['championsUsed'].keys():
                            dataFile[item]['championsUsed'][champion] += dataFile[itemId]['championsUsed'][champion]
    with open(finalPath, 'w+') as f:
        json.dump(dataFile, f)
        f.close()

def createFinalDataSet(patch, mode, server):
    filePath = 'apItems/static/apItems/modified_data/' + patch + '/' + mode + '/' + server + '.json'
    finalPath = 'apItems/static/apItems/final_data/' + patch + '/' + mode + '/' + server + '.json'
    if os.path.isfile(finalPath):
      return
    dataFile = convertJsonToObject(filePath)
    finalData = {}
    for item in dataFile.keys():
        topChampionsUsed = sorted(dataFile[item]['championsUsed'].items(), key=operator.itemgetter(1))
        finalTopChampionDict = {}
        for i in range(len(topChampionsUsed) - 1, len(topChampionsUsed) - 11, -1):
            if topChampionsUsed[i][1] != 0:
                finalTopChampionDict[topChampionsUsed[i][0]] = {
                                                                    'uses': topChampionsUsed[i][1],
                                                                    'name': riotApi.static_get_champion(int(topChampionsUsed[i][0]), champ_data='image')['image']['full']
                                                                }
            else:
                break
        if dataFile[item]['useCount'] != 0:
            win_rate = dataFile[item]['wins']/float(dataFile[item]['useCount'])
        else:
            win_rate = 0
        itemData = riotApi.static_get_item(item, item_data='all');
        fromItems = {};
        intoItems = {};
        if 'from' in itemData:
            fromItems = itemData['from'];
        if 'into' in itemData:
            intoItems = itemData['into'];
        finalData[item] = {
            # the 100000 is from 10000 games with 10 people in them so 10000 * 10
            'buy_rate': dataFile[item]['useCount']/100000.0,
            'win_rate': win_rate,
            'champions': finalTopChampionDict,
            'name': itemData['name'],
            'from': fromItems,
            'intoItems': intoItems
        }
    with open(finalPath, 'w+') as f:
        json.dump(finalData, f)
        f.close()

def createCombinedDataSet():
    for patch in patchesToCompare:
        finalCombinedData = {}
        finalPath = 'apItems/static/apItems/final_data/' + patch + '/' + 'combined_data.json'
        for mode in gameModes:
            for server in servers:
                filePath = 'apItems/static/apItems/final_data/' + patch + '/' + mode + '/' + server + '.json'
                # if os.path.isfile(finalPath):
                #     return
                dataFile = convertJsonToObject(filePath)
                for item in dataFile.keys():
                    if item not in finalCombinedData and dataFile[item]['buy_rate'] != 0:
                        finalCombinedData[item] = {
                            'buy_rate': 0,
                            'win_rate': 0,
                            'name': dataFile[item]['name'],
                            'champions': {},
                            'from': dataFile[item]['from'],
                            'into': dataFile[item]['intoItems']
                        }
                    if dataFile[item]['buy_rate'] != 0:
                        finalCombinedData[item]['buy_rate'] += dataFile[item]['buy_rate']
                        finalCombinedData[item]['win_rate'] += dataFile[item]['win_rate']
                    for champion in dataFile[item]['champions'].keys():
                        if champion not in finalCombinedData[item]['champions']:
                            finalCombinedData[item]['champions'][champion] = dataFile[item]['champions'][champion]
                        else:
                            finalCombinedData[item]['champions'][champion]['uses'] += dataFile[item]['champions'][champion]['uses']
        for item in finalCombinedData.keys():
            if dataFile[item]['buy_rate'] != 0:
                finalCombinedData[item]['buy_rate'] = round(finalCombinedData[item]['buy_rate']/(len(servers) * len(gameModes) * 1.0), 4)
                finalCombinedData[item]['win_rate'] = round(finalCombinedData[item]['win_rate']/(len(servers) * len(gameModes) * 1.0), 4)
            topChampionsUsed = sorted(finalCombinedData[item]['champions'].items(), key=lambda item: item[1]['uses'])
            finalChampionList = []
            for champion in topChampionsUsed:
                finalChampionList.append(champion[1]['name'])
            finalChampionList.reverse()
            finalCombinedData[item]['champions'] = finalChampionList

        with open(finalPath, 'w+') as f:
            json.dump(finalCombinedData, f)
            f.close()

def createFinalizedDataSet():
    for patch in patchesToCompare:
        for mode in gameModes:
            for server in servers:
                print 'fetching data'
                fetchDatafromApi(patch, mode, server)
                print 'normalizing'
                normalizeDataByAddingItemTree(patch, mode, server)
                print 'creating final data set'
                createFinalDataSet(patch, mode, server)

if collectData:
    createFinalizedDataSet()
    print 'combining data'
    createCombinedDataSet()
