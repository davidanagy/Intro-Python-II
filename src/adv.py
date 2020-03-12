from item import Item, LightSource, Weapon
from monster import Monster
from room import Room
from player import Player
import sys
import textwrap

# Declare all the items

item = {
    'rock1': Weapon('small rock', 'A small rock, but large enough to use as a weapon.',
material='rock', power=1),

    'coin1': Item('rusted coin', "An old, rusted bronze coin. You don't recognize the currency."),

    'coin2': Item('green coin', "An odd green coin. You can't tell what it's made of."),

    'pickaxe1': Item('old pickaxe', """An old, but still perfectly usable pickaxe. Perhaps its previous
owner was overloaded with treasure...or perhaps they had to leave in a hurry."""),

    'lamp1': LightSource('flickering lamp', """An old magical lamp. Its magical circuits flicker occasionally,
but still glow enough to let you see your immediate surrounding area."""),

    'club1': Weapon('wooden club', """A thick club made of tough lumber. The rough finishing
is characteristic of goblin make.""", material='wood', power=2)
}

# Declare all the monsters

monster = {
    'goblin': Monster('goblin', health=1, weakness=None, death_string="""The goblin wails and collapses
to the ground with a thud, dark red blood flowing from the wound in its head. Its limbs twitch periodically,
but it's no longer a threat. Its club rolls out of its limp hand.""", dropped_item=item['club1'],
loss_string="""You turn to run away, but you're not fast enough. The goblin smashes your knee
with its club, and you fall to the ground as your leg crumples beneath you. You barely have time
to look up to see the club collide into your face. Vision fading, the last thing
you hear is the goblin's cry of triumph before you feel one last blow to your head.""")
}

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons",
                     items=[]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", items=[item['rock1']]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", items=[item['lamp1']], is_light=False),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", items=[item['pickaxe1'], item['coin1'], item['coin2']],
is_light=False),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south, but there are some
loose rocks to the east. With the right tool, perhaps you could dislodge them?""",
items=[], is_light=False),

    'tunnel': Room("Small Tunnel", """A small tunnel that narrows to the west but grows larger
as you head east.""", items=[], is_light=False),

    'goblin_den': Room("Goblin Den", """A small chamber roughly cut from the surrounding cave
walls. Various animal pelts line the floor, and a pile of skulls lies in one corner. Tunnels
stretch to the east, north, and south.""", items=[], is_light=False, monster=(monster['goblin'],
"""As you enter the chamber, you hear a shriek of alarm. A small, green creature wearing only
a tattered brown cloth charges at you, wooden club held high.""")),

    'placeholder': Room("Placeholder", "Meaningless placeholder room", items=[])
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
room['tunnel'].w_to = room['treasure']
room['tunnel'].e_to = room['goblin_den']
room['goblin_den'].w_to = room['tunnel']

# Set the "open_door" tag

room['treasure'].open_door={'old pickaxe': ('e_to', room['tunnel'], """A few whacks with the pickaxe
is enough to dislodge the eastern rocks, revealing a small tunnel just wide enough
for you to crawl into.""", """You've found the long-lost treasure chamber! Sadly, it has
already been completely empited by earlier adventurers. There's an exit to the south and
a small tunnel to the east.""", False)}

# Invalid command message
invalid_command_message = 'Please enter a valid command.'

# Functions
def print_commands():
    print('Type "n", "s", "e", or "w" to move in that direction.')
    print('Type "return" to return to the previous room.')
    print('You will see information about a room when you first enter it, or by typing "l" or "look."')
    print('Pick up items by typing "get" or "take" followed by the item name.')
    print('Use an item by typing "use" followed by the item name.')
    print('You can also drop an item by typing "drop," or type "it" instead of an item')
    print('name to pick up or drop the last item you interacted with.')
    print('Open your inventory by typing "i" or "inventory".')
    print('See these commands again by typing "h" or "help."')
    print('For information about battles, type "battle help."')
    print('Finally, type "q" to quit anytime.')


def print_battle_info():
    print('\nWhen you enter a room with a monster, it will automatically attack you!')
    print('Most of your commands will no longer work, though you can still check your inventory.')
    print(textwrap.fill('''Choose an item to be your weapon, and type "wield"
or "w" followed by the item name to attack with it.'''))
    print('Be warned, though: if you choose incorrectly, the monster will survive and kill you!')
    print("""If you don't think you can win, type "run" to run away.""")
    print("(Though there are some monsters you can't run away from!)")


