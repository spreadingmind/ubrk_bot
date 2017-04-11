import api_trello
from trello import ResourceUnavailable
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from_telegram_to_trello_ids = {'113973565':'57eb99e4b60861cf2ff79fe0', '239663592':'5786a9bfac32d311f28ea467',
                               '57148692':'549a9856edb25f0551b035d4', '47303188':'5826d8dc749b784306173e93',
                               '185962649':'5779714c645ba31bc35f3f4c'}

def get_issue_list_on_board():
    issues_on_board = api_trello.client.get_board\
    (board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c677a83b683e05b47a3557')
    return issues_on_board


def get_issues_list():
    issues_list = api_trello.client.get_board \
        (board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c677a83b683e05b47a3557') \
        .list_cards()
    return issues_list

def get_assidned_issues():
    name_ids = api_trello.name_ids
    assigned_issue_cards = {card.name: "Илон Маск" if not card.member_id \
        else name_ids[card.member_id[0]] for card in get_issues_list()}
    return assigned_issue_cards

def get_issues_keyboard_list():
    keyboard_list = [key for key in get_assidned_issues().items()]
    return keyboard_list

def get_issues_keyboard():

    take_duty_keybrd = [[InlineKeyboardButton
                    ('%s : %s ' % (item[0],item[1]),callback_data='%s'% item[0])]
                    for item in get_issues_keyboard_list()]
    return take_duty_keybrd


def assigne_issue_from_telegram(card_name, id):
    print('assign started')
    try:
        for card in get_issues_list():
            print ('checking card', card.name)
            if card.name == card_name:
                print('found card x')
                member_id = from_telegram_to_trello_ids[id]
                card.assign(member_id=member_id)
        print ('for done')
        member_id = from_telegram_to_trello_ids[id]
        get_assidned_issues()[card_name] = api_trello.board_members[member_id]
        print ('card assigned')
    except ResourceUnavailable:
        print ('??')
        pass