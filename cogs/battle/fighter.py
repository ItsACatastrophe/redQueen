from cogs.battle import battle

class Fighter():
    user = None
    name = ''
    heart = ''
    circle = ''
    color = None
    position = 0 #The fighter's array index: fighter<array_index>

    weapon = None
    hp = 100
    hp_max = 100

    def __init__(self, user, position):
        self.user = user
        if self.user.nick is None:
            self.name = self.user.name
        else:
            self.name = self.user.nick
        self.position = position
        self.heart = battle.colors.get(position).get('heart')
        self.circle = battle.colors.get(position).get('circle')
        self.color = battle.colors.get(position).get('color')

    def set_weapon(self, weapon): # Either pass emote in weapon_choice or weapon constructor
        if weapon in battle.weapon_choice.keys():
            self.weapon = battle.weapon_choice.get(weapon)()
        else:
            self.weapon = weapon()

    def sub_hp(self, hp):
        self.hp -= hp

    def add_hp(self, hp):
        self.hp += hp

    def attack(self, data):
        results = self.weapon.attack(data)
        data.get('attacked').sub_hp(results.get('damage'))
        return results