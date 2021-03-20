import xmltodict, json
import Globals

xmlname = "threelayers3.xml"


def same_values():
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    sameval = []
    remlist = []
    rules = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]))
    entries = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"]))
    decisions = range(len(jsonvar["definitions"]["decision"]))
    try:
        for k in entries:
            sameval.clear()
            a = 0
            for m in rules:
                sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
            for i in sameval:
                if i == sameval[0]:
                    a = a + 1
            if len(sameval) == a and \
                    jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                Globals.d[str(Globals.myList[k])] = {}
                Globals.d[str(Globals.myList[k])]["value"] = \
                    jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                remlist.append(k)
        for n in sorted(remlist, reverse=True):
            Globals.myList.remove(Globals.myList[n])
        remlist.clear()
    except:
        for n in decisions:
            for k in entries:
                a = 0
                sameval.clear()
                for m in rules:
                    sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                for i in sameval:
                    if i == sameval[0]:
                        a = a + 1
                    if len(sameval) == a and \
                            jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"][
                                "@typeRef"] not in ["double", "integer"]:
                        Globals.d[str(Globals.myList[k])] = {}
                        Globals.d[str(Globals.myList[k])]["value"] = \
                        jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                        remlist.append(k)
                for n in sorted(remlist, reverse=True):
                    Globals.myList.remove(Globals.myList[n])
                remlist.clear()


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
    list = []
    list.clear()

    try:
        for i in range(len(jsonvar["definitions"]["decision"])):
            list.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in list \
                        and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in Globals.myList:
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
