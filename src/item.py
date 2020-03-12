"""Contains item classes for the game"""
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def on_take(self):
        print(f'You have picked up the {self.name}.')

    def on_drop(self):
        print(f'You dropped the {self.name}.')

    def __repr__(self):
        return f'<Item {self.name}>'


class LightSource(Item):
    def on_take(self):
        print(f'You have picked up the {self.name}. It illuminates the surrounding area.')

    def on_drop(self):
        print(f"It's not wise to drop your source of light!")

    def __repr__(self):
        return f'<LightSource {self.name}>'


class Weapon(Item):
    def __init__(self, name, description, material, power):
        super().__init__(name=name, description=description)
        self.material = material
        self.power = power

    def on_take(self):
        print(f'You have picked up the {self.name}. You feel safer with a weapon in hand.')

    def __repr__(self):
        return f'<Weapon {self.name}>'
