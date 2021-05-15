#!/usr/bin/env python3
import os
import urwid
from subprocess import run, PIPE


def debug(message):
    if os.getenv('DEBUG'):
        open('log', 'a').write(message.rstrip('\n') + '\n')


class SelectableText(urwid.Text):
    def __init__(self, markup):
        super().__init__(markup, wrap='clip')

    def selectable(self):
        """ make the widget selectable for navigating """
        return True

    def keypress(self, size, key):
        """ let the widget pass through the keys """
        return key


class PassNode(urwid.AttrMap):
    def __init__(self, text):
        super().__init__(SelectableText(text), '',  'focus')
        self.node = self.original_widget.text


class SearchBox(urwid.Edit):
    def keypress(self, size, key):
        debug("search box keypress: " + key)
        if key in ['esc']:
            self.set_edit_text('')
            passui.contents['footer'] = (passui.footer_widget, None)
            passui.set_focus('body')
            return None
        elif key in ['enter']:
            # dummy search
            return None

        return super().keypress(size, key)


class PassList(urwid.ListBox):
    def __init__(self, body, root=None, allpass=None):
        self.root = root if root else ''
        self._all_pass = allpass
        super().__init__(body)

    def mouse_event(self, size, event, button, col, row, focus):
        debug("passlist mouse event: {} {} {} {} {} {} {}".format(
            size, event, button, col, row, focus, self.focus_position
        ))
        if button in [1] and row == self.focus_position:
            self.dir_navigate('down')
        elif button in [3]:
            self.dir_navigate('up')
        elif button in [4]:
            self.list_navigate(size, -1)
        elif button in [5]:
            self.list_navigate(size, 1)
        else:
            return super().mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        debug("passlist keypress: {} {}".format(key, size))
        list_navigations = {
            'j': 1,
            'k': -1,
            'ctrl n': 1,
            'ctrl p': -1,
            'ctrl f': size[1],
            'ctrl b': -size[1],
            'ctrl d': size[1] // 2,
            'ctrl u': -size[1] // 2,
            'page up': -size[1],
            'page down': size[1],
            # overshoot to go to bottom/top
            'G': len(self.body),
            'g': -len(self.body),
            'end': len(self.body),
            'home': -len(self.body),
        }
        dir_navigations = {
            'l':     'down',
            'h':     'up',
            'right': 'up',
            'left':  'down',
            'enter': 'up',
        }
        if key in list_navigations:
            self.list_navigate(size, list_navigations[key])
        elif key in dir_navigations:
            self.dir_navigate(dir_navigations[key])
        elif key in ['d']:
            # dummy delete
            if len(self.body) > 0:
                self.body.pop(self.focus_position)
        elif key in ['a']:
            # dummy add
            self.body.insert(self.focus_position, PassNode('foonew'))
        elif key in ['/']:
            passui.contents['footer'] = (passui.searchbox, None)
            passui.set_focus('footer')
        else:
            return super().keypress(size, key)

    def dir_navigate(self, direction):
        # record current position
        self._all_pass[self.root].pos = self.focus_position
        if direction in 'down':
            if self.focus.node in self._all_pass[self.root].dirs:
                self.root = os.path.join(self.root, self.focus.node)
        elif direction in 'up':
            self.root = os.path.dirname(self.root)
        # this way the list itself is not replaced, same down there
        self.body[:] = [PassNode(node) for node in self._all_pass[self.root].contents()]
        self.focus_position = self._all_pass[self.root].pos
        urwid.emit_signal(self, 'update_view')

    def list_navigate(self, size, shift):
        if len(self.body) == 0:
            return
        offset = self.get_focus_offset_inset(size)[0]
        new_focus = self.focus_position + shift
        new_offset = offset + shift
        # border check
        if new_focus < 0:
            new_focus = 0
        elif new_focus > len(self.body) - 1:
            new_focus = len(self.body) - 1
        if new_offset < 0:
            new_offset = 0
        elif new_offset > size[1] - 1:
            new_offset = size[1] - 1
        self.change_focus(size, new_focus, offset_inset=new_offset)
        urwid.emit_signal(self, 'update_view')


