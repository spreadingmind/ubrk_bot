from trello import TrelloClient, Board, ResourceUnavailable
from trello.member import Member
import constants
from pprint import pprint
from emoji import emojize
import take_duty_keyboard

client = TrelloClient(
    api_key= constants.api_key,
    api_secret= constants.api_secret,
    token=constants.oauth_token,
    token_secret=constants.oauth_token_secret
)

#avaliable methods:
# from pprint import pprint as pp
# pp(dir(client))

#get list of my Boards
# my_boards = {}
# for board in client.list_boards(board_filter='all'):
#     my_boards[board] = board.id
#
# def print_all_boards():
#     for board in my_boards:
#         print (board, my_boards[board])
# print_all_boards()




ubrk_list = client.get_board(board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c6759a1985cf9264cc200e').list_cards()

ubrk_duties = {duty.name : 'Илон Маск' for duty in ubrk_list }


print ()


finger = emojize(':point_right: ', use_aliases=True)


board_members = client.get_board(board_id='58c675660114d45a75eb1ce4').get_members()

name_ids = {member.id:member.full_name for member in board_members}
print (name_ids)

assigned_cards = { card.name :"Илон Маск" if not card.member_id
                                else name_ids[card.member_id[0]] for card in ubrk_list}

def mass_assign_or_unassign():
    for card in ubrk_list:
        try:
            card_id = card.id
            new_card = client.get_card(card_id=card_id)
            new_card.unassign(member_id='57eb99e4b60861cf2ff79fe0')
        except ResourceUnavailable:
            pass


from_telegram_to_trello_ids = {'113973565':'57eb99e4b60861cf2ff79fe0', '239663592':'5779714c645ba31bc35f3f4c',
                               '57148692':'549a9856edb25f0551b035d4', '47303188':'5826d8dc749b784306173e93'}


def assigne_from_telegram(card_name, id):
    print('assign started')
    try:
        for card in ubrk_list:
            print ('checking card', card.name)
            if card.name == card_name:
                print('found card x')
                card = client.get_card(card_id=card.id)
                member_id = from_telegram_to_trello_ids[id]
                card.assign(member_id=member_id)
        print ('for done')
        assigned_cards[card_name] = name_ids[member_id]
        print ('card assigned')
    except ResourceUnavailable:
        print ('??')
        pass

