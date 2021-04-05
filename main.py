import logging
from telegram import ReplyKeyboardMarkup
import Responses as R
import distutils
import distutils.util
import Globals
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram.ext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    Globals.model = ""
    update.message.reply_text("Hi, I am the DMN chatbot. You can choose the decision you want to make in the list below.\nWhen you want to adjust your previous input, send 'Adjust'.\nIn case you have any questions, send /help", reply_markup=ReplyKeyboardMarkup(Globals.dmnmodels, one_time_keyboard=True, resize_keyboard=True))


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
            if [text] in Globals.dmnmodels:
                Globals.model = text+".xml"
                response = R.ready_responses()
                update.message.reply_text(response)
                predefbuttons(update, context)
            elif text in ("Change"):
                restart(update, context)
            elif text in ("again", "Again"):
                Globals.varinput.clear()
                response = R.ready_responses()
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
    x = str(update.message.document["file_name"]).removesuffix(".dmn")
    Globals.dmnmodels.append([x])
    print(Globals.dmnmodels)
    context.bot.get_file(update.message.document)
    with open("C:/Users/willi/PycharmProjects/pythonProject/"+x+".xml", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

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
