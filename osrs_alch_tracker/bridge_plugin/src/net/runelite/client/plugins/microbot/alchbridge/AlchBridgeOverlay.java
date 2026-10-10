package net.runelite.client.plugins.microbot.alchbridge;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import javax.inject.Inject;
import net.runelite.api.MenuAction;
import net.runelite.client.ui.overlay.OverlayMenuEntry;
import net.runelite.client.ui.overlay.OverlayPanel;
import net.runelite.client.ui.overlay.OverlayPosition;
import net.runelite.client.ui.overlay.OverlayPriority;
import net.runelite.client.ui.overlay.components.LineComponent;
import net.runelite.client.ui.overlay.components.TitleComponent;

public class AlchBridgeOverlay extends OverlayPanel {
    private final AlchBridgePlugin plugin;
    private final AlchBridgeConfig config;

    @Inject
    public AlchBridgeOverlay(AlchBridgePlugin plugin, AlchBridgeConfig config) {
        super(plugin);
        this.plugin = plugin;
        this.config = config;
        setPosition(OverlayPosition.BOTTOM_RIGHT);
        setPriority(OverlayPriority.MED);
        getMenuEntries().add(new OverlayMenuEntry(MenuAction.RUNELITE_OVERLAY, "Toggle Bond Tracker", "Alch Session"));
        getMenuEntries().add(new OverlayMenuEntry(MenuAction.RUNELITE_OVERLAY, "Toggle Cost Basis", "Alch Session"));
        getMenuEntries().add(new OverlayMenuEntry(MenuAction.RUNELITE_OVERLAY, "Reset", "Alch Session"));
    }

