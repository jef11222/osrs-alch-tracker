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
        getMenuEntries().add(new OverlayMenuEntry(MenuAction.RUNELITE_OVERLAY, "Reset", "Alch Session"));
    }

    @Override
    public Dimension render(Graphics2D graphics) {
        if (!config.showOverlay()) {
            return null;
        }

        panelComponent.setPreferredSize(new Dimension(180, 0));
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
        panelComponent.getChildren().add(LineComponent.builder()
            .left("Alchs/hr:")
            .right(alchs > 0 ? String.format("%,d / hr", alchsPerHour) : "--")
            .rightColor(new Color(0, 220, 255))
            .build());

        // Profit / Hour
        if (config.showProfit()) {
            long profitPerHour = plugin.getProfitPerHour();
            Color profitColor = profitPerHour >= 0 ? new Color(76, 175, 80) : new Color(244, 67, 54);
            panelComponent.getChildren().add(LineComponent.builder()
                .left("Profit/hr:")
                .right(alchs > 0 ? (profitPerHour >= 0 ? "+" : "") + formatGp(profitPerHour) + " / hr" : "--")
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

        // Magic XP / Hour
        if (config.showMagicXp()) {
            int xpPerHour = plugin.getXpPerHour();
            panelComponent.getChildren().add(LineComponent.builder()
                .left("XP/hr:")
                .right(alchs > 0 ? String.format("%,d / hr", xpPerHour) : "--")
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
