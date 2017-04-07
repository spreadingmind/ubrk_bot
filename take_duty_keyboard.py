from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import api_trello

def get_keyboard_list():
    keyboard_list = [key for key in api_trello.assigned_cards.items()]
    return keyboard_list

def get_duty_keyboard():


    take_duty_keybrd = [[InlineKeyboardButton
                    ('%s : %s ' % (item[0],item[1]),callback_data='%s'% item[0])]
                    for item in get_keyboard_list()]
    return take_duty_keybrd

# keyboard_back = [[InlineKeyboardButton(" <<< ", callback_data='back')]]

