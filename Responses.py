import Globals
import pyDMNrules


def sample_responses(input_text):
    user_message = str(input_text).capitalize()
    if user_message in ("Business", "Private", "Government"):
        Globals.myList.clear()
        Globals.myList.insert(0,user_message)
        print(Globals.myList)
        return "What is your order size?"

    if user_message in ("Sameday", "Slow"):
        user_message = str(input_text).lower()
        Globals.myList.insert(2, user_message)
        print(Globals.myList)
        return 'If you want to adjust your input, just send new input.\nIf you are ready, send "done"'
    if user_message in ("Done"):
        dmnRules = pyDMNrules.DMN()
        status = dmnRules.load('ExampleRows.xlsx')
        if 'errors' in status:
            print('ExampleRows.xlsx has errors', status['errors'])
        else:
            print('ExampleRows.xlsx loaded')

        print(Globals.myList)

        data = {}
        data['Customer'] = Globals.myList[0]
        data['OrderSize'] = int(Globals.myList[1])
        data['Delivery'] = Globals.myList[2]
        print('Testing', repr(data))
        (status, newData) = dmnRules.decide(data)
        if 'errors' in status:
            return status['errors']
        return "Your discount is: " + str(newData['Result']['Discount'])
    return 'Er is iets fout gegaan, probeer opnieuw'


def integer_responses(input_integer):
    user_integer = str(input_integer)
    if int(user_integer) in [i for i in range(1000)]:
        Globals.myList.insert(1,user_integer)
        print(Globals.myList)
        return 'Do you want sameday or slow delivery?'

    return 'Er is iets fout gegaan, probeer opnieuw'
