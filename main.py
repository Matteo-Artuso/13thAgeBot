import logging
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from random import randint
import json
import Classes
import Races
import Token

# CONV HANDLERS STATES
# createPC
CLASS, ABILITYROLL, ABILITYASSIGN, ABILITYBONUS, MPS, TALENTS, FEAT, ONEUNIQUETHING, ICON, ICONRELATIONSHIPCHOICE, ICONRELATIONSHIPPOINT, ICONRELATIONSHIPSAVE, BACKGROUNDPOINTS, BACKGROUNDSASK = range(14)
# items
TYPE, WEAPON, WEAPONPICKUP, ARMOR, ARMORWEAR, ARMORNOWEAR, GENERIC = range(7)
# balance
AMOUNT, SAVE = range(2)
"""game players"""
number_of_players = 0
with open("players.json", 'r') as fp:
    players = json.load(fp)
"""create playable character"""
points_assign = {}
not_chosen = {}
# The Six Ability Scores
ability_scores = ['Str', 'Con', 'Dex', 'Int', 'Wis', 'Cha']
combat_stats = ['HP', 'Initiative', 'AC', 'can_use_shield', 'PD', 'MD', 'Recoveries', 'Recovery Dice']
ability_scores_assign = {}
ability_points = []
ability_points_backup = []
# Feats
general_feats = ['Further Backgrounding', 'Improved Initiative', 'Linguist', 'Precise Shot', 'Rapid Reload', 'Reach Tricks', 'Skill Escalation', 'Strong Recovery', 'Toughness']
# Icons
icons = ['the Archmage', 'the Crusader', 'the Diabolist', 'the Dwarf King', 'the Elf Queen', 'the Emperor',
         'the Great Gold Wyrm', 'the High Druid', 'the Lich King', 'the Orc Lord', 'the Priestess',
         'the Prince of Shadows', 'The Three']
icon_relationships = ['positive', 'conflicted', 'negative']
"""pickup"""
items_type = ['weapon', 'armor', 'shield', 'generic']
active_type = ['weapon', 'armor', 'shield']
"""balance"""
balance_type = ['platinum', 'gold', 'silver', 'copper']
mul = 1

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# UTILITY FUNCTIONS
# input: n_dice_to_roll"d"dice_type
# output: string with rolls
def roll(dice):
    rolls = []
    d_num = int(dice.split("d")[0])
    d_type = int(dice.split("d")[1])
    while d_num > 0:
        rolls.append(str(randint(1, d_type)))
        d_num -= 1
    return rolls


def list_custom_keyboard(list1):
    keyboard = []
    for item in list1:
        keyboard.append([item])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def ability_rolls():
    global ability_points
    total_rolls = "Here are your rolls:\n"
    i = 1
    while i <= 6:
        rolls = roll("4d6")
        total_rolls += f"Rolls #{i}: " + ", ".join(rolls)
        rolls.sort()
        points = 0
        j = 1
        while j < 4:
            points += int(rolls[j])
            j += 1
        total_rolls += f"\nPoints: {points}\n"
        ability_points.append(points)
        i += 1
    return total_rolls


def save_ability_points_choice(player_name, response):
    global ability_points, ability_scores_assign
    if response == 'RESET':
        ability_scores_assign[player_name] = []
        for ability in ability_scores:
            ability_scores_assign[player_name].append([ability])
        ability_scores_assign[player_name].append(['RESET'])
        ability_points = ability_points_backup.copy()
    else:
        players[player_name]['ability'][response] = ability_points[0]
        ability_scores_assign[player_name].remove([response])
        ability_points.pop(0)


def human_bonus_custom_keyboard(class_ability):
    keyboard = []
    for ability_class in class_ability:
        for ability_human in ability_scores:
            if ability_human not in class_ability:
                keyboard.append([f'{ability_class} + {ability_human}'])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def ability_bonus_custom_keyboard(choose_ability):
    keyboard = []
    for i in range(len(choose_ability)):
        for k in range(i + 1, len(choose_ability)):
            keyboard.append([f'{choose_ability[i]} + {choose_ability[k]}'])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def save_ability_bonus(player_name, ability_bonus_1, ability_bonus_2):
    players[player_name]['ability'][ability_bonus_1] = str(int(players[player_name]['ability'][ability_bonus_1]) + 2)
    players[player_name]['ability'][ability_bonus_2] = str(int(players[player_name]['ability'][ability_bonus_2]) + 2)


def show_final_ability_scores(player_name):
    final_ability_scores = ""
    for ability in ability_scores:
        final_ability_scores += ability + " = " + players[player_name]['ability'][ability] + "\n"
    return final_ability_scores


def ability_mod_calculator(player_name):
    players[player_name]['mod'] = {}
    for ability in ability_scores:
        players[player_name]['mod'][ability] = int((int(players[player_name]['ability'][ability]) - 10) / 2)


def combat_stats_calculator(player_name):
    players[player_name]['combat'] = {}
    player_class = players[player_name]['class']

    hp = Classes.classes[player_class]['HP']
    hp += players[player_name]['mod']['Con']
    hp = hp * 3
    players[player_name]['combat']['HP'] = {
        'MAX': hp,
        'current': hp
    }

    players[player_name]['combat']['Initiative'] = players[player_name]['mod']['Dex'] + 1

    ac = Classes.classes[player_class]['AC']
    mods = [players[player_name]['mod']['Con'], players[player_name]['mod']['Dex'], players[player_name]['mod']['Wis']]
    mods.sort()
    ac += mods[1] + 1
    players[player_name]['combat']['AC'] = ac

    players[player_name]['combat']['can_use_shield'] = Classes.classes[player_class]['can_use_shield']

    pd = Classes.classes[player_class]['PD']
    mods = [players[player_name]['mod']['Con'], players[player_name]['mod']['Dex'],
            players[player_name]['mod']['Str']]
    mods.sort()
    pd += mods[1] + 1
    players[player_name]['combat']['PD'] = pd

    md = Classes.classes[player_class]['MD']
    mods = [players[player_name]['mod']['Int'], players[player_name]['mod']['Cha'],
            players[player_name]['mod']['Wis']]
    mods.sort()
    md += mods[1] + 1
    players[player_name]['combat']['MD'] = md

    players[player_name]['combat']['Recoveries'] = Classes.classes[player_class]['Recoveries']

    players[player_name]['combat']['Recovery Dice'] = Classes.classes[player_class]['Recovery Dice']


