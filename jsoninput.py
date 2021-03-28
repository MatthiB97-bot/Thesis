import requests
import json
import XMLread as xr
import Globals


def execute_dmn():
    xr.readoutput()
    m = []
    for i in range(len(Globals.myList)):
        Globals.d[str(Globals.myList[i])] = {}
        Globals.d[str(Globals.myList[i])]["value"] = Globals.input[i]
    Globals.jsoninput = {"variables": Globals.d}

    for p in range(len(Globals.output)):
        url = "http://localhost:8080/engine-rest/decision-definition/key/"+str(xr.read_decision_key(p))+"/evaluate"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(Globals.jsoninput))
        try:
            m.append(response.json()[0][str(Globals.output[p])]["value"])
        except:
            return "Your input does not match a decision rule. Send 'again' if you would like to try again."
    print(Globals.jsoninput)
    lst = []
    for i in range(len(Globals.output)):
        if i == 0:
            lst.append("The final output for " + str(Globals.output[i]) + " is: " + str(m[i]))
        elif i == 1:
            lst.append("-------------------------------------------------------" + "\nIntermediate output:\n" + "\nThe output for " + str(Globals.output[i]) + " is: " + str(m[i]))
        else:
            lst.append("The output for " + str(Globals.output[i]) + " is: " + str(m[i]))
    try:
        a = ','.join(lst)
    except:
        a = str(lst)
    Globals.d.clear()
    Globals.jsoninput.clear()
    return a.replace("'", "").replace(",", "\n").strip('['']')
