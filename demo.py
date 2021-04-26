import bisect
import os
import sys
import urwid

home = os.getenv("HOME")
pass_dir = os.getenv("PASSWORD_STORE_DIR", os.path.join(home, ".password_store"))

dir_contents = []
for root, dirs, files in os.walk(pass_dir):
    if not root.startswith(os.path.join(pass_dir, '.git')) and root != pass_dir:
        dir_contents.append([root] + dirs + files)


class SelectableText(urwid.Text):
    def selectable(self):
        """ make the widget selectable for navigating """
        return True

    def keypress(self, size, key):
        """ let the widget pass through the keys """
        return key


class SearchBox(urwid.Edit):
    def keypress(self, size, key):
        if key in ('escape'):
            self.set_edit_text('')
            wrapped.contents['footer'] = (footer, None)
            wrapped.set_focus('body')
            return None

        return super().keypress(size, key)


class FileList(urwid.ListBox):
    def mouse_event(self, size, event, button, col, row, focus):
        if button in [4, 5]:
            total = len(self.body)
            curr = self.focus_position
            if button == 4:
                self.set_focus(curr - 1 if curr > 0 else 0)
            if button == 5:
                self.set_focus(curr + 1 if curr < total - 1 else total - 1)
            return None
        else:
            debug.set_text("{} {} {} {} {} {}".format(
                size, event, button, col, row, focus
            ))
        super().mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        keymap = {
            'j': 'down',
            'k': 'up',
            'ctrl y': 'down',
            'ctrl e': 'up',
            'ctrl n': 'down',
            'ctrl p': 'up',
            'ctrl b': 'page up',
            'ctrl f': 'page down',
        }
        debug.set_text("{} {}".format(key, size))

        if key in keymap.keys():
            super().keypress(size, keymap[key])
            return None
        elif key in ['d']:
            if len(content) > 0:
                content.pop(self.focus_position)
            return None
        elif key in ['a']:
            content.append(urwid.AttrMap(SelectableText('foonew'), '',  'focus'))
            return None
        elif key in ['/']:
            wrapped.contents['footer'] = (edit, None)
            wrapped.set_focus('footer')
            return None
        elif key in ['ctrl d', 'ctrl u']:
            total = len(self.body)
            curr = self.focus_position
            offset = int(size[1] / 2)
            if key == 'ctrl u':
                self.set_focus(curr - offset if curr > offset - 1 else 0)
            if key == 'ctrl d':
                self.set_focus(curr + offset if curr < total - offset else total - 1)
            return None

        return super().keypress(size, key)


def unhandled_input(key):
    if key in ['q', 'Q']:
        raise urwid.ExitMainLoop()
    return True


def update_view():
    focus = listbox.get_focus()
    if focus[0] is None:
        middle.contents = [(listbox, ('weight', 100))]
        footer.set_text("0/0")
    else:
        text = focus[0].original_widget.get_text()[0]
        if text[:3] == 'foo':
            middle.contents = [(listbox, ('weight', 100))]
        else:
            middle.contents = [(listbox, ('weight', 2)),
                               (divider, ('pack', None)),
                               (preview, ('weight', 1))]
            preview.original_widget.set_text("\n".join(dir_contents[focus[1]]))

        footer.set_text("{}/{}".format(focus[1] + 1, len(content)))


content = urwid.SimpleListWalker([urwid.AttrMap(SelectableText(walks[0]), '',  'focus')
    for walks in dir_contents])

listbox = FileList(content)

header = urwid.Text('My demo application')
footer = urwid.Text('')
debug = urwid.Text('')
preview = urwid.Filler(urwid.Text(''))
edit = SearchBox("Search: ")
divider = urwid.Divider('-')

middle = urwid.Pile([
    ('weight', 2, listbox),
    ('pack',      divider),
    ('weight', 1, preview)])
wrapped = urwid.Frame(middle, debug, footer, focus_part='body')

palette = [
    ('focus', 'black', 'dark cyan', 'standout'),
    ('normal', 'white', 'dark gray'),
]


# update upon list operations
urwid.connect_signal(content, 'modified', update_view)
update_view()

urwid.MainLoop(wrapped, palette=palette, unhandled_input=unhandled_input).run()
