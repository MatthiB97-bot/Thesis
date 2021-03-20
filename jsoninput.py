import requests
import json
import XMLread as xr
import Globals


def execute_dmn():
    url = "http://localhost:8080/engine-rest/decision-definition/key/"+str(xr.read_decision_key())+"/evaluate"
    Globals.jsoninput = {"variables": Globals.d}

    for i in range(len(Globals.myList)):
        Globals.d[str(Globals.myList[i])] = {}
        Globals.d[str(Globals.myList[i])]["value"] = Globals.input[i]

    print(Globals.jsoninput)
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=json.dumps(Globals.jsoninput))

    xr.readoutput()
    Globals.d.clear()
    Globals.jsoninput.clear()
    return "The output is: " + str(response.json()[0][str(Globals.output[0])]["value"]) + "\nIf you want to try again, send 'again'"
