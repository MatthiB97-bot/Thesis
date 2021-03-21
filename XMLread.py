import xmltodict, json
import Globals

xmlname = "DogLicenseUpdated1.xml"


def same_values():
    with open(xmlname, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    sameval = []
    remlist = []
    decisions = range(len(jsonvar["definitions"]["decision"]))
    try: #one decision table
        rules = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]))
        try:
            entries = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"]))  # number of entries (multiple rules)
        except:
            entries = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]))  # number of entries (one rule)
        try: #multiple rules
            for k in entries:
                sameval.clear()
                a = 0
                for m in rules:
                    sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                if len(sameval) != 0:
                    for i in sameval: #check if all values are the same
                        if i == sameval[0]:
                            a = a + 1
                    if len(sameval) == a and \
                            jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                        Globals.d[str(Globals.myList[k])] = {}
                        Globals.d[str(Globals.myList[k])]["value"] = \
                            jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                        remlist.append(k)
        except: #one rule
            for k in entries:
                sameval.clear()
                a = 0
                sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                if len(sameval) != 0:
                    print(sameval)
                    for i in sameval:
                        if i == sameval[0]:
                            a = a + 1
                    if len(sameval) == a and \
                            jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                        Globals.d[str(Globals.myList[k])] = {}
                        Globals.d[str(Globals.myList[k])]["value"] = \
                            jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                        remlist.append(k)
        if len(remlist) != 0:
            for n in sorted(remlist, reverse=True):
                Globals.myList.remove(Globals.myList[n])
        remlist.clear()
    except: #multiple decision tables
        w = -1
        checklist = []
        for n in decisions:
            rules = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]))
            try:
                entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"])) #number of entries (multiple rules)
            except:
                entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"])) #number of entries (one rule)
            for k in entries:
                if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in checklist:
                    checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"]) #ensure uniqueness
                    a = 0
                    if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.oilist:
                        w = w + 1
                    sameval.clear()
                    try: #multiple rules in decision table
                        for m in rules:
                            sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                        if len(sameval) != 0:
                            for i in sameval:
                                if i == sameval[0]:
                                    a = a + 1
                                if len(sameval) == a and \
                                        jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                    Globals.d[str(Globals.myList[w])] = {}
                                    Globals.d[str(Globals.myList[w])]["value"] = \
                                    jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                                    remlist.append(w)
                                    print(remlist)
                    except: #only one rule in decision table
                        sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                        if len(sameval) != 0:
                            for i in sameval:
                                if i == sameval[0]:
                                    a = a + 1
                                if len(sameval) == a and \
                                        jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                    Globals.d[str(Globals.myList[w])] = {}
                                    Globals.d[str(Globals.myList[w])]["value"] = \
                                    jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                                    remlist.append(w)
                                    print(remlist)
        if len(remlist) !=0:
            for b in sorted(remlist, reverse=True):
                Globals.myList.remove(Globals.myList[b])
        remlist.clear()
        checklist.clear()


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
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in list and\
                        jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in Globals.myList:
                    Globals.myList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
                elif jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] in Globals.myList:
                    pass
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
