from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import api_trello


week_duties_options = {'ubrk cписок': api_trello.ubrk_duties,
                       'расписание дежурств по неделям':['4 неделя марта: Лиза, Виталик',
                                                         '5 неделя марта: все вместе'],
                       'взять себе задачу из ubrk списка': "" }

kkeyboard = [[InlineKeyboardButton(i, callback_data='%s' % i)] for i in week_duties_options]
#print (kkeyboard)

