import requests
import json


def gettopintent(text):
    query = text
    url = "https://bmichatbot.cognitiveservices.azure.com/luis/prediction/v3.0/apps/ecd4adf4-833c-4e88-b394-ec01e2bfcd17/slots/production/predict?subscription-key=382a227e00414effa59e0b00f653ed58&verbose=true&show-all-intents=true&log=true&query=" +query
    response = requests.request("GET", url)
    my_json = json.loads(response.text)
    topintent = my_json["prediction"]["topIntent"]
    return topintent


def gettopintentscore(text):
    query = text
    url = "https://bmichatbot.cognitiveservices.azure.com/luis/prediction/v3.0/apps/ecd4adf4-833c-4e88-b394-ec01e2bfcd17/slots/production/predict?subscription-key=382a227e00414effa59e0b00f653ed58&verbose=true&show-all-intents=true&log=true&query=" +query
    response = requests.request("GET", url)
    my_json = json.loads(response.text)
    topintent = my_json["prediction"]["topIntent"]
    score = my_json["prediction"]["intents"][topintent]["score"]
    return score


def extractnumber(text):
    query = text
    url = "https://bmichatbot.cognitiveservices.azure.com/luis/prediction/v3.0/apps/ecd4adf4-833c-4e88-b394-ec01e2bfcd17/slots/production/predict?subscription-key=382a227e00414effa59e0b00f653ed58&verbose=true&show-all-intents=true&log=true&query=" + query
    response = requests.request("GET", url)
    my_json = json.loads(response.text)
    number = my_json["prediction"]["entities"]["number"]
    return number