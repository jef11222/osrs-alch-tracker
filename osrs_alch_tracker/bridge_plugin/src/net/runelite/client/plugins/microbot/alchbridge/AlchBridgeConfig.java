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

    @ConfigItem(
        keyName = "showOverlay",
        name = "Show In-Game Overlay",
        description = "Display live Alchs/hr and Profit/hr overlay window above inventory",
        position = 3
    )
    default boolean showOverlay() {
        return true;
    }

    @ConfigItem(
        keyName = "showProfit",
        name = "Show Profit / Hr",
        description = "Display estimated profit and profit/hour in the overlay",
        position = 4
    )
    default boolean showProfit() {
        return true;
    }

    @ConfigItem(
        keyName = "showMagicXp",
        name = "Show Magic XP / Hr",
        description = "Display Magic XP gained and XP/hour in the overlay",
        position = 5
    )
    default boolean showMagicXp() {
        return true;
    }

    @ConfigItem(
        keyName = "costBasisMode",
        name = "Profit Cost Basis",
        description = "Calculate alch profit using W308 Player Trade price or Live GE price",
        position = 6
    )
    default CostBasisMode costBasisMode() {
        return CostBasisMode.W308_TRADE;
    }

    @ConfigItem(
        keyName = "manualTradeBuyPrice",
        name = "Manual W308 Buy Price",
        description = "Optional fallback manual price per item if trade window wasn't captured (0 = auto-detect)",
        position = 7
    )
    default int manualTradeBuyPrice() {
        return 0;
    }
}
