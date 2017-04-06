from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, \
    ConversationHandler, Job, JobQueue
import constants
import api_trello
from emoji import emojize
import take_duty_keyboard
import os
import time
import sys
import datetime
import logging

logger = logging.getLogger('ubrk_bot')
logger.setLevel(logging.WARNING)


TELEGRAM_HTTP_API_TOKEN = constants.bot_token
PORT = int(os.environ.get('PORT', '5000'))
FIRST, SECOND, THIRD, FORTH = range(4)

import logging
logger = logging.getLogger('ubrk_bot')
logger.setLevel(logging.WARNING)

def start(bot, update):
    logger.info("ubrk bot started")
    text = emojize('        :recycle:  UBRK  :mushroom:  UPRK ', use_aliases=True)
    keyboard = [
        [InlineKeyboardButton(text, callback_data=str(FIRST))],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Welcome to UBRK bot!',
        reply_markup=reply_markup
    )
    telegram_id = update.message.from_user.id
    return FIRST


def first(bot, update):
    logger.debug("responding to request of some user")
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(u"Week duties", callback_data=str(SECOND))],
        [InlineKeyboardButton(u'Issues', callback_data=str(FORTH))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
        text=u"Choose the option"

    )

    return SECOND

def take_duty(update, bot):
    logger.debug("starting take_duty!")
    query = update.callback_query
    option = query.data
    reply_markup = InlineKeyboardMarkup(take_duty_keyboard.get_duty_keyboard())
    user_id = update.callback_query.from_user.id
    text = 'Помоги Илону Маску! Нажимая на кнопку, ты берёшь на себя важную задачу :)'
    bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)
    print ('from take duty', option)


    return THIRD


def second(bot, update):
    query = update.callback_query
    option = query.data
    print ('from second', option)
    if option == '1':
        return take_duty(update,bot)

    if option == '3':
        forth(bot,update)
    return

def third(bot,update):
    print ('third started')
    query = update.callback_query
    option = query.data
    user_id = str(update.callback_query.from_user.id)
    if option:
        print ('from third: if started')
        api_trello.assigne_from_telegram(option, user_id)
    print ('from third:', option, api_trello.assigned_cards[option])




    keyboard = [[InlineKeyboardButton(u"Back to menu", callback_data=str(FIRST))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
        text=u"Cпасибо,что взял(а) на себя задачу!"
    )

    return FIRST

def forth(bot, update): #here would be issues
    query = update.callback_query

    text = 'Coming soon...'
    bot.sendMessage(chat_id=query.message.chat.id, text=text)

updater = Updater(TELEGRAM_HTTP_API_TOKEN)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ubrk', start)],
    states={
        FIRST: [CallbackQueryHandler(first)],
        SECOND: [CallbackQueryHandler(second)],
        THIRD: [CallbackQueryHandler(third)],
        FORTH: [CallbackQueryHandler(forth)]
    },
    fallbacks=[CommandHandler('ubrk', start)]
)

updater.dispatcher.add_handler(conv_handler)


def restart(bot, update):
    bot.sendMessage(update.message.chat_id, "Bot is restarting...Press /ubrk")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


def mass_unassign(bot, update,job):
    format = "%a %b %d %H:%M:%S %Y"

    while True:
        today = datetime.datetime.today().strftime(format)
        if today.startswith('Thu'):
            api_trello.mass_unassign()
            print ('unassigned')
            bot.sendMessage(text='All tasks are unassigned!', chat_id=update.message.chat_id )
            break
        else:
            continue
    j = updater.job_queue
    job_minute = Job(callback=mass_unassign, interval=0, days=(0, 3), context=update.message.chat_id)

    j.put(job_minute, next_t=0.0)

timer_handler = CommandHandler('ubrk', mass_unassign, pass_job_queue=True)
updater.dispatcher.add_handler(timer_handler)



logger.info("starting dispatcher")
updater.dispatcher.add_handler(CommandHandler('r', restart))

updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TELEGRAM_HTTP_API_TOKEN)
updater.bot.setWebhook('https://ubrk.herokuapp.com/' + TELEGRAM_HTTP_API_TOKEN)
updater.idle()
logger.info("updater set to idle")





