import xmltodict, json
import Globals

xmlname = "ski_guide.xml"


def read_input_values(integer):
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                    return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputValues"]["text"]
    except:
        return jsonvar["definitions"]["decision"]["decisionTable"]["input"][integer]["inputValues"]["text"]


def read_xml():
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    Globals.myList.clear()
    Globals.oilist.clear()
    try:
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] != \
                        jsonvar["definitions"]["decision"][a-1]["decisionTable"]["output"]["@name"]:
                    Globals.myList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
                else:
                    Globals.oilist.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
    except:
        for a in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
            Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][a]["inputExpression"]["text"])
    print(Globals.myList)


def read_decision_key():
    Globals.decisionkey.clear()
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        Globals.decisionkey.append(jsonvar["definitions"]["decision"]["@id"])
    except TypeError:
        for a in range(len(jsonvar["definitions"]["decision"])):
            if not jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] in Globals.oilist:
                Globals.decisionkey.append(jsonvar["definitions"]["decision"][a]["@id"])
    return Globals.decisionkey[0]


def readoutput():
    Globals.output.clear()
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        Globals.output.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
    except TypeError:
        for a in range(len(jsonvar["definitions"]["decision"])):
            if not jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] in Globals.oilist:
                Globals.output.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"])
    print(Globals.output)
