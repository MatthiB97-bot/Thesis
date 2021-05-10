import xmltodict
import json
import Globals
# all functions present in this file, somehow use the XML file of the selected DMN model.


# This function automatically assigns a value for an input variable
# if the value for that input variable is the same for all rules
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
                        if i == sameval[0] and i is not None:
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
                            if i == sameval[0] and i is not None:
                                a = a + 1
                        if len(sameval) == a and jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                            Globals.d[str(Globals.myList[k])] = {}
                            Globals.d[str(Globals.myList[k])]["value"] = jsonvar["definitions"]["decision"]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                            remlist.append(k)
        except:  # one rule
            try:  # one entry
                a = 0
                sameval.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]["text"])
                if len(sameval) != 0:
                    for i in sameval:  # check if all values are the same
                        if i == sameval[0] and i is not None:
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
                            if i == sameval[0] and i is not None:
                                a = a + 1
                        if len(sameval) == a and jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                            Globals.d[str(Globals.myList[k])] = {}
                            Globals.d[str(Globals.myList[k])]["value"] = jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                            remlist.append(k)
        if len(remlist) != 0:
            try:  # one decision, multiple rules, multiple entries - all input the same
                for n in sorted(remlist, reverse=True):
                    Globals.myList.remove(Globals.myList[n])
                    Globals.mylabels.remove(Globals.mylabels[n])
            except:  # one decision, multiple rules, one entry -- all input the same
                Globals.myList.remove(Globals.myList[0])
                Globals.mylabels.remove(Globals.mylabels[0])
            remlist.clear()
    except:  # multiple decision tables
        checklist = []
        for n in decisions:
            if jsonvar["definitions"]["decision"][n]["decisionTable"]["output"]["@name"] == decision:
                rules = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]))
                try:
                    try:
                        entries = range(len({jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"]["text"]}))  # multiple rules, one inputentry
                    except:
                        entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"]))  # multiple rules, multiple inputentries
                except:
                    try:
                        entries = range(len({jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]["text"]}))  # one rule, one inputentry
                    except:
                        entries = range(len(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]))  # one rule multiple inputentries

                for k in entries:
                    try:  # multiple entries
                        try:  # multiple entries, multiple rules
                            a = 0
                            if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in checklist\
                                    and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.oilist:
                                checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"])  # ensure uniqueness
                                Globals.w = Globals.w +1
                                sameval.clear()

                                for m in rules:
                                    sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"][k]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0] and i is not None:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[Globals.w])] = {}
                                            Globals.d[str(Globals.myList[Globals.w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"][k]["text"].strip('"')
                                            remlist.append(Globals.w)

                        except:  # multiple entries, one rule
                            a = 0
                            if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in checklist\
                                    and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.oilist:
                                checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["text"])  # ensure uniqueness
                                Globals.w = Globals.w + 1
                                sameval.clear()
                                sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"])

                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0] and i is not None:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"][k]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[Globals.w])] = {}
                                            Globals.d[str(Globals.myList[Globals.w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"][k]["text"].strip('"')
                                            remlist.append(Globals.w)
                    except:  # one entry
                        try:  # one entry multiple rules
                            a = 0
                            if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"] not in checklist\
                                    and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.oilist:
                                checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"])  # ensure uniqueness
                                Globals.w = Globals.w +1
                                sameval.clear()

                                for m in rules:
                                    sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][m]["inputEntry"]["text"])
                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0] and i is not None:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[Globals.w])] = {}
                                            Globals.d[str(Globals.myList[Globals.w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"][0]["inputEntry"]["text"].strip('"')
                                            remlist.append(Globals.w)

                        except:  # one rule, one entry
                            a = 0
                            if jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"] not in checklist\
                                    and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.oilist:
                                checklist.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["text"])  # ensure uniqueness
                                Globals.w = Globals.w +1
                                sameval.clear()
                                sameval.append(jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]["text"])

                                if len(sameval) != 0:
                                    for i in sameval:
                                        if i == sameval[0] and i is not None:
                                            a = a + 1
                                        if len(sameval) == a and jsonvar["definitions"]["decision"][n]["decisionTable"]["input"]["inputExpression"]["@typeRef"] not in ["double", "integer"]:
                                            Globals.d[str(Globals.myList[Globals.w])] = {}
                                            Globals.d[str(Globals.myList[Globals.w])]["value"] = jsonvar["definitions"]["decision"][n]["decisionTable"]["rule"]["inputEntry"]["text"].strip('"')
                                            remlist.append(Globals.w)

        if len(remlist) != 0:
            for b in sorted(remlist, reverse=True):
                Globals.myList.remove(Globals.myList[b])
                Globals.mylabels.remove(Globals.mylabels[b])
        remlist.clear()
        checklist.clear()


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# This function makes buttons if an input variable has predefined input values
def read_input_values(integer):
    Globals.inputbuttons.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))
    try:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            try:
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
            except:
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] == Globals.myList[integer]:
                    Globals.varinput.append(Globals.myList[integer])
                    try:
                        f = jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputValues"]["text"].replace('"', '').split(",")
                        Globals.inputbuttons = list(divide_chunks(f, 1))
                        return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputValues"]["text"]
                    except:
                        return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputValues"]["text"]
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


