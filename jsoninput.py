import requests
import json
import XMLread as xr
import Globals


def execute_dmn():
    m = []

    try:
        for i in range(len(Globals.myList)):
            Globals.d[str(Globals.myList[i])] = {}
            Globals.d[str(Globals.myList[i])]["value"] = Globals.input[i]
        Globals.jsoninput = {"variables": Globals.d}
    except:
        Globals.jsoninput = {"variables": Globals.d}

    print(Globals.jsoninput)
    for p in range(len(Globals.output)):
        url = "http://localhost:8080/engine-rest/decision-definition/key/"+str(xr.read_decision_key(Globals.output[p]))+"/evaluate"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(Globals.jsoninput))
        try:
            m.append(response.json()[0][str(Globals.output[p])]["value"])
        except:
            return "Unfortunately, I can't make a decision based on your input. If you want to try again, send me 'again'."


    lst = []
    for i in range(len(Globals.output)):
        if i == 0:
            lst.append("Based on your input we calculated the outcome of the " + "`" + str(Globals.output[i]) + "´" + " decision which is " + "`" + str(m[i]) + "´.")
        elif i == 1:
            lst.append("We used the following information in order to find the final outcome:\n" + "- `" + str(Globals.output[i]) + "´ is `" + str(m[i]) + "´")
        else:
            lst.append("- `" + str(Globals.output[i]) + "´ is `" + str(m[i]) + "´")
    try:
        a = ','.join(lst)
    except:
        a = str(lst)
    Globals.d.clear()
    Globals.jsoninput.clear()
    return a.replace("'", "").replace(",", "\n").strip('['']')


def deploy_dmn(name):

    url = "http://localhost:8080/engine-rest/deployment/create"
    payload = {}
    files = [('upload', (name + '.dmn', open('C:/Users/willi/PycharmProjects/pythonProject/'+name+'.dmn', 'rb'), 'application/octet-stream'))]
    requests.request("POST", url, data=payload, files=files)
