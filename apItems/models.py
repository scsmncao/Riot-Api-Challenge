from django.db import models
from riotwatcher import RiotWatcher
import json
import os

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
	listOfGames = getListOfGames()
	dictionaryOfApItems = gatherAllApItems()
	
	# for patch in patchesToCompare:

def gatherAllApItems():
	allItems = riotApi.static_get_item_list(region="na", item_list_data='tags')
	itemsData = allItems['data']
	apItemDictionary = {}
	for itemID in itemsData.keys():
		itemId = itemsData[itemID]
		if 'tags' in itemId:
			if 'SpellDamage' in itemId['tags']:
				if 'Crystal Scar' not in itemId['name'] and 'Showdown' not in itemsData[itemID]['name']:
					apItemDictionary[itemID] = 0
	return apItemDictionary
	

def getListOfGames():
	finalGamesDictionary = {}
	for patch in patchesToCompare:
		finalGamesDictionary[patch] = {}
		for mode in gameModes:
			finalGamesDictionary[patch][mode] = {}
			for server in servers:
				intialFilePath = 'apItems/AP_ITEM_DATASET/' + patch + '/' + mode + '/' + server + '.json'
				listOfGames = convertJsonToObject(intialFilePath)
				finalGamesDictionary[patch][mode][server] = listOfGames
	return finalGamesDictionary

def convertJsonToObject(file_path):
	with open(file_path) as json_data:
		data = json.load(json_data)
		json_data.close()
		return data
fetch()