# this function retrieves the input type of an input variable
def read_input_types(integer):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            try:  # multiple inputs
                for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                    if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                        return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["@typeRef"]
            except:  # one input
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] == Globals.myList[integer]:
                    return jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["@typeRef"]
    except:  # one decision
        try:  # one input
            if jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"] == Globals.myList[integer]:
                return jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["@typeRef"]
        except:  # multiple inputs
            for b in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
                if jsonvar["definitions"]["decision"]["decisionTable"]["input"][b]["inputExpression"]["text"] == Globals.myList[integer]:
                    return jsonvar["definitions"]["decision"]["decisionTable"]["input"][b]["inputExpression"]["@typeRef"]


# this function makes a list of all decisions that have to be executed in case the user wants to execute a subdecision
def subread_xml():
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))
    Globals.myList.clear()
    Globals.mylabels.clear()

    try:  # multiple decisions
        for k in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][k]["decisionTable"]["output"]["@name"] == Globals.name:
                try:
                    for d in range(len(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"])):
                        if jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"] not in Globals.oilist\
                                and jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"] not in Globals.myList:
                            Globals.myList.append(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"])
                            Globals.mylabels.append(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["@label"])
                        else:
                            recursive_function(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"][d]["inputExpression"]["text"])
                except:
                    if jsonvar["definitions"]["decision"][k]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.oilist \
                            and jsonvar["definitions"]["decision"][k]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.myList:
                        Globals.myList.append(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"]["inputExpression"]["text"])
                        Globals.mylabels.append(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"]["@label"])

                    else:
                        recursive_function(jsonvar["definitions"]["decision"][k]["decisionTable"]["input"]["inputExpression"]["text"])
    except:  # one decision
        try:  # one decision one input
            Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"])
            Globals.mylabels.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["@label"])

        except:  # one decision multiple input
            for a in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["input"])):
                Globals.myList.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][a]["inputExpression"]["text"])
                Globals.mylabels.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][a]["@label"])


# this function is used by the subread XML function
def recursive_function(dname):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    for p in range(len(jsonvar["definitions"]["decision"])):
        if jsonvar["definitions"]["decision"][p]["decisionTable"]["output"]["@name"] == dname:
            try:
                for m in range(len(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"])):
                    if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"] not in Globals.oilist\
                            and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"] not in Globals.myList:
                        Globals.myList.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"])
                        Globals.mylabels.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["@label"])
                    else:
                        recursive_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][m]["inputExpression"]["text"])
            except:
                if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.oilist \
                        and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.myList:
                    Globals.myList.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"])
                    Globals.mylabels.append(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["@label"])

                else:
                    recursive_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"])


# This function creates a list with all the names of the decisions in a DMN model
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
            try:
                for b in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                    if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in list \
                            and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] not in Globals.notmyList:
                        Globals.notmyList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
                    elif jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"] in Globals.notmyList:
                        pass
                    else:
                        Globals.oilist.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][b]["inputExpression"]["text"])
            except:
                if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] not in list \
                        and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.notmyList:
                    Globals.notmyList.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"])
                elif jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] in Globals.notmyList:
                    pass
                else:
                    Globals.oilist.append(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"])

        for z in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"] not in Globals.oilist:
                Globals.decisionname.append([jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]])
        Globals.decisionname.append("SUBDECISIONS")
        for z in range(len(jsonvar["definitions"]["decision"])):
            if [jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]] not in Globals.decisionname:
                Globals.decisionname.append([jsonvar["definitions"]["decision"][z]["decisionTable"]["output"]["@name"]])
    except:
        Globals.decisionname.append([jsonvar["definitions"]["decision"]["@name"]])


