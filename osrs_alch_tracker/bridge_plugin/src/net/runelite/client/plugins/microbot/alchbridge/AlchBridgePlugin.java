package net.runelite.client.plugins.microbot.alchbridge;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.google.inject.Provides;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.lang.reflect.Type;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import javax.inject.Inject;
import net.runelite.api.Client;
import net.runelite.api.GameState;
import net.runelite.api.GrandExchangeOffer;
import net.runelite.api.GrandExchangeOfferState;
import net.runelite.api.InventoryID;
import net.runelite.api.ItemContainer;
import net.runelite.api.ItemID;
import net.runelite.api.Player;
import net.runelite.api.Skill;
import net.runelite.api.WorldType;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.GrandExchangeOfferChanged;
import net.runelite.api.events.ItemContainerChanged;
import net.runelite.api.events.StatChanged;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.game.ItemManager;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.ui.ClientToolbar;
import net.runelite.client.ui.NavigationButton;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@PluginDescriptor(
    name = "<html>[<font color=green>A</font>] Alch Dashboard Bridge",
    description = "Pipes live GE trades, 4h timers, cash stack, nature runes, and provides in-game Top 10 Alchs side panel",
    tags = {"alch", "ge", "tracker", "bridge", "dashboard", "microbot", "panel"},
    enabledByDefault = true
)
public class AlchBridgePlugin extends Plugin {
    private static final Logger log = LoggerFactory.getLogger(AlchBridgePlugin.class);

    @Inject
    private Client client;

    @Inject
    private ItemManager itemManager;

    @Inject
    private AlchBridgeConfig config;

    @Inject
    private Gson gson;

    @Inject
    private ClientToolbar clientToolbar;

    @Inject
    private ConfigManager configManager;

    private AlchBridgePanel panel;
    private NavigationButton navButton;

    private HttpClient httpClient;
    private ExecutorService httpExecutor;
    private ScheduledExecutorService pollerExecutor;

    private final Map<Integer, String> lastOfferState = new ConcurrentHashMap<>();
    private final Map<Integer, Integer> lastOfferQty = new ConcurrentHashMap<>();
    private int lastMagicXp = -1;
    private int lastCoins = -1;
    private int lastNatureRunes = -1;

    @Provides
    AlchBridgeConfig provideConfig(ConfigManager configManager) {
        return configManager.getConfig(AlchBridgeConfig.class);
    }

    @Override
    protected void startUp() {
        httpExecutor = Executors.newSingleThreadExecutor();
        httpClient = HttpClient.newBuilder()
            .executor(httpExecutor)
            .connectTimeout(Duration.ofMillis(800))
            .build();

        // Create in-game sidebar panel
        panel = new AlchBridgePanel(this);
        navButton = NavigationButton.builder()
            .tooltip("Alch Tracker - Top 10 Flips")
            .icon(createIcon())
            .priority(6)
            .panel(panel)
            .build();
        clientToolbar.addNavigation(navButton);

        // Start background poller to fetch Top 10 items from Python tracker every 3 seconds
        pollerExecutor = Executors.newSingleThreadScheduledExecutor();
        pollerExecutor.scheduleWithFixedDelay(this::fetchTop10Async, 1, 3, TimeUnit.SECONDS);

        log.info("Alch Dashboard Bridge plugin started (Port: {})", config.bridgePort());

        if (client.getGameState() == GameState.LOGGED_IN) {
            sendAccountSnapshot();
        }
    }

    @Override
    protected void shutDown() {
        if (clientToolbar != null && navButton != null) {
            clientToolbar.removeNavigation(navButton);
        }
        if (pollerExecutor != null && !pollerExecutor.isShutdown()) {
            pollerExecutor.shutdownNow();
        }
        if (httpExecutor != null && !httpExecutor.isShutdown()) {
            httpExecutor.shutdownNow();
        }
        lastOfferState.clear();
        lastOfferQty.clear();
        lastMagicXp = -1;
        lastCoins = -1;
        lastNatureRunes = -1;
        log.info("Alch Dashboard Bridge plugin stopped");
    }

    public void fetchTop10Async() {
        if (httpClient == null) return;
        try {
            int port = config.bridgePort();
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:" + port + "/api/top10"))
                .timeout(Duration.ofMillis(1200))
                .GET()
                .build();

            httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(resp -> {
                    if (resp.statusCode() == 200) {
                        Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
                        List<Map<String, Object>> items = gson.fromJson(resp.body(), listType);
                        if (panel != null) {
                            panel.updateTop10(items, true);
                        }
                    } else {
                        if (panel != null) {
                            panel.updateTop10(null, false);
                        }
                    }
                })
                .exceptionally(ex -> {
                    if (panel != null) {
                        panel.updateTop10(null, false);
                    }
                    return null;
                });
        } catch (Exception e) {
            if (panel != null) {
                panel.updateTop10(null, false);
            }
        }
    }

