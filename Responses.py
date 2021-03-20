from telegram import update, ReplyKeyboardMarkup

import Globals
import XMLread as X
import jsoninput as JS


def ready_responses():
    Globals.input.clear()
    X.read_xml()
    X.same_values()

    try:
        return "Please give a value for the following input: " + str(Globals.myList[0]) + ". \nThese are the possible input values: " + str(X.read_input_values(0))
    except:
        return "Please give a value for the following input: " + str(Globals.myList[0])


def input_response(input):
    Globals.input.append(input)
    print(Globals.input)

    if len(Globals.myList) != 0 and len(Globals.myList) == len(Globals.input):
        Globals.a = 0
        return JS.execute_dmn()

    if Globals.a < len(Globals.myList):
        Globals.a = Globals.a + 1
        try:
            x = ". \nThese are the possible input values: " + str(X.read_input_values(Globals.a))
        except:
            x = ""
        return "Your input has been registered. Please give a value for the next input variable: "+str(Globals.myList[Globals.a]) \
               + x
