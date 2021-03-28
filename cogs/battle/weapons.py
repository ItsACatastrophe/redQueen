# Attack functions are ordered by their damage where 0 is the least.

class RangeDict(dict): # Range keys are not inclusive of their upper boundary.
    def __getitem__(self, item):
        if not isinstance(item, range): 
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


# Abstract base class for all weapons
class Weapon():
    icon = ' '

    def __init__(self):
        return

    def __str__(self):
        return self.__class__.__name__

    def attack(self, seed): # Base attack method
        return 
    # Damage should look like

class Dagger(Weapon):
    icon = '🗡️'

    def attack0(self, data): 
        damage = data.get('seed') % 4 + 5 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ pokes __{{attacked}}__ for **{damage}** damage',
        }
        return out
    
    def attack1(self, data): 
        damage = data.get('seed') % 5 + 10 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ stabs __{{attacked}}__ for **{damage}** damage',
        }
        return out

    def attack2(self, data): 
        damage = data.get('seed') % 5 + 25 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ stabs __{{attacked}}__ in the back for **{damage}** damage 👤🗡️ ',
        }
        return out

    attacks = RangeDict({
        range(0,6): attack0, #poke
        range(6,8): attack1, #stab
        range(8,9): attack2, #backstab
            
    }) 

    def attack(self, data):
        return self.attacks[data.get('seed') % 9](self, data) #The seed should be mod the upper limit of the range of attacks

    
    def __init__(self):
        return

class Gun(Weapon):
    icon = '🔫'

    def attack0(self, data): 
        damage = data.get('seed') % 4 + 9 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ shoots __{{attacked}}__ for **{damage}** damage',
        }
        return out
    
    def attack1(self, data): 
        damage = 100 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'💥**HEADSHOT** __{{attacker}}__ headshots __{{attacked}}__ for **{damage}** damage 💥',
        }
        return out

    attacks = RangeDict({
        range(0,33): attack0, #shoots
        range(33,34): attack1, #headshots
    }) 

    def reloading7(self, data):
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ ran out of bullets and has to reload',
        }
        return out

    def reloading0(self, data):
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__\'s gun is reloaded and ready to fire',
        }
        return out

    reloading = {
        7: reloading7,
        0: reloading0,
    }

    def attack(self, data):
        turn_mod = data.get('turn') % 8
        if turn_mod == 0 or turn_mod == 7:
            return self.reloading[turn_mod](self, data)

        return self.attacks[data.get('seed') % 34](self, data) #The seed should be mod the upper limit of the range of attacks

    
    def __init__(self):
        return
    
class Fists(Weapon):
    icon = '🤜'

    def attack0(self, data): 
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ swings and **misses** __{{attacked}}__ 💫',
        }
        return out
    
    def attack1(self, data): 
        damage = 1 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ smacks __{{attacked}}__ for **{damage}** damage',
        }
        return out

    def attack2(self, data): 
        damage = data.get('seed') % 2 + 3 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ punches __{{attacked}}__ for **{damage}** damage',
        }
        return out

    def attack3(self, data): 
        damage = data.get('seed') % 2 + 6 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ wallops __{{attacked}}__ for  **{damage}** damage',
        }
        return out

    def attack4(self, data): 
        damage = data.get('seed') % 2 + 7 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ slams __{{attacked}}__ for **{damage}** damage',
        }
        return out

    attacks = RangeDict({
        range(0,1): attack0, #miss
        range(1,2): attack1, #jab
        range(2,3): attack2, #punch
        range(3,4): attack3, #wallop
        range(4,5): attack4, #slam   
    }) 

    def attack(self, data):
        return self.attacks[data.get('seed') % 5](self, data) #The seed should be mod the upper limit of the range of attacks

    
    def __init__(self):
        return

class Bomb(Weapon):
    icon = '💣'

    def attack0(self, data): 
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ threw a bomb at __{{attacked}}__',
        }
        return out

    def attack1(self, data): 
        damage = data.get('seed') % 60 + 45 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__\'s bomb exploded for **{damage}** damage to __{{attacked}}__ 🤯',
        }
        return out

    
    def attack2(self, data): 
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ is out of bombs and must use fists 🤜',
        }
        data.get('attacker').set_weapon(Fists)
        return out

    attacks = RangeDict({
        range(1,2): attack0, #throw
        range(2,3): attack1, #explode
        range(3,4): attack2, #fists
    }) 

    def attack(self, data):
        return self.attacks[data.get('turn')](self, data) #The seed should be mod the upper limit of the range of attacks

    def __init__(self):
        return
    
