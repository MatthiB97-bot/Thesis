import Globals
import XMLread as X
import jsoninput as JS


def ready_responses():
    Globals.input.clear()
    X.read_xml()
    X.same_values()
    Globals.q = 0
    Globals.a = 0
    Globals.buttonstext = 'Please choose one of the options:'
    if X.read_input_types(0) == "date":
        return "Please give value for date in the following format:\nYYYY-MM-DDThh:mm:ss\ne.g. 2001-09-11T08:46:12"
    try:
        X.read_input_values(0)
        return "Please give a value for the following input: " + str(Globals.myList[0])
    except:
        return "Please give a value for the following input: " + str(Globals.myList[0])


def input_response(input):
    if X.read_input_types(Globals.q) == "double":
        try:
            input = float(input)
        except:
            pass

    if [input] not in Globals.dmnmodels:
        if type(input) == Globals.typedict[X.read_input_types(Globals.q)]: #check if type of input is correct type
            Globals.input.append(input)
            Globals.q = Globals.q + 1
        else:
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "The type of your input is not correct. The correct input type is: "+str(Globals.typedict[X.read_input_types(Globals.q)])+" Please give a value for the input variable: " + str(Globals.myList[Globals.a])

        if len(Globals.myList) != 0 and len(Globals.myList) == len(Globals.input):
            Globals.a = 0
            Globals.inputbuttons = [["Again"], ["Change"]]
            Globals.buttonstext = "\nIf you want to try again, press 'again'.\nIf you want to change DMN model press 'Change'."
            return JS.execute_dmn()

        if X.read_input_types(Globals.a+1) == "date":
            Globals.a = Globals.a + 1
            return "Please give value for date in the following format:\nYYYY-MM-DDThh:mm:ss\ne.g. 2001-09-11T08:46:12"

        if Globals.a < len(Globals.myList):
            Globals.a = Globals.a + 1
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Your input has been registered. Please give a value for the next input variable: "+str(Globals.myList[Globals.a])
