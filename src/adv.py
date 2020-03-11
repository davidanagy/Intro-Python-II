from item import Item
from room import Room
from player import Player
import sys
import textwrap

# Declare all the items

item = {
    'rock': Item('rock', "A small rock, just large enough to kill a beetle."),

    'coin': Item('coin', "An old, rusted bronze coin. You don't recognize the currency."),

    'pickaxe': Item('pickaxe', """An old, but still perfectly usable pickaxe. Perhaps its previous
owner was overloaded with treasure...or perhaps they had to leave in a hurry.""")
}

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", items=[item['rock']]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", items=[item['pickaxe'], item['coin']]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),

    'placeholder': Room("Placeholder", "Meaningless placeholder room")
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']


# Functions
def start_game(player):
    print("Welcome to David's practice text adventure!")
    print(f'Your name is {player.name}.')
    print('Type "n", "s", "e", or "w" to move in that direction.')
    print('You will see items when you first enter a room, or by typing "l" or "look."')
    print('Pick up items by typing "get" or "take" followed by the item name.')
    print('See your inventory by typing "i" or "inventory".')
    print('Have fun! Type "q" to quit anytime.')


def parse_input(player_input):
    """Determines what type of command the player input"""
    commands = player_input.split(' ')
    if len(commands) == 1:
        if commands[0] == 'q':
            return 'quit'
        elif commands[0] in ['n', 's', 'e', 'w']:
            return 'move'
        elif commands[0] in ['i', 'inventory']:
            return 'inventory'
        elif commands[0] in ['l', 'look']:
            return 'look'
        else:
            return 'invalid'
    elif len(commands) == 2:
        if commands[0] in ['get', 'take', 'drop']:
            return 'item'
        else:
            return 'invalid'
    else:
        return 'invalid'


def look_for_items(room):
    if len(room.items) == 0:
        print("You can't see any items.")
    else:
        print('You can see these items:')
        for i in room.items:
            print(f'* {i.name}')


def get_new_room(current_room, direction):
    """Determine which room the player is attempting to move into"""
    direction_matrix = {
        'n': current_room.n_to,
        's': current_room.s_to,
        'e': current_room.e_to,
        'w': current_room.w_to
    }
    
    new_room = direction_matrix[direction]
    return new_room


def enter_room(player, room):
    """Enters a room, prints description, looks for items"""
    print('\nCurrent room:', room.name)
    print(textwrap.fill(room.description))
    look_for_items(room)
    player.current_room = room


def show_inventory(player):
    if len(player.inventory) == 0:
        print("You aren't carrying anything!")
    else:
        print('You are currently carrying:')
        for it in player.inventory:
            print(f'* "{it.name}": {textwrap.fill(it.description)}')


def take_or_drop_item(player, command):
    room = player.current_room
    commands = command.split(' ')
    action_verb = commands[0]
    action_noun = commands[1]
    it = item[action_noun]
    if action_verb in ['get', 'take']:
        if it in room.items:
            room.items.remove(it)
            player.inventory.append(it)
            it.on_take()
        else:
            print("That item isn't here!")
    elif action_verb in ['drop']:
        if it in player.inventory:
            player.inventory.remove(it)
            room.items.append(it)
            it.on_drop()
        else:
            print("You don't have that item!")


def quit_game():
    print('\nThanks for playing!')


#
# Main
#
args = sys.argv
if len(args) == 1:
    # Default player name
    player_name = 'Alex'
elif len(args) == 2:
    player_name = args[1]
else:
    raise ValueError(f'Must have a maximum of 1 argument')

# Make a new player object that is currently in the 'outside' room.
player = Player(player_name, current_room=room['outside'],
                             previous_room=room['placeholder'])
# The previous_room attribute is an artifact from an earlier version,
# but I'm keeping it so I can implement a "return" command later
# so the player can easily go back to the room they just left.
start_game(player)
enter_room(player, room['outside'])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
while True:
    player_input = input('\nWhat do you want to do?\n')
    command_type = parse_input(player_input)
    if command_type == 'quit':
        break
    elif command_type == 'move':
        destination = get_new_room(player.current_room, player_input)
        if destination is None:
            print("You can't go in that direction!")
        else:
            enter_room(player, destination)
    elif command_type == 'inventory':
        show_inventory(player)
    elif command_type == 'look':
        look_for_items(player.current_room)
    elif command_type == 'item':
        take_or_drop_item(player, player_input)
    elif command_type == 'invalid':
        print('Please enter a valid command.')
    else:
        print('ERROR')

quit_game()
