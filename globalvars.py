from imports import *

card_list = json.load(open("data/card_list.txt", 'r'))
card_list = {
    int(k): card_list[k]
    for k in card_list.keys() if card_list[k] != ''
}

dungeon_list = json.load(open("data/dungeons.txt", 'r'))

monster_list = json.load(open("data/mobs.txt", 'r'))

job_list = sorted([
    '-',
    'Alchimiste',
    'Bijoutier',
    'Bricoleur',
    'Bûcheron',
    'Chasseur',
    'Cordonnier',
    'Façonneur',
    'Forgeron',
    'Mineur',
    'Paysan',
    'Pêcheur',
    'Sculpteur',
    'Tailleur',
])

craft_list = json.load(open("data/crafts.txt", 'r'))

img_path = "cartes_temporis_resized/"
th = None
