import logging
from telegram import ReplyKeyboardMarkup
import Responses as R
import distutils
import distutils.util
import Globals
import jsoninput
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
    update.message.reply_text("Hi, I am the DMN chatbot. Do you want to make a predefined decision or do you want to upload your own decision?\nIn case you have any questions, send /help", reply_markup=ReplyKeyboardMarkup([["Use predefined decision"], ["Upload new decision"]], one_time_keyboard=True, resize_keyboard=True))


def restart(update, context):
    """Send a message when the command /start is issued."""
    Globals.model = ""
    update.message.reply_text('Which decision would you like to make now?', reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))


def predefbuttons(update, context):
    k = Globals.inputbuttons
    if len(Globals.inputbuttons) != 0:
        choice = update.message.reply_text(Globals.buttonstext,
            reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
        return choice
    else:
        pass


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('- you can scroll to view all buttons\n-------------------------------------\nTo go back to the DMN chatbot press /start')


def handle_message(update, context):
    if update.message.text.isdigit():
        text = int(update.message.text)
        response = R.input_response(text)
        update.message.reply_text(response)
        predefbuttons(update, context)
    else:
        try:
            text = float(update.message.text)
            response = R.input_response(text)
            update.message.reply_text(response)
            predefbuttons(update, context)
        except:
            text = str(update.message.text)
            if [text] in Globals.dmnmodels and Globals.counter == 0:
                Globals.counter = Globals.counter + 1
                Globals.model = text+".xml"
                response = R.subdecision_response()
                update.message.reply_text(response)
                predefbuttons(update, context)
            elif text in ("Upload new decision", "Upload your own decision"):
                Globals.counter = 0
                update.message.reply_text("To upload your own decision, press the paperclip button and make sure the file format is .dmn")
            elif text in "Use predefined decision":
                Globals.counter = 0
                update.message.reply_text("This is a list of all existing decisions, you can choose one of them.", reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))
            elif text in "Choose another existing decision":
                Globals.counter = 0
                restart(update, context)
            elif text in ("back", "Back", "BACK"):
                response = R.input_response(text)
                update.message.reply_text(response)
                predefbuttons(update, context)
            elif [text] in Globals.decisionname:
                Globals.subdecvar = 1
                #Globals.key = Globals.decisionkey[Globals.decisionname.index([text])]
                Globals.name = text
                response = R.ready_responses()
                update.message.reply_text(response)
                predefbuttons(update, context)
            elif text in ("again", "Again"):
                Globals.varinput.clear()
                response = R.subdecision_response()
                update.message.reply_text(response)
                predefbuttons(update, context)
            elif text in ("True", "true", "False", "false", "yes", "Yes", "No", "no"):
                text = bool(distutils.util.strtobool(text))
                response = R.input_response(text)
                update.message.reply_text(response)
                predefbuttons(update, context)
            else:
                response = R.input_response(text)
                update.message.reply_text(response)
                predefbuttons(update, context)


def downloader(update, context):
    Globals.deployname = str(update.message.document["file_name"]).removesuffix(".dmn")
    if [Globals.deployname] in Globals.dmnmodels:
        update.message.reply_text("I'm sorry, there already exists a decision with this name. You can choose this decision from the list or rename your file and reupload it.", reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))
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
        update.message.reply_text(response)
        predefbuttons(update, context)


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