def show_final_combat_scores(player_name):
    final_combat_scores = ""
    final_combat_scores += f"Max HP = {str(players[player_name]['combat']['HP']['MAX'])}\n"
    final_combat_scores += f"Current HP = {str(players[player_name]['combat']['HP']['current'])}\n"
    no_hp_stats = combat_stats.copy()
    no_hp_stats.remove('HP')
    for combat in no_hp_stats:
        final_combat_scores += combat + " = " + str(players[player_name]['combat'][combat]) + "\n"
    return final_combat_scores


def show(player_name, key):
    show_string = ""
    for i in players[player_name][key]:
        show_string += i + "\n"
    return show_string


def icon_relationship_custom_keyboard(icon):
    keyboard = []
    for relationship in icon_relationships:
        keyboard.append([f'{icon}: {relationship}'])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def icon_points_custom_keyboard(player_name, icon_chosen):
    keyboard = []
    for point in range(1, points_assign[player_name] + 1):
        keyboard.append([f'{icon_chosen[0]}: ' + str(point)])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def show_icons_relationships(player_name):
    icons_relationships = ""
    for icon in players[player_name]['IconRelationships'].keys():
        icons_relationships += icon + f": {players[player_name]['IconRelationships'][icon]['relationship_type']}, {players[player_name]['IconRelationships'][icon]['points']} points\n"
    return icons_relationships


def background_points_custom_keyboard(player_name, background_chosen):
    keyboard = []
    range_stop = min(points_assign[player_name], 5)
    for point in range(1, range_stop+1):
        keyboard.append([f'{background_chosen}: ' + str(point)])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def show_backgrounds(player_name):
    backgrounds_string = ""
    for background in players[player_name]['Backgrounds'].keys():
        backgrounds_string += background + f": {players[player_name]['Backgrounds'][background]} points\n"
    return backgrounds_string


def show_balance(player_name):
    balance_string = "BALANCE:\n"
    balance = players[player_name]['Balance']
    balance_string += f'platinum pieces: {str(int(balance/1000))}\n'
    balance = balance % 1000
    balance_string += f'gold pieces: {str(int(balance/100))}\n'
    balance = balance % 100
    balance_string += f'silver pieces: {str(int(balance/10))}\n'
    balance = balance % 10
    balance_string += f'copper pieces: {str(balance)}\n'
    return balance_string


# BOT HANDLERS FUNCTIONS
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}!")


def createPC(update: Update, context: CallbackContext):
    global number_of_players
    user = update.effective_user
    if user.name in players.keys():
        update.message.reply_text("Already created your character")
        return ConversationHandler.END
    update.message.reply_text("First time here! Let's build your character")
    # create character sheet as dict
    players[user.name] = {}
    number_of_players += 1
    print('number of players: ', number_of_players)
    # equipment initialize
    players[user.name]['Active'] = {
        'Weapon': '',
        'Armor': '',
        'shield': False
    }
    players[user.name]['Equipment'] = {
        'Weapon': {},
        'Armor': {},
        'shield': 0,
        'generic': {}
    }
    # Race
    reply_markup = list_custom_keyboard(Races.races.keys())
    update.message.reply_text("Choose a Race:", reply_markup=reply_markup)
    return CLASS


def Class(update: Update, context: CallbackContext):
    user = update.message.from_user
    race = update.message.text
    players[user.name]['race'] = race
    players[user.name]['small'] = Races.races[race]['small']
    print(players)
    # Class
    reply_markup = list_custom_keyboard(Classes.classes.keys())
    update.effective_message.reply_text("Choose a Class:", reply_markup=reply_markup)
    return ABILITYROLL


def AbilityRoll(update: Update, context: CallbackContext):
    user = update.message.from_user
    player_class = update.message.text
    players[user.name]['class'] = player_class
    players[user.name]['Basic Attacks'] = Classes.classes[player_class]['Basic Attacks']
    print(players)
    # Ability Rolls
    update.effective_message.reply_text("Now let's determine your Ability Scores. Roll 4d6 six times")
    update.effective_message.reply_text(f"#1 Roll 4d6", reply_markup=ReplyKeyboardMarkup([["ROLL"]], one_time_keyboard=True))
    return ABILITYASSIGN


def AbilityAssign(update: Update, context: CallbackContext):
    global ability_points, ability_points_backup
    user = update.message.from_user
    update.effective_message.reply_text(ability_rolls())
    # Ability Assign
    update.effective_message.reply_text("Ok now associate each point to an Ability")
    players[user.name]['ability'] = {}  # initialize ability dict
    ability_scores_assign[user.name] = []  # initialize ability assign
    for ability in ability_scores:
        ability_scores_assign[user.name].append([ability])
    ability_scores_assign[user.name].append(['RESET'])
    ability_points.sort(reverse=True)
    ability_points = [str(x) for x in ability_points]
    ability_points_backup = ability_points.copy()
    reply_markup = ReplyKeyboardMarkup(ability_scores_assign[user.name], one_time_keyboard=True)
    update.effective_message.reply_text("Your points: " + ", ".join(ability_points_backup) + f"\nAssign {ability_points[0]}", reply_markup=reply_markup)
    return ABILITYBONUS