class Swords(Weapon):
    icon = '⚔️'

    def attack0(self, data): 
        damage = data.get('attacked').hp // 2
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ chopped __{{attacked}}__ in half for **{damage}** damage 👥',
        }
        return out

    def attack1(self, data): 
        damage = data.get('seed') % 2 + 1 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ grazed __{{attacked}}__ for **{damage}** damage',
        }
        return out

    attacks = RangeDict({
        range(0,1): attack0, #half
        range(1,2): attack1, #sliced
    }) 

    def attack(self, data):
        return self.attacks[data.get('seed') % 2](self, data) #The seed should be mod the upper limit of the range of attacks

    def __init__(self):
        return

class Magic(Weapon):
    icon = '🪄'

    def attack0(self, data): 
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ casted a spell. She\'s starting to power up',
        }
        return out
    
    def attack1(self, data):
        out = {
            'damage': 0,
            'text': f'__{{attacker}}__ lost focus and her spell fizzled',
        }
        return out

    #Power 0
    def attack2(self, data): 
        damage = data.get('seed') % 3 + 3 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ shot __{{attacked}}__ with a magic missile for **{damage}** damage',
        }
        return out

    def attack3(self, data): 
        damage = data.get('seed') % 8 + 1 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ blasted __{{attacked}}__ with thunder wave for **{damage}** damage',
        }
        return out

    #Power 1
    def attack4(self, data): 
        damage = data.get('seed') % 7 + 5 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ burned __{{attacked}}__ with scorching rays for **{damage}** damage',
        }
        return out
    
    def attack5(self, data): 
        damage = data.get('seed') % 15 + 3 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ shattered __{{attacked}}__ for **{damage}** damage',
        }
        return out
        
    #Power 2
    def attack6(self, data): 
        damage = data.get('seed') % 8 + 15 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ exploded __{{attacked}}__ with a fireball for **{damage}** damage',
        }
        return out

    def attack7(self, data): 
        damage = data.get('seed') % 20 + 8 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ struck __{{attacked}}__ with a lightning for **{damage}** damage',
        }
        return out

    #Power3
    def attack8(self, data): 
        damage = data.get('seed') % 10 + 20 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ froze __{{attacked}}__ with a cone of cold for **{damage}** damage ❄️',
        }
        return out

    def attack9(self, data): 
        damage = data.get('seed') % 30 + 10 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ slapped __{{attacked}}__ with a giant hand for **{damage}** damage 🖐️',
        }
        return out


    attacks0 = RangeDict({
        range(0,1): attack1, #fizzle
        range(1,3): attack2, #magic missile
        range(3,5): attack3, #thunderwave
    })

    attacks1 = RangeDict({
        range(0,1): attack1, #fizzle
        range(1,3): attack4, #scorching rays
        range(3,5): attack5, #shatter
    })

    attacks2 = RangeDict({
        range(0,1): attack1, #fizzle
        range(1,3): attack6, #fireball
        range(3,5): attack7, #lightning bolt
    })

    attacks3 = RangeDict({
        range(0,1): attack1, #fizzle
        range(1,3): attack8, #cone of cold
        range(3,5): attack9, #bigsby's hand
    })

    def attack(self, data):
        turn = data.get('turn')
        if turn <= 1:
            return self.attack0(data)
        elif turn <= 3:
            return self.attacks0[data.get('seed') % 5](self, data)
        elif turn <= 6:
            return self.attacks1[data.get('seed') % 5](self, data)
        elif turn <= 9:
            return self.attacks2[data.get('seed') % 5](self, data)
        elif turn > 9:
            return self.attacks3[data.get('seed') % 5](self, data)

    def __init__(self):
        return

class Boomerang(Weapon):
    icon = '🪃'
    in_hand = True
    time_without = 1
    lost_messages = [ 
        '__{attacker}__ is looking for her boomerang',
        '__{attacker}__ can\'t find her boomerang',
        'WHERE IS __{attacker}__\'S BOOMERANG 😡',
    ]

    def attack0(self, data): 
        damage = data.get('seed') % 35 + 10 # range = (n), min = b, seed % (n + 1) + b
        out = {
            'damage': damage,
            'text': f'__{{attacker}}__ throws her boomerang at __{{attacked}}__ for **{damage}** damage',
        }
        self.in_hand = False
        return out

    def attack1(self, data):
        out = {
            'damage': 0,
        }
        if data.get('seed') % 4 + 1 <= self.time_without:
            out['text'] = '__{attacker}__ found her boomerang'
            self.in_hand = True
            self.time_without = 1
        else:
            out['text'] = self.lost_messages[(self.time_without - 1)]
            self.time_without += 1
        return out
        

    def attack(self, data):
        if self.in_hand:
            return self.attack0(data)
        else:
            return self.attack1(data)
    
    def __init__(self):
        return