import xmltodict
import json
import Globals


def same_values(decision):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    sameval = []
    remlist = []
    decisions = range(len(jsonvar["definitions"]["decision"]))
    try:  # one decision table
        rules = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]))
        try:
            entries = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"]))  # number of entries (multiple rules)
        except:
            entries = range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]))  # number of entries (one rule)
        try:  # multiple rules
            try:  # one entry
                a = 0
                for m in rules:
                    sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][m]["inputEntry"]["text"])
                if len(sameval) != 0:
                    for i in sameval:  # check if all values are the same
                        if i == sameval[0]:
                            a = a + 1
                    if len(sameval) == a and jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                        Globals.d[str(Globals.myList[0])] = {}
                        Globals.d[str(Globals.myList[0])]["value"] = jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"]["text"].strip('"')
                        remlist.append(0)
            except:  # multiple entries
                for k in entries:
                    sameval.clear()
                    a = 0
                    for m in rules:
                        sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                    if len(sameval) != 0:
                        for i in sameval:  # check if all values are the same
                            if i == sameval[0]:
                                a = a + 1
                        if len(sameval) == a and jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                            Globals.d[str(Globals.myList[k])] = {}
                            Globals.d[str(Globals.myList[k])]["value"] = jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                            remlist.append(k)
        except:  # one rule
            try:  # one entry
                a = 0
                for m in rules:
                    sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]["text"])
                if len(sameval) != 0:
                    for i in sameval:  # check if all values are the same
                        if i == sameval[0]:
                            a = a + 1
                    if len(sameval) == a and \
                            jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"][
                                "@typeRef"] not in ["double", "integer"]:
                        Globals.d[str(Globals.myList[0])] = {}
                        Globals.d[str(Globals.myList[0])]["value"] = \
                        jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]["text"].strip('"')
                        remlist.append(0)
            except:  # multiple entries
                for k in entries:
                    sameval.clear()
                    a = 0
                    sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                    if len(sameval) != 0:
                        for i in sameval:
                            if i == sameval[0]:
                                a = a + 1
                        if len(sameval) == a and jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                            Globals.d[str(Globals.myList[k])] = {}
                            Globals.d[str(Globals.myList[k])]["value"] = jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                            remlist.append(k)
        if len(remlist) != 0:
            try:  # one decision, multiple rules, multiple entries - all input the same
                for n in sorted(remlist, reverse=True):
                    Globals.myList.remove(Globals.myList[n])
            except:  # one decision, multiple rules, one entry -- all input the same
                Globals.myList.remove(Globals.myList[0])
            remlist.clear()
    except:  # multiple decision tables
        w = -1
        checklist = []
        for n in decisions:
            if decision == jsonvar["definitions"]["decision"][n]["decisionTable"]["output"]["@name"]:
                print("ok")
                rules = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]))
                try:
                    entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"]))  # number of entries (multiple rules)
                except:
                    entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]))  # number of entries (one rule)
                for k in entries:
                    if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in checklist:
                        checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"])  # ensure uniqueness
                        a = 0
                        if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.oilist:
                            w = w + 1
                        sameval.clear()
                        try:  # multiple rules
                            try:  # one entry
                                for m in rules:
                                    sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0]:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[w])] = {}
                                            Globals.d[str(Globals.myList[w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"]["text"].strip('"')
                                            remlist.append(w)
                                            print(remlist)
                            except:  # multiple entries
                                for m in rules:
                                    sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0]:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[w])] = {}
                                            Globals.d[str(Globals.myList[w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                                            remlist.append(w)
                                            print(remlist)
                        except:  # one rule
                            try:  # one entry
                                sameval.append(
                                    jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0]:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[w])] = {}
                                            Globals.d[str(Globals.myList[w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]["text"].strip('"')
                                            remlist.append(w)
                                            print(remlist)
                            except:  # multiple entries
                                sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0]:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[w])] = {}
                                            Globals.d[str(Globals.myList[w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                                            remlist.append(w)
                                            print(remlist)
        if len(remlist) != 0:
            for b in sorted(remlist, reverse=True):
                Globals.myList.remove(Globals.myList[b])
        remlist.clear()
        checklist.clear()


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def read_input_values(integer):
    Globals.inputbuttons.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))
    try:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                    Globals.varinput.append(Globals.myList[integer])
                    try:
                        f = jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputValues"]["text"].replace('"', '').split(",")
                        Globals.inputbuttons = list(divide_chunks(f, 1))
                        return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputValues"]["text"]
                    except:
                        return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputValues"]["text"]
                elif read_input_types(integer) == "boolean":
                    Globals.inputbuttons = [["Yes"], ["No"]]
    except:  # one decision
        if read_input_types(integer) == "boolean":
            Globals.inputbuttons = [["Yes"], ["No"]]
        else:
            try:  # one input
                f = jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputValues"]["text"].replace('"', '').split(",")
                Globals.inputbuttons = list(divide_chunks(f, 1))
                Globals.varinput.append(Globals.myList[0])
                return jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputValues"]["text"]
            except:  # multiple inputs
                f = jsonvar["definitions"]["decision"]["decisionTable"]["input"][integer]["inputValues"]["text"].replace('"','').split(",")
                Globals.inputbuttons = list(divide_chunks(f, 1))
                Globals.varinput.append(Globals.myList[integer])
                return jsonvar["definitions"]["decision"]["decisionTable"]["input"][integer]["inputValues"]["text"]


def read_input_types(integer):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                    return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["@typeRef"]
    except:  # one decision
        try:  # one input
            if jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"] == Globals.myList[integer]:
                return jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["@typeRef"]
        except:  # multiple inputs
            for b in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                    return jsonvar["definitions"]["decision"]["decisionTable"]["input"][b]["inputExpression"]["@typeRef"]


def subread_xml():
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    #Globals.notmyList.clear()
    #Globals.oilist.clear()
    Globals.myList.clear()
    #list = []
    #list.clear()

    try:  # multiple decisions
        """for i in range(len(jsonvar["definitions"]["decision"])):
            list.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in list\
                        and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in Globals.notmyList:
                    Globals.notmyList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
                elif jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] in Globals.notmyList:
                    pass
                else:
                    Globals.oilist.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])"""
        for k in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][k]["decisionTable"]["output"]["@name"] == Globals.name:
                for d in range(len(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"])):
                    if jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"] not in Globals.oilist\
                            and jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"] not in Globals.myList:
                        Globals.myList.append(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"])
                    else:
                        recursive_function(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"])
    except:  # one decision
        try:  # one decision one input
            Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"])
        except:  # one decision multiple input
            for a in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
                Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][a]["inputExpression"]["text"])


def recursive_function(dname):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    for p in range(len(jsonvar["definitions"]["decision"])):
        if jsonvar["definitions"]["decision"][p]["decisionTable"]["output"]["@name"] == dname:
            for m in range(len(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"] not in Globals.oilist\
                        and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"] not in Globals.myList:
                    Globals.myList.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"])
                else:
                    recursive_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"])


"""def read_xml():
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    Globals.myList.clear()
    Globals.oilist.clear()
    list = []
    list.clear()
    try:  # multiple decision tables
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
    except:  # one decision table
        try:
            Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"])
        except:
            for a in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
                Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][a]["inputExpression"]["text"])"""


def read_decision_name():
    Globals.decisionname.clear()
    Globals.notmyList.clear()
    Globals.oilist.clear()
    list = []
    list.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:
        for i in range(len(jsonvar["definitions"]["decision"])):
            list.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
        for a in range(len(jsonvar["definitions"]["decision"])):
            for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in list \
                        and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in Globals.notmyList:
                    Globals.notmyList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
                elif jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] in Globals.notmyList:
                    pass
                else:
                    Globals.oilist.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])

        for z in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"] not in Globals.oilist:
                Globals.decisionname.append([jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]])

        for z in range(len(jsonvar["definitions"]["decision"])):
            if [jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]] not in Globals.decisionname:
                Globals.decisionname.append([jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]])
    except:
        Globals.decisionname.append([jsonvar["definitions"]["decision"]["@name"]])


