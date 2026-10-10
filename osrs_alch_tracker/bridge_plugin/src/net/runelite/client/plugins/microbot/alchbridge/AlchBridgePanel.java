package net.runelite.client.plugins.microbot.alchbridge;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.text.NumberFormat;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.PluginPanel;

public class AlchBridgePanel extends PluginPanel {
    private static final Color GOLD = new Color(243, 156, 18);
    private static final Color PROFIT_GREEN = new Color(46, 204, 113);
    private static final Color CARD_BG = new Color(30, 30, 34);
    private static final Color CARD_HOVER = new Color(40, 40, 46);

    private final JLabel statusLabel = new JLabel("Connecting to tracker...");
    private final JLabel bannerLabel = new JLabel("Click item or price to copy");
    private final JPanel listContainer = new JPanel();
    private final NumberFormat numFmt = NumberFormat.getInstance(Locale.US);

    // Inventory Batch UI Elements
    private final JPanel batchCard = new JPanel();
    private final JLabel batchTitleLabel = new JLabel("Alch Batch (Inventory)");
    private final JLabel batchItemLabel = new JLabel("No alchable stack detected");
    private final JLabel batchRunesLabel = new JLabel("Withdraw items to view batch ETA");
    private final JLabel batchEtaLabel = new JLabel("Est. Completion: --");
    private final JLabel batchProfitLabel = new JLabel("Batch Profit: --");
    private final JLabel batchGrossLabel = new JLabel("Magic XP: -- | Gross: --");

    // Skilling Progression UI Elements
    private final JPanel skillingCard = new JPanel();
    private final JLabel skillingTitleLabel = new JLabel("⚡ Skilling Progression");
    private final JLabel skillingActivityLabel = new JLabel("Auto-detecting activity...");
    private final JLabel skillingLevelLabel = new JLabel("Level: -- → --");
    private final JLabel skillingEtaLabel = new JLabel("Est. Next Lvl: --");
    private final JLabel skillingRateLabel = new JLabel("Pace: --");

