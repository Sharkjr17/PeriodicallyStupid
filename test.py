# test.py
# Starter Textual app with three panes: element info, selector, and resource meters.

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button

# Example element data
ELEMENTS = {
    "Hydrogen": {"symbol": "H2", "state": "Gas", "notes": "Lightest element, fuel potential"},
    "Oxygen": {"symbol": "O2", "state": "Gas", "notes": "Supports combustion, vital for respiration"},
}

class SimulationApp(App):

    CSS_PATH = "test.css"

    def compose(self) -> ComposeResult:
        # Left info pane
        self.info = Static("Select an element to view info...", id="info")

        # Top right selector
        self.selector = Vertical(
            *[Button(name, id=name) for name in ELEMENTS.keys()],
            id="selector"
        )

        # Bottom right resource meters
        self.resources = Static("⚡ Energy: 0\n💧 Water: 0\n💵 Money: 0\n⚠️ Risk: 0\n⭐ Reputation: 0", id="resources")

        # Right side split
        right_side = Vertical(self.selector, self.resources, id="right-side")

        # Full layout: left + right
        yield Horizontal(self.info, right_side)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = event.button.id
        if name in ELEMENTS:
            data = ELEMENTS[name]
            self.info.update(f"{name}: {data['symbol']}, {data['state']}")
            self.selector.remove_children()
            self.selector.mount(Button("More Info", id=f"more-{name}"))
        elif name.startswith("more-"):
            element = name.split("more-")[1]
            data = ELEMENTS[element]
            self.info.update(
                f"Element: {element}\nSymbol: {data['symbol']}\nState: {data['state']}\nNotes: {data['notes']}"
            )
            self.selector.remove_children()
            self.selector.mount(Button("Back", id="back"))
        elif name == "back":
            self.info.update("Select an element to view info...")
            self.selector.remove_children()
            for element in ELEMENTS.keys():
                self.selector.mount(Button(element, id=element))

if __name__ == "__main__":
    SimulationApp().run()