import requests
import json
import re

def numberOfCrafts():
    url = "https://www.pathofexile.com/character-window/get-stash-items?league=LEAGUE_NAME&realm=pc&accountName=ACCOUNT_NAME&tabs=0&tabIndex=INDEX_OF_TAB"
    id = "POESESSID:SESSION_ID_HERE"
    headers = {"cookie": id}

    response = requests.get(url, headers=headers)
    #If response is forbidden, session ID value is wrong most likely.
    
    data = response.json()

    keyForItems = "items"
    itemsInStash = data[keyForItems] #itemsInStash is [dicts] 
    itemToIdentify = "Horticrafting Station"

    dictCrafts = {
        "Augment": {},
        "Change": {},
        "Reroll": {},
        "Remove": {
            "Only": {},
            "add": {},
            "non": {},
            },
        "Reforge": {}, #take index -1 of regex array
        "Misc": {},
    }

    for item in itemsInStash:
        if item["typeLine"] ==  itemToIdentify:
            mods = item["craftedMods"]
            for singleCraft in mods:
                filteredString = re.findall(r'\{(.*?)\}', singleCraft) #find all the strings between curly brackets
                storeCraftInfo(dictCrafts, filteredString)

    print(json.dumps(dictCrafts, indent=1))


def storeCraftInfo(dataHolder:dict, stringArray:[str]):
    length = len(stringArray)
    firstKeyword = stringArray[0]
    miscDict = dataHolder["Misc"]
    dictToPopulate = dataHolder.get(firstKeyword, miscDict) #default value of misc, where any additional crafts are stored

    if firstKeyword == "Remove":
        if length == 2:
            secondKeyword = "Only"
        elif "non" in stringArray[1]:
            secondKeyword = "non"
        else:
            secondKeyword = "add"
        dictToPopulate = dictToPopulate[secondKeyword]
    
    targetCraft = stringArray[-1]
    currentCount = dictToPopulate.setdefault(targetCraft,0) + 1
    dictToPopulate[targetCraft] = currentCount

if __name__ == "__main__":
    numberOfCrafts()