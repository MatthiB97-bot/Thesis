import xmltodict, json
import Globals

xmlname = "BMILevel1.xml"


def read_input_values(integer):
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        return jsonvar["definitions"]["decision"]["decisionTable"]["input"][integer]["inputValues"]["text"]
    except TypeError:
        for jsonvar["decision"] in jsonvar["definitions"]:
            return jsonvar["definitions"]["decision"]["decisionTable"]["input"][1]["inputValues"]["text"]


def read_xml():
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    Globals.myList.clear()
    k = -1

    for jsonvar["inputData"] in jsonvar["definitions"]:
        k = k+1
        if k < len(jsonvar["definitions"]["inputData"]):
            Globals.myList.append(jsonvar["definitions"]["inputData"][k]["@name"])


def read_decision_key():
    Globals.decisionkey.clear()
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        Globals.decisionkey.append(jsonvar["definitions"]["decision"]["@id"])
    except TypeError:
        Globals.decisionkey.append(jsonvar["definitions"]["decision"][0]["@id"])

    return Globals.decisionkey[0]


def readoutput():
    Globals.output.clear()
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        Globals.output.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
    except TypeError:
        Globals.output.append(jsonvar["definitions"]["decision"][0]["decisionTable"]["output"]["@name"])