# this function creates a list with all decision keys of all decisions present in a DMN model
def read_decision_key(keyname):
    Globals.decisionname.clear()
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    try:  # one decision
        return jsonvar["definitions"]["decision"]["@id"]
    except TypeError:  # multiple decisions
        for a in range(len(jsonvar["definitions"]["decision"])):
            if jsonvar["definitions"]["decision"][a]["decisionTable"]["output"]["@name"] == keyname:
                return jsonvar["definitions"]["decision"][a]["@id"]


# This functions retrieves all decision rules present in an XML file
def read_decision_rules():
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))
    total = []
    rules = []
    try:  # multiple decisions
        for i in range(len(jsonvar["definitions"]["decision"])):
            try:  # multiple rules
                for j in range(len(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"])):
                    try:  # multiple inputentries
                        if jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["@id"] in Globals.lst:
                            for k in range(len(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["inputEntry"])):
                                rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["input"][k]["inputExpression"]["text"])
                                rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["inputEntry"][k]["text"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["outputEntry"]["text"])
                            total.append(rules)
                    except:  # one inputentry
                        if jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["@id"] in Globals.lst:
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["input"]["inputExpression"]["text"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["inputEntry"]["text"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"][j]["outputEntry"]["text"])
                            total.append(rules)
            except:  # one rule
                try:  # multiple inputentries
                    if jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["@id"] in Globals.lst:
                        for k in range(len(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["inputEntry"])):
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["input"][k]["inputExpression"]["text"])
                            rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["outputEntry"]["text"])
                        total.append(rules)
                except:  # one inputentry
                    if jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["@id"] in Globals.lst:
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["input"]["inputExpression"]["text"])
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["inputEntry"]["text"])
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["output"]["@name"])
                        rules.append(jsonvar["definitions"]["decision"][i]["decisionTable"]["rule"]["outputEntry"]["text"])
                        total.append(rules)
            rules = []
    except:  # one decision
        try:  # multiple rules
            for j in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"])):
                try:  # multiple inputentries
                    if jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["@id"] in Globals.lst:
                        for k in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["inputEntry"])):
                            rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["text"])
                            rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["inputEntry"][k]["text"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["outputEntry"]["text"])
                        total.append(rules)
                except:  # one inputentry
                    if jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["@id"] in Globals.lst:
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["inputEntry"]["text"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"][j]["outputEntry"]["text"])
                        total.append(rules)
        except:  # one rule
            try:  # multiple inputentries
                if jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["@id"] in Globals.lst:
                    for k in range(len(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"])):
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"][k]["inputExpression"]["text"])
                        rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"][k]["text"])
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["outputEntry"]["text"])
                    total.append(rules)
            except:  # one inputentry
                if jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["@id"] in Globals.lst:
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["input"]["inputExpression"]["text"])
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["inputEntry"]["text"])
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["output"]["@name"])
                    rules.append(jsonvar["definitions"]["decision"]["decisionTable"]["rule"]["outputEntry"]["text"])
                    total.append(rules)
    Globals.Globaltotal = total


# This function makes a list of all outputs of a DMN model
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
                Globals.output.append(Globals.name)
                try:
                    for k in range(len(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"])):
                        if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"] in Globals.oilist\
                                and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"] not in Globals.output:
                            recursive_output_function(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"][k]["inputExpression"]["text"])
                except:
                    if jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] in Globals.oilist \
                            and jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.output:
                        recursive_output_function(jsonvar["definitions"]["decision"][a]["decisionTable"]["input"]["inputExpression"]["text"])


# this function is used by the read_output function
def recursive_output_function(oname):
    with open(Globals.model, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        jsonvar = json.loads(json.dumps(obj))

    for p in range(len(jsonvar["definitions"]["decision"])):
        if jsonvar["definitions"]["decision"][p]["decisionTable"]["output"]["@name"] == oname:
            Globals.output.append(oname)
            try:
                for n in range(len(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"])):
                    if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"] in Globals.oilist\
                            and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"] not in Globals.output:
                        recursive_output_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"][n]["inputExpression"]["text"])
            except:
                if jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"] in Globals.oilist \
                        and jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"] not in Globals.output:
                    recursive_output_function(jsonvar["definitions"]["decision"][p]["decisionTable"]["input"]["inputExpression"]["text"])

