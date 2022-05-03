classes = {
    'Fighter': {
        'Ability_Scores': ['Str', 'Con'],
        'Initiative': 'Dex_mod + 1',
        'AC': 10,  # + Con_mod/Dex_mod/Wis_mod
        'can_use_shield': True,
        'PD': 11,  # + Str_mod/Con_mod/Dex_mod
        'MD': 11,  # + Int_mod/Wis_mod/Cha_mod
        'HP': 8,  # + Con_mod) * 3
        'Recoveries': 8,
        'Recovery Dice': 'd10',  # + Con_mod
        'Basic Attacks': {
            'melee': {
                'Target': 'one enemy',
                'Attack': 'Str',  # + level
                'Defence': 'AC',
                'Hit': 'Str',  # + WEAPON
                'Miss': 1  # level
            },
            'ranged': {
                'Target': 'one enemy',
                'Attack': 'Dex',  # + level
                'Defence': 'AC',
                'Hit': 'Dex',  # + WEAPON
                'Miss': 0
            }
        },
        'Weapons': {
            'melee': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'club': {
                    'Category': 'small',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortsword': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'hand axe': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'spear': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d8'
                },
                'longsword': {
                    'Category': 'heavy',
                    'Handed': 'one',
                    'dice': '1d8'
                },
                'warhammer': {
                    'Category': 'heavy',
                    'Handed': 'one',
                    'dice': '1d8'
                },
                'greatsword': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10'
                },
                'greataxe': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10'
                }
            },
            'ranged': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'hand crossbow': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'javelin': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'axe': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'light crossbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'heavy crossbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8'
                },
                'longbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8'
                }
            }
        },
        'Armor': {
            'None': 10,
            'Light Armor': 13,
            'Heavy Armor': 15
        },
        'MPS': ["Brace for It", "Carve an Opening", "Deadly Assault", "Defensive Fighting", "Grim Intent",
                "Heavy Blows", "Precision Attack", "Second Shot", "Shield Bash", "Two Weapon Pressure"],  # choose 3
        'Talents': ["Cleave", "Comeback Strike", "Counter Attack", "Deadeye Archer", "Heavy Warrior", "Power Attack",
                    "Skilled Intercept", "Tough as Iron"],  # choose 3
        'Feats': ["Extra Tough", "Threatening", "Cleave", "Comeback Strike", "Counter Attack", "Deadeye Archer",
                  "Heavy Warrior", "Power Attack", "Skilled Intercept", "Tough as Iron", "Brace for It",
                  "Deadly Assault", "Defensive Fighting", "Precision Attack", "Shield Bash"],  # choose 1
        'Icon_Relationships': 3,
        'Backgrounds': {
            'points': 8,  # max 5 in any one background
            'list': ['swordmaster', 'mercenary captain', 'sea raider', 'shieldwall spearman', 'explorer', 'bouncer',
                     'thug', 'city guardsman', 'former gladiator', 'former orc captive', 'bankrupt nobleman', 'duelist',
                     'goblin-hunter']
        }
    },
    'Rogue': {
        'Ability_Scores': ['Dex', 'Cha'],
        'Initiative': 'Dex_mod + 1',
        'AC': 11,  # + Con_mod/Dex_mod/Wis_mod
        'can_use_shield': False,
        'PD': 13,  # + Str_mod/Con_mod/Dex_mod
        'MD': 11,  # + Int_mod/Wis_mod/Cha_mod
        'HP': 6,  # + Con_mod) * 3
        'Recoveries': 8,
        'Recovery Dice': 'd8',  # + Con_mod
        'Basic Attacks': {
            'melee': {
                'Target': 'one enemy',
                'Attack': 'Dex',  # + level
                'Defence': 'AC',
                'Hit': 'Dex',  # + WEAPON
                'Miss': 1  # level
            },
            'ranged': {
                'Target': 'one enemy',
                'Attack': 'Dex',  # + level
                'Defence': 'AC',
                'Hit': 'Dex',  # + WEAPON
                'Miss': 1  # level
            }
        },
        'Weapons': {
            'melee': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d8'
                },
                'club': {
                    'Category': 'small',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortsword': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d8'
                },
                'wicked knife': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d8'
                },
                'spear': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d8'
                },
                'longsword': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d8',
                    'malus': -2
                },
                'scimitar': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d8',
                    'malus': -2
                },
                'greatsword': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10',
                    'malus': -2
                }
            },
            'ranged': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'hand crossbow': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'javelin': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'axe': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'light crossbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'heavy crossbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -1
                },
                'longbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -2
                }
            }
        },
        'Armor': {
            'None': 11,
            'Light Armor': 12,
            'Heavy Armor': 13
        },
        'MPS': ["Evasive Strike", "Deadly thrust", "Flying Blade", "Roll with It", "Sure Cut", "Tumbling Strike"],  # choose 3
        'Talents': ["Cunning", "Improved Sneak Attack", "Murderous", "Shadow Walk", "Smooth Talk", "Swashbuckle", "Thievery", "Thumble"],  # choose 3
        'Feats': ["Sneak Attack", "Trap Sense", "Cunning", "Improved Sneak Attack", "Murderous", "Shadow Walk", "Smooth Talk", "Thievery", "Thumble", "Evasive Strike", "Deadly thrust", "Flying Blade", "Roll with It", "Sure Cut"],  # choose 1
        'Icon_Relationships': 3,
        'Backgrounds': {
            'points': 8,  # max 5 in any one background
            'list': ['street thug', 'cat burglar', 'diplomat', 'professional gambler', 'courtier', 'jewel thief',
                     'acrobat', 'con artist', 'bartender', 'spy master', 'pirate', 'dandy', 'rat catcher']
        }
    },
    'Cleric': {
        'Ability_Scores': ['Str', 'Wis'],
        'Initiative': 'Dex_mod + 1',
        'AC': 10,  # + Con_mod/Dex_mod/Wis_mod
        'can_use_shield': True,
        'PD': 12,  # + Str_mod/Con_mod/Dex_mod
        'MD': 12,  # + Int_mod/Wis_mod/Cha_mod
        'HP': 7,  # + Con_mod) * 3
        'Recoveries': 8,
        'Recovery Dice': 'd8',  # + Con_mod
        'Basic Attacks': {
            'melee': {
                'Target': 'one enemy',
                'Attack': 'Str',  # + level
                'Defence': 'AC',
                'Hit': 'Str',  # + WEAPON
                'Miss': 1  # level
            },
            'ranged': {
                'Target': 'one enemy',
                'Attack': 'Dex',  # + level
                'Defence': 'AC',
                'Hit': 'Dex',  # + WEAPON
                'Miss': 0
            }
        },
        'Weapons': {
            'melee': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'club': {
                    'Category': 'small',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortsword': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'mace': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'spear': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d8'
                },
                'longsword': {
                    'Category': 'heavy',
                    'Handed': 'one',
                    'dice': '1d8',
                    'malus': -2
                },
                'warhammer': {
                    'Category': 'heavy',
                    'Handed': 'one',
                    'dice': '1d8',
                    'malus': -2
                },
                'greatsword': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10',
                    'malus': -2
                },
                'dire flail': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10',
                    'malus': -2
                }
            },
            'ranged': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'hand crossbow': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'javelin': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'axe': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6'
                },
                'light crossbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6',
                    'malus': -2
                },
                'heavy crossbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -2
                },
                'longbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -2
                }
            }
        },
        'Armor': {
            'None': 10,
            'Light Armor': 12,
            'Heavy Armor': 14
        },
        'MPS': ['Bless', 'Cure Wounds', 'Hammer of Faith', 'Javelin of Faith', 'Shield of Faith',
                'Spirits of the Righteous', 'Turn Undead'],  # choose 3 + 'Heal'
        'Talents': ['Domain: Healing', 'Domain: Justice/Vengeance', 'Domain: Knowledge/Lore', 'Domain: Life/Death',
                    'Domain: Love/Beauty', 'Domain: Protection/Community', 'Domain: Strength',
                    'Domain: Sun/Anti-Undead', 'Domain: Trickery/Illusion', 'Domain: War/Leadership'],  # choose 3
        'Feats': ['Heal', 'Domain: Healing', 'Domain: Justice/Vengeance', 'Domain: Knowledge/Lore',
                  'Domain: Life/Death', 'Domain: Protection/Community', 'Domain: Strength', 'Domain: Sun/Anti-Undead',
                  'Domain: War/Leadership', 'Turn Undead'],  # choose 1
        'Icon_Relationships': 3,
        'Backgrounds': {
            'points': 8,  # max 5 in any one background
            'list': ['healer', 'archivist', 'military chaplain', 'temple guard', 'bartender', 'reformed thief',
                     'dwarven hierophant', 'initiate', 'bishop']
        }
    },
    'Wizard': {
        'Ability_Scores': ['Int', 'Wis'],
        'Initiative': 'Dex_mod + 1',
        'AC': 10,  # + Con_mod/Dex_mod/Wis_mod
        'can_use_shield': False,
        'PD': 11,  # + Str_mod/Con_mod/Dex_mod
        'MD': 13,  # + Int_mod/Wis_mod/Cha_mod
        'HP': 6,  # + Con_mod) * 3
        'Recoveries': 8,
        'Recovery Dice': 'd6',  # + Con_mod
        'Basic Attacks': {
            'melee': {
                'Target': 'one enemy',
                'Attack': 'Str',  # + level
                'Defence': 'AC',
                'Hit': 'Str',  # + WEAPON
                'Miss': 0
            },
            'ranged': {
                'Target': 'one enemy',
                'Attack': 'Dex',  # + level
                'Defence': 'AC',
                'Hit': 'Dex',  # + WEAPON
                'Miss': 0
            }
        },
        'Weapons': {
            'melee': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'staff': {
                    'Category': 'small',
                    'Handed': 'two',
                    'dice': '1d6'
                },
                'shortsword': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6',
                    'malus': -2
                },
                'spear': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -2
                },
                'longsword': {
                    'Category': 'heavy',
                    'Handed': 'one',
                    'dice': '1d8',
                    'malus': -5
                },
                'greatsword': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d10',
                    'malus': -5
                }
            },
            'ranged': {
                'dagger': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'hand crossbow': {
                    'Category': 'small',
                    'Handed': 'one',
                    'dice': '1d4'
                },
                'javelin': {
                    'Category': 'light',
                    'Handed': 'one',
                    'dice': '1d6',
                    'malus': -2
                },
                'light crossbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6',
                    'malus': -1
                },
                'shortbow': {
                    'Category': 'light',
                    'Handed': 'two',
                    'dice': '1d6',
                    'malus': -2
                },
                'heavy crossbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -4
                },
                'longbow': {
                    'Category': 'heavy',
                    'Handed': 'two',
                    'dice': '1d8',
                    'malus': -5
                }
            }
        },
        'Armor': {
            'None': 10,
            'Light Armor': 10,
            'Heavy Armor': 11
        },
        'MPS': ['Acid Arrow', 'Blur', 'Charm Person', 'Color Spray', 'Magic Missile', 'Ray of Frost', 'Shield',
                'Shocking Grasp'],  # choose 3
        'Talents': ['Abjuration', 'Cantrip Mastery', 'Evocation', 'High Arcana', 'Polysyllabic Verbalizations',
                    'Wizard’s Familiar'],  # choose 3
        'Feats': ['Abjuration', 'Cantrip Mastery', 'Color Spray', 'Magic Missile', 'Ray of Frost', 'Rebuke', 'Shield',
                  'Shocking Grasp', 'Wizard’s Familiar'],  # choose 1
        'Icon_Relationships': 3,
        'Backgrounds': {
            'points': 8,  # max 5 in any one background
            'list': ['magical prodigy', 'spell thief', 'hedge wizard', 'transformed familiar', 'ship’s wizard',
                     'royal poisoner']
        }
    }
}
