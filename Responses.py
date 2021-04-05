import Globals
import XMLread as X
import jsoninput as JS


def ready_responses():
    Globals.input.clear()
    X.read_xml()
    X.same_values()
    Globals.q = 0
    Globals.a = 0
    Globals.buttonstext = 'You can use the buttons below to choose one of the options.'
    if X.read_input_types(0) == "date":
        return "Give a date value considering this date format YYYY-MM-DDThh:mm:ss.\ne.g. 2001-09-11T08:46:12"
    try:
        X.read_input_values(0)
        return "Provide " + str(Globals.myList[0]) + " with an input value."
    except:
        return "Provide " + str(Globals.myList[0]) + " with an input value."


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
            return "It seems like you entered the wrong type of input, the correct input type is "+str(X.read_input_types(Globals.q))+". Please try again."

        if len(Globals.myList) != 0 and len(Globals.myList) == len(Globals.input):
            Globals.a = 0
            Globals.inputbuttons = [["Again"], ["Change"]]
            Globals.buttonstext = "\nYou can run the same decision again by pressing the 'again' button. If you want to make another decision, press the 'Change' button."
            return JS.execute_dmn()

        if X.read_input_types(Globals.a+1) == "date":
            Globals.a = Globals.a + 1
            return "Give a date value considering this date format YYYY-MM-DDThh:mm:ss.\ne.g. 2001-09-11T08:46:12"

        if Globals.a < len(Globals.myList):
            Globals.a = Globals.a + 1
            try:
                X.read_input_values(Globals.a)
            except:
                pass
            return "Provide " + str(Globals.myList[Globals.a]) + " with an input value."
