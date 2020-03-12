# Write a class to hold player information, e.g. what room they are in
# currently.
class Player:
    def __init__(self, name, current_room, previous_room, inventory=[], last_item_mentioned=None):
        self.name = name
        self.current_room = current_room
        self.previous_room = previous_room
        self.inventory = inventory

    def __repr__(self):
        return f'<Player {self.name}>'
