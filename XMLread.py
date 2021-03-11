import xmltodict, json
import Globals


def read_xml():
    with open("ApprovalStatus.xml", 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
        xvar = json.loads(json.dumps(obj))

    Globals.myList.clear()
    k = -1

    for xvar["inputData"] in xvar["definitions"]:
        k = k+1
        if k < len(xvar["definitions"]["inputData"]):
            Globals.myList.append(xvar["definitions"]["inputData"][k]["@name"])
