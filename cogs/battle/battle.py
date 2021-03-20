import re

from cogs.battle import weapons

#emotes are the key, emote names are the value
weapon_choice = {
    '🗡️': weapons.Dagger, #:dagger:
    '🔫': weapons.Gun, #:gun:
    # '🤜': weapons.Fists, #:right_fist:
    '💣': weapons.Bomb, #:bomb:
    '⚔️': weapons.Swords, #:crossed_swords:
    '🪄': weapons.Magic, #:magic_wand:
    '🪃': weapons.Boomerang, #:boomerang:
}

colors = {
    0: {
        'heart': '❤️',
        'circle': '🔴',
        'color': 0xff6464,
    },
    1: {
        'heart': '💙',
        'circle': '🔵',
        'color': 0x64b4ff,
    },
}

def text_handler(self, text, desc):
    i = 0
    start = None
    for m in re.finditer('\n', desc):
        if i == 0:
            start = m.end()
        i = i + 1

    if i >= 5:
        desc = desc[start:]

    return f'{desc}{text}\n'
