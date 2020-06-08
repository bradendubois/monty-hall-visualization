#!/usr/bin/env python

import random
import asyncio
import platform


def missing_urwid_debug():
    system = platform.system()

    print("Required module 'urwid' not found.")
    print("It looks like you're running this on: " + system + " .")
    print("To install 'urwid' on your system, try: ")

    interface, command = "", ""

    if system == "Windows":
        interface = "Command Prompt window"
        command = "py -m pip install urwid"
    elif system == "Darwin" or system == "Linux":
        interface = "terminal"
        command = "pip install urwid"
    else:
        print("Your platform is uncertain; please notify me, as Python's platform module has failed.")
        exit(-1)

    print("  In a {}, enter:\n    {}".format(interface, command))
    exit(-1)


try:
    import urwid
except ModuleNotFoundError:
    missing_urwid_debug()


class MontyHallTitle(urwid.Text):

    def __init__(self):

        self.markup = "Monty Hall Visualization"
        self._selectable = False
        super().__init__(self.markup)


class Outcome(urwid.WidgetWrap):

    def __init__(self, title: str, wins=0, total=0):

        self.title = title
        self.wins = wins
        self.total = total

        self.width = 50

        self.wins_widget = urwid.Text(str(wins) + "/" + str(total) + " (" + str(wins/total * 100) + ")")
        self.bar = urwid.Text("[" + (self.width * wins) // total * "X" + (self.width - (self.width * wins) // total) * " " + "]")

        self._w = urwid.LineBox(
            urwid.Pile([
                self.wins_widget,
                self.bar
            ]),
            title=title,
            title_align="left"
        )

        super().__init__(self._w)

    def update_wins(self):
        #self.wins.set_text("I Got hit")
        self.wins_widget.set_text(str(self.wins) + "/" + str(self.total) + " (" + str(self.wins / self.total * 100) + ")")
        self.bar.set_text("[" + (self.width * self.wins) // self.total * "X" + (self.width - (self.width * self.wins) // self.total) * " " + "]")

    def increment_selection(self):
        self.total += 1
        self.update_wins()

    def increment_win(self):
        self.wins += 1
        self.update_wins()


class OutcomeViewer(urwid.WidgetWrap):

    def __init__(self):

        # TODO - Doesn't work. Ty urwid

        self.switches = Outcome("Switches", 1, 1)
        self.stays = Outcome("Stays", 1, 1)

        # urwid.register_signal(SimulationViewer, "Switches_selection")
        #urwid.connect_signal(switches, "Switches_selection", switches.increment_selection)

        #urwid.register_signal(SimulationViewer, "Stays_selection")
        #urwid.connect_signal(stays, "Stays_selection", switches.increment_selection)

        #urwid.register_signal(SimulationViewer, "Switches_win")
        #urwid.connect_signal(switches, "Switches_win", switches.increment_win)

        #urwid.register_signal(SimulationViewer, "Stays_win")
        #urwid.connect_signal(stays, "Stays_win", switches.increment_win)

        #urwid.connect_signal(stays, "Stays_selection", stays.increment_selection)

        #urwid.connect_signal(switches, "Switches_win", switches.increment_win)
        #urwid.connect_signal(stays, "Stays_win", stays.increment_win)

        self._w = urwid.LineBox(
            urwid.Pile([
                self.switches,
                self.stays
            ]),

            title="Outcomes",
            title_align="left"
        )

        self._selectable = False
        super().__init__(self._w)

    def update_data(self):
        pass


class Writer(urwid.WidgetWrap):

    def __init__(self):

        self._w = urwid.Text("")
        self.to_show = ""

        super().__init__(self._w)

    def show(self, message: str):
        self._w.set_text(message)

    def current_shown(self):
        return self._w.text


class Door(urwid.WidgetWrap):

    def __init__(self, door_number: int):

        self.winner = urwid.Text("")
        self.player_selected = urwid.Text("")
        self.revealed = urwid.Text("")
        self.switched = urwid.Text("")

        self._w = urwid.LineBox(
            urwid.Pile([
                self.winner,
                self.player_selected,
                self.revealed,
                self.switched
            ])
        )

        self._w.set_title("Door " + str(door_number))

        super().__init__(self._w)

    def set_winning_door(self):
        self.winner.set_text("Winner")

    def set_player_selected(self):
        self.player_selected.set_text("Chosen")

    def set_revealed(self):
        self.revealed.set_text("Revealed")

    def set_switched(self):
        self.switched.set_text("Switched To")

    def set_stayed(self):
        self.switched.set_text("Stayed")

    def clear(self):
        self.winner.set_text("")
        self.player_selected.set_text("")
        self.revealed.set_text("")
        self.switched.set_text("")


class SimulationViewer(urwid.WidgetWrap):

    def __init__(self, outcome_viewer: OutcomeViewer):

        self.active = False
        self.active_text = urwid.Text("Simulation: ", align="left")

        self.speed_widget = urwid.Text("Speed: ", align="right")

        self.outcome_viewer = outcome_viewer

        self.speed_index = 1
        self.speeds = [0.5, 1, 2, 5, 10, 50, 100, 1000, 10000, 100000]

        self.stay_successes = 0
        self.total_stays = 0

        self.switch_successes = 0
        self.total_switches = 0

        self.output_info = Writer()

        self.doors = [Door(i+1) for i in range(3)]

        self._w = urwid.LineBox(
            urwid.Pile([
                urwid.BoxAdapter(urwid.Filler(urwid.Columns([self.active_text, self.speed_widget]), "top"), 5),
                urwid.BoxAdapter(urwid.Filler(urwid.Columns(self.doors), "middle"), 6),
                self.output_info
            ]),

            title="Simulation",
            title_align="left"
        )

        self.update_speed_widget()

        self._selectable = False
        super().__init__(self._w)

    def results(self) -> tuple:
        return self.stay_successes, self.total_stays, self.switch_successes, self.total_switches

    def update_simulation_status_display(self, message):
        self.output_info.slow_write(message)

    def delay_decrease(self):
        if self.speed_index > 0:
            self.speed_index -= 1
        self.update_speed_widget()

    def delay_increase(self):
        if self.speed_index < len(self.speeds) - 1:
            self.speed_index += 1
        self.update_speed_widget()

    def update_speed_widget(self):
        self.speed_widget.set_text("Speed: " + str(self.speeds[self.speed_index]) + "x")

    def delay(self):
        return self.speeds[self.speed_index]

    async def simulation_handler(self):

        while True:

            if self.active:

                for door in self.doors:
                    door.clear()

                first_reveal_doors = [0, 1, 2]
                switchable_doors = [0, 1, 2]

                # Pick the winning door
                winning_door = random.randint(0, 2)
                self.doors[winning_door].set_winning_door()
                first_reveal_doors.remove(winning_door)

                # TODO
                await asyncio.sleep(1 / self.delay())

                # Pick a door
                selected_door = random.randint(0, 2)
                self.doors[selected_door].set_player_selected()
                if selected_door in first_reveal_doors:
                    first_reveal_doors.remove(selected_door)
                switchable_doors.remove(selected_door)

                # TODO
                await asyncio.sleep(1 / self.delay())

                # Reveal a non-winning door
                reveal_door = first_reveal_doors.pop()
                self.doors[reveal_door].set_revealed()
                switchable_doors.remove(reveal_door)

                # TODO
                await asyncio.sleep(1 / self.delay())

                # Randomly choose whether to switch doors
                to_switch = random.randint(0, 1)
                only_remaining_door = switchable_doors.pop()

                # TODO - Improve relaying whether switched or not, and whether a win or not

                # TODO - Refactor into if/elif of each combination
                if to_switch:
                    selected_door = only_remaining_door
                    self.doors[selected_door].set_switched()
                    self.total_switches += 1

                    self.outcome_viewer.switches.increment_selection()
                    # urwid.emit_signal(self, "Switches_selection")
                else:
                    self.doors[selected_door].set_stayed()
                    self.total_stays += 1

                    self.outcome_viewer.stays.increment_selection()
                    #urwid.emit_signal(self, "Stays_selection")

                if selected_door == winning_door and to_switch:
                    self.switch_successes += 1
                    self.write("Switching doors led to a win.")

                    self.outcome_viewer.switches.increment_win()
                    # urwid.emit_signal(self, "Switches_win")

                elif selected_door == winning_door and not to_switch:
                    self.stay_successes += 1
                    self.write("Staying with chosen door led to a win.")

                    self.outcome_viewer.stays.increment_win()
                    # urwid.emit_signal(self, "Stays_win")
                elif selected_door != winning_door and to_switch:
                    self.write("Switching doors led to a loss.")
                elif selected_door != winning_door and not to_switch:
                    self.write("Staying with chosen door led to a loss.")

                # TODO - Mark a win?

                # TODO
                await asyncio.sleep(1 / self.delay())



                #self.update_text_widget()
                #self.update_simulation_speed()

            await asyncio.sleep(0.00001)

    def write(self, message: str):
        self.output_info.show(message)


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

        self.text_widget = urwid.Edit("")

        self.outcome_viewer = OutcomeViewer()
        self.simulation_viewer = SimulationViewer(self.outcome_viewer)

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
            self.simulation_viewer.active = not self.simulation_viewer.active

        elif key in ["a", "left"]:
            self.simulation_viewer.delay_decrease()

        elif key in ["d", "right"]:
            self.simulation_viewer.delay_increase()

        self.update_text_widget()

    def update_text_widget(self):
        self.text_widget.set_caption(str(self.total))

    async def simulation_handler(self):

        while True:

            if self.active:
                self.total += 1
                self.update_text_widget()
                self.update_simulation_speed()
            await asyncio.sleep(self.delay)


if __name__ == '__main__':

    urwid.set_encoding('utf8')

    mainframe = Mainframe()

    asyncio_loop = asyncio.get_event_loop()
    async_event_loop = urwid.AsyncioEventLoop(loop=asyncio_loop)
    loop = urwid.MainLoop(mainframe, event_loop=async_event_loop)

    asyncio.ensure_future(mainframe.simulation_viewer.simulation_handler())
    # asyncio.ensure_future(mainframe.simulation_viewer.output_info.write_handler())

    loop.run()
