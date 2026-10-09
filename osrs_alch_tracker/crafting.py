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
    },

    # ------------------ SMITHING (STEEL, MITHRIL & ADAMANT EXPANSION) ------------------
    {
        "name": "Steel warhammer",
        "output_id": 1339,
        "skill": "Smithing",
        "level": 35,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel 2h sword",
        "output_id": 1311,
        "skill": "Smithing",
        "level": 44,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel battleaxe",
        "output_id": 1365,
        "skill": "Smithing",
        "level": 40,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel platelegs",
        "output_id": 1069,
        "skill": "Smithing",
        "level": 46,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel plateskirt",
        "output_id": 1083,
        "skill": "Smithing",
        "level": 46,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel kiteshield",
        "output_id": 1193,
        "skill": "Smithing",
        "level": 42,
        "xp": 112.5,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 3}
        ]
    },
    {
        "name": "Steel scimitar",
        "output_id": 1325,
        "skill": "Smithing",
        "level": 35,
        "xp": 75.0,
        "members": False,
        "materials": [
            {"id": 2353, "name": "Steel bar", "qty": 2}
        ]
    },
    {
        "name": "Mithril 2h sword",
        "output_id": 1315,
        "skill": "Smithing",
        "level": 69,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril platelegs",
        "output_id": 1071,
        "skill": "Smithing",
        "level": 66,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril plateskirt",
        "output_id": 1085,
        "skill": "Smithing",
        "level": 66,
        "xp": 150.0,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril kiteshield",
        "output_id": 1197,
        "skill": "Smithing",
        "level": 67,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril battleaxe",
        "output_id": 1369,
        "skill": "Smithing",
        "level": 65,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril warhammer",
        "output_id": 1343,
        "skill": "Smithing",
        "level": 64,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril chainbody",
        "output_id": 1109,
        "skill": "Smithing",
        "level": 61,
        "xp": 150.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 3}
        ]
    },
    {
        "name": "Mithril full helm",
        "output_id": 1159,
        "skill": "Smithing",
        "level": 62,
        "xp": 100.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 2}
        ]
    },
    {
        "name": "Mithril scimitar",
        "output_id": 1329,
        "skill": "Smithing",
        "level": 60,
        "xp": 100.0,
        "members": False,
        "materials": [
            {"id": 2359, "name": "Mithril bar", "qty": 2}
        ]
    },
    {
        "name": "Adamant warhammer",
        "output_id": 1345,
        "skill": "Smithing",
        "level": 84,
        "xp": 187.5,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 3}
        ]
    },
    {
        "name": "Adamant sq shield",
        "output_id": 1183,
        "skill": "Smithing",
        "level": 83,
        "xp": 125.0,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 2}
        ]
    },
    {
        "name": "Adamant full helm",
        "output_id": 1161,
        "skill": "Smithing",
        "level": 82,
        "xp": 125.0,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 2}
        ]
    },
    {
        "name": "Adamant scimitar",
        "output_id": 1331,
        "skill": "Smithing",
        "level": 80,
        "xp": 125.0,
        "members": False,
        "materials": [
            {"id": 2361, "name": "Adamantite bar", "qty": 2}
        ]
    },
    {
        "name": "Iron platebody",
        "output_id": 1115,
        "skill": "Smithing",
        "level": 33,
        "xp": 125.0,
        "members": False,
        "materials": [
            {"id": 2351, "name": "Iron bar", "qty": 5}
        ]
    },
    {
        "name": "Bronze platebody",
        "output_id": 1117,
        "skill": "Smithing",
        "level": 18,
        "xp": 62.5,
        "members": False,
        "materials": [
            {"id": 2349, "name": "Bronze bar", "qty": 5}
        ]
    },

    # ------------------ CRAFTING (ZENYTE END-GAME JEWELLERY) ------------------
    {
        "name": "Zenyte ring",
        "output_id": 19538,
        "skill": "Crafting",
        "level": 89,
        "xp": 150.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 19493, "name": "Zenyte", "qty": 1}
        ]
    },
    {
        "name": "Zenyte necklace",
        "output_id": 19535,
        "skill": "Crafting",
        "level": 92,
        "xp": 165.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 19493, "name": "Zenyte", "qty": 1}
        ]
    },
    {
        "name": "Zenyte bracelet",
        "output_id": 19532,
        "skill": "Crafting",
        "level": 95,
        "xp": 180.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 19493, "name": "Zenyte", "qty": 1}
        ]
    },
    {
        "name": "Zenyte amulet",
        "output_id": 19541,
        "skill": "Crafting",
        "level": 98,
        "xp": 200.0,
        "members": True,
        "materials": [
            {"id": 2357, "name": "Gold bar", "qty": 1},
            {"id": 19493, "name": "Zenyte", "qty": 1},
            {"id": 1759, "name": "Ball of wool", "qty": 1}
        ]
    },

    # ------------------ CRAFTING (SILVER JEWELLERY & LEATHER) ------------------
    {
        "name": "Opal ring",
        "output_id": 21081,
        "skill": "Crafting",
        "level": 1,
        "xp": 10.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1609, "name": "Opal", "qty": 1}
        ]
    },
    {
        "name": "Opal necklace",
        "output_id": 21090,
        "skill": "Crafting",
        "level": 16,
        "xp": 35.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1609, "name": "Opal", "qty": 1}
        ]
    },
    {
        "name": "Jade ring",
        "output_id": 21084,
        "skill": "Crafting",
        "level": 13,
        "xp": 32.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1611, "name": "Jade", "qty": 1}
        ]
    },
    {
        "name": "Jade necklace",
        "output_id": 21093,
        "skill": "Crafting",
        "level": 25,
        "xp": 54.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1611, "name": "Jade", "qty": 1}
        ]
    },
    {
        "name": "Topaz ring",
        "output_id": 21087,
        "skill": "Crafting",
        "level": 16,
        "xp": 35.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1613, "name": "Red topaz", "qty": 1}
        ]
    },
    {
        "name": "Topaz necklace",
        "output_id": 21096,
        "skill": "Crafting",
        "level": 32,
        "xp": 70.0,
        "members": True,
        "materials": [
            {"id": 2355, "name": "Silver bar", "qty": 1},
            {"id": 1613, "name": "Red topaz", "qty": 1}
        ]
    },
    {
        "name": "Leather body",
        "output_id": 1129,
        "skill": "Crafting",
        "level": 14,
        "xp": 25.0,
        "members": False,
        "materials": [
            {"id": 1741, "name": "Leather", "qty": 1}
        ]
    },
    {
        "name": "Hardleather body",
        "output_id": 1131,
        "skill": "Crafting",
        "level": 28,
        "xp": 35.0,
        "members": False,
        "materials": [
            {"id": 1743, "name": "Hard leather", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (FULL BOW CRAFTING FROM LOGS) ------------------
    {
        "name": "Magic longbow (from log)",
        "output_id": 859,
        "skill": "Fletching",
        "level": 85,
        "xp": 183.0,
        "members": True,
        "materials": [
            {"id": 1513, "name": "Magic logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Magic shortbow (from log)",
        "output_id": 861,
        "skill": "Fletching",
        "level": 80,
        "xp": 166.5,
        "members": True,
        "materials": [
            {"id": 1513, "name": "Magic logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Yew longbow (from log)",
        "output_id": 855,
        "skill": "Fletching",
        "level": 70,
        "xp": 150.0,
        "members": True,
        "materials": [
            {"id": 1515, "name": "Yew logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Yew shortbow (from log)",
        "output_id": 857,
        "skill": "Fletching",
        "level": 65,
        "xp": 135.0,
        "members": True,
        "materials": [
            {"id": 1515, "name": "Yew logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Maple longbow (from log)",
        "output_id": 851,
        "skill": "Fletching",
        "level": 55,
        "xp": 116.5,
        "members": True,
        "materials": [
            {"id": 1517, "name": "Maple logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Maple shortbow (from log)",
        "output_id": 853,
        "skill": "Fletching",
        "level": 50,
        "xp": 100.0,
        "members": True,
        "materials": [
            {"id": 1517, "name": "Maple logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Willow longbow (from log)",
        "output_id": 847,
        "skill": "Fletching",
        "level": 40,
        "xp": 83.0,
        "members": True,
        "materials": [
            {"id": 1519, "name": "Willow logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },
    {
        "name": "Oak longbow (from log)",
        "output_id": 845,
        "skill": "Fletching",
        "level": 25,
        "xp": 50.0,
        "members": True,
        "materials": [
            {"id": 1521, "name": "Oak logs", "qty": 1},
            {"id": 1777, "name": "Bow string", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (UNSTRUNG BOW CUTTING) ------------------
    {
        "name": "Magic longbow (u)",
        "output_id": 70,
        "skill": "Fletching",
        "level": 85,
        "xp": 91.5,
        "members": True,
        "materials": [
            {"id": 1513, "name": "Magic logs", "qty": 1}
        ]
    },
    {
        "name": "Magic shortbow (u)",
        "output_id": 72,
        "skill": "Fletching",
        "level": 80,
        "xp": 83.3,
        "members": True,
        "materials": [
            {"id": 1513, "name": "Magic logs", "qty": 1}
        ]
    },
    {
        "name": "Yew longbow (u)",
        "output_id": 66,
        "skill": "Fletching",
        "level": 70,
        "xp": 75.0,
        "members": True,
        "materials": [
            {"id": 1515, "name": "Yew logs", "qty": 1}
        ]
    },
    {
        "name": "Yew shortbow (u)",
        "output_id": 68,
        "skill": "Fletching",
        "level": 65,
        "xp": 67.5,
        "members": True,
        "materials": [
            {"id": 1515, "name": "Yew logs", "qty": 1}
        ]
    },
    {
        "name": "Maple longbow (u)",
        "output_id": 62,
        "skill": "Fletching",
        "level": 55,
        "xp": 58.2,
        "members": True,
        "materials": [
            {"id": 1517, "name": "Maple logs", "qty": 1}
        ]
    },

    # ------------------ FLETCHING (CROSSBOW EXPANSION) ------------------
    {
        "name": "Dragon crossbow",
        "output_id": 21902,
        "skill": "Fletching",
        "level": 78,
        "xp": 135.0,
        "members": True,
        "materials": [
            {"id": 21918, "name": "Dragon limbs", "qty": 1},
            {"id": 9454, "name": "Magic stock", "qty": 1},
            {"id": 9438, "name": "Crossbow string", "qty": 1}
        ]
    },
    {
        "name": "Adamant crossbow",
        "output_id": 9183,
        "skill": "Fletching",
        "level": 61,
        "xp": 82.0,
        "members": True,
        "materials": [
            {"id": 9429, "name": "Adamantite limbs", "qty": 1},
            {"id": 9450, "name": "Maple stock", "qty": 1},
            {"id": 9438, "name": "Crossbow string", "qty": 1}
        ]
    },
    {
        "name": "Mithril crossbow",
        "output_id": 9181,
        "skill": "Fletching",
        "level": 54,
        "xp": 64.0,
        "members": True,
        "materials": [
            {"id": 9427, "name": "Mithril limbs", "qty": 1},
            {"id": 9448, "name": "Willow stock", "qty": 1},
            {"id": 9438, "name": "Crossbow string", "qty": 1}
        ]
    },
    {
        "name": "Steel crossbow",
        "output_id": 9179,
        "skill": "Fletching",
        "level": 46,
        "xp": 54.0,
        "members": True,
        "materials": [
            {"id": 9425, "name": "Steel limbs", "qty": 1},
            {"id": 9446, "name": "Oak stock", "qty": 1},
            {"id": 9438, "name": "Crossbow string", "qty": 1}
        ]
    },

    # ------------------ MAGIC (ZENYTE & ONYX ENCHANTMENTS) ------------------
    {
        "name": "Amulet of torture (enchant)",
        "output_id": 19553,
        "skill": "Magic",
        "level": 93,
        "xp": 110.0,
        "members": True,
        "materials": [
            {"id": 19541, "name": "Zenyte amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1},
            {"id": 565, "name": "Blood rune", "qty": 20}
        ]
    },
    {
        "name": "Necklace of anguish (enchant)",
        "output_id": 19547,
        "skill": "Magic",
        "level": 93,
        "xp": 110.0,
        "members": True,
        "materials": [
            {"id": 19535, "name": "Zenyte necklace", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1},
            {"id": 565, "name": "Blood rune", "qty": 20}
        ]
    },
    {
        "name": "Tormented bracelet (enchant)",
        "output_id": 19544,
        "skill": "Magic",
        "level": 93,
        "xp": 110.0,
        "members": True,
        "materials": [
            {"id": 19532, "name": "Zenyte bracelet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1},
            {"id": 565, "name": "Blood rune", "qty": 20}
        ]
    },
    {
        "name": "Ring of suffering (enchant)",
        "output_id": 19550,
        "skill": "Magic",
        "level": 93,
        "xp": 110.0,
        "members": True,
        "materials": [
            {"id": 19538, "name": "Zenyte ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1},
            {"id": 565, "name": "Blood rune", "qty": 20}
        ]
    },
    {
        "name": "Amulet of fury",
        "output_id": 6585,
        "skill": "Magic",
        "level": 87,
        "xp": 97.0,
        "members": True,
        "materials": [
            {"id": 6581, "name": "Onyx amulet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Berserker necklace",
        "output_id": 11128,
        "skill": "Magic",
        "level": 87,
        "xp": 97.0,
        "members": True,
        "materials": [
            {"id": 6577, "name": "Onyx necklace", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Regen bracelet",
        "output_id": 11133,
        "skill": "Magic",
        "level": 87,
        "xp": 97.0,
        "members": True,
        "materials": [
            {"id": 11130, "name": "Onyx bracelet", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ring of stone",
        "output_id": 6583,
        "skill": "Magic",
        "level": 87,
        "xp": 97.0,
        "members": True,
        "materials": [
            {"id": 6575, "name": "Onyx ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ring of recoil",
        "output_id": 2550,
        "skill": "Magic",
        "level": 7,
        "xp": 17.5,
        "members": False,
        "materials": [
            {"id": 1637, "name": "Sapphire ring", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Skills necklace(4)",
        "output_id": 11105,
        "skill": "Magic",
        "level": 68,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 1664, "name": "Dragon necklace", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },

    # ------------------ MAGIC (ENCHANTED CROSSBOW BOLTS) ------------------
    {
        "name": "Onyx bolts (e)",
        "output_id": 9245,
        "skill": "Magic",
        "level": 87,
        "xp": 97.0,
        "members": True,
        "materials": [
            {"id": 9342, "name": "Onyx bolts", "qty": 1},
            {"id": 560, "name": "Death rune", "qty": 1}
        ]
    },
    {
        "name": "Dragonstone bolts (e)",
        "output_id": 9244,
        "skill": "Magic",
        "level": 68,
        "xp": 78.0,
        "members": True,
        "materials": [
            {"id": 9341, "name": "Dragonstone bolts", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Diamond bolts (e)",
        "output_id": 9243,
        "skill": "Magic",
        "level": 57,
        "xp": 67.0,
        "members": True,
        "materials": [
            {"id": 9340, "name": "Diamond bolts", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    },
    {
        "name": "Ruby bolts (e)",
        "output_id": 9242,
        "skill": "Magic",
        "level": 49,
        "xp": 59.0,
        "members": True,
        "materials": [
            {"id": 9339, "name": "Ruby bolts", "qty": 1},
            {"id": 564, "name": "Cosmic rune", "qty": 1}
        ]
    }
]
