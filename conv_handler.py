from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
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
FIRST, SECOND, THIRD, FORTH, FIFTH = range(5)

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

def forth(bot, update):
    query = update.callback_query

    text = 'Coming soon...'
    bot.sendMessage(chat_id=query.message.chat.id, text=text)

def unassign(bot,job):
    format = "%a %b %d %H:%M:%S %Y"

    while True:
        today = datetime.datetime.today().strftime(format)
        print ('Today is ', today)
        if today.startswith('Thu'):
            api_trello.mass_unassign()
            print ('unassigned')
            # bot.sendMessage(text='All tasks are unassigned!', chat_id=update.message.chat_id )
            break
        else:
            continue


def fri_reminder(bot,job):
    bot.sendMessage(text='heya, it is almost weekends. Did you took your task?',
                    chat_id=job.context)


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

j = updater.job_queue
job_unassign = Job(callback=unassign, interval=0, days=(0,), repeat=True)
j.put(job_unassign, next_t=0.0)
bot = Bot(token=TELEGRAM_HTTP_API_TOKEN)
job_fri_reminder = JobQueue(bot, prevent_autostart=None)

update = Update(update_id=1)

job_fri_reminder.run_daily(fri_reminder, time=16, days=(4,), context=update.message.chat_id)


def restart(bot, update):
    bot.sendMessage(update.message.chat_id, "Bot is restarting...Press /ubrk")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)



logger.info("starting dispatcher")
updater.dispatcher.add_handler(CommandHandler('r', restart))

updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TELEGRAM_HTTP_API_TOKEN)
updater.bot.setWebhook('https://ubrk.herokuapp.com/' + TELEGRAM_HTTP_API_TOKEN)
updater.idle()
logger.info("updater set to idle")