def start_game(player):
    print("Welcome to David's practice text adventure!")
    print(f'Your name is {player.name}.')
    print_commands()
    print('Have fun!')


def parse_input(player_input):
    """Determines what type of command the player input"""
    commands = player_input.split(' ')
    if len(commands) == 1:
        if commands[0] == 'q':
            return 'quit'
        elif commands[0] in ['h', 'help']:
            return 'help'
        elif commands[0] in ['n', 's', 'e', 'w']:
            return 'move'
        elif commands[0] in ['return']:
            return 'return'
        elif commands[0] in ['i', 'inventory']:
            return 'inventory'
        elif commands[0] in ['l', 'look']:
            return 'look'
        else:
            return 'invalid'
    elif len(commands) in range(2, 4):
        if commands[0] in ['get', 'take', 'use', 'drop']:
            return 'item'
        elif player_input == 'battle help':
            return 'battle help'
        else:
            return 'invalid'
    else:
        return 'invalid'


def is_illuminated(room, player):
    """Determines if a room is illuminated or not. Returns True
    if it is, False if it isn't."""
    illumination = False
    if room.is_light is True:
        illumination = True
    else:
        for it in room.items:
            if isinstance(it, LightSource):
                illumination = True
                break
        for it in player.inventory:
            if isinstance(it, LightSource):
                illumination = True
                break
    return illumination


def look_at_room(player):
    """Prints room name, description, and items--as long as it's illuminated."""
    room = player.current_room
    illumination = is_illuminated(room, player)
    if illumination is True:
        print('\nCurrent room:', room.name)
        print(textwrap.fill(room.description))
        if len(room.items) == 0:
            print("You can't see any items.")
        else:
            print('You can see these items:')
            for i in room.items:
                print(f'* {i.name}')
    else:
        print("It's pitch black!")


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
    """Enters a room, prints description, looks for items, starts battle
    if monster is present."""
    player.previous_room = player.current_room
    player.current_room = room
    if room.monster is None:
        look_at_room(player)
    else:
        illumination = is_illuminated(room, player)
        if illumination is True:
            print('\nCurrent room:', room.name)
            print(textwrap.fill(room.description))
            mon = room.monster[0]
            begin_fight_string = room.monster[1]
            print(begin_fight_string)
            fight_monster(player, mon)
        else:
            print(textwrap("""It's pitch black! As you stumble around, you can hear
something approaching. You try to get away, but it's too late. The last thing you feel
is a sense of overwhelming fear."""))
            player.current_room == 'death'


def show_inventory(player):
    if len(player.inventory) == 0:
        print("You aren't carrying anything!")
    else:
        print('You are currently carrying:')
        for it in player.inventory:
            print(f'* "{it.name}": {textwrap.fill(it.description)}')


def match_item(commands, action_noun, item_list, failure_message):
    """Takes a list of commands, the noun in the commands, a list of items
    to look through, and a message to print in event of failure.
    Returns either "None" (if a matching item can't be found) or the item
    that matches the action_noun."""
    matching_items = []
    for i in item_list:
        if action_noun in i.name:
            matching_items.append(i)
    if len(matching_items) == 0:
        print(failure_message)
        return None
    elif len(matching_items) == 1:
        match = matching_items[0]
        return match
    else:
        if len(commands) == 2:
            print_strings = ["I don't know which you mean:"]
            for i in matching_items:
                print_strings.append(i.name)
                print_strings.append('or')
            # remove the final "or"
            del print_strings[-1]
            print(' '.join(print_strings))
            return None
        else:
            action_adjective = commands[1]
            for i in matching_items:
                if i.name == action_adjective + ' ' + action_noun:
                    match = i
                    break
            return match


def take_item(player, item):
    player.last_item_mentioned = item
    room = player.current_room
    room.items.remove(item)
    player.inventory.append(item)
    item.on_take()


def use_item(player, item):
    """Attempts to use an item to open a new path."""
    player.last_item_mentioned = item
    room = player.current_room
    room.player_opens_door(player, item)


def drop_item(player, item):
    player.last_item_mentioned = item
    room = player.current_room
    player.inventory.remove(item)
    room.items.append(item)
    item.on_drop()