def read_decision_key(keyname):
    Globals.decisionkey.clear()
    Globals.decisionname.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:  # one decision
        Globals.decisionkey.append(jsonvar["definitions"]["decision"]["@id"])
        return jsonvar["definitions"]["decision"]["@id"]
        #Globals.decisionname.append([jsonvar["definitions"]["decision"]["@name"]])
    except TypeError:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] == keyname:
                #if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] not in Globals.oilist:
                #Globals.decisionkey.append(jsonvar["definitions"]["decision"][a]["@id"])
                return jsonvar["definitions"]["decision"][a]["@id"]
                #Globals.decisionname.append([jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"]])
        """for a in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][a]["@id"] not in Globals.decisionkey:
                Globals.decisionkey.append(jsonvar["definitions"]["decision"][a]["@id"])"""
                #Globals.decisionname.append([jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"]])



def readoutput():
    Globals.output.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:  # one decision
        Globals.output.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
    except TypeError:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] == Globals.name:
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] in Globals.oilist:
                    for k in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                        if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"] in Globals.oilist\
                                and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.output:
                            recursive_output_function(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"])

                        elif jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] not in Globals.output:
                            Globals.output.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"])
                else:
                    for h in range(len(jsonvar["definitions"]["decision"])):
                        Globals.output.append(jsonvar["definitions"]["decision"][h]["decisionTable"]["output"]["@name"])
    print(Globals.output)


def recursive_output_function(oname):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))


    for p in range(len(jsonvar["definitions"]["decision"])):
        if oname in Globals.oilist:
            for n in range(len(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"] in Globals.oilist\
                        and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"] not in Globals.output:
                    recursive_output_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"])
                elif jsonvar["definitions"]["decision"][p]["decisionTable"]["output"]["@name"] not in Globals.output:
                    Globals.output.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"])



            """if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] not in Globals.oilist:
                Globals.output.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"])
        for a in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] not in Globals.output:
                Globals.output.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"])"""