def AbilityBonus(update: Update, context: CallbackContext):
    user = update.message.from_user
    save_ability_points_choice(user.name, update.message.text)
    if len(ability_points) > 0:
        reply_markup = ReplyKeyboardMarkup(ability_scores_assign[user.name], one_time_keyboard=True)
        update.effective_message.reply_text(
            "Your points: " + ", ".join(ability_points_backup) + f"\nAssign {ability_points[0]}",
            reply_markup=reply_markup)
        print(players)
        return ABILITYBONUS
    update.effective_message.reply_text("Points associated!")
    print(players)
    # +2 bonus
    chosen_class = players[user.name]['class']
    class_ability = Classes.classes[chosen_class]['Ability_Scores']
    chosen_race = players[user.name]['race']
    if chosen_race == 'Human':
        reply_markup = human_bonus_custom_keyboard(class_ability)
        update.effective_message.reply_text(
            "Since you are Human, your race allows you to choose any ability to a +2 increase.\nChoose one:",
            reply_markup=reply_markup)
    else:
        race_ability = Races.races[chosen_race]['Ability_Scores']
        choose_ability = race_ability + class_ability
        choose_ability = list(dict.fromkeys(choose_ability))
        reply_markup = ability_bonus_custom_keyboard(choose_ability)
        if len(choose_ability) == 2:
            update.effective_message.reply_text("Your race and class pair gives you just one +2 increase choice",
                                                reply_markup=reply_markup)
        else:
            update.effective_message.reply_text("Choose which abilities to give a +2 increase", reply_markup=reply_markup)
    return MPS


def Mps(update: Update, context: CallbackContext):
    user = update.message.from_user
    response = update.message.text.split(' + ')
    save_ability_bonus(user.name, response[0], response[1])
    update.effective_message.reply_text(f"Here are your final Ability Scores:\n{show_final_ability_scores(user.name)}")
    ability_mod_calculator(user.name)
    combat_stats_calculator(user.name)
    update.effective_message.reply_text(f"Here are your final Combat Stats:\n{show_final_combat_scores(user.name)}")
    # MPS
    player_class = players[user.name]['class']
    points_assign[user.name] = 3
    not_chosen[user.name] = Classes.classes[player_class]['MPS']
    reply_markup = list_custom_keyboard(not_chosen[user.name])
    players[user.name]['MPS'] = []
    if player_class == 'Cleric':
        players[user.name]['MPS'].append('Heal')
    update.effective_message.reply_text("Now determine your 3 Maneuvers/Powers/Spells")
    update.effective_message.reply_text("Choose a MPS to have:", reply_markup=reply_markup)
    return TALENTS


def Talents(update: Update, context: CallbackContext):
    user = update.effective_user
    mps = update.message.text
    players[user.name]['MPS'].append(mps)
    points_assign[user.name] -= 1
    print(players)
    if points_assign[user.name] > 0:
        update.effective_message.reply_text(f"You have this MPS:\n{mps}")
        not_chosen[user.name].remove(mps)
        reply_markup = list_custom_keyboard(not_chosen[user.name])
        update.effective_message.reply_text("Choose another MPS:", reply_markup=reply_markup)
        return TALENTS
    update.effective_message.reply_text(f"Here are your MPS:\n{show(user.name,'MPS')}", reply_markup=ReplyKeyboardRemove())
    # talents
    points_assign[user.name] = 3
    not_chosen[user.name] = Classes.classes[players[user.name]['class']]['Talents']
    reply_markup = list_custom_keyboard(not_chosen[user.name])
    players[user.name]['Talents'] = []
    update.effective_message.reply_text("Now determine your 3 Talents")
    update.effective_message.reply_text("Choose a Talent to have:", reply_markup=reply_markup)
    return FEAT


def Feat(update: Update, context: CallbackContext):
    user = update.effective_user
    talent = update.message.text
    players[user.name]['Talents'].append(talent)
    points_assign[user.name] -= 1
    print(players)
    if points_assign[user.name] > 0:
        update.effective_message.reply_text(f"You have this Talent:\n{talent}")
        not_chosen[user.name].remove(talent)
        reply_markup = list_custom_keyboard(not_chosen[user.name])
        update.effective_message.reply_text("Choose another Talent:", reply_markup=reply_markup)
        return FEAT
    update.effective_message.reply_text(f"Here are your Talents:\n{show(user.name,'Talents')}", reply_markup=ReplyKeyboardRemove())
    # feats
    not_chosen[user.name] = general_feats.copy()
    for feat in Classes.classes[players[user.name]['class']]['Feats']:
        if feat in players[user.name]['Talents']:
            not_chosen[user.name].append(feat)
        elif feat in players[user.name]['MPS']:
            not_chosen[user.name].append(feat)
    reply_markup = list_custom_keyboard(not_chosen[user.name])
    players[user.name]['Feats'] = []
    update.effective_message.reply_text("Now determine your Feat")
    update.effective_message.reply_text("Choose a Feat to have:", reply_markup=reply_markup)
    return ONEUNIQUETHING


def OneUniqueThing(update: Update, context: CallbackContext):
    user = update.effective_user
    players[user.name]['Feats'].append(update.message.text)
    print(players)
    update.effective_message.reply_text(f"Here is your Feat:\n{show(user.name, 'Feats')}", reply_markup=ReplyKeyboardRemove())
    # racial power
    players[user.name]['racial power'] = Races.races[players[user.name]['race']]['racial power']
    # One Unique Thing
    update.effective_message.reply_text("Now choose your One Unique Thing, please write it", reply_markup=ReplyKeyboardRemove())
    return ICON


def Icon(update: Update, context: CallbackContext):
    user = update.effective_user
    players[user.name]['OneUniqueThing'] = update.message.text
    update.effective_message.reply_text("One Unique Thing setted:")
    update.effective_message.reply_text(update.message.text)
    print(players)
    # icon relationships
    points_assign[user.name] = 3
    not_chosen[user.name] = icons.copy()
    reply_markup = list_custom_keyboard(not_chosen[user.name])
    players[user.name]['IconRelationships'] = {}
    update.effective_message.reply_text("Now determine your Icon Relationships")
    update.effective_message.reply_text("Choose an icon to have a Relationship with:", reply_markup=reply_markup)
    return ICONRELATIONSHIPCHOICE


def IconRelationshipChoice(update: Update, context: CallbackContext):
    user = update.effective_user
    response = update.message.text
    players[user.name]['IconRelationships'][response] = {}
    reply_markup = icon_relationship_custom_keyboard(response)
    update.effective_message.reply_text(f"Choose which type of relationship you want", reply_markup=reply_markup)
    return ICONRELATIONSHIPPOINT


