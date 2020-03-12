# Implement a class to hold room information. This should have name and
# description attributes.
import textwrap


class Room:
    def __init__(self, name, description, items, is_light=True, monster=None):
        self.name = name
        self.description = description
        self.items = items
        self.is_light = is_light
        self.monster = monster
        # set default directions to None
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        # set default value for open_door property
        self.open_door = {'placeholder': 'this is a meaningless placeholder'}

    def player_opens_door(self, player, item):
        if item.name in self.open_door.keys():
            open_results = self.open_door[item.name]
            new_direction = open_results[0]
            new_room = open_results[1]
            success_string = open_results[2]
            new_description = open_results[3]
            destroy_item = open_results[4]
            setattr(self, new_direction, new_room)
            print(textwrap.fill(success_string))
            self.description = new_description
            if destroy_item is True:
                player.inventory.remove(item.name)
            self.open_door.pop(item.name)
        else:
            print('Nothing happens...')

    def __repr__(self):
        return f'<Room {self.name}>'
