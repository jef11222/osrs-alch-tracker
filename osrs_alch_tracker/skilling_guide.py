"""
OSRS Skilling & Level Training Guide Database.
Provides structured level brackets, quest skips, and training recipes with live market rate evaluation
for Smithing, Fletching, Crafting, and Magic.
"""

def get_xp_for_level(lvl):
    """Calculates exact official OSRS XP required for a given level (1-99+)."""
    if lvl <= 1:
        return 0
    total = 0
    for i in range(1, lvl):
        total += int(i + 300.0 * (2.0 ** (i / 7.0)))
    return total // 4

def get_level_for_xp(xp):
    """Calculates the current OSRS level corresponding to an XP amount."""
    if xp <= 0:
        return 1
    for lvl in range(1, 127):
        if get_xp_for_level(lvl + 1) > xp:
            return lvl
    return 126

SKILLING_GUIDES = {
    "Smithing": {
        "icon": "\u2692\ufe0f",
        "quests": [
            {
                "name": "The Knight's Sword",
                "members": False,
                "xp": 12725,
                "skip": "Skips Level 1 \u2794 29 instantly! (12,725 XP)",
                "reqs": "10 Mining, Redberry pie, 2 Iron bars",
                "wiki_slug": "The_Knight's_Sword",
                "tip": "Crucial 20-minute F2P quest. Skips the entire slow Bronze and Iron grind for free."
            },
            {
                "name": "Sleeping Giants",
                "members": True,
                "xp": 6000,
                "skip": "Unlocks Giants' Foundry Minigame",
                "reqs": "15 Smithing",
                "wiki_slug": "Sleeping_Giants",
                "tip": "Unlocks the premier mid-level smithing minigame for huge GP/XP and Double Ammo mould."
            },
            {
                "name": "Elemental Workshop I",
                "members": True,
                "xp": 5000,
                "skip": "5,000 Smithing & Crafting XP",
                "reqs": "20 Mining, 20 Smithing, 20 Crafting",
                "wiki_slug": "Elemental_Workshop_I",
                "tip": "Quick puzzle quest that gives flat 5k XP."
            },
            {
                "name": "Elemental Workshop II",
                "members": True,
                "xp": 7500,
                "skip": "7,500 Smithing & Crafting XP",
                "reqs": "20 Magic, 30 Smithing",
                "wiki_slug": "Elemental_Workshop_II",
                "tip": "Great continuation grant after Workshop I."
            },
            {
                "name": "The Tourist Trap",
                "members": True,
                "xp": 9300,
                "skip": "9,300 Smithing or Fletching XP (2x 4,650)",
                "reqs": "10 Fletching, 20 Smithing",
                "wiki_slug": "The_Tourist_Trap",
                "tip": "Can choose Smithing twice for 9.3k free XP."
            },
            {
                "name": "Family Crest",
                "members": True,
                "xp": 0,
                "skip": "Unlocks Goldsmith Gauntlets (2.5x Gold Smelt XP)",
                "reqs": "40 Mining, 40 Smithing, 59 Magic, 40 Crafting",
                "wiki_slug": "Family_Crest",
                "tip": "Unlocks Goldsmith gauntlets. Boosts Gold bar smelting from 22.5 \u2794 56.2 XP ea! Enables 350k+ XP/hr at Blast Furnace."
            }
        ],
        "brackets": [
            {
                "min_lvl": 1,
                "max_lvl": 29,
                "name": "The Knight's Sword (Quest Skip)",
                "item_name": "The Knight's Sword Quest",
                "output_id": 0,
                "members": False,
                "xp_per_action": 12725,
                "materials": [],
                "nature_cost": 0,
                "style": "quest",
                "xp_rate": 40000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 Instant 1\u279429 Skip: Do this quest first! Never waste gold smithing low tiers."
            },
            {
                "min_lvl": 1,
                "max_lvl": 15,
                "name": "Bronze bar (Furnace Smelt)",
                "item_name": "Bronze bar",
                "output_id": 2349,
                "members": False,
                "xp_per_action": 6.25,
                "materials": [
                    {
                        "id": 436,
                        "name": "Copper ore",
                        "qty": 1
                    },
                    {
                        "id": 438,
                        "name": "Tin ore",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 9000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 Beginner Furnace Smelt: 1 Copper + 1 Tin ore at any furnace. Solid F2P starter if not questing."
            },
            {
                "min_lvl": 18,
                "max_lvl": 33,
                "name": "Bronze platebody (Smithing Bridge)",
                "item_name": "Bronze platebody",
                "output_id": 1117,
                "members": False,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2349,
                        "name": "Bronze bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd28 Level 18\u279433 Bridge: Smith Bronze platebodies at Varrock anvil to bridge from Level 29 (The Knight's Sword) to Level 33."
            },
            {
                "min_lvl": 15,
                "max_lvl": 30,
                "name": "Iron bar (Furnace Smelt)",
                "item_name": "Iron bar",
                "output_id": 2351,
                "members": False,
                "xp_per_action": 12.5,
                "materials": [
                    {
                        "id": 440,
                        "name": "Iron ore",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 17500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 Early Furnace Smelt: 50% base success without Ring of forging. Easy low-effort smelting."
            },
            {
                "min_lvl": 19,
                "max_lvl": 33,
                "name": "Iron dart tip (High XP Fletch/GE)",
                "item_name": "Iron dart tip",
                "output_id": 820,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 25.0,
                "materials": [
                    {
                        "id": 2351,
                        "name": "Iron bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 25000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 1 Iron bar makes 10 dart tips. High volume item for Fletching."
            },
            {
                "min_lvl": 20,
                "max_lvl": 30,
                "name": "Silver bar (Furnace Smelt)",
                "item_name": "Silver bar",
                "output_id": 2355,
                "members": False,
                "xp_per_action": 13.75,
                "materials": [
                    {
                        "id": 442,
                        "name": "Silver ore",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 19000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 100% Success Smelt: Smelt Silver ore into Silver bars for Crafting or GE profit."
            },
            {
                "min_lvl": 22,
                "max_lvl": 33,
                "name": "Iron knife (Smith + GE)",
                "item_name": "Iron knife",
                "output_id": 863,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 25.0,
                "materials": [
                    {
                        "id": 2351,
                        "name": "Iron bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 25000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd2a 1 Iron bar makes 5 throwing knives. Popular low-tier Ranged ammo."
            },
            {
                "min_lvl": 33,
                "max_lvl": 48,
                "name": "Iron platebody (Smith + Alch)",
                "item_name": "Iron platebody",
                "output_id": 1115,
                "members": False,
                "xp_per_action": 125.0,
                "materials": [
                    {
                        "id": 2351,
                        "name": "Iron bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 100000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd28 Core Anvil Meta (33\u279448): Requires Level 33! In F2P, this is the fastest method to bridge all the way to Level 48 Steel platebodies."
            },
            {
                "min_lvl": 30,
                "max_lvl": 48,
                "name": "Steel bar (Blast Furnace)",
                "item_name": "Steel bar",
                "output_id": 2353,
                "members": True,
                "xp_per_action": 17.5,
                "materials": [
                    {
                        "id": 440,
                        "name": "Iron ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 95000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Premier Blast Furnace Profit: Halved coal (1 Coal per Iron ore). Outstanding 700k-1M GP/hr profit!"
            },
            {
                "min_lvl": 30,
                "max_lvl": 48,
                "name": "Steel bar (Furnace Smelt)",
                "item_name": "Steel bar",
                "output_id": 2353,
                "members": False,
                "xp_per_action": 17.5,
                "materials": [
                    {
                        "id": 440,
                        "name": "Iron ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 2
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 22000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 F2P Furnace Smelt: Requires 1 Iron ore + 2 Coal. Reliable F2P training at Edgeville furnace."
            },
            {
                "min_lvl": 33,
                "max_lvl": 48,
                "name": "Steel bolts (unf) (Smith + GE)",
                "item_name": "Steel bolts (unf)",
                "output_id": 9378,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 35000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd29 1 Steel bar makes 10 unfinished bolts. Steady demand on GE."
            },
            {
                "min_lvl": 34,
                "max_lvl": 48,
                "name": "Steel dart tip (High XP Fletch/GE)",
                "item_name": "Steel dart tip",
                "output_id": 821,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 37500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf Popular P2P Fletching Material: 1 bar = 10 dart tips. High trade volume."
            },
            {
                "min_lvl": 35,
                "max_lvl": 48,
                "name": "Cannonballs (AFK Profit)",
                "item_name": "Cannonball",
                "output_id": 2,
                "output_qty": 4,
                "members": True,
                "xp_per_action": 25.6,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 14000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Passive AFK Profit: 1 Steel bar makes 4 cannonballs. Steady GP earner on GE."
            },
            {
                "min_lvl": 35,
                "max_lvl": 48,
                "name": "Steel arrowtips (Smith + GE)",
                "item_name": "Steel arrowtips",
                "output_id": 41,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 37500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 Steel bar makes 15 arrowtips. Fast smithing with high demand."
            },
            {
                "min_lvl": 35,
                "max_lvl": 48,
                "name": "Steel scimitar (Smith + Alch/GE)",
                "item_name": "Steel scimitar",
                "output_id": 1325,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 60000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 2 bars = 75 XP. Great early weapon smithing."
            },
            {
                "min_lvl": 37,
                "max_lvl": 48,
                "name": "Steel knife (Smith + GE)",
                "item_name": "Steel knife",
                "output_id": 865,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 37500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd2a 1 Steel bar makes 5 throwing knives. Solid Ranged training item."
            },
            {
                "min_lvl": 44,
                "max_lvl": 48,
                "name": "Steel 2h sword (Smith + Alch)",
                "item_name": "Steel 2h sword",
                "output_id": 1311,
                "members": False,
                "xp_per_action": 112.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 90000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 Fast 3-bar method right before platebodies."
            },
            {
                "min_lvl": 46,
                "max_lvl": 48,
                "name": "Steel platelegs (Smith + Alch)",
                "item_name": "Steel platelegs",
                "output_id": 1069,
                "members": False,
                "xp_per_action": 112.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 90000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 3-bar leg armor with solid alch return."
            },
            {
                "min_lvl": 48,
                "max_lvl": 68,
                "name": "Steel platebody (Smith + Alch)",
                "item_name": "Steel platebody",
                "output_id": 1119,
                "members": False,
                "xp_per_action": 187.5,
                "materials": [
                    {
                        "id": 2353,
                        "name": "Steel bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 135000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 High volume staple: 5 bars = 1,200 gp alch floor. Fast XP with low loss."
            },
            {
                "min_lvl": 40,
                "max_lvl": 99,
                "name": "Gold bar (Goldsmith Gauntlets BF)",
                "item_name": "Gold bar",
                "output_id": 2357,
                "members": True,
                "xp_per_action": 56.2,
                "materials": [
                    {
                        "id": 444,
                        "name": "Gold ore",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 350000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\u26a1 Fastest Smithing XP in OSRS (350k+ XP/hr)! Wear Goldsmith gauntlets (Family Crest quest) at Blast Furnace."
            },
            {
                "min_lvl": 40,
                "max_lvl": 50,
                "name": "Gold bar (Furnace Smelt)",
                "item_name": "Gold bar",
                "output_id": 2357,
                "members": False,
                "xp_per_action": 22.5,
                "materials": [
                    {
                        "id": 444,
                        "name": "Gold ore",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 31000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 Regular Furnace Smelt: 22.5 XP per bar (without gauntlets). Relaxed F2P furnace training."
            },
            {
                "min_lvl": 50,
                "max_lvl": 70,
                "name": "Mithril bar (Blast Furnace)",
                "item_name": "Mithril bar",
                "output_id": 2359,
                "members": True,
                "xp_per_action": 30.0,
                "materials": [
                    {
                        "id": 447,
                        "name": "Mithril ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 2
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 110000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 High Profit Blast Furnace: 2 Coal per Mithril ore. High GP/hr profit while leveling."
            },
            {
                "min_lvl": 50,
                "max_lvl": 70,
                "name": "Mithril bar (Furnace Smelt)",
                "item_name": "Mithril bar",
                "output_id": 2359,
                "members": False,
                "xp_per_action": 30.0,
                "materials": [
                    {
                        "id": 447,
                        "name": "Mithril ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 4
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 25000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 F2P Furnace Smelt: Requires 1 Mithril ore + 4 Coal. Steady AFK furnace training."
            },
            {
                "min_lvl": 50,
                "max_lvl": 68,
                "name": "Mithril dagger (Smith + GE)",
                "item_name": "Mithril dagger",
                "output_id": 1209,
                "members": False,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 45000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udde1\ufe0f 1 Mithril bar starter at Level 50."
            },
            {
                "min_lvl": 53,
                "max_lvl": 68,
                "name": "Mithril bolts (unf) (Smith + GE)",
                "item_name": "Mithril bolts (unf)",
                "output_id": 9379,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd29 1 Mithril bar makes 10 unfinished bolts. High demand for broad bolt crafting."
            },
            {
                "min_lvl": 54,
                "max_lvl": 68,
                "name": "Mithril dart tip (High XP Fletch/GE)",
                "item_name": "Mithril dart tip",
                "output_id": 822,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf Premier Training & Profit: 1 bar = 10 dart tips. Massive volume on GE!"
            },
            {
                "min_lvl": 54,
                "max_lvl": 68,
                "name": "Mithril sword (Smith + Alch)",
                "item_name": "Mithril sword",
                "output_id": 1285,
                "members": False,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 45000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 1 bar = 50 XP. Quick 1-bar sword for early level 50s."
            },
            {
                "min_lvl": 55,
                "max_lvl": 68,
                "name": "Mithril scimitar (Smith + Alch/GE)",
                "item_name": "Mithril scimitar",
                "output_id": 1329,
                "members": False,
                "xp_per_action": 100.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 80000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 2 bars = 100 XP. High demand weapon on GE."
            },
            {
                "min_lvl": 55,
                "max_lvl": 68,
                "name": "Mithril arrowtips (Smith + GE)",
                "item_name": "Mithril arrowtips",
                "output_id": 42,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 bar = 15 arrowtips. Excellent Fletching component with huge GE volume."
            },
            {
                "min_lvl": 57,
                "max_lvl": 68,
                "name": "Mithril knife (Smith + GE)",
                "item_name": "Mithril knife",
                "output_id": 866,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd2a 1 bar = 5 knives. Widely used for Ranged combat."
            },
            {
                "min_lvl": 64,
                "max_lvl": 68,
                "name": "Mithril 2h sword (Smith + Alch)",
                "item_name": "Mithril 2h sword",
                "output_id": 1315,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 3 bars = 150 XP. Fast 3-bar training before platebody."
            },
            {
                "min_lvl": 66,
                "max_lvl": 68,
                "name": "Mithril platelegs (Smith + Alch)",
                "item_name": "Mithril platelegs",
                "output_id": 1071,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 3 bars = 150 XP. Great alch floor."
            },
            {
                "min_lvl": 68,
                "max_lvl": 88,
                "name": "Mithril platebody (Smith + Alch)",
                "item_name": "Mithril platebody",
                "output_id": 1121,
                "members": False,
                "xp_per_action": 250.0,
                "materials": [
                    {
                        "id": 2359,
                        "name": "Mithril bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 180000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 Premier mid-level XP rate: High smith speed at Varrock anvil."
            },
            {
                "min_lvl": 70,
                "max_lvl": 85,
                "name": "Adamantite bar (Blast Furnace)",
                "item_name": "Adamantite bar",
                "output_id": 2361,
                "members": True,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 449,
                        "name": "Adamantite ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 3
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 110000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Elite Blast Furnace Profit: 3 Coal per Adamantite ore. 800k-1.2M GP/hr profit on GE."
            },
            {
                "min_lvl": 70,
                "max_lvl": 85,
                "name": "Adamantite bar (Furnace Smelt)",
                "item_name": "Adamantite bar",
                "output_id": 2361,
                "members": False,
                "xp_per_action": 37.5,
                "materials": [
                    {
                        "id": 449,
                        "name": "Adamantite ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 6
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 22000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 F2P Furnace Smelt: Requires 1 Adamantite ore + 6 Coal. High value F2P smelting (+450 gp/bar)."
            },
            {
                "min_lvl": 70,
                "max_lvl": 88,
                "name": "Adamant dagger (Smith + GE/Alch)",
                "item_name": "Adamant dagger",
                "output_id": 1211,
                "members": False,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 55000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udde1\ufe0f 1 bar = 62.5 XP. Unlocks right at Level 70."
            },
            {
                "min_lvl": 71,
                "max_lvl": 88,
                "name": "Adamant axe (Smith + GE)",
                "item_name": "Adamant axe",
                "output_id": 1357,
                "members": False,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 55000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude93 1 bar woodcutting tool with consistent trade volume."
            },
            {
                "min_lvl": 71,
                "max_lvl": 88,
                "name": "Adamant pickaxe (Smith + GE)",
                "item_name": "Adamant pickaxe",
                "output_id": 1271,
                "members": False,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 55000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\u26cf\ufe0f 1 bar mining tool with steady GE liquidity."
            },
            {
                "min_lvl": 73,
                "max_lvl": 88,
                "name": "Adamant bolts(unf) (Smith + GE)",
                "item_name": "Adamant bolts(unf)",
                "output_id": 9380,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 62500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd29 1 bar = 10 bolts. Core material for Ruby and Diamond bolts(e)!"
            },
            {
                "min_lvl": 74,
                "max_lvl": 88,
                "name": "Adamant dart tip (High XP Fletch/GE)",
                "item_name": "Adamant dart tip",
                "output_id": 823,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 62500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf Top-tier P2P Fletching Item: 1 bar = 10 dart tips. Massive volume and great profit!"
            },
            {
                "min_lvl": 74,
                "max_lvl": 88,
                "name": "Adamant sword (Smith + Alch)",
                "item_name": "Adamant sword",
                "output_id": 1287,
                "members": False,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 55000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 1 bar = 62.5 XP. Convenient 1-bar item."
            },
            {
                "min_lvl": 75,
                "max_lvl": 88,
                "name": "Adamant scimitar (Smith + Alch/GE)",
                "item_name": "Adamant scimitar",
                "output_id": 1331,
                "members": False,
                "xp_per_action": 125.0,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 95000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 2 bars = 125 XP. High demand weapon on GE."
            },
            {
                "min_lvl": 75,
                "max_lvl": 88,
                "name": "Adamant arrowtips (Smith + GE)",
                "item_name": "Adamant arrowtips",
                "output_id": 43,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 62500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 bar = 15 arrowtips. Excellent profit and easy to sell."
            },
            {
                "min_lvl": 77,
                "max_lvl": 88,
                "name": "Adamant knife (Smith + GE)",
                "item_name": "Adamant knife",
                "output_id": 867,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 62.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 62500,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd2a 1 bar = 5 knives. High demand Ranged training ammo."
            },
            {
                "min_lvl": 84,
                "max_lvl": 88,
                "name": "Adamant 2h sword (Smith + Alch)",
                "item_name": "Adamant 2h sword",
                "output_id": 1317,
                "members": False,
                "xp_per_action": 187.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 135000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 3 bars = 187.5 XP. Great high-XP anvil bridge to Level 88."
            },
            {
                "min_lvl": 86,
                "max_lvl": 88,
                "name": "Adamant platelegs (Smith + Alch)",
                "item_name": "Adamant platelegs",
                "output_id": 1073,
                "members": False,
                "xp_per_action": 187.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 135000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 3 bars = 187.5 XP. Strong alch value."
            },
            {
                "min_lvl": 88,
                "max_lvl": 99,
                "name": "Adamant platebody (Smith + Alch)",
                "item_name": "Adamant platebody",
                "output_id": 1123,
                "members": False,
                "xp_per_action": 312.5,
                "materials": [
                    {
                        "id": 2361,
                        "name": "Adamantite bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 225000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Top Tier Method: 9,984 gp alch floor frequently yields net PROFIT even buying bars on live GE!"
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Runite bar (Blast Furnace)",
                "item_name": "Runite bar",
                "output_id": 2363,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 451,
                        "name": "Runite ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 4
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 110000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 Master Smelting Moneymaker: 4 Coal per Runite ore. 1.2M-1.8M+ GP/hr profit selling Runite bars on GE!"
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Runite bar (Furnace Smelt)",
                "item_name": "Runite bar",
                "output_id": 2363,
                "members": False,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 451,
                        "name": "Runite ore",
                        "qty": 1
                    },
                    {
                        "id": 453,
                        "name": "Coal",
                        "qty": 8
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 18000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 F2P Furnace Smelt: Requires 1 Runite ore + 8 Coal. Massive +750 gp/bar profit in F2P!"
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Rune dagger (Smith + GE/Alch)",
                "item_name": "Rune dagger",
                "output_id": 1213,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udde1\ufe0f 1 bar = 75 XP. The very first Rune weapon unlocked at Level 85."
            },
            {
                "min_lvl": 86,
                "max_lvl": 99,
                "name": "Rune axe (Smith + GE)",
                "item_name": "Rune axe",
                "output_id": 1359,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude93 1 bar = 75 XP. Iconic woodcutting tool with high daily demand."
            },
            {
                "min_lvl": 86,
                "max_lvl": 99,
                "name": "Rune pickaxe (Smith + GE)",
                "item_name": "Rune pickaxe",
                "output_id": 1275,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\u26cf\ufe0f 1 bar = 75 XP. Essential mining tool sold constantly on the GE."
            },
            {
                "min_lvl": 87,
                "max_lvl": 99,
                "name": "Rune mace (Smith + Alch/GE)",
                "item_name": "Rune mace",
                "output_id": 1432,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd28 1 bar = 75 XP. Fast single-bar crush weapon."
            },
            {
                "min_lvl": 88,
                "max_lvl": 99,
                "name": "Rune med helm (Smith + Alch/GE)",
                "item_name": "Rune med helm",
                "output_id": 1147,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f First Rune Armor Piece! 1 bar = 75 XP. Alchs for 11,520 gp."
            },
            {
                "min_lvl": 88,
                "max_lvl": 99,
                "name": "Runite bolts (unf) (Smith + GE)",
                "item_name": "Runite bolts (unf)",
                "output_id": 9381,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 75000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd29 1 bar = 10 unfinished bolts. Crucial for Diamond and Dragonstone bolts(e)!"
            },
            {
                "min_lvl": 89,
                "max_lvl": 99,
                "name": "Rune dart tip (High XP Fletch/GE)",
                "item_name": "Rune dart tip",
                "output_id": 824,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 75000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf Top-tier P2P Dart Smithing: 1 bar = 10 dart tips. Enormous demand for Blowpipe ammo!"
            },
            {
                "min_lvl": 89,
                "max_lvl": 99,
                "name": "Rune sword (Smith + Alch/GE)",
                "item_name": "Rune sword",
                "output_id": 1289,
                "members": False,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 65000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 1 bar = 75 XP. Alchs for 12,480 gp\u2014frequently turns a profit when alched!"
            },
            {
                "min_lvl": 89,
                "max_lvl": 99,
                "name": "Rune nails (Smith + GE)",
                "item_name": "Rune nails",
                "output_id": 4824,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 75000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd28 1 bar = 15 nails. Used in high-level Construction."
            },
            {
                "min_lvl": 90,
                "max_lvl": 99,
                "name": "Rune scimitar (Smith + Alch/GE)",
                "item_name": "Rune scimitar",
                "output_id": 1333,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 2 bars = 150 XP. Most iconic F2P weapon in RuneScape history."
            },
            {
                "min_lvl": 90,
                "max_lvl": 99,
                "name": "Rune arrowtips (Smith + GE)",
                "item_name": "Rune arrowtips",
                "output_id": 44,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 75000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 bar = 15 arrowtips. Excellent profit on GE with immense trade volume."
            },
            {
                "min_lvl": 90,
                "max_lvl": 99,
                "name": "Rune cannonball (Smith + GE)",
                "item_name": "Rune cannonball",
                "output_id": 31914,
                "output_qty": 4,
                "members": True,
                "xp_per_action": 50.5,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 30000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udca3 1 Runite bar = 4 Rune cannonballs. High value slayer ammo."
            },
            {
                "min_lvl": 91,
                "max_lvl": 99,
                "name": "Runite limbs (Smith + GE)",
                "item_name": "Runite limbs",
                "output_id": 9431,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 bar = 75 XP. Essential component for Rune crossbows."
            },
            {
                "min_lvl": 91,
                "max_lvl": 99,
                "name": "Rune longsword (Smith + Alch/GE)",
                "item_name": "Rune longsword",
                "output_id": 1303,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u2694\ufe0f 2 bars = 150 XP. Alchs for 19,200 gp."
            },
            {
                "min_lvl": 91,
                "max_lvl": 99,
                "name": "Rune javelin tips (Smith + GE)",
                "item_name": "Rune javelin tips",
                "output_id": 19580,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 1 bar = 5 javelin tips. Ballista ammunition crafting."
            },
            {
                "min_lvl": 92,
                "max_lvl": 99,
                "name": "Rune full helm (Smith + Alch/GE)",
                "item_name": "Rune full helm",
                "output_id": 1163,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 2 bars = 150 XP. Alchs for 21,120 gp."
            },
            {
                "min_lvl": 92,
                "max_lvl": 99,
                "name": "Rune knife (Smith + GE)",
                "item_name": "Rune knife",
                "output_id": 868,
                "output_qty": 5,
                "members": True,
                "xp_per_action": 75.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd2a 1 bar = 5 throwing knives. High speed Ranged training ammo."
            },
            {
                "min_lvl": 93,
                "max_lvl": 99,
                "name": "Rune sq shield (Smith + Alch/GE)",
                "item_name": "Rune sq shield",
                "output_id": 1185,
                "members": False,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 2 bars = 150 XP. Alchs for 23,040 gp."
            },
            {
                "min_lvl": 94,
                "max_lvl": 99,
                "name": "Rune warhammer (Smith + Alch/GE)",
                "item_name": "Rune warhammer",
                "output_id": 1347,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd28 3 bars = 225 XP. Alchs for 24,900 gp."
            },
            {
                "min_lvl": 95,
                "max_lvl": 99,
                "name": "Rune battleaxe (Smith + Alch/GE)",
                "item_name": "Rune battleaxe",
                "output_id": 1373,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude93 3 bars = 225 XP. Alchs for 24,960 gp."
            },
            {
                "min_lvl": 96,
                "max_lvl": 99,
                "name": "Rune chainbody (Smith + Alch/GE)",
                "item_name": "Rune chainbody",
                "output_id": 1113,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 3 bars = 225 XP. First Rune torso armor piece, alchs for 30,000 gp."
            },
            {
                "min_lvl": 97,
                "max_lvl": 99,
                "name": "Rune kiteshield (Smith + Alch/GE)",
                "item_name": "Rune kiteshield",
                "output_id": 1201,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udee1\ufe0f 3 bars = 225 XP. Alchs for 32,640 gp."
            },
            {
                "min_lvl": 98,
                "max_lvl": 99,
                "name": "Rune claws (Smith + GE)",
                "item_name": "Rune claws",
                "output_id": 3101,
                "members": True,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 2
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc3e 2 bars = 150 XP. Unlocked after Death Plateau."
            },
            {
                "min_lvl": 99,
                "max_lvl": 99,
                "name": "Rune 2h sword (Smith + Alch/GE)",
                "item_name": "Rune 2h sword",
                "output_id": 1319,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 Master Profit: 38,400 gp alch floor! Consistently earns pure profit on live GE."
            },
            {
                "min_lvl": 99,
                "max_lvl": 99,
                "name": "Rune platelegs (Smith + Alch/GE)",
                "item_name": "Rune platelegs",
                "output_id": 1079,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 Master Leg Armor: 38,400 gp alch floor. High profit and massive trade liquidity."
            },
            {
                "min_lvl": 99,
                "max_lvl": 99,
                "name": "Rune plateskirt (Smith + Alch/GE)",
                "item_name": "Rune plateskirt",
                "output_id": 1093,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 3
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 Master Leg Armor: Identical alch value to legs (38,400 gp) with excellent profit margins."
            },
            {
                "min_lvl": 99,
                "max_lvl": 99,
                "name": "Rune platebody (Smith + Alch/GE)",
                "item_name": "Rune platebody",
                "output_id": 1127,
                "members": False,
                "xp_per_action": 375.0,
                "materials": [
                    {
                        "id": 2363,
                        "name": "Runite bar",
                        "qty": 5
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 270000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a0\ufe0f Iconic Dragon Slayer Armor: 5 bars = 375 XP. Alchs for 39,000 gp (heavy loss due to 5 bars)."
            }
        ]
    },
    "Fletching": {
        "icon": "\ud83c\udff9",
        "quests": [
            {
                "name": "The Tourist Trap",
                "members": True,
                "xp": 9300,
                "skip": "Skips Level 1 \u2794 26 instantly! (9,300 XP)",
                "reqs": "10 Fletching, 20 Smithing",
                "wiki_slug": "The_Tourist_Trap",
                "tip": "Choose Fletching twice for 9,300 XP. Skips normal logs and goes straight to Oak longbows."
            },
            {
                "name": "Animal Magnetism",
                "members": True,
                "xp": 1000,
                "skip": "Unlocks Ava's Accumulator / Attractor",
                "reqs": "18 Slayer, 19 Crafting, 30 Ranged, 35 Woodcutting",
                "wiki_slug": "Animal_Magnetism",
                "tip": "Essential ranged quest; retrieves ammo automatically."
            },
            {
                "name": "Zogre Flesh Eaters",
                "members": True,
                "xp": 2000,
                "skip": "2,000 Fletching & Ranged XP",
                "reqs": "8 Herblore, 30 Fletching, 30 Ranged",
                "wiki_slug": "Zogre_Flesh_Eaters",
                "tip": "Quick lore quest granting free fletching XP."
            }
        ],
        "brackets": [
            {
                "min_lvl": 1,
                "max_lvl": 20,
                "name": "The Tourist Trap (Quest Skip)",
                "item_name": "The Tourist Trap Quest",
                "output_id": 0,
                "members": True,
                "xp_per_action": 9300,
                "materials": [],
                "nature_cost": 0,
                "style": "quest",
                "xp_rate": 30000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 Instant 1\u279426 Skip: Put quest reward XP into Fletching twice for 9,300 free XP!"
            },
            {
                "min_lvl": 1,
                "max_lvl": 20,
                "name": "Headless arrows (AFK Alternative)",
                "item_name": "Headless arrow",
                "output_id": 53,
                "members": True,
                "xp_per_action": 1.0,
                "materials": [
                    {
                        "id": 52,
                        "name": "Arrow shaft",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 45000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 Relaxed, stackable Fletching XP. Zero loss."
            },
            {
                "min_lvl": 1,
                "max_lvl": 22,
                "name": "Bronze dart (Ultra Fast Darts)",
                "item_name": "Bronze dart",
                "output_id": 806,
                "members": True,
                "xp_per_action": 1.8,
                "materials": [
                    {
                        "id": 820,
                        "name": "Bronze dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 150000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 150k+ XP/hr! Rapid click dart fletching."
            },
            {
                "min_lvl": 20,
                "max_lvl": 25,
                "name": "Oak shortbow (u + s)",
                "item_name": "Oak shortbow",
                "output_id": 843,
                "members": True,
                "xp_per_action": 33.0,
                "materials": [
                    {
                        "id": 1521,
                        "name": "Oak logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 60000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 Cut logs then string bow for combined 33 XP per bow."
            },
            {
                "min_lvl": 22,
                "max_lvl": 34,
                "name": "Iron dart (Ultra Fast Darts)",
                "item_name": "Iron dart",
                "output_id": 807,
                "members": True,
                "xp_per_action": 3.8,
                "materials": [
                    {
                        "id": 820,
                        "name": "Iron dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 300000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 300k+ XP/hr! Lightning fast dart fletching."
            },
            {
                "min_lvl": 25,
                "max_lvl": 40,
                "name": "Oak longbow (u + s)",
                "item_name": "Oak longbow",
                "output_id": 845,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 1521,
                        "name": "Oak logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 80000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 50 XP per bow. Fast bridge to Level 40."
            },
            {
                "min_lvl": 34,
                "max_lvl": 52,
                "name": "Steel dart (Ultra Fast Darts)",
                "item_name": "Steel dart",
                "output_id": 808,
                "members": True,
                "xp_per_action": 7.5,
                "materials": [
                    {
                        "id": 821,
                        "name": "Steel dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 600000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 600k+ XP/hr! Incredible rapid leveling."
            },
            {
                "min_lvl": 40,
                "max_lvl": 50,
                "name": "Willow longbow (u + s)",
                "item_name": "Willow longbow",
                "output_id": 847,
                "members": True,
                "xp_per_action": 83.0,
                "materials": [
                    {
                        "id": 1519,
                        "name": "Willow logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 Willow logs are dirt cheap on the GE. Near-zero cost training."
            },
            {
                "min_lvl": 50,
                "max_lvl": 55,
                "name": "Maple shortbow (u + s)",
                "item_name": "Maple shortbow",
                "output_id": 851,
                "members": True,
                "xp_per_action": 100.0,
                "materials": [
                    {
                        "id": 1517,
                        "name": "Maple logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 130000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 100 XP per bow. Quick bridge to Level 55."
            },
            {
                "min_lvl": 52,
                "max_lvl": 67,
                "name": "Mithril dart (Ultra Fast Darts)",
                "item_name": "Mithril dart",
                "output_id": 809,
                "members": True,
                "xp_per_action": 11.2,
                "materials": [
                    {
                        "id": 822,
                        "name": "Mithril dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 900000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 900k+ XP/hr! High speed dart fletching with great liquidity."
            },
            {
                "min_lvl": 55,
                "max_lvl": 70,
                "name": "Maple longbow (u + s)",
                "item_name": "Maple longbow",
                "output_id": 855,
                "members": True,
                "xp_per_action": 116.5,
                "materials": [
                    {
                        "id": 1517,
                        "name": "Maple logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 150000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 Ultimate budget fletching: Maple logs cost ~8 gp each. Highly cost effective!"
            },
            {
                "min_lvl": 55,
                "max_lvl": 70,
                "name": "Broad arrows (Ultra Fast XP)",
                "item_name": "Broad arrows",
                "output_id": 4160,
                "members": True,
                "xp_per_action": 15.0,
                "materials": [
                    {
                        "id": 53,
                        "name": "Headless arrow",
                        "qty": 1
                    },
                    {
                        "id": 11874,
                        "name": "Broad arrowheads",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 450000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 450k+ XP/hr! Non-tradeable finished arrows, but unbeatable speed."
            },
            {
                "min_lvl": 67,
                "max_lvl": 81,
                "name": "Adamant dart (Ultra Fast Darts)",
                "item_name": "Adamant dart",
                "output_id": 810,
                "members": True,
                "xp_per_action": 15.0,
                "materials": [
                    {
                        "id": 823,
                        "name": "Adamant dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 1200000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 1.2M+ XP/hr! Blistering fast dart fletching."
            },
            {
                "min_lvl": 70,
                "max_lvl": 85,
                "name": "Yew longbow (Fletch + Alch)",
                "item_name": "Yew longbow",
                "output_id": 855,
                "members": True,
                "xp_per_action": 150.0,
                "materials": [
                    {
                        "id": 1515,
                        "name": "Yew logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 175000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 768 gp alch floor! Stringing Yew longbows often yields pure gold profit."
            },
            {
                "min_lvl": 76,
                "max_lvl": 99,
                "name": "Amethyst broad bolts (Fletch + GE)",
                "item_name": "Amethyst broad bolts",
                "output_id": 21316,
                "members": True,
                "xp_per_action": 10.6,
                "materials": [
                    {
                        "id": 11875,
                        "name": "Broad bolts",
                        "qty": 1
                    },
                    {
                        "id": 21338,
                        "name": "Amethyst bolt tips",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 350000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 350k+ XP/hr! Highly profitable endgame ammunition fletching."
            },
            {
                "min_lvl": 81,
                "max_lvl": 99,
                "name": "Rune dart (Ultra Fast Darts)",
                "item_name": "Rune dart",
                "output_id": 811,
                "members": True,
                "xp_per_action": 18.8,
                "materials": [
                    {
                        "id": 824,
                        "name": "Rune dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 1500000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 1.5M+ XP/hr! High tier Blowpipe ammunition fletching."
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Magic longbow (Fletch + Alch)",
                "item_name": "Magic longbow",
                "output_id": 859,
                "members": True,
                "xp_per_action": 183.0,
                "materials": [
                    {
                        "id": 1513,
                        "name": "Magic logs",
                        "qty": 1
                    },
                    {
                        "id": 1777,
                        "name": "Bow string",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 210000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 King of Fletching: 1,536 gp alch value guarantees profit or breaks even."
            },
            {
                "min_lvl": 95,
                "max_lvl": 99,
                "name": "Dragon dart (Ultra Fast Darts)",
                "item_name": "Dragon dart",
                "output_id": 11230,
                "members": True,
                "xp_per_action": 25.0,
                "materials": [
                    {
                        "id": 11232,
                        "name": "Dragon dart tip",
                        "qty": 1
                    },
                    {
                        "id": 314,
                        "name": "Feather",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 2000000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\u26a1 2.0M+ XP/hr! Best in slot Blowpipe ammo fletching."
            }
        ]
    },
    "Crafting": {
        "icon": "\ud83d\udd28",
        "quests": [
            {
                "name": "Misthalin Mystery",
                "members": False,
                "xp": 600,
                "skip": "Skips Level 1 \u2794 8 (600 XP)",
                "reqs": "None (F2P)",
                "wiki_slug": "Misthalin_Mystery",
                "tip": "Short 10-minute F2P quest. Skips early leather gloves."
            },
            {
                "name": "Murder Mystery",
                "members": True,
                "xp": 1406,
                "skip": "Skips Level 8 \u2794 16 (1,406 XP)",
                "reqs": "None",
                "wiki_slug": "Murder_Mystery",
                "tip": "Quick Sinclair Mansion whodunit quest."
            },
            {
                "name": "The Golem",
                "members": True,
                "xp": 1000,
                "skip": "1,000 Crafting & Thieving XP",
                "reqs": "25 Thieving, 20 Crafting",
                "wiki_slug": "The_Golem",
                "tip": "Unlocks Uzer ruins and grants 1k XP."
            },
            {
                "name": "Elemental Workshop I",
                "members": True,
                "xp": 5000,
                "skip": "5,000 Crafting & Smithing XP",
                "reqs": "20 Mining, 20 Smithing, 20 Crafting",
                "wiki_slug": "Elemental_Workshop_I",
                "tip": "Skips past cut gems straight into jewellery tiers."
            }
        ],
        "brackets": [
            {
                "min_lvl": 1,
                "max_lvl": 20,
                "name": "Misthalin Mystery (Quest Skip)",
                "item_name": "Misthalin Mystery Quest",
                "output_id": 0,
                "members": False,
                "xp_per_action": 600,
                "materials": [],
                "nature_cost": 0,
                "style": "quest",
                "xp_rate": 20000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 Quick 10-minute F2P quest. Skips early level 1-8 Crafting instantly."
            },
            {
                "min_lvl": 7,
                "max_lvl": 20,
                "name": "Gold bracelet (Craft + Alch/GE)",
                "item_name": "Gold bracelet",
                "output_id": 11069,
                "members": False,
                "xp_per_action": 25.0,
                "materials": [
                    {
                        "id": 2357,
                        "name": "Gold bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 35000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Great low level profit: 1 Gold bar makes 1 Gold bracelet. High F2P liquidity."
            },
            {
                "min_lvl": 14,
                "max_lvl": 20,
                "name": "Leather body (Early Leather)",
                "item_name": "Leather body",
                "output_id": 1129,
                "members": False,
                "xp_per_action": 25.0,
                "materials": [
                    {
                        "id": 1741,
                        "name": "Leather",
                        "qty": 1
                    },
                    {
                        "id": 1734,
                        "name": "Thread",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 30000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83e\uddf5 Solid early craft: Buy leather and needle/thread. Quick XP to reach gems."
            },
            {
                "min_lvl": 16,
                "max_lvl": 30,
                "name": "Silver tiara (Craft + GE)",
                "item_name": "Tiara",
                "output_id": 5525,
                "members": False,
                "xp_per_action": 52.5,
                "materials": [
                    {
                        "id": 2355,
                        "name": "Silver bar",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 45000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 1 Silver bar makes 1 Tiara. Runecrafting utility item."
            },
            {
                "min_lvl": 20,
                "max_lvl": 27,
                "name": "Cut Sapphire (Gems)",
                "item_name": "Sapphire",
                "output_id": 1607,
                "members": False,
                "xp_per_action": 50.0,
                "materials": [
                    {
                        "id": 1623,
                        "name": "Uncut sapphire",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 140000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 140k+ XP/hr! High speed gem cutting at the Grand Exchange."
            },
            {
                "min_lvl": 20,
                "max_lvl": 46,
                "name": "Sapphire ring (Craft + Alch)",
                "item_name": "Sapphire ring",
                "output_id": 1637,
                "members": False,
                "xp_per_action": 40.0,
                "materials": [
                    {
                        "id": 2357,
                        "name": "Gold bar",
                        "qty": 1
                    },
                    {
                        "id": 1607,
                        "name": "Sapphire",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 55000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8d Reliable F2P jewellery: Smelt into Recoil rings or sell directly."
            },
            {
                "min_lvl": 27,
                "max_lvl": 34,
                "name": "Cut Emerald (Gems)",
                "item_name": "Emerald",
                "output_id": 1605,
                "members": False,
                "xp_per_action": 67.5,
                "materials": [
                    {
                        "id": 1621,
                        "name": "Uncut emerald",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 180000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 180k+ XP/hr! Lightning fast gem cutting."
            },
            {
                "min_lvl": 34,
                "max_lvl": 43,
                "name": "Cut Ruby (Gems)",
                "item_name": "Ruby",
                "output_id": 1603,
                "members": False,
                "xp_per_action": 85.0,
                "materials": [
                    {
                        "id": 1619,
                        "name": "Uncut ruby",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 220000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 220k+ XP/hr! Blazing fast cutting with high resale value."
            },
            {
                "min_lvl": 34,
                "max_lvl": 46,
                "name": "Ruby ring (Craft + Alch)",
                "item_name": "Ruby ring",
                "output_id": 1641,
                "members": False,
                "xp_per_action": 70.0,
                "materials": [
                    {
                        "id": 2357,
                        "name": "Gold bar",
                        "qty": 1
                    },
                    {
                        "id": 1603,
                        "name": "Ruby",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 70000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Great profit margin: High volume due to Ring of forging crafting."
            },
            {
                "min_lvl": 43,
                "max_lvl": 55,
                "name": "Cut Diamond (Gems)",
                "item_name": "Diamond",
                "output_id": 1601,
                "members": False,
                "xp_per_action": 107.5,
                "materials": [
                    {
                        "id": 1617,
                        "name": "Uncut diamond",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 280000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 280k+ XP/hr! Premier high-speed gem leveling."
            },
            {
                "min_lvl": 46,
                "max_lvl": 66,
                "name": "Unpowered orb (Glassblowing AFK)",
                "item_name": "Unpowered orb",
                "output_id": 567,
                "members": True,
                "xp_per_action": 52.5,
                "materials": [
                    {
                        "id": 1775,
                        "name": "Molten glass",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 90000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udffa Pure AFK staple: Low cost, zero banking stress, high demand for battlestaff charging."
            },
            {
                "min_lvl": 54,
                "max_lvl": 66,
                "name": "Water battlestaff (Craft + Alch)",
                "item_name": "Water battlestaff",
                "output_id": 1395,
                "members": True,
                "xp_per_action": 100.0,
                "materials": [
                    {
                        "id": 1391,
                        "name": "Battlestaff",
                        "qty": 1
                    },
                    {
                        "id": 571,
                        "name": "Water orb",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 200000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude84 9,300 gp alch floor! 200k+ XP/hr with consistent high alch profit."
            },
            {
                "min_lvl": 55,
                "max_lvl": 70,
                "name": "Cut Dragonstone (Gems)",
                "item_name": "Dragonstone",
                "output_id": 1615,
                "members": True,
                "xp_per_action": 137.5,
                "materials": [
                    {
                        "id": 1631,
                        "name": "Uncut dragonstone",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 350000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 350k+ XP/hr! Elite ultra-fast gem cutting."
            },
            {
                "min_lvl": 56,
                "max_lvl": 66,
                "name": "Diamond necklace (Craft + Alch)",
                "item_name": "Diamond necklace",
                "output_id": 1662,
                "members": False,
                "xp_per_action": 90.0,
                "materials": [
                    {
                        "id": 2357,
                        "name": "Gold bar",
                        "qty": 1
                    },
                    {
                        "id": 1601,
                        "name": "Diamond",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 80000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcff High alch value floor: Reliable F2P moneymaker when enchanting or alching."
            },
            {
                "min_lvl": 58,
                "max_lvl": 66,
                "name": "Earth battlestaff (Craft + Alch)",
                "item_name": "Earth battlestaff",
                "output_id": 1399,
                "members": True,
                "xp_per_action": 112.5,
                "materials": [
                    {
                        "id": 1391,
                        "name": "Battlestaff",
                        "qty": 1
                    },
                    {
                        "id": 575,
                        "name": "Earth orb",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 220000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude84 9,300 gp alch floor! 220k+ XP/hr. Attaching orbs is lightning fast."
            },
            {
                "min_lvl": 62,
                "max_lvl": 66,
                "name": "Fire battlestaff (Craft + Alch)",
                "item_name": "Fire battlestaff",
                "output_id": 1393,
                "members": True,
                "xp_per_action": 125.0,
                "materials": [
                    {
                        "id": 1391,
                        "name": "Battlestaff",
                        "qty": 1
                    },
                    {
                        "id": 569,
                        "name": "Fire orb",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 240000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83e\ude84 9,300 gp alch floor! 240k+ XP/hr. High volume staple."
            },
            {
                "min_lvl": 63,
                "max_lvl": 71,
                "name": "Green d'hide body (Craft + Alch)",
                "item_name": "Green d'hide body",
                "output_id": 1135,
                "members": True,
                "xp_per_action": 186.0,
                "materials": [
                    {
                        "id": 1745,
                        "name": "Green dragon leather",
                        "qty": 3
                    },
                    {
                        "id": 1734,
                        "name": "Thread",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 280000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 Premier 280k+ XP/hr! 3 leather per body. High alch floor (4,680 gp)."
            },
            {
                "min_lvl": 66,
                "max_lvl": 99,
                "name": "Air battlestaff (Premier Meta)",
                "item_name": "Air battlestaff",
                "output_id": 1397,
                "members": True,
                "xp_per_action": 137.5,
                "materials": [
                    {
                        "id": 1391,
                        "name": "Battlestaff",
                        "qty": 1
                    },
                    {
                        "id": 573,
                        "name": "Air orb",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 270000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc51 King of Crafting: 137.5 XP per staff. 9,300 gp alch floor yields steady profit."
            },
            {
                "min_lvl": 71,
                "max_lvl": 77,
                "name": "Blue d'hide body (Craft + Alch)",
                "item_name": "Blue d'hide body",
                "output_id": 2499,
                "members": True,
                "xp_per_action": 210.0,
                "materials": [
                    {
                        "id": 2505,
                        "name": "Blue dragon leather",
                        "qty": 3
                    },
                    {
                        "id": 1734,
                        "name": "Thread",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 320000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 320k+ XP/hr! 5,616 gp alch floor. Fast leveling with moderate loss."
            },
            {
                "min_lvl": 77,
                "max_lvl": 84,
                "name": "Red d'hide body (Craft + Alch)",
                "item_name": "Red d'hide body",
                "output_id": 2501,
                "members": True,
                "xp_per_action": 234.0,
                "materials": [
                    {
                        "id": 2507,
                        "name": "Red dragon leather",
                        "qty": 3
                    },
                    {
                        "id": 1734,
                        "name": "Thread",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 350000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\ud83d\udd25 Blazing 350k+ XP/hr: 6,738 gp alch floor. Fast 77\u279484 leveling."
            },
            {
                "min_lvl": 83,
                "max_lvl": 99,
                "name": "Amethyst bolt tips (Craft + GE)",
                "item_name": "Amethyst bolt tips",
                "output_id": 21338,
                "output_qty": 8,
                "members": True,
                "xp_per_action": 60.0,
                "materials": [
                    {
                        "id": 21347,
                        "name": "Amethyst",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 100000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udc8e 1 Amethyst = 8 bolt tips. High volume endgame ammo component."
            },
            {
                "min_lvl": 84,
                "max_lvl": 99,
                "name": "Black d'hide body (Craft + Alch)",
                "item_name": "Black d'hide body",
                "output_id": 2503,
                "members": True,
                "xp_per_action": 258.0,
                "materials": [
                    {
                        "id": 2509,
                        "name": "Black dragon leather",
                        "qty": 3
                    },
                    {
                        "id": 1734,
                        "name": "Thread",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 380000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "\u26a1 380k+ XP/hr! 8,088 gp alch floor. Top tier leather training method in OSRS."
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Amethyst arrowtips (Craft + GE)",
                "item_name": "Amethyst arrowtips",
                "output_id": 21332,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 60.0,
                "materials": [
                    {
                        "id": 21347,
                        "name": "Amethyst",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 100000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udff9 1 Amethyst = 15 arrowtips. Excellent profit and trade velocity."
            },
            {
                "min_lvl": 89,
                "max_lvl": 99,
                "name": "Amethyst dart tips (Craft + GE)",
                "item_name": "Amethyst dart tips",
                "output_id": 25853,
                "output_qty": 8,
                "members": True,
                "xp_per_action": 60.0,
                "materials": [
                    {
                        "id": 21347,
                        "name": "Amethyst",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 100000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83c\udfaf 1 Amethyst = 8 dart tips. Premier Blowpipe ammo crafting."
            }
        ]
    },
    "Magic": {
        "icon": "\u2728",
        "quests": [
            {
                "name": "Imp Catcher",
                "members": False,
                "xp": 875,
                "skip": "Skips Level 1 \u2794 8 (875 XP)",
                "reqs": "4 Beads (Red, Yellow, Black, White)",
                "wiki_slug": "Imp_Catcher",
                "tip": "Buy beads on GE and hand to Wizard Mizgog for instant Level 8."
            },
            {
                "name": "Witch's Potion",
                "members": False,
                "xp": 325,
                "skip": "325 Magic XP",
                "reqs": "Rat's tail, burnt meat, onion, eye of newt",
                "wiki_slug": "Witch's_Potion",
                "tip": "Quick 5-minute F2P quest in Rimmington."
            },
            {
                "name": "Mage Arena I & II",
                "members": True,
                "xp": 0,
                "skip": "Unlocks God Spells & Imbued God Capes",
                "reqs": "60 Magic (Arena I), 75 Magic (Arena II)",
                "wiki_slug": "Mage_Arena_II",
                "tip": "Best-in-slot magic cape upgrade in the deep wilderness."
            },
            {
                "name": "Lunar Diplomacy",
                "members": True,
                "xp": 5000,
                "skip": "Unlocks Lunar Spellbook & Humidify/Plank Make",
                "reqs": "61 Crafting, 40 Defence, 49 Firemaking, 65 Magic, 60 Mining",
                "wiki_slug": "Lunar_Diplomacy",
                "tip": "Unlocks the utility skilling spellbook."
            }
        ],
        "brackets": [
            {
                "min_lvl": 1,
                "max_lvl": 15,
                "name": "Imp Catcher + Strike Spells",
                "item_name": "Strike Spells / Quest",
                "output_id": 0,
                "members": False,
                "xp_per_action": 875,
                "materials": [],
                "nature_cost": 0,
                "style": "quest",
                "xp_rate": 20000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 Instant 1\u27948 Skip with beads, then Wind/Fire Strike to reach Level 15."
            },
            {
                "min_lvl": 15,
                "max_lvl": 55,
                "name": "Fire Bolt / Splashing / Teleports",
                "item_name": "Fire Bolt / Teleports",
                "output_id": 0,
                "members": False,
                "xp_per_action": 22.5,
                "materials": [
                    {
                        "id": 562,
                        "name": "Chaos rune",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\ud83e\ude84 Train with Chaos gauntlets or spam Varrock/Falador/Camelot teleports."
            },
            {
                "min_lvl": 27,
                "max_lvl": 55,
                "name": "Enchant Sapphire/Emerald/Ruby",
                "item_name": "Ring of recoil (Enchant)",
                "output_id": 2550,
                "members": False,
                "xp_per_action": 37.0,
                "materials": [
                    {
                        "id": 1637,
                        "name": "Sapphire ring",
                        "qty": 1
                    },
                    {
                        "id": 564,
                        "name": "Cosmic rune",
                        "qty": 1
                    }
                ],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Profitable Magic: Enchanting jewellery with Cosmic runes yields solid profits on GE."
            },
            {
                "min_lvl": 55,
                "max_lvl": 99,
                "name": "High Level Alchemy (Master Training)",
                "item_name": "High Alchemy Spell",
                "output_id": 561,
                "members": False,
                "xp_per_action": 65.0,
                "materials": [
                    {
                        "id": 561,
                        "name": "Nature rune",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 78000,
                "can_alch": True,
                "can_sell_ge": False,
                "verdict": "\ud83d\udc51 78,000 XP/hr (1,200 casts/hr): 100% PROFITABLE with dashboard items all the way to 99!"
            },
            {
                "min_lvl": 70,
                "max_lvl": 99,
                "name": "Ice Burst / Barrage (Maniacal Monkeys)",
                "item_name": "Ice Burst Spell",
                "output_id": 560,
                "members": True,
                "xp_per_action": 180.0,
                "materials": [
                    {
                        "id": 560,
                        "name": "Death rune",
                        "qty": 2
                    },
                    {
                        "id": 562,
                        "name": "Chaos rune",
                        "qty": 4
                    }
                ],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 280000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "\u26a1 280k-350k XP/hr: Multi-target combat bursting in MM2 tunnels. High rune cost."
            },
            {
                "min_lvl": 86,
                "max_lvl": 99,
                "name": "Plank Make (Lunar Utility)",
                "item_name": "Plank Make Spell",
                "output_id": 90,
                "members": True,
                "xp_per_action": 90.0,
                "materials": [
                    {
                        "id": 9075,
                        "name": "Astral rune",
                        "qty": 2
                    },
                    {
                        "id": 561,
                        "name": "Nature rune",
                        "qty": 1
                    },
                    {
                        "id": 1511,
                        "name": "Logs",
                        "qty": 1
                    }
                ],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 90000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "\ud83d\udcb0 Profitable Lunar Spell: Convert logs to planks on GE for profit + 90 XP per cast."
            }
        ]
    }
}

SMITHING_MATERIAL_CHAINS = [
    {
        "tier": "Bronze",
        "bar_name": "Bronze bar",
        "bar_id": 2349,
        "ore_name": "Copper ore",
        "ore_id": 436,
        "second_name": "Tin ore",
        "second_id": 438,
        "coal_qty_bf": 0,
        "coal_qty_reg": 0,
        "smelt_lvl": 1,
        "smelt_xp": 6.25,
        "members": False,
        "items": [
            {
                "name": "Bronze dagger",
                "id": 1205,
                "level": 1,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze axe",
                "id": 1351,
                "level": 1,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze pickaxe",
                "id": 1265,
                "level": 1,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze mace",
                "id": 1422,
                "level": 2,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze med helm",
                "id": 1139,
                "level": 3,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze sword",
                "id": 1277,
                "level": 4,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze dart tip",
                "id": 819,
                "level": 4,
                "bars": 1,
                "xp": 12.5,
                "qty": 10,
                "members": True
            },
            {
                "name": "Bronze nails",
                "id": 4819,
                "level": 4,
                "bars": 1,
                "xp": 12.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Bronze scimitar",
                "id": 1321,
                "level": 5,
                "bars": 2,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze arrowtips",
                "id": 39,
                "level": 5,
                "bars": 1,
                "xp": 12.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Bronze limbs",
                "id": 9420,
                "level": 6,
                "bars": 1,
                "xp": 12.5,
                "qty": 1,
                "members": True
            },
            {
                "name": "Bronze longsword",
                "id": 1291,
                "level": 6,
                "bars": 2,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze full helm",
                "id": 1155,
                "level": 7,
                "bars": 2,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze knife",
                "id": 864,
                "level": 7,
                "bars": 1,
                "xp": 12.5,
                "qty": 5,
                "members": True
            },
            {
                "name": "Bronze sq shield",
                "id": 1173,
                "level": 8,
                "bars": 2,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze warhammer",
                "id": 1337,
                "level": 9,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze battleaxe",
                "id": 1375,
                "level": 10,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze chainbody",
                "id": 1103,
                "level": 11,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze kiteshield",
                "id": 1189,
                "level": 12,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze claws",
                "id": 3095,
                "level": 13,
                "bars": 2,
                "xp": 25.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Bronze 2h sword",
                "id": 1307,
                "level": 14,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze platelegs",
                "id": 1075,
                "level": 16,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze plateskirt",
                "id": 1087,
                "level": 16,
                "bars": 3,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Bronze platebody",
                "id": 1117,
                "level": 18,
                "bars": 5,
                "xp": 62.5,
                "qty": 1,
                "members": False
            }
        ]
    },
    {
        "tier": "Iron",
        "bar_name": "Iron bar",
        "bar_id": 2351,
        "ore_name": "Iron ore",
        "ore_id": 440,
        "second_name": "",
        "second_id": 0,
        "coal_qty_bf": 0,
        "coal_qty_reg": 0,
        "smelt_lvl": 15,
        "smelt_xp": 12.5,
        "members": False,
        "items": [
            {
                "name": "Iron dagger",
                "id": 1203,
                "level": 15,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron axe",
                "id": 1349,
                "level": 16,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron pickaxe",
                "id": 1267,
                "level": 16,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron mace",
                "id": 1420,
                "level": 17,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron med helm",
                "id": 1137,
                "level": 18,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron sword",
                "id": 1279,
                "level": 19,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron dart tip",
                "id": 820,
                "level": 19,
                "bars": 1,
                "xp": 25.0,
                "qty": 10,
                "members": True
            },
            {
                "name": "Iron nails",
                "id": 4820,
                "level": 19,
                "bars": 1,
                "xp": 25.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Iron scimitar",
                "id": 1323,
                "level": 20,
                "bars": 2,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron arrowtips",
                "id": 40,
                "level": 20,
                "bars": 1,
                "xp": 25.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Iron limbs",
                "id": 9423,
                "level": 21,
                "bars": 1,
                "xp": 25.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Iron longsword",
                "id": 1293,
                "level": 21,
                "bars": 2,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron full helm",
                "id": 1153,
                "level": 22,
                "bars": 2,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron knife",
                "id": 863,
                "level": 22,
                "bars": 1,
                "xp": 25.0,
                "qty": 5,
                "members": True
            },
            {
                "name": "Iron sq shield",
                "id": 1175,
                "level": 23,
                "bars": 2,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron warhammer",
                "id": 1335,
                "level": 24,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron battleaxe",
                "id": 1363,
                "level": 25,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron chainbody",
                "id": 1101,
                "level": 26,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron kiteshield",
                "id": 1191,
                "level": 27,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron claws",
                "id": 3096,
                "level": 28,
                "bars": 2,
                "xp": 50.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Iron 2h sword",
                "id": 1309,
                "level": 29,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron platelegs",
                "id": 1067,
                "level": 31,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron plateskirt",
                "id": 1081,
                "level": 31,
                "bars": 3,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Iron platebody",
                "id": 1115,
                "level": 33,
                "bars": 5,
                "xp": 125.0,
                "qty": 1,
                "members": False
            }
        ]
    },
    {
        "tier": "Steel",
        "bar_name": "Steel bar",
        "bar_id": 2353,
        "ore_name": "Iron ore",
        "ore_id": 440,
        "second_name": "Coal",
        "second_id": 453,
        "coal_qty_bf": 1,
        "coal_qty_reg": 2,
        "smelt_lvl": 30,
        "smelt_xp": 17.5,
        "members": False,
        "items": [
            {
                "name": "Steel dagger",
                "id": 1207,
                "level": 30,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel axe",
                "id": 1353,
                "level": 31,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel pickaxe",
                "id": 1269,
                "level": 31,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel mace",
                "id": 1424,
                "level": 32,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel med helm",
                "id": 1141,
                "level": 33,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel bolts (unf)",
                "id": 9378,
                "level": 33,
                "bars": 1,
                "xp": 37.5,
                "qty": 10,
                "members": True
            },
            {
                "name": "Steel sword",
                "id": 1281,
                "level": 34,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel dart tip",
                "id": 821,
                "level": 34,
                "bars": 1,
                "xp": 37.5,
                "qty": 10,
                "members": True
            },
            {
                "name": "Steel nails",
                "id": 1539,
                "level": 34,
                "bars": 1,
                "xp": 37.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Cannonballs",
                "id": 2,
                "level": 35,
                "bars": 1,
                "xp": 25.6,
                "qty": 4,
                "members": True
            },
            {
                "name": "Steel scimitar",
                "id": 1325,
                "level": 35,
                "bars": 2,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel arrowtips",
                "id": 41,
                "level": 35,
                "bars": 1,
                "xp": 37.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Steel limbs",
                "id": 9425,
                "level": 36,
                "bars": 1,
                "xp": 37.5,
                "qty": 1,
                "members": True
            },
            {
                "name": "Steel longsword",
                "id": 1295,
                "level": 36,
                "bars": 2,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel full helm",
                "id": 1157,
                "level": 37,
                "bars": 2,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel knife",
                "id": 865,
                "level": 37,
                "bars": 1,
                "xp": 37.5,
                "qty": 5,
                "members": True
            },
            {
                "name": "Steel sq shield",
                "id": 1179,
                "level": 38,
                "bars": 2,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel warhammer",
                "id": 1339,
                "level": 39,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel battleaxe",
                "id": 1365,
                "level": 40,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel chainbody",
                "id": 1105,
                "level": 41,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel kiteshield",
                "id": 1193,
                "level": 42,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel claws",
                "id": 3097,
                "level": 43,
                "bars": 2,
                "xp": 75.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Steel 2h sword",
                "id": 1311,
                "level": 44,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel platelegs",
                "id": 1069,
                "level": 46,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel plateskirt",
                "id": 1083,
                "level": 46,
                "bars": 3,
                "xp": 112.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Steel platebody",
                "id": 1119,
                "level": 48,
                "bars": 5,
                "xp": 187.5,
                "qty": 1,
                "members": False
            }
        ]
    },
    {
        "tier": "Mithril",
        "bar_name": "Mithril bar",
        "bar_id": 2359,
        "ore_name": "Mithril ore",
        "ore_id": 447,
        "second_name": "Coal",
        "second_id": 453,
        "coal_qty_bf": 2,
        "coal_qty_reg": 4,
        "smelt_lvl": 50,
        "smelt_xp": 30.0,
        "members": False,
        "items": [
            {
                "name": "Mithril dagger",
                "id": 1209,
                "level": 50,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril axe",
                "id": 1355,
                "level": 51,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril pickaxe",
                "id": 1273,
                "level": 51,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril mace",
                "id": 1428,
                "level": 52,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril med helm",
                "id": 1143,
                "level": 53,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril bolts (unf)",
                "id": 9379,
                "level": 53,
                "bars": 1,
                "xp": 50.0,
                "qty": 10,
                "members": True
            },
            {
                "name": "Mithril sword",
                "id": 1285,
                "level": 54,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril dart tip",
                "id": 822,
                "level": 54,
                "bars": 1,
                "xp": 50.0,
                "qty": 10,
                "members": True
            },
            {
                "name": "Mithril nails",
                "id": 4822,
                "level": 54,
                "bars": 1,
                "xp": 50.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Mithril scimitar",
                "id": 1329,
                "level": 55,
                "bars": 2,
                "xp": 100.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril arrowtips",
                "id": 42,
                "level": 55,
                "bars": 1,
                "xp": 50.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Mithril limbs",
                "id": 9427,
                "level": 56,
                "bars": 1,
                "xp": 50.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Mithril longsword",
                "id": 1299,
                "level": 56,
                "bars": 2,
                "xp": 100.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril full helm",
                "id": 1159,
                "level": 57,
                "bars": 2,
                "xp": 100.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril knife",
                "id": 866,
                "level": 57,
                "bars": 1,
                "xp": 50.0,
                "qty": 5,
                "members": True
            },
            {
                "name": "Mithril sq shield",
                "id": 1181,
                "level": 58,
                "bars": 2,
                "xp": 100.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril warhammer",
                "id": 1343,
                "level": 59,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril battleaxe",
                "id": 1369,
                "level": 60,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril chainbody",
                "id": 1109,
                "level": 61,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril kiteshield",
                "id": 1197,
                "level": 62,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril claws",
                "id": 3098,
                "level": 63,
                "bars": 2,
                "xp": 100.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Mithril 2h sword",
                "id": 1315,
                "level": 64,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril platelegs",
                "id": 1071,
                "level": 66,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril plateskirt",
                "id": 1085,
                "level": 66,
                "bars": 3,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Mithril platebody",
                "id": 1121,
                "level": 68,
                "bars": 5,
                "xp": 250.0,
                "qty": 1,
                "members": False
            }
        ]
    },
    {
        "tier": "Adamant",
        "bar_name": "Adamantite bar",
        "bar_id": 2361,
        "ore_name": "Adamantite ore",
        "ore_id": 449,
        "second_name": "Coal",
        "second_id": 453,
        "coal_qty_bf": 3,
        "coal_qty_reg": 6,
        "smelt_lvl": 70,
        "smelt_xp": 37.5,
        "members": False,
        "items": [
            {
                "name": "Adamant dagger",
                "id": 1211,
                "level": 70,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant axe",
                "id": 1357,
                "level": 71,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant pickaxe",
                "id": 1271,
                "level": 71,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant mace",
                "id": 1430,
                "level": 72,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant med helm",
                "id": 1145,
                "level": 73,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant bolts(unf)",
                "id": 9380,
                "level": 73,
                "bars": 1,
                "xp": 62.5,
                "qty": 10,
                "members": True
            },
            {
                "name": "Adamant sword",
                "id": 1287,
                "level": 74,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant dart tip",
                "id": 823,
                "level": 74,
                "bars": 1,
                "xp": 62.5,
                "qty": 10,
                "members": True
            },
            {
                "name": "Adamantite nails",
                "id": 4823,
                "level": 74,
                "bars": 1,
                "xp": 62.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Adamant scimitar",
                "id": 1331,
                "level": 75,
                "bars": 2,
                "xp": 125.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant arrowtips",
                "id": 43,
                "level": 75,
                "bars": 1,
                "xp": 62.5,
                "qty": 15,
                "members": True
            },
            {
                "name": "Adamantite limbs",
                "id": 9429,
                "level": 76,
                "bars": 1,
                "xp": 62.5,
                "qty": 1,
                "members": True
            },
            {
                "name": "Adamant longsword",
                "id": 1301,
                "level": 76,
                "bars": 2,
                "xp": 125.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant full helm",
                "id": 1161,
                "level": 77,
                "bars": 2,
                "xp": 125.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant knife",
                "id": 867,
                "level": 77,
                "bars": 1,
                "xp": 62.5,
                "qty": 5,
                "members": True
            },
            {
                "name": "Adamant sq shield",
                "id": 1183,
                "level": 78,
                "bars": 2,
                "xp": 125.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant warhammer",
                "id": 1345,
                "level": 79,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant battleaxe",
                "id": 1371,
                "level": 80,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant chainbody",
                "id": 1111,
                "level": 81,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant kiteshield",
                "id": 1199,
                "level": 82,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant claws",
                "id": 3099,
                "level": 83,
                "bars": 2,
                "xp": 125.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Adamant 2h sword",
                "id": 1317,
                "level": 84,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant platelegs",
                "id": 1073,
                "level": 86,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant plateskirt",
                "id": 1091,
                "level": 86,
                "bars": 3,
                "xp": 187.5,
                "qty": 1,
                "members": False
            },
            {
                "name": "Adamant platebody",
                "id": 1123,
                "level": 88,
                "bars": 5,
                "xp": 312.5,
                "qty": 1,
                "members": False
            }
        ]
    },
    {
        "tier": "Rune",
        "bar_name": "Runite bar",
        "bar_id": 2363,
        "ore_name": "Runite ore",
        "ore_id": 451,
        "second_name": "Coal",
        "second_id": 453,
        "coal_qty_bf": 4,
        "coal_qty_reg": 8,
        "smelt_lvl": 85,
        "smelt_xp": 50.0,
        "members": False,
        "items": [
            {
                "name": "Rune dagger",
                "id": 1213,
                "level": 85,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune axe",
                "id": 1359,
                "level": 86,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune pickaxe",
                "id": 1275,
                "level": 86,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune mace",
                "id": 1432,
                "level": 87,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune med helm",
                "id": 1147,
                "level": 88,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Runite bolts (unf)",
                "id": 9381,
                "level": 88,
                "bars": 1,
                "xp": 75.0,
                "qty": 10,
                "members": True
            },
            {
                "name": "Rune sword",
                "id": 1289,
                "level": 89,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune dart tip",
                "id": 824,
                "level": 89,
                "bars": 1,
                "xp": 75.0,
                "qty": 10,
                "members": True
            },
            {
                "name": "Rune nails",
                "id": 4824,
                "level": 89,
                "bars": 1,
                "xp": 75.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Rune scimitar",
                "id": 1333,
                "level": 90,
                "bars": 2,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune arrowtips",
                "id": 44,
                "level": 90,
                "bars": 1,
                "xp": 75.0,
                "qty": 15,
                "members": True
            },
            {
                "name": "Rune cannonball",
                "id": 31914,
                "level": 90,
                "bars": 1,
                "xp": 50.5,
                "qty": 4,
                "members": True
            },
            {
                "name": "Runite limbs",
                "id": 9431,
                "level": 91,
                "bars": 1,
                "xp": 75.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Rune longsword",
                "id": 1303,
                "level": 91,
                "bars": 2,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune javelin tips",
                "id": 19580,
                "level": 91,
                "bars": 1,
                "xp": 75.0,
                "qty": 5,
                "members": True
            },
            {
                "name": "Rune full helm",
                "id": 1163,
                "level": 92,
                "bars": 2,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune knife",
                "id": 868,
                "level": 92,
                "bars": 1,
                "xp": 75.0,
                "qty": 5,
                "members": True
            },
            {
                "name": "Rune sq shield",
                "id": 1185,
                "level": 93,
                "bars": 2,
                "xp": 150.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune warhammer",
                "id": 1347,
                "level": 94,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune battleaxe",
                "id": 1373,
                "level": 95,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune chainbody",
                "id": 1113,
                "level": 96,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune kiteshield",
                "id": 1201,
                "level": 97,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune claws",
                "id": 3101,
                "level": 98,
                "bars": 2,
                "xp": 150.0,
                "qty": 1,
                "members": True
            },
            {
                "name": "Rune 2h sword",
                "id": 1319,
                "level": 99,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune platelegs",
                "id": 1079,
                "level": 99,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune plateskirt",
                "id": 1093,
                "level": 99,
                "bars": 3,
                "xp": 225.0,
                "qty": 1,
                "members": False
            },
            {
                "name": "Rune platebody",
                "id": 1127,
                "level": 99,
                "bars": 5,
                "xp": 375.0,
                "qty": 1,
                "members": False
            }
        ]
    }
]
