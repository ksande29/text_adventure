# FUNCTIONS - - - - - - - - - - -
def print_location():
    print('You are currently in the ', player.get('location'))


def print_map():
    print('''
    ----------------------------------
    |             Foyer              |
    |                                |
    -----   --------------   ---------
    |  Parlor      |     Library     |
    |              |   (w/ ghost)    |
    ----   -----------------   -------
    |            Kitchen             |
    |                                |
    -----  --------------------------
    |      Pantry      |
    |   (w/ monster)   |
    --------------------
    ''')


def print_inventory():
    print('Your inventory: ', player.get('inventory_list', 'Your inventory is empty'))


def print_conversation():
    if len(conversation) == 0:
        print('You have not talked to the ghost yet')
    else:
        print('Here is your last conversation with the ghost:')
        for index, el in enumerate(conversation):
            if index % 2 == 0:
                print("Ghost: ", conversation[index])
            else:
                print("Adventurer: ", conversation[index])


# GAME SET UP - - - - - - - - - -
file = open("instructions", "r")
print(file.read())
print_map()

# GLOBAL VARIABLES - - - - - - - - - - -
player = {'inventory_list': {'courage'}, 'location': 'foyer'}
rooms = {'foyer': {'description': 'entry to the house',
                   'items': ['umbrella', 'coat', 'keys'],
                   'exits': ['parlor', 'library']
                   },
         'parlor': {'description': 'formal sitting room',
                    'items': ['painting', 'flowers', 'pillow'],
                    'exits': ['foyer', 'kitchen']
                    },
         'library': {'description': 'home of all the books in the house',
                     'items': ['book', 'glasses', 'lamp'],
                     'exits': ['foyer', 'kitchen']
                     },
         'kitchen': {'description': 'where food is prepared',
                     'items': ['apple', 'pot', 'salt'],
                     'exits': ['parlor', 'library', 'pantry']
                     },
         'pantry': {'description': 'where food is stored',
                    'items': ['can', 'garlic', 'jar'],
                    'exits': ['kitchen']
                    }
         }
monster = {'health': 1, 'sanity': 1, 'alive': True}
conversation = []
things_ghost_says = ["Talk to me. ",
                     "That's interesting. Talk to me some more. ",
                     "Hello, Im a ghost in the library. I am lonely.  I like conversation.  If you really don't want "
                     "to converse type 'stop'. "]

# PLAY GAME - - - - - - - - - -
while True:
    room = player.get('location')
    print('\n')
    print_location()

    # talk to ghost
    if room == 'library':
        user_input = input(things_ghost_says[2])
        conversation.append(things_ghost_says[2])
        conversation.append(user_input)
        counter = 0
        while user_input != 'stop':
            user_input = input(things_ghost_says[counter % 2])
            conversation.append(things_ghost_says[counter % 2])
            conversation.append(user_input)
            counter = counter + 1

    # fight monster
    if room == 'pantry':
        if monster['alive']:
            user_input = input("Watch out! A monster is attacking you! To slay him you must hit and also hypnotize him"
                               " (use the commands'karate chop' or 'hypnotize'):")
            while monster['alive']:
                if user_input == 'karate chop':
                    monster['health'] = 0
                    print('Good job, you have injured the monster. His health is now 0')
                if user_input == 'hypnotize':
                    monster['sanity'] = 0
                    print('Good job, you have driven the monster crazy. His sanity is now 0')
                if monster['health'] == 0 and monster['sanity'] == 0:
                    monster['alive'] = False
                else:
                    user_input = input("You are hurting the monster but you haven't slayed him. To slay him you must "
                                       "hit and also hypnotize him (Use the commands 'karate chop' or 'hypnotize')")
        if not monster['alive']:
            print('There is a monster in this room but you slayed it')

    user_input = input("Enter a command like 'enter [room name]', 'inventory', 'take all items', 'take [item]', "
                       "'items', 'conversation', 'map', 'quit': ").lower().split(" ")
    command = ''
    verb = ''
    if len(user_input) == 1:
        command = user_input[0]
    if len(user_input) > 1:
        verb = user_input[0]
        noun = user_input[1]

    if verb == 'enter':
        if noun in rooms[room]['exits']:
            player.update({'location': noun})
        else:
            print('You cannot enter that room from here')

    if command == 'map':
        print_map()

    if command == 'items':
        print("The items that are in the room: ", rooms[room]['items'])

    if command == 'inventory':
        print_inventory()

    if command == 'conversation':
        print_conversation()

    if command == 'quit':
        print('Your adventure has ended!')
        break

    if verb == 'take' and noun == 'all':
        new_set = player['inventory_list']
        for el in rooms[room]['items']:
            new_set.add(el)
        player.update({'inventory_list': new_set})
        rooms[room]['items'] = []
    elif verb == 'take':
        if noun in rooms[room]['items']:
            new_set = player['inventory_list']
            new_set.add(noun)
            player.update({'inventory_list': new_set})
            rooms[room]['items'].remove(noun)
        else:
            print("that items is not in the room")
