import logging
from telegram import ReplyKeyboardMarkup
import Responses as R
import distutils
import distutils.util
import Globals
import jsoninput
import XMLread as X
import NLPmodule as NLP
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    Globals.model = ""
    update.message.reply_text("Hi, I am the DMN chatbot. How can I help you today?\nIn case you have any questions, just ask for help.", reply_markup=ReplyKeyboardMarkup([["I want to execute a predefined DMN model"], ["I want to upload a new DMN model"]], one_time_keyboard=True, resize_keyboard=True))


def restart(update, context):
    Globals.model = ""
    update.message.reply_text('Which decision would you want to make now?', reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))


def predefbuttons(update, context, text):
    k = Globals.inputbuttons
    if len(Globals.inputbuttons) != 0:
        choice = update.message.reply_text(text,
            reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
        return choice
    else:
        return update.message.reply_text(text)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Step-by-step plan of having a conversation with the DMN chatbot:\n\n"
                              "1. To start a conversation with me, send 'hi'.\n2. Press the right button to either "
                              "choose or upload a model.\n3. If you decide to execute a predefined model, choose the "
                              "decision model you want to execute.\n4. If you decide to upload your own DMN model, "
                              "upload a .dmn file.\n5. Choose which decision you want to execute.\n6. Enter all"
                              "necessary inputs.\n7. After the execution of the decision, choose what you want to"
                              "do next from the list.")


def handle_message(update, context):
    NLP.sendquery(update.message.text)

    try:
        if X.read_input_types(Globals.a) == 'date':
            a = NLP.extractdate()
            update.message.text = str(a)
        else:
            try:
                a = NLP.extractnumber()
                update.message.text = str(a)
            except:
                pass
    except:
        pass

    if NLP.gettopintent() == "BackIntent" and NLP.gettopintentscore() > 0.8:
        update.message.text = "back"
    elif NLP.gettopintent() == "EndIntent" and NLP.gettopintentscore() > 0.8:
        update.message.text = "End the conversation"
    elif NLP.gettopintent() == "StartIntent" and NLP.gettopintentscore() > 0.8:
        update.message.text = "start"
    elif NLP.gettopintent() == "HelpIntent" and NLP.gettopintentscore() > 0.8:
        update.message.text = "help"

    if update.message.text.isdigit():
        text = int(update.message.text)
        response = R.input_response(text)
        predefbuttons(update, context, response)
    else:
        try:
            text = float(update.message.text)
            response = R.input_response(text)
            predefbuttons(update, context, response)
        except:
            text = str(update.message.text)
            if [text] in Globals.dmnmodels and Globals.counter == 0:
                Globals.counter = Globals.counter + 1
                Globals.model = text+".xml"
                response = R.subdecision_response()
                predefbuttons(update, context, response)
            elif text in ("Upload your own DMN model", "I want to upload a new DMN model"):
                Globals.w = -1
                Globals.counter = 0
                update.message.reply_text("To upload your own DMN model press the attach button. Notice, the file format has to be .dmn.")
            elif text in "Show executed rules":
                response = jsoninput.show_executed_rules()
                predefbuttons(update, context, response)
            elif text in "I want to execute a predefined DMN model":
                Globals.w = -1
                Globals.counter = 0
                update.message.reply_text("Choose one of the existing DMN models below.", reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))
            elif text in "Choose another existing DMN model":
                Globals.w = -1
                Globals.counter = 0
                restart(update, context)
            elif text in "End the conversation":
                update.message.reply_text("I hope I have helped you, do not hesitate to message me again if you need any help.\nGoodbye!")
            elif text in ("back", "Back", "BACK"):
                response = R.input_response(text)
                predefbuttons(update, context, response)
            elif [text] in Globals.decisionname:
                Globals.subdecvar = 1
                Globals.name = text
                response = R.ready_responses()
                predefbuttons(update, context, response)
            elif text in ("again", "Again"):
                Globals.w = -1
                Globals.varinput.clear()
                response = R.subdecision_response()
                predefbuttons(update, context, response)
            elif text in ("True", "true", "False", "false", "yes", "Yes", "No", "no"):
                text = bool(distutils.util.strtobool(text))
                response = R.input_response(text)
                predefbuttons(update, context, response)
            elif text in "start":
                start(update, context)
            elif text in "help":
                help(update, context)
            else:
                try:
                    response = R.input_response(text)
                    predefbuttons(update, context, response)
                except:
                    update.message.reply_text("I don't know what you mean by that. If you need help, don't be afraid to ask.")


def downloader(update, context):
    if ".dmn" in update.message.document["file_name"]:
        Globals.deployname = str(update.message.document["file_name"]).removesuffix(".dmn")
        if [Globals.deployname] in Globals.dmnmodels:
            update.message.reply_text("I'm sorry, there already exists a DMN model with this name. You can choose this model from the list or rename your file and try to upload it again.", reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))
        else:
            Globals.dmnmodels.append([Globals.deployname])
            with open("C:/Users/willi/PycharmProjects/pythonProject/"+Globals.deployname+".dmn", 'wb') as f:
                context.bot.get_file(update.message.document).download(out=f)
            with open("C:/Users/willi/PycharmProjects/pythonProject/"+Globals.deployname+".xml", 'wb') as f:
                context.bot.get_file(update.message.document).download(out=f)
            Globals.model = ""
            Globals.model = Globals.deployname+".xml"
            jsoninput.deploy_dmn(Globals.deployname)
            response = R.subdecision_response()
            predefbuttons(update, context, response)
    else:
        update.message.reply_text("Please make sure the document is a DMN file.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bots token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1617530928:AAGZ4muwD2r_pD0KabvGHklncMXMnEyetgg", use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.text, predefbuttons))
    dp.add_handler(MessageHandler(Filters.document, downloader))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
