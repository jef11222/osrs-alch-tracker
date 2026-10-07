"""
Craft & Alch recipes database with materials, required skills, and output items.
"""

CRAFTING_RECIPES = [
    # Battlestaves
    {
        "name": "Air battlestaff",
        "output_id": 1397,
        "skill": "Crafting",
        "level": 66,
        "xp": 137.5,
        "members": True,
        "materials": [
            {"id": 1391, "name": "Battlestaff", "qty": 1},
            {"id": 573, "name": "Air orb", "qty": 1}
        ]
    },
    {
        "name": "Fire battlestaff",
        "output_id": 1393,
        "skill": "Crafting",
        "level": 62,
        "xp": 125.0,
        "members": True,
        "materials": [
            {"id": 1391, "name": "Battlestaff", "qty": 1},
            {"id": 569, "name": "Fire orb", "qty": 1}
        ]
    },
    {
        "name": "Water battlestaff",
        "output_id": 1395,
        "skill": "Crafting",
        "level": 54,
        "xp": 100.0,
        "members": True,
        "materials": [
            {"id": 1391, "name": "Battlestaff", "qty": 1},
            {"id": 571, "name": "Water orb", "qty": 1}
        ]
    },
    {
        "name": "Earth battlestaff",
        "output_id": 1399,
        "skill": "Crafting",
        "level": 58,
        "xp": 112.5,
        "members": True,
        "materials": [
            {"id": 1391, "name": "Battlestaff", "qty": 1},
            {"id": 575, "name": "Earth orb", "qty": 1}
        ]
    },

    # Dragonhide Bodies & Chaps
    {
        "name": "Black d'hide body",
        "output_id": 2503,
        "skill": "Crafting",
        "level": 84,
        "xp": 258.0,
        "members": True,
        "materials": [
            {"id": 2509, "name": "Black dragon leather", "qty": 3}
        ]
    },
    {
        "name": "Black d'hide chaps",
        "output_id": 2497,
        "skill": "Crafting",
        "level": 82,
        "xp": 172.0,
        "members": True,
        "materials": [
            {"id": 2509, "name": "Black dragon leather", "qty": 2}
        ]
    },
    {
        "name": "Black d'hide vambraces",
        "output_id": 2491,
        "skill": "Crafting",
        "level": 79,
        "xp": 86.0,
        "members": True,
        "materials": [
            {"id": 2509, "name": "Black dragon leather", "qty": 1}
        ]
    },
    {
        "name": "Red d'hide body",
        "output_id": 2501,
        "skill": "Crafting",
        "level": 77,
        "xp": 234.0,
        "members": True,
        "materials": [
            {"id": 2507, "name": "Red dragon leather", "qty": 3}
        ]
    },
    {
        "name": "Red d'hide chaps",
        "output_id": 2495,
        "skill": "Crafting",
        "level": 73,
        "xp": 156.0,
        "members": True,
        "materials": [
            {"id": 2507, "name": "Red dragon leather", "qty": 2}
        ]
    },
    {
        "name": "Blue d'hide body",
        "output_id": 2499,
        "skill": "Crafting",
        "level": 71,
        "xp": 210.0,
        "members": True,
        "materials": [
            {"id": 2505, "name": "Blue dragon leather", "qty": 3}
        ]
    },
    {
        "name": "Blue d'hide chaps",
        "output_id": 2493,
        "skill": "Crafting",
        "level": 68,
        "xp": 140.0,
        "members": True,
        "materials": [
            {"id": 2505, "name": "Blue dragon leather", "qty": 2}
        ]
    },
    {
        "name": "Green d'hide body",
        "output_id": 1135,
        "skill": "Crafting",
        "level": 63,
        "xp": 186.0,
        "members": True,
        "materials": [
            {"id": 1745, "name": "Green dragon leather", "qty": 3}
        ]
    },
    {
        "name": "Green d'hide chaps",
        "output_id": 1099,
        "skill": "Crafting",
        "level": 60,
        "xp": 124.0,
        "members": True,
        "materials": [
            {"id": 1745, "name": "Green dragon leather", "qty": 2}
        ]
    },

    # Fletching (Stringing Bows)
    {
        "name": "Magic longbow (strung)",
        "output_id": 859,
        "skill": "Fletching",
        "level": 85,
        "xp": 91.5,
        "members": True,
        "materials": [
            {"id": 70, "name": "Magic longbow (u)", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Yew longbow (strung)",
        "output_id": 855,
        "skill": "Fletching",
        "level": 70,
        "xp": 75.0,
        "members": True,
        "materials": [
            {"id": 66, "name": "Yew longbow (u)", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Maple longbow (strung)",
        "output_id": 851,
        "skill": "Fletching",
        "level": 55,
        "xp": 58.2,
        "members": True,
        "materials": [
            {"id": 62, "name": "Maple longbow (u)", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },

    # Jewellery (Bracelets & Necklaces)
    {
        "name": "Dragonstone bracelet",
        "output_id": 11115,
        "skill": "Crafting",
        "level": 74,
        "xp": 110.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1615, "name": "Dragonstone", "qty": 1}
        ]
    },
    {
        "name": "Diamond bracelet",
        "output_id": 11095,
        "skill": "Crafting",
        "level": 58,
        "xp": 95.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1601, "name": "Diamond", "qty": 1}
        ]
    },
    {
        "name": "Ruby bracelet",
        "output_id": 11085,
        "skill": "Crafting",
        "level": 42,
        "xp": 80.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1603, "name": "Ruby", "qty": 1}
        ]
    },
    {
        "name": "Emerald bracelet",
        "output_id": 11076,
        "skill": "Crafting",
        "level": 30,
        "xp": 67.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1605, "name": "Emerald", "qty": 1}
        ]
    },
    {
        "name": "Gold bracelet (F2P)",
        "output_id": 11069,
        "skill": "Crafting",
        "level": 7,
        "xp": 25.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1}
        ]
    }
]