def IconRelationshipPoint(update: Update, context: CallbackContext):
    user = update.effective_user
    icon_chosen = update.message.text.split(': ')
    players[user.name]['IconRelationships'][icon_chosen[0]]['relationship_type'] = icon_chosen[1]
    reply_markup = icon_points_custom_keyboard(user.name, icon_chosen)
    update.effective_message.reply_text(
        f"You have {points_assign[user.name]} points left. Choose how many points assign in your {icon_chosen[1]} Relationship with {icon_chosen[0]}",
        reply_markup=reply_markup)
    return ICONRELATIONSHIPSAVE


def IconRelationshipSave(update: Update, context: CallbackContext):
    user = update.effective_user
    icon_chosen = update.message.text.split(': ')
    players[user.name]['IconRelationships'][icon_chosen[0]]['points'] = icon_chosen[1]
    points_assign[user.name] -= int(icon_chosen[1])
    print(players)
    if points_assign[user.name] > 0:
        update.effective_message.reply_text(f"You have this relationship:\n{show_icons_relationships(user.name)}")
        not_chosen[user.name].remove(icon_chosen[0])
        reply_markup = list_custom_keyboard(not_chosen[user.name])
        update.effective_message.reply_text("Choose another icon to have a Relationship with:", reply_markup=reply_markup)
        return ICONRELATIONSHIPCHOICE
    update.effective_message.reply_text(f"Here are your Icons Relationships:\n{show_icons_relationships(user.name)}")
    # background
    points_assign[user.name] = Classes.classes[players[user.name]['class']]['Backgrounds']['points']
    not_chosen[user.name] = Classes.classes[players[user.name]['class']]['Backgrounds']['list']
    if 'Further Backgrounding' in players[user.name]['Feats']:
        points_assign[user.name] += 2
    reply_markup = list_custom_keyboard(not_chosen[user.name])
    players[user.name]['Backgrounds'] = {}
    update.effective_message.reply_text("Now determine your Backgrounds")
    update.effective_message.reply_text("Choose a Background to have:", reply_markup=reply_markup)
    return BACKGROUNDPOINTS


def BackgroundPoints(update: Update, context: CallbackContext):
    user = update.effective_user
    background_chosen = update.message.text
    reply_markup = background_points_custom_keyboard(user.name, background_chosen)
    update.effective_message.reply_text(
        f"You have {points_assign[user.name]} points left. Choose how many points assign to {background_chosen}",
        reply_markup=reply_markup)
    return BACKGROUNDSASK


def BackgroundsAsk(update: Update, context: CallbackContext):
    user = update.effective_user
    background = update.message.text.split(': ')
    players[user.name]['Backgrounds'][background[0]] = background[1]
    points_assign[user.name] -= int(background[1])
    print(players)
    if points_assign[user.name] > 0:
        update.effective_message.reply_text(f"You have this background:\n{show_backgrounds(user.name)}")
        not_chosen[user.name].remove(background[0])
        reply_markup = list_custom_keyboard(not_chosen[user.name])
        update.effective_message.reply_text("Choose another Background to have:", reply_markup=reply_markup)
        return BACKGROUNDPOINTS
    update.effective_message.reply_text(f"Here are your backgrounds:\n{show_backgrounds(user.name)}", reply_markup=ReplyKeyboardRemove())
    # gold
    players[user.name]['Balance'] = 2500
    update.effective_message.reply_text(show_balance(user.name))
    update.effective_message.reply_text("Your character  is completed!")
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def Roll(update: Update, context: CallbackContext):
    update.message.reply_text("Write how many and which dice do you want to roll in dice notation")
    return AMOUNT


def RollResult(update: Update, context: CallbackContext):
    try:
        rolls = roll(update.message.text)
    except:
        update.message.reply_text("Write in dice notation")
        return AMOUNT
    tot = 0
    for i in rolls:
        tot += int(i)
    if len(rolls) > 1:
        update.message.reply_text('rolls: ' + ', '.join(rolls) + f'\ntot: {tot}')
    else:
        update.message.reply_text(f'roll: {tot}')
    return ConversationHandler.END


