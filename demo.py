import bisect
import os
import sys
import urwid

home = os.getenv("HOME")
pass_dir = os.getenv("PASSWORD_STORE_DIR", os.path.join(home, ".password_store"))


class SelectableText(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class MyListBox(urwid.ListBox):
    def mouse_event(self, size, event, button, col, row, focus):
        if super().mouse_event(size, event, button, col, row, focus) is None:
            return None
        if button in (4, 5, '4', '5'):
            debug.set_text("down")
        else:
            debug.set_text("{} {} {} {} {} {}".format(
                size, event, button, col, row, focus
            ))

    def keypress(self, size, key):
        if super().keypress(size, key) is None:
            return None

        keymap = {
            'j': 'down',
            'k': 'up',
            'ctrl y': 'down',
            'ctrl e': 'up',
        }
        debug.set_text("{} {}".format(key, size))

        if key in ('j', 'k', 'ctrl e', 'ctrl y'):
            super().keypress(size, keymap[key])
            return None
        elif key in ('d'):
            content.pop()
            return None
        elif key in ('a'):
            content.append(urwid.AttrMap(SelectableText('foonew'), '',  'focus'))
            return None

        return key


def unhandled_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    return True


def update_view():
    focus = listbox.get_focus()
    text = focus[0].original_widget.get_text()[0]
    if text[:3] != 'foo':
        middle.contents = [(listbox, ('weight', 100))]
    else:
        middle.contents = [(listbox, ('weight', 50)), (preview, ('weight', 50))]

    footer.set_text("{}/{}".format(focus[1] + 1, len(content)))


content = urwid.SimpleListWalker([])

listbox = MyListBox(content)

header = urwid.Text('My demo application')
footer = urwid.Text('')
debug = urwid.Text('')
preview = urwid.Filler(urwid.Text(''))

middle = urwid.Pile([('weight', 50, listbox), ('weight', 50, preview)])
wrapped = urwid.Frame(middle, debug, footer)

palette = [
    ('focus', 'black', 'dark cyan', 'standout'),
    ('normal', 'white', 'dark gray'),
]


# update upon list operations
urwid.connect_signal(content, 'modified', update_view)

urwid.MainLoop(wrapped, palette=palette, unhandled_input=unhandled_input).run()
