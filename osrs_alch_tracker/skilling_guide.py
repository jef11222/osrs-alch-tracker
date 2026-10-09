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

# -------------------------------------------------------------
# SKILL PROGRESSION & QUEST DATABASE
# -------------------------------------------------------------

SKILLING_GUIDES = {
    "Smithing": {
        "icon": "⚒️",
        "quests": [
            {
                "name": "The Knight's Sword",
                "members": False,
                "xp": 12725,
                "skip": "Skips Level 1 ➔ 29 instantly! (12,725 XP)",
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
                "verdict": "⚡ Instant 1➔29 Skip: Do this quest first! Never waste gold smithing Bronze."
            },
            {
                "min_lvl": 29,
                "max_lvl": 35,
                "name": "Iron platebody (Smith + Alch)",
                "item_name": "Iron platebody",
                "output_id": 1115,
                "members": False,
                "xp_per_action": 125.0,
                "materials": [{"id": 2351, "name": "Iron bar", "qty": 5}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 65000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "🔨 Cheap anvil training at Varrock West to bridge into Cannonballs/Steel."
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
                "materials": [{"id": 2353, "name": "Steel bar", "qty": 1}],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 14000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "💰 Passive AFK Profit: 1 Steel bar makes 4 cannonballs. Steady GP earner on GE."
            },
            {
                "min_lvl": 35,
                "max_lvl": 48,
                "name": "Steel warhammer (Smith + Alch)",
                "item_name": "Steel warhammer",
                "output_id": 1339,
                "members": False,
                "xp_per_action": 112.5,
                "materials": [{"id": 2353, "name": "Steel bar", "qty": 3}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 80000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "⚡ Fast 3-bar method to reach Level 48 Steel platebodies."
            },
            {
                "min_lvl": 48,
                "max_lvl": 68,
                "name": "Steel platebody (Smith + Alch)",
                "item_name": "Steel platebody",
                "output_id": 1119,
                "members": False,
                "xp_per_action": 187.5,
                "materials": [{"id": 2353, "name": "Steel bar", "qty": 5}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 135000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "👑 High volume staple: 5 bars = 1,200 gp alch floor. Fast XP with low loss."
            },
            {
                "min_lvl": 68,
                "max_lvl": 88,
                "name": "Mithril platebody (Smith + Alch)",
                "item_name": "Mithril platebody",
                "output_id": 1121,
                "members": False,
                "xp_per_action": 250.0,
                "materials": [{"id": 2359, "name": "Mithril bar", "qty": 5}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 180000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "⚡ Premier mid-level XP rate: High smith speed at Varrock anvil."
            },
            {
                "min_lvl": 88,
                "max_lvl": 99,
                "name": "Adamant platebody (Smith + Alch)",
                "item_name": "Adamant platebody",
                "output_id": 1123,
                "members": False,
                "xp_per_action": 312.5,
                "materials": [{"id": 2361, "name": "Adamantite bar", "qty": 5}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 225000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "💰 Top Tier Method: 9,984 gp alch floor frequently yields net PROFIT on live GE!"
            },
            {
                "min_lvl": 99,
                "max_lvl": 99,
                "name": "Rune 2h sword / Platelegs",
                "item_name": "Rune 2h sword",
                "output_id": 1319,
                "members": False,
                "xp_per_action": 225.0,
                "materials": [{"id": 2363, "name": "Runite bar", "qty": 3}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 160000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "👑 Master Profit: 38,400 gp alch floor. Earns millions of GP while grinding post-99."
            }
        ]
    },

    "Fletching": {
        "icon": "🏹",
        "quests": [
            {
                "name": "The Tourist Trap",
                "members": True,
                "xp": 9300,
                "skip": "Skips Level 1 ➔ 26 instantly! (9,300 XP)",
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
                "xp_rate": 35000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "⚡ Instant 1➔26 Skip: Put both reward books into Fletching to skip low-tier bows."
            },
            {
                "min_lvl": 1,
                "max_lvl": 20,
                "name": "Headless arrows (AFK Alternative)",
                "item_name": "Headless arrow",
                "output_id": 53,
                "output_qty": 15,
                "members": True,
                "xp_per_action": 15.0,
                "materials": [{"id": 52, "name": "Arrow shaft", "qty": 15}, {"id": 314, "name": "Feather", "qty": 15}],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 45000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "☕ Chill AFK: Combine shafts and feathers. Easy zero-loss early training."
            },
            {
                "min_lvl": 20,
                "max_lvl": 35,
                "name": "Oak longbow (u + s)",
                "item_name": "Oak longbow",
                "output_id": 845,
                "members": True,
                "xp_per_action": 50.0,
                "materials": [{"id": 1521, "name": "Oak log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 75000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "🏹 Cut logs into unstrung bows, then string with bowstrings for double XP."
            },
            {
                "min_lvl": 35,
                "max_lvl": 50,
                "name": "Willow longbow (u + s)",
                "item_name": "Willow longbow",
                "output_id": 847,
                "members": True,
                "xp_per_action": 83.0,
                "materials": [{"id": 1519, "name": "Willow log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 110000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "⚡ High speed bow cutting. Willow logs are dirt cheap on the GE."
            },
            {
                "min_lvl": 50,
                "max_lvl": 55,
                "name": "Maple shortbow (u + s)",
                "item_name": "Maple shortbow",
                "output_id": 853,
                "members": True,
                "xp_per_action": 100.0,
                "materials": [{"id": 1517, "name": "Maple log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 135000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "🏹 5-level bridge into Maple longbows. Very cheap raw maple logs."
            },
            {
                "min_lvl": 55,
                "max_lvl": 70,
                "name": "Maple longbow (u + s)",
                "item_name": "Maple longbow",
                "output_id": 851,
                "members": True,
                "xp_per_action": 116.5,
                "materials": [{"id": 1517, "name": "Maple log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 150000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "👑 Excellent mid-tier staple: Maple logs cost ~8 gp. Huge XP for almost nothing."
            },
            {
                "min_lvl": 55,
                "max_lvl": 70,
                "name": "Broad arrows (Ultra Fast XP)",
                "item_name": "Broad arrows",
                "output_id": 4160,
                "output_qty": 10,
                "members": True,
                "xp_per_action": 150.0,
                "materials": [{"id": 11874, "name": "Broad arrowheads", "qty": 10}, {"id": 53, "name": "Headless arrow", "qty": 10}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 450000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "⚡ Ultra-Fast 450k XP/hr: Untradeable ammo creation. High speed click training."
            },
            {
                "min_lvl": 70,
                "max_lvl": 85,
                "name": "Yew longbow (Fletch + Alch)",
                "item_name": "Yew longbow",
                "output_id": 855,
                "members": True,
                "xp_per_action": 150.0,
                "materials": [{"id": 1515, "name": "Yew log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 165000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "💰 Profit / Break-even King: 768 gp alch value covers logs, strings, and runes!"
            },
            {
                "min_lvl": 85,
                "max_lvl": 99,
                "name": "Magic longbow (Fletch + Alch)",
                "item_name": "Magic longbow",
                "output_id": 859,
                "members": True,
                "xp_per_action": 183.0,
                "materials": [{"id": 1513, "name": "Magic log", "qty": 1}, {"id": 1777, "name": "Bow string", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 185000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "👑 1,536 gp Alch Value: Consistently profitable all the way from Level 85 to 99!"
            }
        ]
    },

    "Crafting": {
        "icon": "🔨",
        "quests": [
            {
                "name": "Misthalin Mystery",
                "members": False,
                "xp": 600,
                "skip": "Skips Level 1 ➔ 8 (600 XP)",
                "reqs": "None (F2P)",
                "wiki_slug": "Misthalin_Mystery",
                "tip": "Short 10-minute F2P quest. Skips early leather gloves."
            },
            {
                "name": "Murder Mystery",
                "members": True,
                "xp": 1406,
                "skip": "Skips Level 8 ➔ 16 (1,406 XP)",
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
                "xp_rate": 25000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "⚡ Instant 1➔8 Skip: Zero requirement F2P quest."
            },
            {
                "min_lvl": 1,
                "max_lvl": 20,
                "name": "Cut Sapphire (Gems)",
                "item_name": "Sapphire",
                "output_id": 1607,
                "members": False,
                "xp_per_action": 50.0,
                "materials": [{"id": 1623, "name": "Uncut sapphire", "qty": 1}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 140000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "💎 Cut uncut gems with chisel. Very fast early leveling."
            },
            {
                "min_lvl": 20,
                "max_lvl": 46,
                "name": "Sapphire ring (Craft + Alch)",
                "item_name": "Sapphire ring",
                "output_id": 1637,
                "members": False,
                "xp_per_action": 40.0,
                "materials": [{"id": 2357, "name": "Gold bar", "qty": 1}, {"id": 1607, "name": "Sapphire", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 60000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "💰 900 gp alch floor covers bar + cut gem with positive margin."
            },
            {
                "min_lvl": 34,
                "max_lvl": 46,
                "name": "Ruby ring (Craft + Alch)",
                "item_name": "Ruby ring",
                "output_id": 1641,
                "members": False,
                "xp_per_action": 70.0,
                "materials": [{"id": 2357, "name": "Gold bar", "qty": 1}, {"id": 1603, "name": "Ruby", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 85000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "💰 1,215 gp alch floor. Reliable profit craft."
            },
            {
                "min_lvl": 46,
                "max_lvl": 66,
                "name": "Unpowered orb (Glassblowing AFK)",
                "item_name": "Unpowered orb",
                "output_id": 567,
                "members": True,
                "xp_per_action": 52.5,
                "materials": [{"id": 1775, "name": "Molten glass", "qty": 1}],
                "nature_cost": 0,
                "style": "afk",
                "xp_rate": 95000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "☕ Ultimate AFK: Blow molten glass with glassblowing pipe. Low cost, relaxed clicks."
            },
            {
                "min_lvl": 56,
                "max_lvl": 66,
                "name": "Diamond necklace (Craft + Alch)",
                "item_name": "Diamond necklace",
                "output_id": 1662,
                "members": False,
                "xp_per_action": 90.0,
                "materials": [{"id": 2357, "name": "Gold bar", "qty": 1}, {"id": 1601, "name": "Diamond", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 105000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "💰 2,400 gp alch value. Excellent GP yield per batch."
            },
            {
                "min_lvl": 63,
                "max_lvl": 71,
                "name": "Green d'hide body (Craft + Alch)",
                "item_name": "Green d'hide body",
                "output_id": 1135,
                "members": True,
                "xp_per_action": 186.0,
                "materials": [{"id": 1745, "name": "Green dragon leather", "qty": 3}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 280000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "⚡ Massive 280k XP/hr: 4,680 gp alch value. Fast dragonhide body crafting."
            },
            {
                "min_lvl": 66,
                "max_lvl": 99,
                "name": "Air battlestaff (Premier Meta)",
                "item_name": "Air battlestaff",
                "output_id": 1397,
                "members": True,
                "xp_per_action": 137.5,
                "materials": [{"id": 1391, "name": "Battlestaff", "qty": 1}, {"id": 573, "name": "Air orb", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 335000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "👑 Premier 335k XP/hr Meta: 9,300 gp alch floor + 18,000 limit. The king of Crafting."
            },
            {
                "min_lvl": 77,
                "max_lvl": 99,
                "name": "Red d'hide body (Craft + Alch)",
                "item_name": "Red d'hide body",
                "output_id": 2501,
                "members": True,
                "xp_per_action": 234.0,
                "materials": [{"id": 2507, "name": "Red dragon leather", "qty": 3}],
                "nature_cost": 1,
                "style": "fast",
                "xp_rate": 350000,
                "can_alch": True,
                "can_sell_ge": True,
                "verdict": "⚡ High Tier Speed: 6,738 gp alch value. 350k XP/hr burst training."
            }
        ]
    },

    "Magic": {
        "icon": "✨",
        "quests": [
            {
                "name": "Imp Catcher",
                "members": False,
                "xp": 875,
                "skip": "Skips Level 1 ➔ 8 (875 XP)",
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
                "verdict": "⚡ Instant 1➔8 Skip with beads, then Wind/Fire Strike to reach Level 15."
            },
            {
                "min_lvl": 15,
                "max_lvl": 55,
                "name": "Fire Bolt / Splashing / Teleports",
                "item_name": "Fire Bolt / Teleports",
                "output_id": 0,
                "members": False,
                "xp_per_action": 22.5,
                "materials": [{"id": 562, "name": "Chaos rune", "qty": 1}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 50000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "🪄 Train with Chaos gauntlets or spam Varrock/Falador/Camelot teleports."
            },
            {
                "min_lvl": 27,
                "max_lvl": 55,
                "name": "Enchant Sapphire/Emerald/Ruby",
                "item_name": "Ring of recoil (Enchant)",
                "output_id": 2550,
                "members": False,
                "xp_per_action": 37.0,
                "materials": [{"id": 1637, "name": "Sapphire ring", "qty": 1}, {"id": 564, "name": "Cosmic rune", "qty": 1}],
                "nature_cost": 0,
                "style": "profit",
                "xp_rate": 65000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "💰 Profitable Magic: Enchanting jewellery with Cosmic runes yields solid profits on GE."
            },
            {
                "min_lvl": 55,
                "max_lvl": 99,
                "name": "High Level Alchemy (Master Training)",
                "item_name": "High Alchemy Spell",
                "output_id": 561,
                "members": False,
                "xp_per_action": 65.0,
                "materials": [{"id": 561, "name": "Nature rune", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 78000,
                "can_alch": True,
                "can_sell_ge": False,
                "verdict": "👑 78,000 XP/hr (1,200 casts/hr): 100% PROFITABLE with dashboard items all the way to 99!"
            },
            {
                "min_lvl": 70,
                "max_lvl": 99,
                "name": "Ice Burst / Barrage (Maniacal Monkeys)",
                "item_name": "Ice Burst Spell",
                "output_id": 560,
                "members": True,
                "xp_per_action": 180.0,
                "materials": [{"id": 560, "name": "Death rune", "qty": 2}, {"id": 562, "name": "Chaos rune", "qty": 4}],
                "nature_cost": 0,
                "style": "fast",
                "xp_rate": 280000,
                "can_alch": False,
                "can_sell_ge": False,
                "verdict": "⚡ 280k-350k XP/hr: Multi-target combat bursting in MM2 tunnels. High rune cost."
            },
            {
                "min_lvl": 86,
                "max_lvl": 99,
                "name": "Plank Make (Lunar Utility)",
                "item_name": "Plank Make Spell",
                "output_id": 90,
                "members": True,
                "xp_per_action": 90.0,
                "materials": [{"id": 9075, "name": "Astral rune", "qty": 2}, {"id": 561, "name": "Nature rune", "qty": 1}, {"id": 1511, "name": "Logs", "qty": 1}],
                "nature_cost": 1,
                "style": "profit",
                "xp_rate": 90000,
                "can_alch": False,
                "can_sell_ge": True,
                "verdict": "💰 Profitable Lunar Spell: Convert logs to planks on GE for profit + 90 XP per cast."
            }
        ]
    }
}
