from pathlib import Path

from textual.app import App
from textual.widgets import Static, Button
from textual.reactive import reactive
from textual.containers import Grid, Container
from textual import log

class Viz(App):
    CSS_PATH = "viz_textual.css"

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.set_interval(1 / 60, self.step)
        self.pixel_iterator = enumerate(_iter_pixels(Path(__file__).parent / "input.txt"))

    def step(self) -> None:
        """Method to update the time to the current time."""
        try:
            idx, val = next(self.pixel_iterator)
            log(idx, val)
            if val == "#":
                self.query_one(f"#box{idx}").add_class("active")
        except StopIteration:
            log("stop iteration")
            pass
    
    def compose(self):
        yield Grid(*[
            Static("", id=f"box{i}", classes="box")
            for i in range(240)
        ])
        # for i in range(240):
        #     yield Static("", id=f"box{i}", classes="box")

def _noop():
    yield 0

def _addx(v: str):
    yield 0
    yield int(v)

COMMANDS = {
    "noop": _noop,
    "addx": _addx,
}

def _iter_pixels(input_file: Path):
    commands = input_file.read_text().splitlines()
    cycle = 0
    x_register = 1
    for command in commands:
        cmd, *args = command.split()
        for v in COMMANDS[cmd](*args):
            if x_register - 1 <= cycle%40 <= x_register + 1:
                yield "#"
            else:
                yield"."
            cycle += 1
            x_register += int(v)

# if __name__ == "__main__":
app = Viz()
app.run()