    @Override
    public Dimension render(Graphics2D graphics) {
        if (!config.showOverlay()) {
            return null;
        }

        panelComponent.setPreferredSize(new Dimension(185, 0));
        panelComponent.getChildren().clear();

        // Header Title
        panelComponent.getChildren().add(TitleComponent.builder()
            .text("OSRS Alch Tracker")
            .color(new Color(243, 156, 18))
            .build());

        int alchs = plugin.getSessionAlchs();
        boolean isActive = plugin.isSessionActive();
        String statusText = alchs == 0 ? "Idle" : (isActive ? "Alching \uD83D\uDFE2" : "Paused \u23F8\uFE0F");
        Color statusColor = alchs == 0 ? Color.GRAY : (isActive ? new Color(76, 175, 80) : new Color(255, 193, 7));

        // Alchs Count & Status
        panelComponent.getChildren().add(LineComponent.builder()
            .left("Alchs:")
            .right(String.format("%,d", alchs))
            .rightColor(Color.WHITE)
            .build());

        panelComponent.getChildren().add(LineComponent.builder()
            .left("Status:")
            .right(statusText)
            .rightColor(statusColor)
            .build());

        panelComponent.getChildren().add(LineComponent.builder()
            .left("Time:")
            .right(plugin.getFormattedSessionTime())
            .rightColor(Color.WHITE)
            .build());

        // Alchs / Hour
        int alchsPerHour = plugin.getAlchsPerHour();
        String alchsHrStr = alchs < 3 ? "Warming up..." : String.format("%,d / hr", alchsPerHour);
        panelComponent.getChildren().add(LineComponent.builder()
            .left("Alchs/hr:")
            .right(alchsHrStr)
            .rightColor(new Color(0, 220, 255))
            .build());

        // Remaining Batch ETA (if items detected in inventory)
        if (plugin.getBatchItemQty() > 0) {
            long remSec = plugin.getBatchEstSeconds();
            String timeStr = formatDuration(remSec);
            panelComponent.getChildren().add(LineComponent.builder()
                .left("Batch ETA:")
                .right(String.format("%s (%,d)", timeStr, plugin.getBatchItemQty()))
                .rightColor(new Color(255, 183, 77)) // Soft Orange
                .build());
        }

        // Cost Basis Mode (W308 Trade vs Live GE)
        CostBasisMode mode = plugin.getCostBasisMode();
        String basisText;
        Color basisColor;
        if (mode == CostBasisMode.W308_TRADE) {
            int price = plugin.getActiveW308Price();
            if (price > 0) {
                basisText = String.format("W308 (%,d gp)", price);
            } else {
                basisText = "W308 Trade";
            }
            basisColor = new Color(255, 179, 0);
        } else {
            basisText = "Live GE";
            basisColor = new Color(79, 195, 247);
        }

        panelComponent.getChildren().add(LineComponent.builder()
            .left("Basis:")
            .right(basisText)
            .rightColor(basisColor)
            .build());

        // Profit / Hour
        if (config.showProfit()) {
            long profitPerHour = plugin.getProfitPerHour();
            Color profitColor = profitPerHour >= 0 ? new Color(76, 175, 80) : new Color(244, 67, 54);
            String profitHrStr = alchs < 3 ? "--" : ((profitPerHour >= 0 ? "+" : "") + formatGp(profitPerHour) + " / hr");
            panelComponent.getChildren().add(LineComponent.builder()
                .left("Profit/hr:")
                .right(profitHrStr)
                .rightColor(profitColor)
                .build());

            long totalProfit = plugin.getSessionProfit();
            Color totalProfColor = totalProfit >= 0 ? new Color(76, 175, 80) : new Color(244, 67, 54);
            panelComponent.getChildren().add(LineComponent.builder()
                .left("Net Profit:")
                .right((totalProfit >= 0 ? "+" : "") + formatGp(totalProfit))
                .rightColor(totalProfColor)
                .build());
        }

        // Bond Progress & Live ETA
        if (plugin.isBondTrackerEnabled()) {
            long totalCoins = plugin.getTotalCoins();
            long bondPrice = plugin.getBondPrice();
            double bondPct = bondPrice > 0 ? ((double) totalCoins / (double) bondPrice * 100.0) : 0.0;
            String bondText;
            Color bondColor;

            if (totalCoins >= bondPrice) {
                bondText = String.format("Ready! (%.1fM)", totalCoins / 1_000_000.0);
                bondColor = new Color(46, 204, 113); // Bright Green
            } else {
                bondText = String.format("%.1fM / %.1fM (%.1f%%)", totalCoins / 1_000_000.0, bondPrice / 1_000_000.0, bondPct);
                bondColor = bondPct >= 50.0 ? new Color(255, 193, 7) : new Color(255, 152, 0); // Gold or Orange
            }

            panelComponent.getChildren().add(LineComponent.builder()
                .left("Bond:")
                .right(bondText)
                .rightColor(bondColor)
                .build());

            long profitPerHour = plugin.getProfitPerHour();
            if (totalCoins < bondPrice && profitPerHour > 0) {
                long remGp = bondPrice - totalCoins;
                double hrs = (double) remGp / (double) profitPerHour;
                String etaText = hrs >= 24.0 ? String.format("~%.1f days", hrs / 24.0) : String.format("~%.1f hrs", hrs);
                panelComponent.getChildren().add(LineComponent.builder()
                    .left("Bond ETA:")
                    .right(etaText)
                    .rightColor(new Color(186, 104, 200)) // Pastel Purple
                    .build());
            }
        }

        // Magic XP / Hour
        if (config.showMagicXp()) {
            int xpPerHour = plugin.getXpPerHour();
            String xpHrStr = alchs < 3 ? "--" : String.format("%,d / hr", xpPerHour);
            panelComponent.getChildren().add(LineComponent.builder()
                .left("XP/hr:")
                .right(xpHrStr)
                .rightColor(new Color(255, 235, 59))
                .build());
        }

        // Last Alched Item
        String lastItem = plugin.getLastAlchedItem();
        if (lastItem != null && !lastItem.isEmpty()) {
            panelComponent.getChildren().add(LineComponent.builder()
                .left("Last:")
                .right(lastItem)
                .rightColor(Color.LIGHT_GRAY)
                .build());
        }

        return super.render(graphics);
    }

    private String formatDuration(long seconds) {
        if (seconds <= 0) return "0s";
        long h = seconds / 3600;
        long m = (seconds % 3600) / 60;
        long s = seconds % 60;
        if (h > 0) {
            return String.format("%dh %02dm", h, m);
        } else if (m > 0) {
            return String.format("%dm %02ds", m, s);
        } else {
            return String.format("%ds", s);
        }
    }

    private String formatGp(long amount) {
        long abs = Math.abs(amount);
        if (abs >= 1_000_000) {
            return String.format("%.2fM gp", amount / 1_000_000.0);
        } else if (abs >= 1_000) {
            return String.format("%.1fk gp", amount / 1_000.0);
        } else {
            return String.format("%,d gp", amount);
        }
    }
}
