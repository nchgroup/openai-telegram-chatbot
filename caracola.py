import openai
from telegram.ext import Updater, CommandHandler
from telegram import constants
from functools import wraps
import logging


# Set up the OpenAI API key
openai.api_key = "<OPENAI-KEY>"


LIST_OF_ADMINS = [-9999999] # Telegram Chat Group
TOKEN_BOT = "<TELEGRAM-TOKEN-BOT>"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Protection
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.message.chat_id
        print(update.message.chat_id)
        if not user_id in LIST_OF_ADMINS:
            print(f"{user_id} not in {LIST_OF_ADMINS}")
            print("Unauthorized access denied for {}:\nmessage: {}.".format(str(update.effective_user),str(context.args)))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


# Create a new Telegram bot
updater = Updater(TOKEN_BOT, use_context=True)
dispatcher = updater.dispatcher


@restricted
def handle_message(update, context):
    # Use the OpenAI API to generate a response to the user's message
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=" ".join(context.args),
        max_tokens=1024,
        temperature=0.5,
    )

    # Send the response back to the user
    context.bot.send_message(update.effective_chat.id, f"```\n{response['choices'][0]['text']}\n```",parse_mode=constants.PARSEMODE_MARKDOWN_V2,)

dp = updater.dispatcher
dp.add_handler(CommandHandler("caracola", handle_message))

# Set up the message handler
#message_handler = MessageHandler(Filters.text, handle_message)
#dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()


updater.idle()
