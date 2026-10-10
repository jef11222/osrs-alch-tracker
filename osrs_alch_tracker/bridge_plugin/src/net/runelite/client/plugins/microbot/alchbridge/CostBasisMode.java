package net.runelite.client.plugins.microbot.alchbridge;

public enum CostBasisMode {
    W308_TRADE("W308 Trade"),
    GRAND_EXCHANGE("Live GE");

    private final String displayName;

    CostBasisMode(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
