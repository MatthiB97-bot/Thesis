import requests
import json
import Globals


# This function sends every message of the user to the NLP module and then returns a json containing the top intent
# and all detected entities, if there are any
def sendquery(text):
    query = text
    url = "https://bmichatbot.cognitiveservices.azure.com/luis/prediction/v3.0/apps/ecd4adf4-833c-4e88-b394-ec01e2bfcd17/slots/production/predict?subscription-key=382a227e00414effa59e0b00f653ed58&verbose=true&show-all-intents=true&log=true&query=" + query
    response = requests.request("GET", url)
    Globals.jsonobject = json.loads(response.text)


# This function extracts the top intent from the JSON received from the NLP module
def gettopintent():
    topintent = Globals.jsonobject["prediction"]["topIntent"]
    return topintent


# This function returns the score of the top intent
def gettopintentscore():
    topintent = Globals.jsonobject["prediction"]["topIntent"]
    score = Globals.jsonobject["prediction"]["intents"][topintent]["score"]
    return score


# this function extracts the number entity from the JSON received from the NLP module
def extractnumber():
    number = Globals.jsonobject["prediction"]["entities"]["number"]
    return number[0]


# this function extracts the date entity from the JSON received from the NLP module
def extractdate():
    date = Globals.jsonobject["prediction"]["entities"]["datetimeV2"][0]["values"][0]["resolution"][0]["value"]
    date = date.replace(" ", "T")

    if "T" not in date:
        date = date + "T00:00:00"

    return date
