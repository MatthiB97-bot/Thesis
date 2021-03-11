import Globals
import XMLread as X


def sample_responses(input_text):
    user_message = str(input_text).capitalize()
    if user_message == "Ready":
        X.read_xml()
        return "Please give a value for the following inputs:" + str(Globals.myList)

    return 'Something went wrong, please try again'

