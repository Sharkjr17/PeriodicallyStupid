# =========================
# ======= IMPORTS =========
# =========================

import sys, subprocess, json, math, random, time, threading, collections, html, copy, statistics

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button


# =========================
# ======= GLOBALS =========
# =========================
saveFile = {}



# =========================
# ====== LOAD DATA ========
# =========================

try:
    with open('data.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: data.json not found. Please ensure the game data file exists.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: data.json is not valid JSON ({e}).")
    sys.exit(1)

# Validate required keys (expand later as needed)
required_keys = []
for k in required_keys:
    if k not in data:
        print(f"Error: data.json missing required key '{k}'.")
        sys.exit(1)

def save_check():
    """Check if save.json exists or create new save."""
    global saveFile
    while True:
        choice = input("Do you have a save file? Y/N --> ").strip().lower()
        if choice in ("y", "yes"):
            try:
                with open('save.json', 'r') as file:
                    saveFile = json.load(file)
            except FileNotFoundError:
                print("No save.json found. Creating a new save instead.")
                _create_new_save()
            break
        elif choice in ("n", "no"):
            _create_new_save()
            break
        else:
            print("Please enter Y or N.")

def _create_new_save():
    """Helper to create a new save file."""
    global saveFile
    saveFile = {
        "version": 1,
        "created_at": time.time(),
        "progress": {}
    }
    export_save()

def export_save():
    """Write saveFile dictionary to save.json file."""
    try:
        with open("save.json", "w") as f:
            json.dump(saveFile, f, indent=2)
        print("Game saved.")
    except Exception as e:
        print(f"Error saving game: {e}")





# =========================
# ======= HELPERS =========
# =========================

def clear_screen():
    """Completely clears the terminal."""
    cmd = 'cls' if sys.platform.startswith('win') else 'clear'
    subprocess.run(cmd, shell=True)








# =========================
# ======= UI LAYOUT =======
# =========================

MAIN_TABS = ["Production", "Staff", "Market", "Bank", "Encyclopedia", "Settings"]

SUBMENUS = {
    "production": ["Factories", "Resources", "Outputs"],
    "staff": ["Hire", "Train", "Assign"],
    "market": ["Buy", "Sell", "Upgrade"],   # NEW sub-tabs
    "bank": ["Account", "Loans", "Properties", "Stock"],
    "encyclopedia": ["Elements", "Mechanics", "Glossary"],
    "settings": ["Credits", "See Raw", "Save", "Save & Exit"],
}

class SimulationApp(App):
    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        self.info = Static("Select a tab to view info...", id="info")

        # Right side: selector + resources
        self.selector = Vertical(
            *[Button(tab, id=tab.lower()) for tab in MAIN_TABS],
            id="selector"
        )

        self.resources = Static(
            "⚡ Energy: 0\n💧 Water: 0\n💵 Money: 0\n⚠️ Risk: 0\n⭐ Reputation: 0",
            id="resources"
        )

        right_side = Vertical(self.selector, self.resources, id="right-side")
        yield Horizontal(self.info, right_side)

    def show_main_tabs(self):
        """Restore the main tab list."""
        self.info.update("Select a tab to view info...")
        self.selector.remove_children()
        for tab in MAIN_TABS:
            self.selector.mount(Button(tab, id=tab.lower()))

    def show_submenu(self, tab_id: str):
        """Show submenu options for a given tab."""
        self.info.update(f"{tab_id.capitalize()} tab selected.")
        self.selector.remove_children()
        for option in SUBMENUS.get(tab_id, []):
            safe_id = f"{tab_id}-{option.lower().replace(' ', '-').replace('&', 'and')}"
            self.selector.mount(Button(option, id=safe_id))
        self.selector.mount(Button("Back", id="back-main"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        # Handle main tabs
        if btn_id in [t.lower() for t in MAIN_TABS]:
            self.show_submenu(btn_id)

        # Handle back button
        elif btn_id == "back-main":
            self.show_main_tabs()

        # Handle settings submenu
        elif btn_id.startswith("settings-"):
            action = btn_id.split("settings-")[1]
            if action == "credits":
                self.info.update("Credits:\nGame design by Jackson.\nPowered by Textual.")
            elif action == "see-raw":
                self.info.update(f"Raw save data:\n{json.dumps(saveFile, indent=2)}")
            elif action == "save":
                export_save()
                self.info.update("Game saved successfully.")
            elif action == "save-exit":
                export_save()
                self.info.update("Game saved. Exiting...")
                self.exit()

        # Handle bank submenu
        elif btn_id.startswith("bank-"):
            action = btn_id.split("bank-")[1]
            if action == "account":
                self.info.update("Bank → Account:\nView balances, deposits, and withdrawals.")
            elif action == "loans":
                self.info.update("Bank → Loans:\nManage active loans, apply for new ones.")
            elif action == "properties":
                self.info.update("Bank → Properties:\nTrack owned properties and mortgages.")
            elif action == "stock":
                self.info.update("Bank → Stock:\nBuy, sell, and monitor stock investments.")

        # Handle market submenu
        elif btn_id.startswith("market-"):
            action = btn_id.split("market-")[1]
            if action == "buy":
                self.info.update("Market → Buy:\nPurchase goods and resources.")
            elif action == "sell":
                self.info.update("Market → Sell:\nSell products and surplus stock.")
            elif action == "upgrade":
                self.info.update("Market → Upgrade:\nInvest in better trading tools or market reach.")

        # Generic placeholder for other submenu actions
        else:
            self.info.update(f"Selected option: {btn_id}")







# =========================
# ======= ENTRY POINT =====
# =========================

if __name__ == "__main__":
    save_check()
    print("Setup complete. Launching UI...")
    SimulationApp().run()
