from trello import TrelloClient, Board, ResourceUnavailable
from trello.member import Member
import constants
from emoji import emojize
import take_duty_keyboard

client = TrelloClient(
    api_key= constants.api_key,
    api_secret= constants.api_secret,
    token=constants.oauth_token,
    token_secret=constants.oauth_token_secret
)


ubrk_list = client.get_board(board_id='58c675660114d45a75eb1ce4').get_list(list_id='58c6759a1985cf9264cc200e').list_cards()

ubrk_duties = {duty.name : 'Илон Маск' for duty in ubrk_list }


print ()


finger = emojize(':point_right: ', use_aliases=True)


board_members = client.get_board(board_id='58c675660114d45a75eb1ce4').get_members()

name_ids = {member.id:member.full_name for member in board_members}
print (name_ids)

assigned_cards = { card.name :"Илон Маск" if not card.member_id
                                else name_ids[card.member_id[0]] for card in ubrk_list}

def mass_unassign():

    try:
        for card in ubrk_list:
            if len(card.member_id) > 0:
                for member in card.member_id:
                    card.unassign(member_id=member)
                    print ('from mass_unassign: Done')
        #как обновить мемберов карточек?
            assigned_cards[card.name] = card.member_id

        # take_duty_keyboard.get_duty_keyboard()

    except ResourceUnavailable:
        pass


from_telegram_to_trello_ids = {'113973565':'57eb99e4b60861cf2ff79fe0', '239663592':'5786a9bfac32d311f28ea467',
                               '57148692':'549a9856edb25f0551b035d4', '47303188':'5826d8dc749b784306173e93',
                               '185962649':'5779714c645ba31bc35f3f4c'}


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

