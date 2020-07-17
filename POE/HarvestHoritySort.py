import requests
import json
import re

def numberOfCrafts():
    # url = "https://www.pathofexile.com/character-window/get-stash-items?league=LEAGUE_NAME&realm=pc&accountName=ACCOUNT_NAME&tabs=0&tabIndex=INDEX_OF_TAB"
    # id = "POESESSID:SESSION_ID_HERE"

    with open('POE/credentials.json') as f:
        credentials = json.load(f)

    url = credentials.get("url")
    id = "POESESSID=" + credentials.get("POESESSID")
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
        "Randomise": {},
        "Reforge": {}, #take index -1 of regex array
        "Misc": {},
    }

    for item in itemsInStash:
        if item["typeLine"] ==  itemToIdentify:
            mods = item["craftedMods"]
            for singleCraft in mods:
                #\{(.*?)\} regex will find all strings that are between curly brackets
                filteredString = re.findall(r'([non-]*?[A-Z][a-z]+)', singleCraft) #find all the strings between curly brackets
                storeCraftInfo(dictCrafts, filteredString)

    #bark lines
    for craft in dictCrafts:
        print("-----" + craft + "-----")
        for typeOfCraft in dictCrafts[craft]:
            if (craft == "Remove"):
                for subtype in dictCrafts[craft][typeOfCraft]:
                    print(typeOfCraft + "-" + subtype + ": {}".format(dictCrafts[craft][typeOfCraft][subtype]))
            else:
                print(typeOfCraft + ": {}".format(dictCrafts[craft][typeOfCraft]))


def storeCraftInfo(dataHolder:dict, stringArray:[str]):
    length = len(stringArray)
    firstKeyword = stringArray[0]
    # miscDict = dataHolder["Misc"]
    dictToPopulate = dataHolder.get(firstKeyword, "Misc") #default value of misc, where any additional crafts are stored

    if firstKeyword == "Remove":
        if length == 2:
            secondKeyword = "Only"
        elif "non" in stringArray[1]:
            secondKeyword = "non"
        else:
            secondKeyword = "add"
        dictToPopulate = dictToPopulate[secondKeyword]
    
    
    #Capture what the elemental change is.
    if firstKeyword == "Change":
        targetCraft = stringArray[1] + " to " + stringArray[3]
    elif dictToPopulate == "Misc":
        targetCraft = " ".join(stringArray)
        dictToPopulate = dataHolder["Misc"]
    elif firstKeyword == "Augment":
        targetCraft = findTargetCraft(stringArray)
    else:
        targetCraft = stringArray[-1]
    currentCount = dictToPopulate.setdefault(targetCraft,0) + 1
    dictToPopulate[targetCraft] = currentCount


def findTargetCraft(stringArray:[str]):
    '''
    This is for the "Augment" craft. The regex finds the capital words and the placement of 
    targeted craft is different depending on if it is a lucky craft or not.
    '''
    possibleAugmentCrafts = {"Fire", "Cold", "Lightning", "Physical", "Attack",
                        "Life", "Speed", "Defence", "Caster", "Critical", "Chaos", "Influence"}

    #If it is a "Lucky" craft, then the craft is located one index before.
    if stringArray[-1] == "Lucky":
        return stringArray[-2]

    #Using the reversed stringArray for quicker lookup time since craft is usually near the end of the array.
    for string in reversed(stringArray):
        if string in possibleAugmentCrafts:
            return string
    
    unidentified = "Can not identify craft for: " + " ".join(stringArray)
    return unidentified

if __name__ == "__main__":
    numberOfCrafts()