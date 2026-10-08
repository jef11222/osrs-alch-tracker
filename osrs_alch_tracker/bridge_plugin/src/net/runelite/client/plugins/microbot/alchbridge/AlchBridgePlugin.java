package net.runelite.client.plugins.microbot.alchbridge;

import com.google.gson.Gson;
import com.google.inject.Provides;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@PluginDescriptor(
    name = "<html>[<font color=green>A</font>] Alch Dashboard Bridge",
    description = "Pipes live GE trades, 4h timers, cash stack, nature runes, and alch XP to OSRS Alch Dashboard",
    tags = {"alch", "ge", "tracker", "bridge", "dashboard", "microbot"},
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

    private HttpClient httpClient;
    private ExecutorService httpExecutor;

    private final Map<Integer, String> lastOfferState = new ConcurrentHashMap<>();
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

        log.info("Alch Dashboard Bridge plugin started (Port: {})", config.bridgePort());

        if (client.getGameState() == GameState.LOGGED_IN) {
            sendAccountSnapshot();
        }
    }

    @Override
    protected void shutDown() {
        if (httpExecutor != null && !httpExecutor.isShutdown()) {
            httpExecutor.shutdownNow();
        }
        lastOfferState.clear();
        lastMagicXp = -1;
        lastCoins = -1;
        lastNatureRunes = -1;
        log.info("Alch Dashboard Bridge plugin stopped");
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
    public void onGrandExchangeOfferChanged(GrandExchangeOfferChanged event) {
        GrandExchangeOffer offer = event.getOffer();
        if (offer == null) {
            return;
        }

        int slot = event.getSlot();
        int itemId = offer.getItemId();
        int qtySold = offer.getQuantitySold();
        int totalQty = offer.getTotalQuantity();
        long price = offer.getPrice();
        long spent = offer.getSpent();
        GrandExchangeOfferState state = offer.getState();
        String stateStr = state != null ? state.name() : "EMPTY";

        // De-duplicate unchanged duplicate events
        String offerKey = itemId + "_" + qtySold + "_" + totalQty + "_" + stateStr + "_" + spent;
        String prev = lastOfferState.get(slot);
        if (offerKey.equals(prev)) {
            return;
        }
        lastOfferState.put(slot, offerKey);

        String itemName = "";
        if (itemId > 0) {
            try {
                itemName = itemManager.getItemComposition(itemId).getName();
            } catch (Exception ignored) {
            }
        }

        Map<String, Object> data = new HashMap<>();
        data.put("event", "GE_OFFER");
        data.put("account", getAccountName());
        data.put("slot", slot);
        data.put("itemId", itemId);
        data.put("itemName", itemName);
        data.put("quantitySold", qtySold);
        data.put("totalQuantity", totalQty);
        data.put("price", price);
        data.put("spent", spent);
        data.put("state", stateStr);
        data.put("world", client.getWorld());
        data.put("isMembers", isMembersWorld());
        data.put("timestamp", System.currentTimeMillis() / 1000.0);

        sendPayload(data);
    }

    @Subscribe
    public void onItemContainerChanged(ItemContainerChanged event) {
        if (!config.syncCashAndRunes()) {
            return;
        }

        int containerId = event.getContainerId();
        ItemContainer container = event.getItemContainer();
        if (container == null) {
            return;
        }

        if (containerId == InventoryID.INVENTORY.getId()) {
            int coins = container.count(ItemID.COINS_995);
            int nats = container.count(ItemID.NATURE_RUNE);

            if (coins != lastCoins || nats != lastNatureRunes) {
                lastCoins = coins;
                lastNatureRunes = nats;

                Map<String, Object> data = new HashMap<>();
                data.put("event", "INVENTORY_SYNC");
                data.put("account", getAccountName());
                data.put("coins", coins);
                data.put("natureRunes", nats);
                data.put("timestamp", System.currentTimeMillis() / 1000.0);

                sendPayload(data);
            }
        } else if (containerId == InventoryID.BANK.getId()) {
            int bankCoins = container.count(ItemID.COINS_995);
            int bankNats = container.count(ItemID.NATURE_RUNE);

            Map<String, Object> data = new HashMap<>();
            data.put("event", "BANK_SYNC");
            data.put("account", getAccountName());
            data.put("bankCoins", bankCoins);
            data.put("bankNatureRunes", bankNats);
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);
        }
    }

    @Subscribe
    public void onStatChanged(StatChanged event) {
        Skill skill = event.getSkill();
        if (skill == Skill.MAGIC) {
            int currentXp = event.getXp();
            if (config.trackAlchCasts() && lastMagicXp > 0) {
                int xpDiff = currentXp - lastMagicXp;
                if (xpDiff == 65) { // Exactly 1 High Alchemy cast!
                    Map<String, Object> data = new HashMap<>();
                    data.put("event", "ALCH_CAST");
                    data.put("account", getAccountName());
                    data.put("xpGained", 65);
                    data.put("timestamp", System.currentTimeMillis() / 1000.0);

                    sendPayload(data);
                }
            }
            lastMagicXp = currentXp;
        }

        // Send skill level updates
        if (skill == Skill.CRAFTING || skill == Skill.FLETCHING || skill == Skill.MAGIC) {
            Map<String, Object> data = new HashMap<>();
            data.put("event", "SKILLS_SYNC");
            data.put("account", getAccountName());
            data.put("crafting", client.getRealSkillLevel(Skill.CRAFTING));
            data.put("fletching", client.getRealSkillLevel(Skill.FLETCHING));
            data.put("magic", client.getRealSkillLevel(Skill.MAGIC));
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);
        }
    }

    @Subscribe
    public void onGameStateChanged(GameStateChanged event) {
        if (event.getGameState() == GameState.LOGGED_IN) {
            sendAccountSnapshot();
        }
    }

    private void sendAccountSnapshot() {
        try {
            Map<String, Object> data = new HashMap<>();
            data.put("event", "ACCOUNT_LOGIN");
            data.put("account", getAccountName());
            data.put("world", client.getWorld());
            data.put("isMembers", isMembersWorld());
            data.put("crafting", client.getRealSkillLevel(Skill.CRAFTING));
            data.put("fletching", client.getRealSkillLevel(Skill.FLETCHING));
            data.put("magic", client.getRealSkillLevel(Skill.MAGIC));

            ItemContainer inv = client.getItemContainer(InventoryID.INVENTORY);
            if (inv != null) {
                data.put("coins", inv.count(ItemID.COINS_995));
                data.put("natureRunes", inv.count(ItemID.NATURE_RUNE));
            }
            data.put("timestamp", System.currentTimeMillis() / 1000.0);

            sendPayload(data);
        } catch (Exception e) {
            log.debug("Error preparing account snapshot: {}", e.getMessage());
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
