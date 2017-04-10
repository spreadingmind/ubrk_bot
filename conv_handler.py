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
import issues

logger = logging.getLogger('ubrk_bot')
logger.setLevel(logging.WARNING)


TELEGRAM_HTTP_API_TOKEN = constants.bot_token
PORT = int(os.environ.get('PORT', '5000'))
FIRST, SECOND, THIRD, FORTH, FIFTH, SIXTH = range(6)

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

    return FIRST


def first(bot, update):
    logger.debug("responding to request of some user")
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(u"Week duties", callback_data=str(SECOND))],
        [InlineKeyboardButton(u'Issues', callback_data=str(FORTH))],
        [InlineKeyboardButton(u'Go to Trello board', callback_data=str(FIFTH))]
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
    if option == '4':
        open_trello(bot, update)
    else:
        sixth(bot, update)

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
    text = emojize(u"Cпасибо,что взял(а) на себя задачу! :kissing_heart: ",use_aliases=True)
    bot.sendMessage(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
        text=text
    )
    return FIRST

def forth(bot, update):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(issues.get_issues_keyboard())
    text = emojize(':fire: Issues! No code reqiured(probably) :v: ', use_aliases=True)
    bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup)
    return SIXTH

def sixth(bot, update):
    query = update.callback_query
    option = query.data
    user_id = str(update.callback_query.from_user.id)
    if option:
        issues.assigne_issue_from_telegram(option, user_id)

    keyboard = [[InlineKeyboardButton(u"Back to menu", callback_data=str(FIRST))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = emojize(u"Cпасибо,что взял(а) на себя задачу! :kissing_heart: ", use_aliases=True)
    bot.sendMessage(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup,
        text=text
    )

    return FIRST

def open_trello(bot,update):
    query = update.callback_query
    bot.sendMessage(chat_id=query.message.chat_id, text='https://trello.com/b/jFPgFoqm/ubrk-is-fun',
                    parse_mode='HTML')


def unassign(bot,job):
    format = "%a %b %d %H:%M:%S %Y"

    while True:
        today = datetime.datetime.today().strftime(format)
        print ('Today is ', today)
        if today.startswith('Mon') and today.split()[3].startswith('1') :
            api_trello.mass_unassign()
            print ('unassigned')
            bot.sendMessage(text='All week tasks are unassigned! Ready for new one? ;)',chat_id='-1001092676323' )
            break
        else:
            continue
    return FIRST


def fri_reminder(bot, job):
    today = datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y")
    if today.startswith('Fri') and today.split()[3].startswith('1'):
        text = emojize('Heya! It is almost weekends :eyes: Did you take your UBRK task? ;)', use_aliases=True)
        bot.sendMessage(text=text, chat_id='-1001092676323')

    if today.startswith('Sun') and today.split()[3].startswith('1'):
        text = emojize('It is last day of the week to make our flat shiny. Rock this boat! :sunglasses:',use_aliases=True)
        bot.sendMessage(text=text,chat_id='-1001092676323')

updater = Updater(TELEGRAM_HTTP_API_TOKEN)

j = updater.job_queue
job_unassign = Job(callback=unassign, interval=None, days=(0,)) #repeat=True)
j.put(job_unassign, next_t=0.0)


job_fri_reminder = Job(callback=fri_reminder, interval=None,days=(4,6)) #repeat=True

j.put(job_fri_reminder, next_t=10)

def restart(bot, update):
    bot.sendMessage(update.message.chat_id, "Bot is restarting...Press /ubrk")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

logger.info("starting dispatcher")
updater.dispatcher.add_handler(CommandHandler('r', restart))

def add_issue(bot, update, args):

    issue_name = ' '.join(args)
    if len(issue_name) > 0:
        issues.get_issue_list_on_board().add_card(name=issue_name)

        print('issue added')
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=emojize('Issue added to list. Cool :clap:', use_aliases=True)
                        )
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Issue name should be non-empty!')
    reply_markup = InlineKeyboardMarkup(issues.get_issues_keyboard())
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='See other issues: ',
                    reply_markup=reply_markup)
    return FORTH

issue_handler = CommandHandler('issue', add_issue, pass_args=True)
updater.dispatcher.add_handler(issue_handler)

def delete_issue(bot, update, args):
    issue_to_del = ' '.join(args)
    if len(issue_to_del) > 0:
        for card in issues.get_issues_list():
            print (card.name)
            if card.name == issue_to_del:

                card.delete()
                bot.sendMessage(chat_id=update.message.chat_id, text=emojize('Issue removed Great job! :wink:', use_aliases=True))

    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Issue name should be non-empty!')
    reply_markup = InlineKeyboardMarkup(issues.get_issues_keyboard())
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='See other issues: ',
                    reply_markup=reply_markup)
    return FORTH

issue_to_del_handler = CommandHandler('delissue', delete_issue, pass_args=True)
updater.dispatcher.add_handler(issue_to_del_handler)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ubrk', start)],
    states={
        FIRST: [CallbackQueryHandler(first)],
        SECOND: [CallbackQueryHandler(second)],
        THIRD: [CallbackQueryHandler(third)],
        FORTH: [CallbackQueryHandler(forth)],
        FIFTH:[CallbackQueryHandler(open_trello)],
        SIXTH: [CallbackQueryHandler(sixth)]

    },
    fallbacks=[CommandHandler('ubrk', start)]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TELEGRAM_HTTP_API_TOKEN)
updater.bot.setWebhook('https://ubrk.herokuapp.com/' + TELEGRAM_HTTP_API_TOKEN)
updater.idle()
logger.info("updater set to idle")





