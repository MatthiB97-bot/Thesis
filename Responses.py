import Globals
import XMLread as X
import jsoninput as JS


def subdecision_response():
    X.read_decision_name()

    if len(Globals.decisionname) > 1:
        Globals.inputbuttons = Globals.decisionname
        return "Choose one of the decisions. To know the final outcome, select the decision on top."
    else:
        return ready_responses()


def ready_responses():
    Globals.input.clear()
    X.subread_xml()
    X.readoutput()


    for i in range(len(Globals.output)):
        X.same_values(Globals.output[i])

    if len(Globals.myList) == 0:
        Globals.inputbuttons = [["Again"], ["Show executed rules"], ["Choose another existing DMN model"], ["Upload your own DMN model"], ["End the conversation"]]
        return JS.execute_dmn()
    Globals.q = 0
    Globals.a = 0
    if X.read_input_types(0) == "date":
        try:
            X.read_input_values(Globals.a)
        except:
            pass
        return "Provide " + str(Globals.mylabels[0]) + " with an input value, considering this date format YYYY-MM-DDThh:mm:ss.\ne.g. 2023-06-11T08:46:12"
    try:
        X.read_input_values(0)
        return "Provide " + str(Globals.mylabels[0]) + " with an input value."
    except:
        return "Provide " + str(Globals.mylabels[0]) + " with an input value."


def input_response(input):
    if X.read_input_types(Globals.q) == "double":
        try:
            input = float(input)
        except:
            pass

    if [input] not in Globals.dmnmodels:
        if input in ("Back", "back", "BACK"):
            Globals.a = Globals.a - 1
            Globals.q = Globals.q - 1
            Globals.input.pop()
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Provide " + str(Globals.mylabels[Globals.a]) + " with an input value."
        if type(input) == Globals.typedict[X.read_input_types(Globals.q)]: #check if type of input is correct type
            Globals.input.append(input)
            Globals.q = Globals.q + 1
        else:
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "It seems like you entered the wrong type of input, the correct input type is "+str(X.read_input_types(Globals.q))+". Give it another shot!"

        if len(Globals.myList) != 0 and len(Globals.myList) == len(Globals.input):
            Globals.a = 0
            Globals.inputbuttons = [["Again"], ["Show executed rules"], ["Choose another existing DMN model"], ["Upload your own DMN model"], ["End the conversation"]]
            return JS.execute_dmn()

        if X.read_input_types(Globals.a+1) == "date":
            Globals.a = Globals.a + 1
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Provide " + str(Globals.mylabels[Globals.a]) + " with an input value, considering this date format YYYY-MM-DDThh:mm:ss.\ne.g. 2023-06-11T08:46:12"

        if Globals.a < len(Globals.myList):
            Globals.a = Globals.a + 1
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Provide " + str(Globals.mylabels[Globals.a]) + " with an input value."
