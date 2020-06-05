#!/usr/bin/env python
import time

import urwid
import asyncio
import threading

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
            col,
            title="Outcomes",
            title_align="left"
        )
        self._selectable = False
        super().__init__(self._w)



    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


class SimulationViewer(urwid.WidgetWrap):

    def __init__(self):

        col = urwid.Columns([urwid.Text('heey')])

        self._w = urwid.LineBox(
            col,
            title="Simulation",
            title_align="left"
        )

        self._selectable = False
        super().__init__(self._w)


    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


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

        list = [urwid.Text(option) for option in options]
            #list.append(urwid.AttrMap(text, None, "reveal focus"))

            #list.append(urwid.Text(option))

            #list.append(("pack", urwid.Padding(text, width="pack")))

            #("pack", urwid.Padding(urwid.Text(("table_message", message)), width="pack",align="center"))

        self._w = urwid.LineBox(
            urwid.Columns(list),
            title="Controls",
            title_align="left"
        )

        self._selectable = False
        super().__init__(self._w)

    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


class Mainframe(urwid.WidgetWrap):

    def __init__(self):

        #self._w = urwid.LineBox(urwid.Frame(urwid.Filler(urwid.LineBox(col))))

        self.text_widget = urwid.Edit("Here")

        self._w = urwid.Filler(
            urwid.Pile([
                urwid.BoxAdapter(urwid.Filler(MontyHallTitle()), 5),
                urwid.Columns([OutcomeViewer(), SimulationViewer()]),
                Controls(),
                self.text_widget
            ])
        )

        self.total = 0
        self.delay = 3

        self.active = False

        super().__init__(self._w)

    def keypress(self, size, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()
        if key == "a":
            self.active = not self.active

    async def simulation_handler(self):

        while True:

            if self.active:
                self.total += 1
                self.text_widget.set_caption(str(self.total))

            await asyncio.sleep(2)


def main():

    urwid.set_encoding('utf8')

    mainframe = Mainframe()

    def keypress(key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()

 #   main_loop = urwid.MainLoop(mainframe, unhandled_input=keypress)
 #   main_loop.run()

    aloop = asyncio.get_event_loop()
    ev_loop = urwid.AsyncioEventLoop(loop=aloop)
    loop = urwid.MainLoop(mainframe, unhandled_input=keypress, event_loop=ev_loop)


    asyncio.ensure_future(mainframe.simulation_handler())


    loop.run()

    #urwid_loop = urwid.MainLoop(Mainframe(), unhandled_input=keypress, handle_mouse=False)

    #urwid_loop.run()

#    try:
#        # Returns when the connection is closed.
#        loop.run_until_complete(mainframe.simulation())
#
#    finally:
#        # Ensure urwid cleans up properly and doesn't wreck the terminal.
#        urwid_loop.stop()
#        loop.close()

    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()

if __name__ == '__main__':
    main()
