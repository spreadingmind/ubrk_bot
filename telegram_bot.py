from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import constants
from telegram import bot, update




updater = Updater(token=constants.bot_token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def send_message(bot,update, text, reply_markup):

    bot.sendMessage(text=text, chat_id=update.message.chat_id, reply_markup=reply_markup)

dispatcher.add_handler(CallbackQueryHandler(send_message))

def build_menu(buttons: list,
               n_cols: int,
               header_buttons: list = None,
    ):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)

    return menu


button_list = [
    InlineKeyboardButton("week duties", switch_inline_query_current_chat=None),
    InlineKeyboardButton("hot tasks", switch_inline_query_current_chat=None),
]

reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

send_message(bot, update, text='Menu', reply_markup=reply_markup)

dispatcher.add_handler(CallbackQueryHandler('ubrk',build_menu))


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()