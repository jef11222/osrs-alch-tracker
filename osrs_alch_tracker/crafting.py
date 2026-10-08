"""
Craft & Alch recipes database with materials, required skills, and output items.
Includes comprehensive coverage of:
- Gold Rings, Necklaces, Bracelets, and Amulets
- Amulet Stringing
- Battlestaves
- Dragonhide Bodies, Chaps, and Vambraces
- Bow & Crossbow Fletching
- Silver Jewellery
"""

CRAFTING_RECIPES = [
    # ------------------ GOLD RINGS ------------------
    {
        "name": "Diamond ring",
        "output_id": 1643,
        "skill": "Crafting",
        "level": 43,
        "xp": 85.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1601, "name": "Diamond", "qty": 1}
        ]
    },
    {
        "name": "Ruby ring",
        "output_id": 1641,
        "skill": "Crafting",
        "level": 34,
        "xp": 70.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1603, "name": "Ruby", "qty": 1}
        ]
    },
    {
        "name": "Emerald ring",
        "output_id": 1639,
        "skill": "Crafting",
        "level": 27,
        "xp": 55.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1605, "name": "Emerald", "qty": 1}
        ]
    },
    {
        "name": "Sapphire ring",
        "output_id": 1637,
        "skill": "Crafting",
        "level": 20,
        "xp": 40.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1607, "name": "Sapphire", "qty": 1}
        ]
    },
    {
        "name": "Gold ring",
        "output_id": 1635,
        "skill": "Crafting",
        "level": 5,
        "xp": 15.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1}
        ]
    },
    {
        "name": "Dragonstone ring",
        "output_id": 1645,
        "skill": "Crafting",
        "level": 55,
        "xp": 100.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1615, "name": "Dragonstone", "qty": 1}
        ]
    },
    {
        "name": "Onyx ring",
        "output_id": 6575,
        "skill": "Crafting",
        "level": 67,
        "xp": 115.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 6573, "name": "Onyx", "qty": 1}
        ]
    },

    # ------------------ GOLD NECKLACES ------------------
    {
        "name": "Diamond necklace",
        "output_id": 1662,
        "skill": "Crafting",
        "level": 56,
        "xp": 90.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1601, "name": "Diamond", "qty": 1}
        ]
    },
    {
        "name": "Ruby necklace",
        "output_id": 1660,
        "skill": "Crafting",
        "level": 40,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1603, "name": "Ruby", "qty": 1}
        ]
    },
    {
        "name": "Emerald necklace",
        "output_id": 1658,
        "skill": "Crafting",
        "level": 29,
        "xp": 60.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1605, "name": "Emerald", "qty": 1}
        ]
    },
    {
        "name": "Sapphire necklace",
        "output_id": 1656,
        "skill": "Crafting",
        "level": 22,
        "xp": 55.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1607, "name": "Sapphire", "qty": 1}
        ]
    },
    {
        "name": "Gold necklace",
        "output_id": 1654,
        "skill": "Crafting",
        "level": 6,
        "xp": 20.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1}
        ]
    },
    {
        "name": "Dragon necklace",
        "output_id": 1664,
        "skill": "Crafting",
        "level": 72,
        "xp": 105.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1615, "name": "Dragonstone", "qty": 1}
        ]
    },
    {
        "name": "Onyx necklace",
        "output_id": 6577,
        "skill": "Crafting",
        "level": 82,
        "xp": 120.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 6573, "name": "Onyx", "qty": 1}
        ]
    },

    # ------------------ GOLD BRACELETS ------------------
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
        "output_id": 11092,
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
        "xp": 65.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1605, "name": "Emerald", "qty": 1}
        ]
    },
    {
        "name": "Sapphire bracelet",
        "output_id": 11072,
        "skill": "Crafting",
        "level": 23,
        "xp": 60.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1607, "name": "Sapphire", "qty": 1}
        ]
    },
    {
        "name": "Gold bracelet",
        "output_id": 11069,
        "skill": "Crafting",
        "level": 7,
        "xp": 25.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1}
        ]
    },
    {
        "name": "Onyx bracelet",
        "output_id": 11130,
        "skill": "Crafting",
        "level": 84,
        "xp": 125.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 6573, "name": "Onyx", "qty": 1}
        ]
    },

    # ------------------ AMULETS (CRAFT & STRING) ------------------
    {
        "name": "Diamond amulet",
        "output_id": 1700,
        "skill": "Crafting",
        "level": 70,
        "xp": 104.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1601, "name": "Diamond", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Ruby amulet",
        "output_id": 1698,
        "skill": "Crafting",
        "level": 50,
        "xp": 89.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1603, "name": "Ruby", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Emerald amulet",
        "output_id": 1696,
        "skill": "Crafting",
        "level": 31,
        "xp": 74.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1605, "name": "Emerald", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Sapphire amulet",
        "output_id": 1694,
        "skill": "Crafting",
        "level": 24,
        "xp": 69.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1607, "name": "Sapphire", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Gold amulet",
        "output_id": 1692,
        "skill": "Crafting",
        "level": 8,
        "xp": 34.0,
        "members": False,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Dragonstone amulet",
        "output_id": 1702,
        "skill": "Crafting",
        "level": 80,
        "xp": 154.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 1615, "name": "Dragonstone", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Onyx amulet",
        "output_id": 6581,
        "skill": "Crafting",
        "level": 90,
        "xp": 169.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 6573, "name": "Onyx", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },

    # ------------------ AMULETS (STRINGING ONLY) ------------------
    {
        "name": "Diamond amulet (string)",
        "output_id": 1700,
        "skill": "Crafting",
        "level": 70,
        "xp": 4.0,
        "members": False,
        "materials": [
            {"id": 1681, "name": "Diamond amulet (u)", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Ruby amulet (string)",
        "output_id": 1698,
        "skill": "Crafting",
        "level": 50,
        "xp": 4.0,
        "members": False,
        "materials": [
            {"id": 1679, "name": "Ruby amulet (u)", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Emerald amulet (string)",
        "output_id": 1696,
        "skill": "Crafting",
        "level": 31,
        "xp": 4.0,
        "members": False,
        "materials": [
            {"id": 1677, "name": "Emerald amulet (u)", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Sapphire amulet (string)",
        "output_id": 1694,
        "skill": "Crafting",
        "level": 24,
        "xp": 4.0,
        "members": False,
        "materials": [
            {"id": 1675, "name": "Sapphire amulet (u)", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },
    {
        "name": "Dragonstone amulet (string)",
        "output_id": 1702,
        "skill": "Crafting",
        "level": 80,
        "xp": 4.0,
        "members": True,
        "materials": [
            {"id": 1683, "name": "Dragonstone amulet (u)", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },

    # ------------------ BATTLESTAVES ------------------
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

    # ------------------ DRAGONHIDE BODIES, CHAPS & VAMBRACES ------------------
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
        "name": "Red d'hide vambraces",
        "output_id": 2489,
        "skill": "Crafting",
        "level": 73,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 2507, "name": "Red dragon leather", "qty": 1}
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
        "name": "Blue d'hide vambraces",
        "output_id": 2487,
        "skill": "Crafting",
        "level": 66,
        "xp": 70.0,
        "members": True,
        "materials": [
            {"id": 2505, "name": "Blue dragon leather", "qty": 1}
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
    {
        "name": "Green d'hide vambraces",
        "output_id": 1065,
        "skill": "Crafting",
        "level": 57,
        "xp": 62.0,
        "members": True,
        "materials": [
            {"id": 1745, "name": "Green dragon leather", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (STRINGING BOWS) ------------------
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
        "name": "Magic shortbow (strung)",
        "output_id": 861,
        "skill": "Fletching",
        "level": 80,
        "xp": 83.3,
        "members": True,
        "materials": [
            {"id": 72, "name": "Magic shortbow (u)", "qty": 1},
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
        "name": "Yew shortbow (strung)",
        "output_id": 857,
        "skill": "Fletching",
        "level": 65,
        "xp": 67.5,
        "members": True,
        "materials": [
            {"id": 68, "name": "Yew shortbow (u)", "qty": 1},
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
    {
        "name": "Maple shortbow (strung)",
        "output_id": 853,
        "skill": "Fletching",
        "level": 50,
        "xp": 50.0,
        "members": True,
        "materials": [
            {"id": 64, "name": "Maple shortbow (u)", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (CROSSBOWS) ------------------
    {
        "name": "Rune crossbow",
        "output_id": 9185,
        "skill": "Fletching",
        "level": 69,
        "xp": 100.0,
        "members": True,
        "materials": [
            {"id": 9431, "name": "Runite limbs", "qty": 1},
            {"id": 9452, "name": "Yew stock", "qty": 1},
            {"id": 9438, "name": "Crossbow string", "qty": 1}
        ]
    },

    # ------------------ SILVER JEWELLERY ------------------
    {
        "name": "Tiara",
        "output_id": 5525,
        "skill": "Crafting",
        "level": 23,
        "xp": 52.5,
        "members": False,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1}
        ]
    },
    {
        "name": "Unstrung symbol",
        "output_id": 1714,
        "skill": "Crafting",
        "level": 16,
        "xp": 50.0,
        "members": False,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1}
        ]
    },
    {
        "name": "Unstrung emblem",
        "output_id": 1720,
        "skill": "Crafting",
        "level": 17,
        "xp": 50.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1}
        ]
    },
    {
        "name": "Topaz bracelet",
        "output_id": 21123,
        "skill": "Crafting",
        "level": 38,
        "xp": 75.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1613, "name": "Red topaz", "qty": 1}
        ]
    },
    {
        "name": "Jade bracelet",
        "output_id": 21120,
        "skill": "Crafting",
        "level": 29,
        "xp": 60.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1611, "name": "Jade", "qty": 1}
        ]
    },
    {
        "name": "Opal bracelet",
        "output_id": 21117,
        "skill": "Crafting",
        "level": 22,
        "xp": 45.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1609, "name": "Opal", "qty": 1}
        ]
    },

    # ------------------ SMITHING (RUNITE) ------------------
    {
        "name": "Rune platebody",
        "output_id": 1127,
        "skill": "Smithing",
        "level": 99,
        "xp": 375.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 5}
        ]
    },
    {
        "name": "Rune 2h sword",
        "output_id": 1319,
        "skill": "Smithing",
        "level": 99,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune platelegs",
        "output_id": 1079,
        "skill": "Smithing",
        "level": 99,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune plateskirt",
        "output_id": 1093,
        "skill": "Smithing",
        "level": 99,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune kiteshield",
        "output_id": 1201,
        "skill": "Smithing",
        "level": 97,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune chainbody",
        "output_id": 1113,
        "skill": "Smithing",
        "level": 96,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune battleaxe",
        "output_id": 1373,
        "skill": "Smithing",
        "level": 95,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune warhammer",
        "output_id": 1347,
        "skill": "Smithing",
        "level": 94,
        "xp": 225.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 3}
        ]
    },
    {
        "name": "Rune sq shield",
        "output_id": 1185,
        "skill": "Smithing",
        "level": 93,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 2}
        ]
    },
    {
        "name": "Rune full helm",
        "output_id": 1163,
        "skill": "Smithing",
        "level": 92,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 2}
        ]
    },
    {
        "name": "Rune longsword",
        "output_id": 1303,
        "skill": "Smithing",
        "level": 91,
        "xp": 150.0,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 2}
        ]
    },
    {
        "name": "Rune scimitar",
        "output_id": 1333,
        "skill": "Smithing",
        "level": 90,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 2}
        ]
    },
    {
        "name": "Rune sword",
        "output_id": 1289,
        "skill": "Smithing",
        "level": 89,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },
    {
        "name": "Rune med helm",
        "output_id": 1147,
        "skill": "Smithing",
        "level": 88,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },
    {
        "name": "Rune mace",
        "output_id": 1432,
        "skill": "Smithing",
        "level": 87,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },
    {
        "name": "Rune axe",
        "output_id": 1359,
        "skill": "Smithing",
        "level": 86,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },
    {
        "name": "Rune pickaxe",
        "output_id": 1275,
        "skill": "Smithing",
        "level": 86,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },
    {
        "name": "Rune dagger",
        "output_id": 1213,
        "skill": "Smithing",
        "level": 85,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2363, "name": "Runite bar", "qty": 1}
        ]
    },

    # ------------------ SMITHING (ADAMANTITE) ------------------
    {
        "name": "Adamant platebody",
        "output_id": 1123,
        "skill": "Smithing",
        "level": 88,
        "xp": 312.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 5}
        ]
    },
    {
        "name": "Adamant 2h sword",
        "output_id": 1317,
        "skill": "Smithing",
        "level": 89,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant platelegs",
        "output_id": 1073,
        "skill": "Smithing",
        "level": 86,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant plateskirt",
        "output_id": 1091,
        "skill": "Smithing",
        "level": 86,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant kiteshield",
        "output_id": 1199,
        "skill": "Smithing",
        "level": 87,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant battleaxe",
        "output_id": 1371,
        "skill": "Smithing",
        "level": 85,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant chainbody",
        "output_id": 1111,
        "skill": "Smithing",
        "level": 81,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },

    # ------------------ SMITHING (MITHRIL & STEEL) ------------------
    {
        "name": "Mithril platebody",
        "output_id": 1121,
        "skill": "Smithing",
        "level": 68,
        "xp": 250.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 5}
        ]
    },
    {
        "name": "Steel platebody",
        "output_id": 1119,
        "skill": "Smithing",
        "level": 48,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 5}
        ]
    },

    # ------------------ MAGIC (JEWELLERY ENCHANTING) ------------------
    {
        "name": "Amulet of glory",
        "output_id": 1704,
        "skill": "Magic",
        "level": 68,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 1662, "name": "Dragonstone amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Amulet of power",
        "output_id": 1731,
        "skill": "Magic",
        "level": 57,
        "xp": 67.0,
        "members": False,
        "materials": [
            {"id": 1660, "name": "Diamond amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Amulet of strength",
        "output_id": 1725,
        "skill": "Magic",
        "level": 49,
        "xp": 59.0,
        "members": False,
        "materials": [
            {"id": 1658, "name": "Ruby amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Amulet of defence",
        "output_id": 1729,
        "skill": "Magic",
        "level": 27,
        "xp": 37.0,
        "members": False,
        "materials": [
            {"id": 1656, "name": "Emerald amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Amulet of magic",
        "output_id": 1727,
        "skill": "Magic",
        "level": 7,
        "xp": 17.5,
        "members": False,
        "materials": [
            {"id": 1654, "name": "Sapphire amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ring of wealth",
        "output_id": 2572,
        "skill": "Magic",
        "level": 68,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 1645, "name": "Dragonstone ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ring of life",
        "output_id": 2570,
        "skill": "Magic",
        "level": 57,
        "xp": 67.0,
        "members": True,
        "materials": [
            {"id": 1643, "name": "Diamond ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ring of dueling(8)",
        "output_id": 2552,
        "skill": "Magic",
        "level": 27,
        "xp": 37.0,
        "members": True,
        "materials": [
            {"id": 1639, "name": "Emerald ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Games necklace(8)",
        "output_id": 3853,
        "skill": "Magic",
        "level": 7,
        "xp": 17.5,
        "members": True,
        "materials": [
            {"id": 1654, "name": "Sapphire necklace", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Combat bracelet",
        "output_id": 11126,
        "skill": "Magic",
        "level": 68,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 11115, "name": "Dragonstone bracelet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (SHIELDS) ------------------
    {
        "name": "Magic shield",
        "output_id": 22263,
        "skill": "Fletching",
        "level": 87,
        "xp": 183.0,
        "members": True,
        "materials": [
            {"id": 1513, "name": "Magic logs", "qty": 2}
        ]
    },
    {
        "name": "Yew shield",
        "output_id": 22260,
        "skill": "Fletching",
        "level": 72,
        "xp": 150.0,
        "members": True,
        "materials": [
            {"id": 1515, "name": "Yew logs", "qty": 2}
        ]
    },
    {
        "name": "Maple shield",
        "output_id": 22257,
        "skill": "Fletching",
        "level": 57,
        "xp": 116.5,
        "members": True,
        "materials": [
            {"id": 1517, "name": "Maple logs", "qty": 2}
        ]
    }
]