def Pickup(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(items_type)
    update.message.reply_text("What do you want to pick up?", reply_markup=reply_markup)
    return TYPE


def PickupType(update: Update, context: CallbackContext):
    user = update.effective_user
    object_type = update.message.text
    if object_type == 'weapon':
        update.message.reply_text("Is it melee or ranged?", reply_markup=ReplyKeyboardMarkup([["melee"],["ranged"]], one_time_keyboard=True))
        return WEAPON
    if object_type == 'armor':
        update.message.reply_text("Do you want to wear it?", reply_markup=ReplyKeyboardMarkup([["yes"],["no"]], one_time_keyboard=True))
        return ARMOR
    if object_type == 'shield':
        if object_type in players[user.name]['Equipment'].keys():
            players[user.name]['Equipment'][object_type] += 1
        else:
            players[user.name]['Equipment'][object_type] = 1
        update.effective_message.reply_text(f"shield picked up (tot: {players[user.name]['Equipment'][object_type]})", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END
    if object_type == 'generic':
        update.message.reply_text("Please write it", reply_markup=ReplyKeyboardRemove())
        return GENERIC


def WeaponChoice(update: Update, context: CallbackContext):
    user = update.effective_user
    weapon_type = update.message.text
    reply_markup = list_custom_keyboard(Classes.classes[players[user.name]['class']]['Weapons'][weapon_type].keys())
    update.message.reply_text("What weapon is?", reply_markup=reply_markup)
    return WEAPONPICKUP


def WeaponPickup(update: Update, context: CallbackContext):
    user = update.effective_user
    weapon = update.message.text
    if weapon in players[user.name]['Equipment']['Weapon'].keys():
        players[user.name]['Equipment']['Weapon'][weapon] += 1
    else:
        players[user.name]['Equipment']['Weapon'][weapon] = 1
    update.effective_message.reply_text(f"{weapon} picked up (tot: {players[user.name]['Equipment']['Weapon'][weapon]})", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def ArmorPickup(update: Update, context: CallbackContext):
    wear = update.message.text
    update.message.reply_text("What kind of armor is?", reply_markup=ReplyKeyboardMarkup([["Light Armor"], ["Heavy Armor"]], one_time_keyboard=True))
    if wear == 'no':
        return ARMORNOWEAR
    return ARMORWEAR


def ArmorPickupWear(update: Update, context: CallbackContext):
    user = update.effective_user
    armor_type = update.message.text
    # recalculate AC
    ac = Classes.classes[players[user.name]['class']]['Armor'][armor_type]
    mods = [players[user.name]['mod']['Con'], players[user.name]['mod']['Dex'], players[user.name]['mod']['Wis']]
    mods.sort()
    ac += mods[1] + 1
    players[user.name]['combat']['AC'] = ac
    if len(players[user.name]['Active']['Armor']) == 0:
        players[user.name]['Active']['Armor'] = armor_type
        update.effective_message.reply_text(f"{armor_type} picked up and wore, new AC: {ac}", reply_markup=ReplyKeyboardRemove())
    else:
        old_armor = players[user.name]['Active']['Armor']
        if old_armor in players[user.name]['Equipment']['Armor'].keys():
            players[user.name]['Equipment']['Armor'][old_armor] += 1
        else:
            players[user.name]['Equipment']['Armor'][old_armor] = 1
        players[user.name]['Active']['Armor'] = armor_type
        update.effective_message.reply_text(f"{armor_type} picked up and wore, new AC: {ac}\n{old_armor} putted in equipment", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def ArmorPickupNoWear(update: Update, context: CallbackContext):
    user = update.effective_user
    armor_type = update.message.text
    if armor_type in players[user.name]['Equipment']['Armor'].keys():
        players[user.name]['Equipment']['Armor'][armor_type] += 1
    else:
        players[user.name]['Equipment']['Armor'][armor_type] = 1
    update.effective_message.reply_text(f"{armor_type} picked up (tot: {players[user.name]['Equipment']['Armor'][armor_type]}) and not wore", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def GenericPickup(update: Update, context: CallbackContext):
    user = update.effective_user
    item = update.message.text
    if item in players[user.name]['Equipment']['generic'].keys():
        players[user.name]['Equipment']['generic'][item] += 1
    else:
        players[user.name]['Equipment']['generic'][item] = 1
    update.effective_message.reply_text(f"{item} picked up (tot: {players[user.name]['Equipment']['generic'][item]})", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def Drop(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(items_type)
    update.message.reply_text("What do you want to drop?", reply_markup=reply_markup)
    return TYPE


def DropType(update: Update, context: CallbackContext):
    user = update.effective_user
    object_type = update.message.text
    if object_type == 'weapon':
        if len(players[user.name]['Equipment']['Weapon']) == 0:
            update.message.reply_text("You don't have any weapon to drop (can't drop equipped items)", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        reply_markup = list_custom_keyboard(players[user.name]['Equipment']['Weapon'].keys())
        update.message.reply_text("Select a weapon to drop", reply_markup=reply_markup)
        return WEAPON
    if object_type == 'armor':
        if len(players[user.name]['Equipment']['Armor']) == 0:
            update.message.reply_text("You don't have any armor to drop (can't drop equipped items)", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        reply_markup = list_custom_keyboard(players[user.name]['Equipment']['Armor'].keys())
        update.message.reply_text("Select an armor to drop", reply_markup=reply_markup)
        return ARMOR
    if object_type == 'shield':
        if players[user.name]['Equipment'][object_type] == 0:
            update.effective_message.reply_text("You don't have any shield to drop (can't drop equipped items)", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        players[user.name]['Equipment'][object_type] -= 1
        if players[user.name]['Equipment'][object_type] == 0:
            update.effective_message.reply_text("shield dropped (none left)", reply_markup=ReplyKeyboardRemove())
        else:
            update.effective_message.reply_text(f"shield dropped (tot left: {players[user.name]['Equipment'][object_type]})", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END
    if object_type == 'generic':
        if len(players[user.name]['Equipment']['generic']) == 0:
            update.message.reply_text("You don't have any generic item", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        reply_markup = list_custom_keyboard(players[user.name]['Equipment']['generic'].keys())
        update.message.reply_text("Select an item to drop", reply_markup=reply_markup)
        return GENERIC


def WeaponDrop(update: Update, context: CallbackContext):
    user = update.effective_user
    weapon = update.message.text
    if players[user.name]['Equipment']['Weapon'][weapon] == 1:
        del players[user.name]['Equipment']['Weapon'][weapon]
        update.effective_message.reply_text(f"{weapon} dropped (none left)", reply_markup=ReplyKeyboardRemove())
    else:
        players[user.name]['Equipment']['Weapon'][weapon] -= 1
        update.effective_message.reply_text(f"{weapon} dropped (tot left: {players[user.name]['Equipment']['Weapon'][weapon]})", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def ArmorDrop(update: Update, context: CallbackContext):
    user = update.effective_user
    armor = update.message.text
    if players[user.name]['Equipment']['Armor'][armor] == 1:
        del players[user.name]['Equipment']['Armor'][armor]
        update.effective_message.reply_text(f"{armor} dropped (none left)", reply_markup=ReplyKeyboardRemove())
    else:
        players[user.name]['Equipment']['Armor'][armor] -= 1
        update.effective_message.reply_text(f"{armor} dropped (tot left: {players[user.name]['Equipment']['Armor'][armor]})", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def GenericDrop(update: Update, context: CallbackContext):
    user = update.effective_user
    item = update.message.text
    if players[user.name]['Equipment']['generic'][item] == 1:
        del players[user.name]['Equipment']['generic'][item]
        update.effective_message.reply_text(f"{item} dropped (none left)", reply_markup=ReplyKeyboardRemove())
    else:
        players[user.name]['Equipment']['generic'][item] -= 1
        update.effective_message.reply_text(f"{item} dropped (tot left: {players[user.name]['Equipment']['generic'][item]})", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def Equip(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(active_type)
    update.message.reply_text("What do you want to equip?", reply_markup=reply_markup)
    return TYPE


def EquipType(update: Update, context: CallbackContext):
    user = update.effective_user
    object_type = update.message.text
    if object_type == 'weapon':
        if len(players[user.name]['Equipment']['Weapon']) == 0:
            update.message.reply_text("You don't have any weapon to equip", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        reply_markup = list_custom_keyboard(players[user.name]['Equipment']['Weapon'].keys())
        update.message.reply_text("Select a weapon to equip", reply_markup=reply_markup)
        return WEAPON
    if object_type == 'armor':
        if len(players[user.name]['Equipment']['Armor']) == 0:
            update.message.reply_text("You don't have any armor to equip", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        reply_markup = list_custom_keyboard(players[user.name]['Equipment']['Armor'].keys())
        update.message.reply_text("Select an armor to equip", reply_markup=reply_markup)
        return ARMOR
    if object_type == 'shield':
        if players[user.name]['Active'][object_type]:
            update.effective_message.reply_text("Shield already equipped", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        if players[user.name]['Equipment'][object_type] == 0:
            update.effective_message.reply_text("You don't have any shield to equip", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        players[user.name]['Equipment'][object_type] -= 1
        players[user.name]['Active'][object_type] = True
        players[user.name]['combat']['AC'] += 1
        update.effective_message.reply_text(f"shield equipped, new AC: {players[user.name]['combat']['AC']}", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END


def EquipWeapon(update: Update, context: CallbackContext):
    user = update.effective_user
    weapon = update.message.text
    old_weapon = players[user.name]['Active']['Weapon']
    if weapon == old_weapon:
        update.effective_message.reply_text(f"{weapon} already equipped", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    # add new to Active
    players[user.name]['Active']['Weapon'] = weapon
    if players[user.name]['Equipment']['Weapon'][weapon] == 1:
        del players[user.name]['Equipment']['Weapon'][weapon]
    else:
        players[user.name]['Equipment']['Weapon'][weapon] -= 1
    if old_weapon != '':
        # add old in Equipment
        if old_weapon in players[user.name]['Equipment']['Weapon'].keys():
            players[user.name]['Equipment']['Weapon'][old_weapon] += 1
        else:
            players[user.name]['Equipment']['Weapon'][old_weapon] = 1
        update.effective_message.reply_text(f"{weapon} equipped, {old_weapon} putted in equipment", reply_markup=ReplyKeyboardRemove())
    else:
        update.effective_message.reply_text(f"{weapon} equipped", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def EquipArmor(update: Update, context: CallbackContext):
    user = update.effective_user
    armor = update.message.text
    old_armor = players[user.name]['Active']['Armor']
    if armor == old_armor:
        update.effective_message.reply_text(f"{armor} already equipped", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    # recalculate AC
    ac = Classes.classes[players[user.name]['class']]['Armor'][armor]
    mods = [players[user.name]['mod']['Con'], players[user.name]['mod']['Dex'], players[user.name]['mod']['Wis']]
    mods.sort()
    ac += mods[1] + 1
    players[user.name]['combat']['AC'] = ac
    # add new to Active
    players[user.name]['Active']['Armor'] = armor
    if players[user.name]['Equipment']['Armor'][armor] == 1:
        del players[user.name]['Equipment']['Armor'][armor]
    else:
        players[user.name]['Equipment']['Armor'][armor] -= 1
    if old_armor != '':
        # add old in Equipment
        if old_armor in players[user.name]['Equipment']['Armor'].keys():
            players[user.name]['Equipment']['Armor'][old_armor] += 1
        else:
            players[user.name]['Equipment']['Armor'][old_armor] = 1
        update.effective_message.reply_text(f"{armor} equipped, new AC: {ac}\n{old_armor} putted in equipment", reply_markup=ReplyKeyboardRemove())
    else:
        update.effective_message.reply_text(f"{armor} equipped, new AC: {ac}", reply_markup=ReplyKeyboardRemove())
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def Unequip(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(active_type)
    update.message.reply_text("What do you want to unequip?", reply_markup=reply_markup)
    return TYPE


def UnequipType(update: Update, context: CallbackContext):
    user = update.effective_user
    object_type = update.message.text
    if object_type == 'weapon':
        if len(players[user.name]['Active']['Weapon']) == 0:
            update.message.reply_text("You don't have any equipped weapon", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        weapon = players[user.name]['Active']['Weapon']
        if weapon in players[user.name]['Equipment']['Weapon'].keys():
            players[user.name]['Equipment']['Weapon'][weapon] += 1
        else:
            players[user.name]['Equipment']['Weapon'][weapon] = 1
        players[user.name]['Active']['Weapon'] = ''
        update.effective_message.reply_text(f"{weapon} unequipped and putted in equipment", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END
    if object_type == 'armor':
        # recalculate AC
        ac = Classes.classes[players[user.name]['class']]['Armor']['None']
        mods = [players[user.name]['mod']['Con'], players[user.name]['mod']['Dex'], players[user.name]['mod']['Wis']]
        mods.sort()
        ac += mods[1] + 1
        players[user.name]['combat']['AC'] = ac
        if len(players[user.name]['Equipment']['Armor']) == 0:
            update.message.reply_text("You don't have any equipped armor", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        armor = players[user.name]['Active']['Armor']
        if armor in players[user.name]['Equipment']['Armor'].keys():
            players[user.name]['Equipment']['Armor'][armor] += 1
        else:
            players[user.name]['Equipment']['Armor'][armor] = 1
        players[user.name]['Active']['Armor'] = ''
        update.effective_message.reply_text(f"{armor} unequipped and putted in equipment, new AC: {ac}", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END
    if object_type == 'shield':
        if not players[user.name]['Active']['shield']:
            update.effective_message.reply_text("You don't have any equipped shield", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        players[user.name]['Equipment'][object_type] += 1
        players[user.name]['Active'][object_type] = False
        players[user.name]['combat']['AC'] -= 1
        update.effective_message.reply_text(f"shield unequipped and putted in equipment, new AC: {players[user.name]['combat']['AC']}", reply_markup=ReplyKeyboardRemove())
        print(players)
        with open("players.json", 'w') as f:
            json.dump(players, f, indent=4)
        return ConversationHandler.END


def Cash(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(balance_type)
    update.message.reply_text("Which piece do you want to cash?", reply_markup=reply_markup)
    return AMOUNT


def Amount(update: Update, context: CallbackContext):
    global mul
    piece = update.message.text
    if piece == 'platinum':
        mul = 1000
    elif piece == 'gold':
        mul = 100
    elif piece == 'silver':
        mul = 10
    elif piece == 'copper':
        mul = 1
    else:
        update.message.reply_text("Use custom keyboard")
        return AMOUNT
    update.message.reply_text("Insert the amount", reply_markup=ReplyKeyboardRemove())
    return SAVE


def CashSave(update: Update, context: CallbackContext):
    user = update.effective_user
    try:
        amount = int(update.message.text)
    except:
        update.message.reply_text("Insert the amount as int")
        return SAVE
    players[user.name]['Balance'] += amount * mul
    update.message.reply_text(show_balance(user.name))
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def Spend(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    reply_markup = list_custom_keyboard(balance_type)
    update.message.reply_text("Which piece do you want to spend?", reply_markup=reply_markup)
    return AMOUNT


def SpendSave(update: Update, context: CallbackContext):
    user = update.effective_user
    try:
        amount = int(update.message.text)
    except:
        update.message.reply_text("Insert the amount as int")
        return SAVE
    players[user.name]['Balance'] -= amount * mul
    update.message.reply_text(show_balance(user.name))
    print(players)
    with open("players.json", 'w') as f:
        json.dump(players, f, indent=4)
    return ConversationHandler.END


def ShowBasicAttacks(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    weapon = players[user.name]['Active']['Weapon']
    basic_attacks_string = 'BASIC ATTACKS\n'
    basic_attacks_string += 'MELEE:\n'
    basic_attacks_string += f"Target: {players[user.name]['Basic Attacks']['melee']['Target']}\n"
    if weapon != '' and weapon in Classes.classes[players[user.name]['class']]['Weapons']['melee']:
        if 'malus' in Classes.classes[players[user.name]['class']]['Weapons']['melee'][weapon].keys():
            basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['melee']['Attack']]} + 1 {Classes.classes[players[user.name]['class']]['Weapons']['melee'][weapon]['malus']} vs. {players[user.name]['Basic Attacks']['melee']['Defence']}\n"
        else:
            basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['melee']['Attack']]} + 1 vs. {players[user.name]['Basic Attacks']['melee']['Defence']}\n"
        basic_attacks_string += f"Hit: {Classes.classes[players[user.name]['class']]['Weapons']['melee'][weapon]['dice']} + {players[user.name]['mod'][players[user.name]['Basic Attacks']['melee']['Hit']]}\n"
    else:
        basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['melee']['Attack']]} + 1 vs. {players[user.name]['Basic Attacks']['melee']['Defence']}\n"
        basic_attacks_string += f"Hit: {players[user.name]['mod'][players[user.name]['Basic Attacks']['melee']['Hit']]}\n"
    basic_attacks_string += f"Miss: {players[user.name]['Basic Attacks']['melee']['Miss']}\n"
    basic_attacks_string += 'RANGED:\n'
    basic_attacks_string += f"Target: {players[user.name]['Basic Attacks']['ranged']['Target']}\n"
    if weapon != '' and weapon in Classes.classes[players[user.name]['class']]['Weapons']['ranged']:
        if 'malus' in Classes.classes[players[user.name]['class']]['Weapons']['ranged'][weapon].keys():
            basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['ranged']['Attack']]} + 1 {Classes.classes[players[user.name]['class']]['Weapons']['ranged'][weapon]['malus']} vs. {players[user.name]['Basic Attacks']['ranged']['Defence']}\n"
        else:
            basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['ranged']['Attack']]} + 1 vs. {players[user.name]['Basic Attacks']['ranged']['Defence']}\n"
        basic_attacks_string += f"Hit: {Classes.classes[players[user.name]['class']]['Weapons']['ranged'][weapon]['dice']} + {players[user.name]['mod'][players[user.name]['Basic Attacks']['ranged']['Hit']]}\n"
    else:
        basic_attacks_string += f"Attack: 1d20 + {players[user.name]['mod'][players[user.name]['Basic Attacks']['ranged']['Attack']]} + 1 vs. {players[user.name]['Basic Attacks']['ranged']['Defence']}\n"
        basic_attacks_string += f"Hit: {players[user.name]['mod'][players[user.name]['Basic Attacks']['ranged']['Hit']]}\n"
    basic_attacks_string += f"Miss: {players[user.name]['Basic Attacks']['ranged']['Miss']}\n"
    update.effective_message.reply_text(basic_attacks_string)


def ShowMPS(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    update.effective_message.reply_text('\n'.join(players[user.name]['MPS']))


def ShowTalents(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    update.effective_message.reply_text('\n'.join(players[user.name]['Talents']))


def ShowFeat(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    update.effective_message.reply_text('\n'.join(players[user.name]['Feats']))


def ShowRacialPower(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    update.effective_message.reply_text(players[user.name]['racial power'])


def ShowEquipment(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    equipment = "WEAPON:\n"
    if len(players[user.name]['Equipment']['Weapon']) == 0:
        equipment += "none\n"
    else:
        for key, value in players[user.name]['Equipment']['Weapon'].items():
            equipment += f"{value} {key}\n"
    equipment += "ARMOR:\n"
    if len(players[user.name]['Equipment']['Armor']) == 0:
        equipment += "none\n"
    else:
        for key, value in players[user.name]['Equipment']['Armor'].items():
            equipment += f"{value} {key}\n"
    if players[user.name]['Equipment']['shield'] != 0:
        equipment += f"{players[user.name]['Equipment']['shield']} shield\n"
    equipment += "GENERIC:\n"
    if len(players[user.name]['Equipment']['generic']) == 0:
        equipment += "none\n"
    else:
        for key, value in players[user.name]['Equipment']['generic'].items():
            equipment += f"{value} {key}\n"
    update.effective_message.reply_text(equipment)


def ShowActive(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    if players[user.name]['Active']['Weapon'] != '':
        equipment = f"{players[user.name]['Active']['Weapon']}\n"
    else:
        equipment = "no weapon\n"
    if players[user.name]['Active']['Armor'] != '':
        equipment += f"{players[user.name]['Active']['Armor']}\n"
    else:
        equipment += "no armor\n"
    if players[user.name]['Active']['shield']:
        equipment += "shield"
    else:
        equipment += "no shield"
    update.effective_message.reply_text(equipment)


def ShowBalance(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name not in players.keys():
        update.message.reply_text("Create your character first")
        return ConversationHandler.END
    update.effective_message.reply_text(show_balance(user.name))


# unused function but necessary as fallback
def error(update: Update, context: CallbackContext):
    update.effective_message.reply_text("ERROR")
    return ConversationHandler.END


### START ###
# Create the Updater and pass it your bot token.
updater = Updater(Token.token)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# handlers
create_pc_handler = ConversationHandler(
    entry_points=[CommandHandler("create_pc", createPC)],
    states={
        CLASS: [MessageHandler(Filters.text, Class)],
        ABILITYROLL: [MessageHandler(Filters.text, AbilityRoll)],
        ABILITYASSIGN: [MessageHandler(Filters.text, AbilityAssign)],
        ABILITYBONUS: [MessageHandler(Filters.text, AbilityBonus)],
        MPS: [MessageHandler(Filters.text, Mps)],     # Maneuvers, Powers, Spells
        TALENTS: [MessageHandler(Filters.text, Talents)],
        FEAT: [MessageHandler(Filters.text, Feat)],
        ONEUNIQUETHING: [MessageHandler(Filters.text, OneUniqueThing)],
        ICON: [MessageHandler(Filters.text, Icon)],
        ICONRELATIONSHIPCHOICE: [MessageHandler(Filters.text, IconRelationshipChoice)],
        ICONRELATIONSHIPPOINT: [MessageHandler(Filters.text, IconRelationshipPoint)],
        ICONRELATIONSHIPSAVE: [MessageHandler(Filters.text, IconRelationshipSave)],
        BACKGROUNDPOINTS: [MessageHandler(Filters.text, BackgroundPoints)],
        BACKGROUNDSASK: [MessageHandler(Filters.text, BackgroundsAsk)]
    },
    fallbacks=[CommandHandler('stop', error)]
)
roll_handler = ConversationHandler(
    entry_points=[CommandHandler("roll", Roll)],
    states={
        AMOUNT: [MessageHandler(Filters.text, RollResult)],
    },
    fallbacks=[CommandHandler('stop', error)]
)
pickup_handler = ConversationHandler(
    entry_points=[CommandHandler("pickup", Pickup)],
    states={
        TYPE: [MessageHandler(Filters.text, PickupType)],
        WEAPON: [MessageHandler(Filters.text, WeaponChoice)],
        WEAPONPICKUP: [MessageHandler(Filters.text, WeaponPickup)],
        ARMOR: [MessageHandler(Filters.text, ArmorPickup)],
        ARMORWEAR: [MessageHandler(Filters.text, ArmorPickupWear)],
        ARMORNOWEAR: [MessageHandler(Filters.text, ArmorPickupNoWear)],
        GENERIC: [MessageHandler(Filters.text, GenericPickup)]
    },
    fallbacks=[CommandHandler('stop', error)]
)
drop_handler = ConversationHandler(
    entry_points=[CommandHandler("drop", Drop)],
    states={
        TYPE: [MessageHandler(Filters.text, DropType)],
        WEAPON: [MessageHandler(Filters.text, WeaponDrop)],
        ARMOR: [MessageHandler(Filters.text, ArmorDrop)],
        GENERIC: [MessageHandler(Filters.text, GenericDrop)]
    },
    fallbacks=[CommandHandler('stop', error)]
)
equip_handler = ConversationHandler(
    entry_points=[CommandHandler("equip", Equip)],
    states={
        TYPE: [MessageHandler(Filters.text, EquipType)],
        WEAPON: [MessageHandler(Filters.text, EquipWeapon)],
        ARMOR: [MessageHandler(Filters.text, EquipArmor)]
    },
    fallbacks=[CommandHandler('stop', error)]
)
unequip_handler = ConversationHandler(
    entry_points=[CommandHandler("unequip", Unequip)],
    states={
        TYPE: [MessageHandler(Filters.text, UnequipType)],
    },
    fallbacks=[CommandHandler('stop', error)]
)
cash_handler = ConversationHandler(
    entry_points=[CommandHandler("cash", Cash)],
    states={
        AMOUNT: [MessageHandler(Filters.text, Amount)],
        SAVE: [MessageHandler(Filters.text, CashSave)],
    },
    fallbacks=[CommandHandler('stop', error)]
)
spend_handler = ConversationHandler(
    entry_points=[CommandHandler("spend", Spend)],
    states={
        AMOUNT: [MessageHandler(Filters.text, Amount)],
        SAVE: [MessageHandler(Filters.text, SpendSave)],
    },
    fallbacks=[CommandHandler('stop', error)]
)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(create_pc_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(pickup_handler)
dispatcher.add_handler(drop_handler)
dispatcher.add_handler(equip_handler)
dispatcher.add_handler(unequip_handler)
dispatcher.add_handler(cash_handler)
dispatcher.add_handler(spend_handler)
dispatcher.add_handler(CommandHandler("show_basic_attacks", ShowBasicAttacks))
dispatcher.add_handler(CommandHandler("show_mps", ShowMPS))
dispatcher.add_handler(CommandHandler("show_talents", ShowTalents))
dispatcher.add_handler(CommandHandler("show_feat", ShowFeat))
dispatcher.add_handler(CommandHandler("show_racial_power", ShowRacialPower))
dispatcher.add_handler(CommandHandler("show_equipment", ShowEquipment))
dispatcher.add_handler(CommandHandler("show_equipped", ShowActive))
dispatcher.add_handler(CommandHandler("show_balance", ShowBalance))


# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
