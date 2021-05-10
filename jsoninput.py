import requests
import json
import XMLread as xr
import Globals


# The execute_dmn function sends the user's input to the camunda dmn executor in JSON format
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
            Globals.d.clear()
            Globals.jsoninput.clear()
            Globals.inputbuttons.remove(["Show executed rules"])
            return "Unfortunately, I couldn't make a decision based on your input. If you want to try again, send me 'again'."


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


# the deploy function deploys the DMN model of the user if the user decides to upload its own DMN model
def deploy_dmn(name):

    url = "http://localhost:8080/engine-rest/deployment/create"
    payload = {}
    files = [('upload', (name + '.dmn', open('C:/Users/willi/PycharmProjects/pythonProject/'+name+'.dmn', 'rb'), 'application/octet-stream'))]
    requests.request("POST", url, data=payload, files=files)


# this function sends all executed rules to the user if he wants to know why he received a certain output
def show_executed_rules():
    Globals.lst = []
    url = "http://localhost:8080/engine-rest/history/decision-instance?includeOutputs=true&sortBy=evaluationTime&sortOrder=desc&maxResults=1000"
    response = requests.request("GET", url)
    my_json = json.loads(response.text)

    keys = []

    for k in range(len(Globals.output)):
        keys.append(xr.read_decision_key(Globals.output[k]))

    for k in range(0, 100):
        if my_json[k]["decisionDefinitionKey"] in keys and my_json[k]["outputs"][0]["ruleId"] not in Globals.lst and len(Globals.lst) <= (len(keys)-1):
            Globals.lst.append(my_json[k]["outputs"][0]["ruleId"])

    xr.read_decision_rules()

    var = []
    values = []
    text = []
    try:  # multiple rules
        for x in range(len(Globals.Globaltotal)):
            for k in range(len(Globals.Globaltotal[x])):
                if Globals.Globaltotal[x][k] is None:
                    Globals.Globaltotal[x][k] = "Unspecified"
                if k%2 == 0:
                    var.append(Globals.Globaltotal[x][k])
                else:
                    values.append(Globals.Globaltotal[x][k])
            text.append("Rule " + str(x)+":")
            for a in range(len(var)-1):
                text.append("If " + var[a] + " is " + values[a])
            text.append("Then the output for " + str(var.pop()) + " is " + str(values.pop()) + ",")
            var = []
            values = []
    except:  # one rule
        for k in range(len(Globals.Globaltotal)):
            if Globals.Globaltotal[k] is None:
                Globals.Globaltotal[k] = "Unspecified"
            if k % 2 == 0:
                var.append(Globals.Globaltotal[k])
            else:
                values.append(Globals.Globaltotal[k])
        text.append("Rule 0" + ":")
        for a in range(len(var) - 1):
            text.append("If " + var[a] + " is " + values[a])
        text.append("Then the output for " + str(var.pop()) + " is " + str(values.pop()) + ",")
        var = []
        values = []

    n = str(text)

    return n.replace("'", "").replace(",", "\n").strip('['']')
