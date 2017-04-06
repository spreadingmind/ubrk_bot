import datetime
import api_trello


format = "%a %b %d %H:%M:%S %Y"

while True:
    today = datetime.datetime.today().strftime(format)
    if today.startswith('Thu'):
        api_trello.mass_unassign()
        break
    else:
        continue