    public AlchBridgePanel(AlchBridgePlugin plugin) {
        super(false);
        setLayout(new BorderLayout());
        setBackground(ColorScheme.DARK_GRAY_COLOR);

        // Header
        JPanel headerPanel = new JPanel();
        headerPanel.setLayout(new BoxLayout(headerPanel, BoxLayout.Y_AXIS));
        headerPanel.setBorder(new EmptyBorder(10, 10, 8, 10));
        headerPanel.setBackground(ColorScheme.DARKER_GRAY_COLOR);

        JLabel titleLabel = new JLabel("OSRS Alch Tracker");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 15));
        titleLabel.setForeground(GOLD);
        titleLabel.setAlignmentX(CENTER_ALIGNMENT);

        statusLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        statusLabel.setForeground(Color.GRAY);
        statusLabel.setAlignmentX(CENTER_ALIGNMENT);

        bannerLabel.setFont(new Font("Segoe UI", Font.ITALIC, 11));
        bannerLabel.setForeground(new Color(180, 180, 180));
        bannerLabel.setAlignmentX(CENTER_ALIGNMENT);

        JPanel btnRow = new JPanel(new BorderLayout());
        btnRow.setOpaque(false);
        btnRow.setBorder(new EmptyBorder(6, 0, 0, 0));

        JButton refreshBtn = new JButton("🔄 Refresh Top 10");
        refreshBtn.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        refreshBtn.setFocusPainted(false);
        refreshBtn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        refreshBtn.addActionListener(e -> plugin.fetchTop10Async());
        btnRow.add(refreshBtn, BorderLayout.CENTER);

        headerPanel.add(titleLabel);
        headerPanel.add(Box.createVerticalStrut(3));
        headerPanel.add(statusLabel);
        headerPanel.add(Box.createVerticalStrut(4));
        headerPanel.add(bannerLabel);
        headerPanel.add(btnRow);

        JPanel topContainer = new JPanel();
        topContainer.setLayout(new BoxLayout(topContainer, BoxLayout.Y_AXIS));
        topContainer.setBackground(ColorScheme.DARK_GRAY_COLOR);
        topContainer.add(headerPanel);
        topContainer.add(Box.createVerticalStrut(6));
        topContainer.add(createBatchCard());
        topContainer.add(Box.createVerticalStrut(4));
        topContainer.add(createSkillingProgressionCard());
        topContainer.add(Box.createVerticalStrut(4));

        add(topContainer, BorderLayout.NORTH);

        // Content List Container
        listContainer.setLayout(new BoxLayout(listContainer, BoxLayout.Y_AXIS));
        listContainer.setBackground(ColorScheme.DARK_GRAY_COLOR);
        listContainer.setBorder(new EmptyBorder(6, 6, 6, 6));

        showEmptyState("Waiting for Alch Tracker data...\nMake sure the Python app is open.");

        JScrollPane scrollPane = new JScrollPane(listContainer);
        scrollPane.setBackground(ColorScheme.DARK_GRAY_COLOR);
        scrollPane.setBorder(null);
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        add(scrollPane, BorderLayout.CENTER);
    }

    private void showEmptyState(String msg) {
        listContainer.removeAll();
        JLabel emptyLabel = new JLabel("<html><center>" + msg.replace("\n", "<br>") + "</center></html>");
        emptyLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        emptyLabel.setForeground(Color.GRAY);
        emptyLabel.setHorizontalAlignment(SwingConstants.CENTER);
        emptyLabel.setAlignmentX(CENTER_ALIGNMENT);
        listContainer.add(Box.createVerticalStrut(20));
        listContainer.add(emptyLabel);
        listContainer.revalidate();
        listContainer.repaint();
    }

    public void updateTop10(List<Map<String, Object>> items, boolean connected) {
        SwingUtilities.invokeLater(() -> {
            if (!connected) {
                statusLabel.setText("🔴 Tracker Offline (Port 18833)");
                statusLabel.setForeground(new Color(231, 76, 60));
                showEmptyState("Cannot reach Alch Tracker app.\nCheck that the tracker is running.");
                return;
            }

            statusLabel.setText("🟢 Connected to Alch Tracker");
            statusLabel.setForeground(PROFIT_GREEN);

            if (items == null || items.isEmpty()) {
                showEmptyState("No profitable items found matching current filters.");
                return;
            }

            listContainer.removeAll();
            int rank = 1;
            for (Map<String, Object> it : items) {
                String name = String.valueOf(it.getOrDefault("name", "Unknown"));
                long buyPrice = parseLong(it.get("buy_price"));
                long alchVal = parseLong(it.get("alch_value"));
                long profitEa = parseLong(it.get("profit_ea"));
                long limit = parseLong(it.get("limit"));
                long vol5m = parseLong(it.get("vol_5m"));

                JPanel card = createItemCard(rank++, name, buyPrice, alchVal, profitEa, limit, vol5m);
                listContainer.add(card);
                listContainer.add(Box.createVerticalStrut(6));
            }

            listContainer.revalidate();
            listContainer.repaint();
        });
    }

    private JPanel createItemCard(int rank, String name, long buyPrice, long alchVal, long profitEa, long limit, long vol5m) {
        JPanel card = new JPanel();
        card.setLayout(new BoxLayout(card, BoxLayout.Y_AXIS));
        card.setBackground(CARD_BG);
        card.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(50, 50, 56), 1),
            new EmptyBorder(6, 8, 6, 8)
        ));

        // Line 1: Rank + Name (Click to copy name)
        JPanel line1 = new JPanel(new BorderLayout());
        line1.setOpaque(false);

        JLabel rankLabel = new JLabel("#" + rank + " ");
        rankLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        rankLabel.setForeground(GOLD);

        JLabel nameLabel = new JLabel(name);
        nameLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        nameLabel.setForeground(Color.WHITE);
        nameLabel.setCursor(new Cursor(Cursor.HAND_CURSOR));
        nameLabel.setToolTipText("Click to copy item name to clipboard");
        nameLabel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                copyText(name, "Copied name: " + name);
            }
        });

        line1.add(rankLabel, BorderLayout.WEST);
        line1.add(nameLabel, BorderLayout.CENTER);

        // Line 2: Target Buy Price (Click to copy price) + Copy Button
        JPanel line2 = new JPanel(new BorderLayout());
        line2.setOpaque(false);
        line2.setBorder(new EmptyBorder(3, 0, 2, 0));

        JLabel buyLabel = new JLabel("Buy: " + numFmt.format(buyPrice) + " gp");
        buyLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        buyLabel.setForeground(new Color(52, 152, 219));
        buyLabel.setCursor(new Cursor(Cursor.HAND_CURSOR));
        buyLabel.setToolTipText("Click to copy buy offer price to clipboard");
        buyLabel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                copyText(String.valueOf(buyPrice), "Copied price: " + buyPrice);
            }
        });

        JButton copyBtn = new JButton("Copy Price");
        copyBtn.setFont(new Font("Segoe UI", Font.PLAIN, 10));
        copyBtn.setFocusPainted(false);
        copyBtn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        copyBtn.setPreferredSize(new Dimension(80, 20));
        copyBtn.addActionListener(e -> copyText(String.valueOf(buyPrice), "Copied price: " + buyPrice));

        line2.add(buyLabel, BorderLayout.CENTER);
        line2.add(copyBtn, BorderLayout.EAST);

        // Line 3: High Alch + Profit
        JPanel line3 = new JPanel(new GridLayout(1, 2));
        line3.setOpaque(false);

        JLabel alchLabel = new JLabel("Alch: " + numFmt.format(alchVal) + " gp");
        alchLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        alchLabel.setForeground(new Color(241, 196, 15));

        JLabel profitLabel = new JLabel("+" + numFmt.format(profitEa) + " gp ea", SwingConstants.RIGHT);
        profitLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        profitLabel.setForeground(PROFIT_GREEN);

        line3.add(alchLabel);
        line3.add(profitLabel);

        // Line 4: Limit + 5m Volume
        JPanel line4 = new JPanel(new BorderLayout());
        line4.setOpaque(false);
        line4.setBorder(new EmptyBorder(2, 0, 0, 0));

        String volStr = vol5m > 0 ? (vol5m + " sold (5m)") : "0 sold (5m)";
        JLabel metaLabel = new JLabel("Limit: " + numFmt.format(limit) + " | " + volStr);
        metaLabel.setFont(new Font("Segoe UI", Font.PLAIN, 10));
        metaLabel.setForeground(new Color(150, 150, 150));
        line4.add(metaLabel, BorderLayout.CENTER);

        card.add(line1);
        card.add(line2);
        card.add(line3);
        card.add(line4);

        // Card hover highlight
        card.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                card.setBackground(CARD_HOVER);
            }
            @Override
            public void mouseExited(MouseEvent e) {
                card.setBackground(CARD_BG);
            }
        });

        return card;
    }

    private void copyText(String text, String bannerMsg) {
        StringSelection sel = new StringSelection(text);
        Clipboard cb = Toolkit.getDefaultToolkit().getSystemClipboard();
        cb.setContents(sel, sel);

        bannerLabel.setText("✓ " + bannerMsg);
        bannerLabel.setForeground(PROFIT_GREEN);
    }

    private JPanel createBatchCard() {
        batchCard.setLayout(new BoxLayout(batchCard, BoxLayout.Y_AXIS));
        batchCard.setBackground(CARD_BG);
        batchCard.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createEmptyBorder(0, 6, 0, 6),
            BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(55, 55, 62), 1),
                new EmptyBorder(7, 8, 7, 8)
            )
        ));

        batchTitleLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        batchTitleLabel.setForeground(GOLD);
        batchTitleLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchItemLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        batchItemLabel.setForeground(Color.LIGHT_GRAY);
        batchItemLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchRunesLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        batchRunesLabel.setForeground(new Color(170, 170, 170));
        batchRunesLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchEtaLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        batchEtaLabel.setForeground(Color.GRAY);
        batchEtaLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchProfitLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        batchProfitLabel.setForeground(Color.GRAY);
        batchProfitLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchGrossLabel.setFont(new Font("Segoe UI", Font.PLAIN, 10));
        batchGrossLabel.setForeground(new Color(130, 130, 130));
        batchGrossLabel.setAlignmentX(LEFT_ALIGNMENT);

        batchCard.add(batchTitleLabel);
        batchCard.add(Box.createVerticalStrut(3));
        batchCard.add(batchItemLabel);
        batchCard.add(Box.createVerticalStrut(2));
        batchCard.add(batchRunesLabel);
        batchCard.add(Box.createVerticalStrut(3));
        batchCard.add(batchEtaLabel);
        batchCard.add(Box.createVerticalStrut(2));
        batchCard.add(batchProfitLabel);
        batchCard.add(Box.createVerticalStrut(2));
        batchCard.add(batchGrossLabel);

        return batchCard;
    }

    private JPanel createSkillingProgressionCard() {
        skillingCard.setLayout(new BoxLayout(skillingCard, BoxLayout.Y_AXIS));
        skillingCard.setBackground(CARD_BG);
        skillingCard.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createEmptyBorder(0, 6, 0, 6),
            BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(41, 128, 185), 1),
                new EmptyBorder(7, 8, 7, 8)
            )
        ));

        skillingTitleLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        skillingTitleLabel.setForeground(new Color(0, 229, 255));
        skillingTitleLabel.setAlignmentX(LEFT_ALIGNMENT);

        skillingActivityLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        skillingActivityLabel.setForeground(Color.LIGHT_GRAY);
        skillingActivityLabel.setAlignmentX(LEFT_ALIGNMENT);

        skillingLevelLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        skillingLevelLabel.setForeground(new Color(170, 170, 170));
        skillingLevelLabel.setAlignmentX(LEFT_ALIGNMENT);

        skillingEtaLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        skillingEtaLabel.setForeground(new Color(105, 240, 174));
        skillingEtaLabel.setAlignmentX(LEFT_ALIGNMENT);

        skillingRateLabel.setFont(new Font("Segoe UI", Font.PLAIN, 10));
        skillingRateLabel.setForeground(new Color(160, 160, 160));
        skillingRateLabel.setAlignmentX(LEFT_ALIGNMENT);

        skillingCard.add(skillingTitleLabel);
        skillingCard.add(Box.createVerticalStrut(3));
        skillingCard.add(skillingActivityLabel);
        skillingCard.add(Box.createVerticalStrut(2));
        skillingCard.add(skillingLevelLabel);
        skillingCard.add(Box.createVerticalStrut(3));
        skillingCard.add(skillingEtaLabel);
        skillingCard.add(Box.createVerticalStrut(2));
        skillingCard.add(skillingRateLabel);

        return skillingCard;
    }

    public void updateSkillingProgression(
        String skillName, String activityName,
        int curLvl, int nextLvl, int remXp,
        double xpHr, long estSeconds
    ) {
        SwingUtilities.invokeLater(() -> {
            if (skillName == null || skillName.isEmpty()) {
                skillingActivityLabel.setText("Auto-detecting activity...");
                skillingActivityLabel.setForeground(Color.GRAY);
                skillingLevelLabel.setText("Level: -- → --");
                skillingEtaLabel.setText("Est. Next Lvl: --");
                skillingRateLabel.setText("Pace: --");
                return;
            }

            skillingTitleLabel.setText("⚡ " + skillName + " Progression");
            skillingActivityLabel.setText(activityName != null && !activityName.isEmpty() ? activityName : (skillName + " Training"));
            skillingActivityLabel.setForeground(Color.WHITE);

            skillingLevelLabel.setText(String.format("Level %d → %d (%s XP left)", curLvl, nextLvl, numFmt.format(remXp)));
            skillingLevelLabel.setForeground(new Color(220, 220, 220));

            if (estSeconds > 0) {
                skillingEtaLabel.setText(String.format("Est. Next Lvl: %s", formatDuration(estSeconds)));
                skillingEtaLabel.setForeground(new Color(105, 240, 174));
            } else {
                skillingEtaLabel.setText("Est. Next Lvl: Calculating...");
                skillingEtaLabel.setForeground(Color.GRAY);
            }

            if (xpHr > 1000) {
                skillingRateLabel.setText(String.format("Live Pace: %,d XP/hr", (int) Math.round(xpHr)));
                skillingRateLabel.setForeground(new Color(255, 235, 59));
            } else {
                skillingRateLabel.setText("Pace: Warming up...");
                skillingRateLabel.setForeground(new Color(140, 140, 140));
            }
        });
    }

    public void updateInventoryBatch(
        List<AlchBridgePlugin.BatchItemEntry> entries, int totalQty,
        long totalProfit, long grossGp, long estSeconds,
        int natRunes, String fireSource, int alchsPerHour
    ) {
        SwingUtilities.invokeLater(() -> {
            if (entries == null || entries.isEmpty() || totalQty <= 0) {
                batchTitleLabel.setText("Alch Batch (Inventory)");
                batchItemLabel.setText("No alchable stack detected");
                batchItemLabel.setForeground(Color.GRAY);
                batchItemLabel.setToolTipText(null);
                batchCard.setToolTipText(null);
                batchRunesLabel.setText("Withdraw items to view batch ETA");
                batchRunesLabel.setForeground(new Color(110, 110, 110));
                batchEtaLabel.setText("Est. Completion: --");
                batchEtaLabel.setForeground(Color.GRAY);
                batchProfitLabel.setText("Batch Profit: --");
                batchProfitLabel.setForeground(Color.GRAY);
                batchGrossLabel.setText("Magic XP: -- | Gross: --");
                batchGrossLabel.setForeground(new Color(110, 110, 110));
                return;
            }

            int distinctTypes = entries.size();
            if (distinctTypes == 1) {
                batchTitleLabel.setText("Alch Batch (Inventory)");
                AlchBridgePlugin.BatchItemEntry single = entries.get(0);
                String notedTag = single.isNoted ? " (noted)" : "";
                batchItemLabel.setText(String.format("%,dx %s%s", single.qty, single.name, notedTag));
                batchItemLabel.setForeground(Color.WHITE);
                batchItemLabel.setToolTipText(null);
                batchCard.setToolTipText(null);

                String profStr = totalProfit >= 0 ? ("+" + formatGp(totalProfit)) : formatGp(totalProfit);
                String profEaStr = single.profitEa >= 0 ? ("+" + numFmt.format(single.profitEa)) : numFmt.format(single.profitEa);
                batchProfitLabel.setText(String.format("Batch Profit: %s (%s ea)", profStr, profEaStr));
            } else {
                batchTitleLabel.setText(String.format("Alch Batch (%d Item Types)", distinctTypes));
                batchItemLabel.setText(String.format("%,dx Alchables (%d types)", totalQty, distinctTypes));
                batchItemLabel.setForeground(Color.WHITE);

                StringBuilder tooltip = new StringBuilder("<html><b>Inventory Batch (")
                    .append(String.format("%,d", totalQty)).append(" items, ").append(distinctTypes).append(" types):</b><br/>");
                for (AlchBridgePlugin.BatchItemEntry e : entries) {
                    String pEaStr = e.profitEa >= 0 ? ("+" + numFmt.format(e.profitEa)) : numFmt.format(e.profitEa);
                    tooltip.append("• ").append(String.format("%,dx %s", e.qty, e.name))
                           .append(" <font color='#aaaaaa'>(").append(pEaStr).append(" ea)</font><br/>");
                }
                tooltip.append("</html>");
                batchItemLabel.setToolTipText(tooltip.toString());
                batchCard.setToolTipText(tooltip.toString());

                int avgProfitEa = (int) Math.round((double) totalProfit / (double) totalQty);
                String profStr = totalProfit >= 0 ? ("+" + formatGp(totalProfit)) : formatGp(totalProfit);
                String avgEaStr = avgProfitEa >= 0 ? ("+" + numFmt.format(avgProfitEa)) : numFmt.format(avgProfitEa);
                batchProfitLabel.setText(String.format("Batch Profit: %s (avg %s ea)", profStr, avgEaStr));
            }

            // Nature runes & Fire status
            String natStatus;
            if (natRunes >= totalQty) {
                natStatus = String.format("Nats: %,d/%,d [OK]", natRunes, totalQty);
            } else {
                int def = totalQty - natRunes;
                natStatus = String.format("Nats: %,d/%,d [Need %,d]", natRunes, totalQty, def);
            }
            batchRunesLabel.setText(String.format("%s | Fire: %s", natStatus, fireSource));
            batchRunesLabel.setForeground(natRunes >= totalQty ? new Color(189, 195, 199) : new Color(255, 183, 77));

            // Est. Completion ETA
            String timeStr = formatDuration(estSeconds);
            String speedTag = (alchsPerHour > 600) ? String.format("@ %,d/hr", alchsPerHour) : "@ 1.2k/hr";
            batchEtaLabel.setText(String.format("Est. Completion: %s (%s)", timeStr, speedTag));
            batchEtaLabel.setForeground(new Color(0, 220, 255));

            batchProfitLabel.setForeground(totalProfit >= 0 ? PROFIT_GREEN : new Color(231, 76, 60));

            long totalXp = (long) totalQty * 65L;
            batchGrossLabel.setText(String.format("Magic XP: +%,d XP | Gross: %s", totalXp, formatGp(grossGp)));
            batchGrossLabel.setForeground(new Color(160, 160, 160));
        });
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

    private long parseLong(Object obj) {
        if (obj == null) return 0;
        if (obj instanceof Number) return ((Number) obj).longValue();
        try {
            return Long.parseLong(String.valueOf(obj).trim());
        } catch (Exception e) {
            return 0;
        }
    }
}
