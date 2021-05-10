import Globals
import XMLread as X
import jsoninput as JS


# This function creates list of buttons of all decisions present in the chosen DMN model
def subdecision_response():
    X.read_decision_name()

    if len(Globals.decisionname) > 1:
        Globals.inputbuttons = Globals.decisionname
        return "Choose one of the decisions. To know the final outcome, select the decision on top."
    else:
        return ready_responses()


# This function asks for input values for the first input variable
# This function triggers the execution of the decision in the camunda decision engine when all input are collected.
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

    try:
        X.read_input_values(0)
        return "Provide " + str(Globals.mylabels[0]) + " with an input value."
    except:
        return "Provide " + str(Globals.mylabels[0]) + " with an input value."


# This function asks for input values for all input variables except the first (only difference with previous function)
# This function triggers the execution of the decision in the camunda decision engine when all input are collected.
def input_response(input):
    if Globals.model == "":
        return "Please make sure the document is a DMN file."

    if X.read_input_types(Globals.q) == "double":
        try:
            input = float(input)
        except:
            pass

    if [input] not in Globals.dmnmodels:
        if input in ("Back", "back", "BACK"):
            if len(Globals.input) >= 1:
                Globals.a = Globals.a - 1
                Globals.q = Globals.q - 1
                Globals.input.pop()
                try:
                    X.read_input_values(Globals.a)
                except:
                    pass
                return "Provide " + str(Globals.mylabels[Globals.a]) + " with an input value."
            else:
                return "You can't go back any further. Provide " + str(Globals.mylabels[Globals.a]) + " with an input value."

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

        if X.read_input_types(Globals.a) == "date":
            if "-" not in input:
                Globals.q = Globals.q - 1
                Globals.input.pop()
                return "Make sure the date is as specific as possible. Month and day are mandatory values."

        if Globals.a < len(Globals.myList):
            Globals.a = Globals.a + 1
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Provide " + str(Globals.mylabels[Globals.a]) + " with an input value."