    private BufferedImage createIcon() {
        BufferedImage image = new BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(new Color(243, 156, 18));
        g.fillOval(1, 1, 14, 14);
        g.setColor(new Color(211, 84, 0));
        g.drawOval(1, 1, 14, 14);
        g.setColor(Color.WHITE);
        g.setFont(new Font("SansSerif", Font.BOLD, 10));
        FontMetrics fm = g.getFontMetrics();
        int x = (16 - fm.stringWidth("A")) / 2;
        int y = ((16 - fm.getHeight()) / 2) + fm.getAscent();
        g.drawString("A", x, y);
        g.dispose();
        return image;
    }

    private String getAccountName() {
        Player local = client.getLocalPlayer();
        if (local != null && local.getName() != null && !local.getName().isEmpty()) {
            return local.getName();
        }
        return "Unknown";
    }

    private boolean isMembersWorld() {
        try {
            return client.getWorldType() != null && client.getWorldType().contains(WorldType.MEMBERS);
        } catch (Exception e) {
            return true;
        }
    }

    @Subscribe
    public void onGameStateChanged(GameStateChanged event) {
        if (event.getGameState() == GameState.LOGGED_IN) {
            sendAccountSnapshot();
        }
    }

    @Subscribe
    public void onGrandExchangeOfferChanged(GrandExchangeOfferChanged event) {
        GrandExchangeOffer offer = event.getOffer();
        int slot = event.getSlot();

        GrandExchangeOfferState state = offer.getState();
        if (state == GrandExchangeOfferState.EMPTY) {
            lastOfferState.remove(slot);
            lastOfferQty.remove(slot);
            Map<String, Object> data = new HashMap<>();
            data.put("event", "GE_OFFER");
            data.put("account", getAccountName());
            data.put("slot", slot);
            data.put("state", "EMPTY");
            sendPayload(data);
            return;
        }

        String stateName = state.name();
        String lastState = lastOfferState.get(slot);
        int qtySold = offer.getQuantitySold();
        int lastQty = lastOfferQty.getOrDefault(slot, -1);

        if (stateName.equals(lastState) && qtySold == lastQty) {
            return;
        }
        lastOfferState.put(slot, stateName);
        lastOfferQty.put(slot, qtySold);

        // Track BUY offers (active BUYING, completed BOUGHT, or cancelled partial CANCELLED_BUY)
        if (state == GrandExchangeOfferState.BUYING 
            || state == GrandExchangeOfferState.BOUGHT 
            || state == GrandExchangeOfferState.CANCELLED_BUY) {
            int itemId = offer.getItemId();
            if (itemId <= 0) {
                return;
            }
            String itemName = itemManager.getItemComposition(itemId).getName();

            Map<String, Object> data = new HashMap<>();
            data.put("event", "GE_OFFER");
            data.put("account", getAccountName());
            data.put("slot", slot);
            data.put("state", stateName);
            data.put("itemId", itemId);
            data.put("itemName", itemName);
            data.put("price", offer.getPrice());
            data.put("spent", offer.getSpent());
            data.put("quantitySold", qtySold);
            data.put("totalQuantity", offer.getTotalQuantity());
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);

            if (state == GrandExchangeOfferState.BOUGHT || state == GrandExchangeOfferState.CANCELLED_BUY) {
                syncGrandExchangeLimitsAndTrades();
            }
        }
    }

    @Subscribe
    public void onItemContainerChanged(ItemContainerChanged event) {
        if (!config.syncCashAndRunes()) {
            return;
        }

        if (event.getContainerId() == InventoryID.INVENTORY.getId()) {
            ItemContainer inv = event.getItemContainer();
            int coins = inv.count(ItemID.COINS_995);
            int natureRunes = inv.count(ItemID.NATURE_RUNE);

            if (coins != lastCoins || natureRunes != lastNatureRunes) {
                lastCoins = coins;
                lastNatureRunes = natureRunes;

                Map<String, Object> data = new HashMap<>();
                data.put("event", "INVENTORY_SYNC");
                data.put("account", getAccountName());
                data.put("coins", coins);
                data.put("natureRunes", natureRunes);
                data.put("timestamp", System.currentTimeMillis() / 1000.0);

                sendPayload(data);
            }
        } else if (event.getContainerId() == InventoryID.BANK.getId()) {
            ItemContainer bank = event.getItemContainer();
            int coins = bank.count(ItemID.COINS_995);
            int natureRunes = bank.count(ItemID.NATURE_RUNE);

            Map<String, Object> data = new HashMap<>();
            data.put("event", "BANK_SYNC");
            data.put("account", getAccountName());
            data.put("bankCoins", coins);
            data.put("bankNatureRunes", natureRunes);
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);
        }
    }

    @Subscribe
    public void onStatChanged(StatChanged event) {
        Skill skill = event.getSkill();
        if (skill == Skill.MAGIC && config.trackAlchCasts()) {
            int currentXp = event.getXp();
            if (lastMagicXp > 0) {
                int diff = currentXp - lastMagicXp;
                if (diff == 65) {
                    Map<String, Object> data = new HashMap<>();
                    data.put("event", "ALCH_CAST");
                    data.put("account", getAccountName());
                    data.put("xpGained", 65);
                    data.put("magicLevel", event.getLevel());
                    data.put("timestamp", System.currentTimeMillis() / 1000.0);
                    sendPayload(data);
                }
            }
            lastMagicXp = currentXp;
        }

        if (skill == Skill.CRAFTING || skill == Skill.FLETCHING || skill == Skill.MAGIC || skill == Skill.SMITHING) {
            Map<String, Object> data = new HashMap<>();
            data.put("event", "SKILLS_SYNC");
            data.put("account", getAccountName());
            data.put("crafting", client.getRealSkillLevel(Skill.CRAFTING));
            data.put("smithing", client.getRealSkillLevel(Skill.SMITHING));
            data.put("fletching", client.getRealSkillLevel(Skill.FLETCHING));
            data.put("magic", client.getRealSkillLevel(Skill.MAGIC));
            data.put("timestamp", System.currentTimeMillis() / 1000.0);
            sendPayload(data);
        }
    }

    private void sendAccountSnapshot() {
        try {
            Map<String, Object> data = new HashMap<>();
            data.put("event", "ACCOUNT_SNAPSHOT");
            data.put("account", getAccountName());
            data.put("world", client.getWorld());
            data.put("isMembers", isMembersWorld());
            data.put("crafting", client.getRealSkillLevel(Skill.CRAFTING));
            data.put("smithing", client.getRealSkillLevel(Skill.SMITHING));
            data.put("fletching", client.getRealSkillLevel(Skill.FLETCHING));
            data.put("magic", client.getRealSkillLevel(Skill.MAGIC));

            ItemContainer inv = client.getItemContainer(InventoryID.INVENTORY);
            if (inv != null) {
                data.put("coins", inv.count(ItemID.COINS_995));
                data.put("natureRunes", inv.count(ItemID.NATURE_RUNE));
            }
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);
            syncActiveGeOffers();
            syncGrandExchangeLimitsAndTrades();
        } catch (Exception e) {
            log.debug("Error preparing account snapshot: {}", e.getMessage());
        }
    }

    private void syncGrandExchangeLimitsAndTrades() {
        if (configManager == null) {
            return;
        }
        try {
            String profileKey = configManager.getRSProfileKey();
            if (profileKey == null) {
                return;
            }

            String tradeHistoryJson = configManager.getRSProfileConfiguration("grandexchange", "tradeHistory");
            List<String> buylimitKeys = configManager.getRSProfileConfigurationKeys("grandexchange", profileKey, "buylimit");
            Map<String, String> limits = new HashMap<>();
            if (buylimitKeys != null) {
                for (String k : buylimitKeys) {
                    String val = configManager.getConfiguration("grandexchange", profileKey, k);
                    if (val != null) {
                        String iid = k.substring(k.lastIndexOf('.') + 1);
                        limits.put(iid, val);
                    }
                }
            }

            Map<String, Object> data = new HashMap<>();
            data.put("event", "GE_SYNC");
            data.put("account", getAccountName());
            data.put("buylimits", limits);
            if (tradeHistoryJson != null && !tradeHistoryJson.isEmpty()) {
                Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
                List<Map<String, Object>> trades = gson.fromJson(tradeHistoryJson, listType);
                data.put("tradeHistory", trades);
            }
            data.put("timestamp", System.currentTimeMillis() / 1000.0);
            sendPayload(data);
        } catch (Exception e) {
            log.debug("Error syncing GE limits and trades: {}", e.getMessage());
        }
    }

    private void syncActiveGeOffers() {
        try {
            GrandExchangeOffer[] offers = client.getGrandExchangeOffers();
            if (offers == null) {
                return;
            }
            for (int slot = 0; slot < offers.length; slot++) {
                GrandExchangeOffer offer = offers[slot];
                if (offer == null) {
                    continue;
                }
                GrandExchangeOfferState state = offer.getState();
                if (state == GrandExchangeOfferState.BUYING) {
                    int itemId = offer.getItemId();
                    if (itemId <= 0) {
                        continue;
                    }
                    String itemName = itemManager.getItemComposition(itemId).getName();
                    Map<String, Object> data = new HashMap<>();
                    data.put("event", "GE_OFFER");
                    data.put("account", getAccountName());
                    data.put("slot", slot);
                    data.put("state", "BUYING");
                    data.put("itemId", itemId);
                    data.put("itemName", itemName);
                    data.put("price", offer.getPrice());
                    data.put("spent", offer.getSpent());
                    data.put("quantitySold", offer.getQuantitySold());
                    data.put("totalQuantity", offer.getTotalQuantity());
                    data.put("timestamp", System.currentTimeMillis() / 1000.0);
                    sendPayload(data);
                }
            }
        } catch (Exception e) {
            log.debug("Error syncing active GE offers: {}", e.getMessage());
        }
    }

    private void sendPayload(Map<String, Object> data) {
        if (httpClient == null) {
            return;
        }

        try {
            String json = gson.toJson(data);
            String url = "http://127.0.0.1:" + config.bridgePort() + "/api/event";

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .timeout(Duration.ofMillis(1200))
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

            httpClient.sendAsync(request, HttpResponse.BodyHandlers.discarding())
                .exceptionally(ex -> null); // Non-blocking: quietly drop if dashboard is closed
        } catch (Exception ignored) {
        }
    }
}
