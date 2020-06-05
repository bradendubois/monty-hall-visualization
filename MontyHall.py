#!/usr/bin/env python
import random
import time

import urwid
import asyncio


class MontyHallTitle(urwid.Text):

    def __init__(self):

        self.markup = "Monty Hall Visualization"
        self._selectable = False
        super().__init__(self.markup)


    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


class OutcomeViewer(urwid.WidgetWrap):

    def __init__(self):
        col = urwid.Columns([urwid.Text('heey'), urwid.Text("There")])

        self._w = urwid.LineBox(
            urwid.BoxAdapter(urwid.Filler(col, "top"), 5),
            title="Outcomes",
            title_align="left"
        )
        self._selectable = False
        super().__init__(self._w)


class Writer(urwid.WidgetWrap):

    def __init__(self):

        self._w = urwid.Text("Here")
        self.to_show = ""

        super().__init__(self._w)

    def show(self, message: str):
        self._w.set_text(message)

    def current_shown(self):
        return self._w.text

class Door(urwid.WidgetWrap):

    def __init__(self, door_number: int):

        self.player_selected = urwid.Text("")
        self.winner = urwid.Text("")
        self.revealed = urwid.Text("")

        self._w = urwid.LineBox(
            urwid.Pile([
                self.player_selected,
                self.winner,
                self.revealed

            ])
        )

        self._w.set_title("Door " + str(door_number))

        super().__init__(self._w)

    def set_player_selected(self):
        self.player_selected.set_text("Chosen")

    def set_winning_door(self):
        self.winner.set_text("Winner")

    def set_revealed(self):
        self.revealed.set_text("Revealed")


class SimulationViewer(urwid.WidgetWrap):

    def __init__(self):

        self.active = urwid.Text("Simulation: ", align="left")
        self.speed = urwid.Text("Speed: ", align="right")

        self.stay_successes = 0
        self.total_stays = 0

        self.switch_successes = 0
        self.total_switches = 0

        self.output_info = Writer()

        self.doors = [Door(i+1) for i in range(3)]

        self._w = urwid.LineBox(
            urwid.Pile([
                urwid.BoxAdapter(urwid.Filler(urwid.Columns([self.active, self.speed]), "top"), 5),
                urwid.BoxAdapter(urwid.Filler(urwid.Columns(self.doors), "middle"), 5),
                urwid.Columns([urwid.Text("Here"), urwid.Text("Here")]),
                Controls(),
                self.output_info
            ]),

            title="Simulation",
            title_align="left"
        )

        self._selectable = False
        super().__init__(self._w)

    def update_speed_display(self, new_value: str):
        self.speed.set_text("Speed: " + new_value)

    def update_simulation_status_display(self, message):
        self.output_info.slow_write(message)

    async def simulation_handler(self):

        while True:

            if self.active:

                first_reveal_doors = [0, 1, 2]
                switchable_doors = [0, 1, 2]

                # Pick the winning door
                winning_door = random.randint(0, 2)
                self.doors[winning_door].set_winning_door()
                first_reveal_doors.remove(winning_door)

                # TODO
                await asyncio.sleep(1)

                # Pick a door
                selected_door = random.randint(0, 2)
                self.doors[selected_door].set_winning_door()
                first_reveal_doors.remove(selected_door)
                switchable_doors.remove(selected_door)

                # TODO
                await asyncio.sleep(1)

                # Reveal a non-winning door
                reveal_door = first_reveal_doors.pop()
                self.doors[reveal_door].set_revealed()
                switchable_doors.remove(reveal_door)

                # TODO
                await asyncio.sleep(1)

                # Randomly choose whether to switch doors
                to_switch = random.randint(0, 1)
                only_remaining_door = switchable_doors.pop()
                # TODO - Improve relaying whether switched or not, and whether a win or not

                # TODO - Refactor into if/elif of each combination
                if to_switch:
                    selected_door = only_remaining_door
                    self.total_switches += 1
                else:
                    self.total_stays += 1

                if selected_door == winning_door:

                    if to_switch:
                        self.switch_successes += 1
                    else:
                        self.stay_successes += 1

                    # TODO - Mark a win?

                # TODO
                await asyncio.sleep(1)

                self.total += 1
                self.update_text_widget()
                self.update_simulation_speed()
            await asyncio.sleep(self.delay)


class Controls(urwid.WidgetWrap):

    def __init__(self):

        options = [
            "Q: Quit",
            "Space: Start/Stop Simulation",
            "Left: Simulation Speed Down",
            "Right: Simulation Speed Up",
            "R: Restart Simulation"
        ]

        self._selectable = False

        text_options = [urwid.Text(option) for option in options]

        self._w = urwid.LineBox(
            urwid.Columns(text_options),
            title="Controls",
            title_align="left"
        )

        self._selectable = False
        super().__init__(self._w)


class Mainframe(urwid.WidgetWrap):

    def __init__(self):

        self.total = 0
        self.delay = 1

        self.active = False

        self.text_widget = urwid.Edit("Here")
        self.update_text_widget()

        self.outcome_viewer = OutcomeViewer()

        self.simulation_viewer = SimulationViewer()
        self.update_simulation_speed()

        self._w = urwid.Filler(
            urwid.Pile([
                urwid.BoxAdapter(urwid.Filler(MontyHallTitle()), 5),
                urwid.Columns([self.outcome_viewer, self.simulation_viewer]),
                Controls(),
                self.text_widget
            ])
        )


        super().__init__(self._w)

    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()
        elif key in ["s", "space"]:
            self.active = not self.active

            if self.active:
                self.simulation_viewer.output_info.show("A new message")
            else:
                self.simulation_viewer.output_info.show("Different message")

        elif key in ["a", "left"]:
            if self.delay < 10:
                self.delay *= 10
        elif key in ["d", "right", "RIGHT"]:
            if self.delay > 0.00001:
                self.delay /= 10

        self.update_text_widget()
        self.update_simulation_speed()

    def update_text_widget(self):
        self.text_widget.set_caption(str(self.total))

    def update_simulation_speed(self):
        self.simulation_viewer.update_speed_display("{0:.2f}x".format(1 / self.delay))

    async def simulation_handler(self):

        while True:

            if self.active:
                self.total += 1
                self.update_text_widget()
                self.update_simulation_speed()
            await asyncio.sleep(self.delay)


def keypress(key):
    if key in ["q", "Q"]:
        raise urwid.ExitMainLoop()


if __name__ == '__main__':

    urwid.set_encoding('utf8')

    mainframe = Mainframe()

    asyncio_loop = asyncio.get_event_loop()
    async_event_loop = urwid.AsyncioEventLoop(loop=asyncio_loop)
    loop = urwid.MainLoop(mainframe, unhandled_input=keypress, event_loop=async_event_loop)

    asyncio.ensure_future(mainframe.simulation_handler())
    #asyncio.ensure_future(mainframe.simulation_viewer.output_info.write_handler())

    loop.run()
