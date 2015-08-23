from django.db import models
from riotwatcher import RiotWatcher
import json
import os
import time
import copy
import requests
import os.path

requests.packages.urllib3.disable_warnings()

with open('apItems/dev_api_key', 'r') as f:
	devApiKey = f.readline()

patchesToCompare = ['5.11', '5.14']
servers = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
gameModes = ['NORMAL_5X5', 'RANKED_SOLO']
riotApi = RiotWatcher(devApiKey)

# Create your models here.
class Item(models.Model):
	item_name = models.CharField(max_length=200)
	buy_rate = models.FloatField(default=0)
	win_rate = models.FloatField(default=0)
	patch = models.CharField(max_length=200)
	def __str__(self):
		itemString = ''
		itemString += 'Patch: ' + self.patch + '\n'
		itemString += 'Item Name: ' + self.item_name + '\n'
		itemString += 'Buy Rate: ' + self.buy_rate + '\n'
		itemString += 'Win Rate: ' + self.win_rate + '\n'
		return itemString

def fetch():
	listOfGamesAndCount = getListOfGamesAndCount()
	numberOfGamesCountByRegion = listOfGamesAndCount[0]
	with open('static/apItems/data/games_count.json', 'w+') as f:
		json.dump(numberOfGamesCountByRegion, f)
		f.close()
	listOfGames = listOfGamesAndCount[1]
	dictionaryOfApItems = gatherAllApItems()

	gamesCount = 0

	for patch in patchesToCompare:
		for mode in gameModes:
			for server in servers:
				filePath = 'static/apItems/data/' + patch + '/' + mode + '/' + server + '.json'
				if os.path.isfile(filePath):
					continue
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
fetch()
