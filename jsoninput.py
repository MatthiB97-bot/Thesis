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
            return "Unfortunately, I can't make a decision based on your input. If you want to try again, send me 'again'."
    print(Globals.jsoninput)
    lst = []
    for i in range(len(Globals.output)):
        if i == 0:
            lst.append("The outcome of the " + str(Globals.output[i]) + " decision is " + str(m[i]) + ".")
        elif i == 1:
            lst.append("We used the following information in order to find the final outcome:\n" + "- The " + str(Globals.output[i]) + " is " + str(m[i]) )
        else:
            lst.append("- The " + str(Globals.output[i]) + " is " + str(m[i]))
    try:
        a = ','.join(lst)
    except:
        a = str(lst)
    Globals.d.clear()
    Globals.jsoninput.clear()
    return a.replace("'", "").replace(",", "\n").strip('['']')


def deploy_dmn():

    url = "http://localhost:8080/engine-rest/deployment/create"

    payload = {}
    files = [('upload', ('deploycheck.dmn', open('/C:/Users/willi/Documents/THESIS/deploycheck.dmn', 'rb'), 'application/octet-stream'))]
    headers = {'Content-Type': 'multipart/form-data'}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
