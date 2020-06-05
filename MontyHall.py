#!/usr/bin/env python

import urwid


class OutcomeViewer(urwid.WidgetWrap):

    def __init__(self):
        col = urwid.Columns([urwid.Text('heey'), urwid.Text("There")])

        self._w = urwid.LineBox(col)
        self._selectable = False

        super().__init__(self._w)


class Controls(urwid.WidgetWrap):

    def __init__(self):

        self._w = urwid.ListBox(
            urwid.SimpleListWalker([
                urwid.AttrMap(urwid.Text("A"), None, "reveal focus"),
                urwid.AttrMap(urwid.Text("B"), None, "reveal focus")
            ])
        )

        super().__init__(self._w)

class Mainframe(urwid.WidgetWrap):

    def __init__(self):

        col = urwid.Columns([urwid.Text('heey'), urwid.Text("There")])
        #self._w = urwid.LineBox(urwid.Frame(urwid.Filler(urwid.LineBox(col))))
        self._w = urwid.Filler(
            urwid.Pile([
                OutcomeViewer(),
                OutcomeViewer(),
                urwid.BoxAdapter(Controls(), 1)
            ])
        )
        #self._w = Controls()
        super().__init__(self._w)

    def keypress(self, size, key):
        if key in ["q", "Q"]:
            return key

def main():

    urwid.set_encoding('utf8')

    def quit(*args, **kwargs):
        raise urwid.ExitMainLoop()

    def handle_key(key):
        if key in ('q', 'Q'):
            quit()

    urwid.MainLoop(Mainframe()).run()


if __name__ == '__main__':
    main()
