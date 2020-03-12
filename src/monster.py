"""Contains the Monster class for the game"""
import textwrap


class Monster:
    def __init__(self, name, health, weakness, death_string, dropped_item, loss_string, run_away=True):
        self.name = name
        self.health = health
        self.weakness = weakness
        self.death_string = death_string
        self.dropped_item = dropped_item
        self.loss_string = loss_string
        self.run_away = run_away


    def on_attack(self, player, weapon):
        room = player.current_room
        print(f'You attack the {self.name} with your {weapon.name}!')
        if weapon.power >= self.health:
            print(f'You defeated the {self.name}!')
            print(textwrap.fill(self.death_string))
            room.items.append(self.dropped_item)
            return True
        elif weapon.material == self.weakness:
            print(f'The {self.name} collapses. Looks like it was weak to your {weapon.material}.')
            print(textwrap.fill(self.death_string))
            room.items.append(self.dropped_item)
            return True
        else:
            print(f'The {self.name} remains standing!')
            print(textwrap.fill(self.loss_string))
            return False