class Directory():
    def __init__(self, root, dirs, files):
        self.root = root
        self.dirs = sorted(dirs)
        self.files = sorted(files)
        self.pos = 0

    def contents(self):
        return self.dirs + self.files


class UI(urwid.Frame):
    def __init__(self, allpass=None):
        self._last_preview = None
        self._app_string = 'Pass tui'
        self._all_pass = allpass
        self.header_widget = urwid.AttrMap(urwid.Text(''), 'border')
        self.footer_widget = urwid.AttrMap(urwid.Text('', align='right'), 'border')
        self.divider = urwid.AttrMap(urwid.Divider('-'), 'border')
        self.preview = urwid.Filler(urwid.Text(''), valign='top')
        self.searchbox = SearchBox("/")

        self.walker = urwid.SimpleListWalker([
            PassNode(directory) for directory in self._all_pass[''].contents()
        ])
        self.listbox = PassList(self.walker)
        if arg_preview in ['side', 'horizontal']:
            self.middle = urwid.Columns([self.listbox, self.preview], dividechars=1)
        elif arg_preview in ['bottom', 'vertical']:
            self.middle = urwid.Pile([self.listbox, ('pack', self.divider), self.preview])

        # update upon list operations
        urwid.register_signal(PassList, ['update_view'])
        urwid.connect_signal(self.listbox, 'update_view', self.update_view)
        super().__init__(self.middle, self.header_widget, self.footer_widget, focus_part='body')

    def update_view(self):
        if self.listbox.focus is None:
            self.footer.original_widget.set_text("0/0")
            return

        text = self.listbox.focus.node
        node = os.path.join(self.listbox.root, text)

        if node == self._last_preview:
            return

        if text in self._all_pass[self.listbox.root].dirs:
            preview = "\n".join(self._all_pass[node].contents())
        else:
            preview = Pass.show(node)
            debug("password: " + preview)
        self.preview.original_widget.set_text(preview)
        self._last_preview = node

        self.contents['header'][0].original_widget.set_text('{}: {}'.format(
            self._app_string,
            os.path.join(Pass.PASS_DIR, self.listbox.root)
        ))
        self.contents['footer'][0].original_widget.set_text("{}/{}".format(
            self.listbox.focus_position + 1,
            len(self.listbox.body)
        ))


class Pass:
    FALLBACK_PASS_DIR = os.path.join(os.getenv("HOME"), ".password_store")
    PASS_DIR = os.getenv("PASSWORD_STORE_DIR", FALLBACK_PASS_DIR)

    @classmethod
    def extract_all(cls):
        """ pass files traversal """
        dir_contents = {}
        for root, dirs, files in os.walk(cls.PASS_DIR, topdown=True):
            if not root.startswith(os.path.join(cls.PASS_DIR, '.git')):
                dirs = [os.path.join('', d) for d in dirs if d != '.git']
                files = [file.rstrip('.gpg') for file in files if file.endswith('.gpg')]
                relroot = os.path.normpath(os.path.relpath(root, cls.PASS_DIR))
                if relroot == '.':
                    relroot = ''
                dir_contents[relroot] = Directory(relroot, dirs, files)
        return dir_contents

    @staticmethod
    def show(node):
        result = run(['pass', 'show', node], stdout=PIPE, stderr=PIPE, text=True)
        return result.stderr if result.returncode else result.stdout


def unhandled_input(key):
    if key in ['q', 'Q']:
        raise urwid.ExitMainLoop()
    return True


if __name__ == '__main__':
    arg_preview = 'side'

    # UI
    passui = UI(allpass=Pass.extract_all())
    # manually update when first opening the program
    passui.update_view()

    # main loop
    loop = urwid.MainLoop(passui, unhandled_input=unhandled_input, palette=[
        # name          fg              bg              styles
        ('focus',       'black',        'dark cyan',    'standout'),
        ('border',      'light cyan',   'default'),
    ])
    # set the timeout after escape, or, set instant escape
    loop.screen.set_input_timeouts(complete_wait=0)
    loop.run()
