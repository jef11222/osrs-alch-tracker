package net.runelite.client.plugins.microbot.alchbridge;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;

@ConfigGroup("alchbridge")
public interface AlchBridgeConfig extends Config {
    @ConfigItem(
        keyName = "bridgePort",
        name = "Dashboard Port",
        description = "Local port where OSRS Alch Dashboard listens (default: 18833)",
        position = 0
    )
    default int bridgePort() {
        return 18833;
    }

    @ConfigItem(
        keyName = "syncCashAndRunes",
        name = "Sync Coins & Nature Runes",
        description = "Automatically report Coins and Nature Runes count to dashboard",
        position = 1
    )
    default boolean syncCashAndRunes() {
        return true;
    }

    @ConfigItem(
        keyName = "trackAlchCasts",
        name = "Track Alch Casts",
        description = "Detect Magic XP drops (+65 XP) to track active High Alch casts",
        position = 2
    )
    default boolean trackAlchCasts() {
        return true;
    }
}
