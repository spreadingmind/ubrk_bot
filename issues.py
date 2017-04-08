import api_trello
from trello import ResourceUnavailable
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

issues_on_board = api_trello.client.get_board\
    (board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c677a83b683e05b47a3557')



issues_list = api_trello.client.get_board\
    (board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c677a83b683e05b47a3557')\
    .list_cards()
board_members = api_trello.board_members
name_ids = api_trello.name_ids

assigned_issue_cards = { card.name :"Илон Маск" if not card.member_id
                                else name_ids[card.member_id[0]] for card in issues_list}


from_telegram_to_trello_ids = {'113973565':'57eb99e4b60861cf2ff79fe0', '239663592':'5786a9bfac32d311f28ea467',
                               '57148692':'549a9856edb25f0551b035d4', '47303188':'5826d8dc749b784306173e93',
                               '185962649':'5779714c645ba31bc35f3f4c'}

def get_issues_keyboard_list():
    keyboard_list = [key for key in assigned_issue_cards.items()]
    return keyboard_list

def get_issues_keyboard():


    take_duty_keybrd = [[InlineKeyboardButton
                    ('%s : %s ' % (item[0],item[1]),callback_data='%s'% item[0])]
                    for item in get_issues_keyboard_list()]
    return take_duty_keybrd









def assigne_issue_from_telegram(card_name, id):
    print('assign started')
    try:
        for card in issues_list:
            print ('checking card', card.name)
            if card.name == card_name:
                print('found card x')
                member_id = from_telegram_to_trello_ids[id]
                card.assign(member_id=member_id)
        print ('for done')
        assigned_issue_cards[card_name] = name_ids[member_id]
        print ('card assigned')
    except ResourceUnavailable:
        print ('??')
        pass