def take_use_drop_item(player, command):
    room = player.current_room
    commands = command.split(' ')
    if len(commands) == 2:
        action_verb = commands[0]
        action_noun = commands[1]
    else:
        # other option is that len(commands) == 3
        action_verb = commands[0]
        action_adjective = commands[1]
        action_noun = commands[2]
    if action_verb in ['get', 'take']:
        illumination = is_illuminated(room, player)
        if illumination is True:
            take_failure = "That item isn't here!"
            if action_noun == 'it':
                it = player.last_item_mentioned
                if it in room.items:
                    take_item(player, it)
                else:
                    print(take_failure)
            else:
                it = match_item(commands, action_noun, room.items, take_failure)
                if it is not None:
                    take_item(player, it)
        else:
            print('Good luck finding that in the dark!')

    elif action_verb in ['use']:
        illumination = is_illuminated(room, player)
        if illumination is True:
            use_failure = "You don't have that item!"
            if action_noun == 'it':
                it = player.last_item_mentioned
                if it in player.inventory:
                    use_item(player, it)
                else:
                    print(use_failure)
            else:
                it = match_item(commands, action_noun, player.inventory, use_failure)
                if it is not None:
                    use_item(player, it)

    elif action_verb in ['drop']:
        drop_failure = "You don't have that item!"
        if action_noun == 'it':
            it = player.last_item_mentioned
            if it in player.inventory:
                drop_item(player, it)
            else:
                print(drop_failure)
        else:
            it = match_item(commands, action_noun, player.inventory, drop_failure)
            if it is not None:
                drop_item(player, it)


def fight_monster(player, mon):
    while True:
        room = player.current_room
        player_input = input('\nFight to survive! (For help, type "battle help".)\n')
        commands = player_input.split(' ')
        if len(commands) not in range(1,4):
            print(invalid_command_message)
        elif player_input == 'q':
            player.current_room = 'quit'
            break
        elif player_input == 'battle help':
            print_battle_info()
        elif player_input == 'run':
            if mon.run_away is True:
                print('You successfully run away!')
                enter_room(player, player.previous_room)
                break
            else:
                print("You can't run away!")
                print(mon.loss_string)
                player.current_room = 'death'
                break
        elif player_input in ['i', 'inventory']:
            show_inventory(player)
        elif commands[0] in ['wield', 'w']:
            if len(commands) not in range(2,4):
                print(invalid_command_message)
            elif len(player.inventory) == 0:
                print("Oh no, you don't have any weapons! You can't fight back!")
                print(mon.loss_string)
                player.current_room = 'death'
                break
            else:
                attack_failure = "You don't have that item!"
                if len(commands) == 2:
                    action_noun = commands[1]
                elif len(commands) == 3:
                    action_noun = commands[2]
                it = match_item(commands, action_noun, player.inventory, attack_failure)
                if it is not None:
                    if isinstance(it, Weapon):
                        victory = mon.on_attack(player, it)
                        if victory:
                            room.monster = None
                            break
                        else:
                            player.current_room = 'death'
                            break
                    else:
                        print(f"Oh no, that's not a weapon! The {mon.name} is unaffected!")
                        print(mon.loss_string)
                        player.current_room = 'death'
                        break
        else:
            print(invalid_command_message)


def print_death_message():
    print('\nSorry, you died. And unfortunately, this game has no save functionality!')
    print('Despite that, I hope you play again!')


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
while player.current_room not in ['death', 'quit']:
    player_input = input('\nWhat do you want to do?\n')
    command_type = parse_input(player_input)
    if command_type == 'quit':
        player.current_room = 'quit'
    elif command_type == 'help':
        print_commands()
    elif command_type == 'battle help':
        print_battle_info()
    elif command_type == 'move':
        destination = get_new_room(player.current_room, player_input)
        if destination is None:
            print("You can't go in that direction!")
        else:
            enter_room(player, destination)
    elif command_type == 'return':
        enter_room(player, player.previous_room)
    elif command_type == 'inventory':
        show_inventory(player)
    elif command_type == 'look':
        look_at_room(player)
    elif command_type == 'item':
        take_use_drop_item(player, player_input)
    elif command_type == 'invalid':
        print(invalid_command_message)
    else:
        print('ERROR')

if player.current_room == 'death':
    print_death_message()
elif player.current_room == 'quit':
    quit_game()
else:
    print('ERROR')
