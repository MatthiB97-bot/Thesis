import requests
import json
import XMLread as xr
import Globals


def execute_dmn():
    url = "http://localhost:8080/engine-rest/decision-definition/key/"+str(xr.read_decision_key())+"/evaluate"
    d = {}

    for i in range(len(Globals.myList)):
        d[str(Globals.myList[i])] = {}
        d[str(Globals.myList[i])]["value"] = Globals.input[i]

    input = {"variables": d}

    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=json.dumps(input))

    return response.text[1:-1]
