#!/usr/bin/env python3
import os
import urwid
from subprocess import run, PIPE


def debug(message):
    if os.getenv('DEBUG'):
        open('log', 'a').write(message.rstrip('\n') + '\n')
        passui.message(message)


class PassNode(urwid.AttrMap):
    def __init__(self, text, isdir=False):
        self.node = text
        text = ('/' if isdir else ' ') + text
        normal = 'dir' if isdir else ''
        focused = 'focusdir' if isdir else 'focus'
        super().__init__(urwid.Text(text, wrap='clip'), normal, focused)

    def selectable(self):
        """ make the widget selectable for navigating """
        return True

    def keypress(self, size, key):
        """ let the widget pass through the keys to parent widget """
        return key


class SearchBox(urwid.Edit):
    def keypress(self, size, key):
        debug("search box keypress: " + key)
        if key in ['esc']:
            self.set_edit_text('')
            passui.contents['footer'] = (passui.footer_widget, None)
            passui.set_focus('body')
        elif key in ['enter']:
            # dummy search
            pass
        else:
            return super().keypress(size, key)


class PassList(urwid.ListBox):
    def __init__(self, body, root=None, allpass=None, ui=None):
        self.root = root if root else ''
        self._all_pass = allpass
        self._ui = ui
        super().__init__(body)

    def mouse_event(self, size, event, button, col, row, focus):
        focus_offset = self.get_focus_offset_inset(size)[0]
        debug("passlist mouse event: {} {} {} {} {} {} {} {}".format(
            size, event, button, col, row, focus, self.focus_position, focus_offset
        ))
        if button in [1]:
            if size[1] > len(self.body):
                # NOTE: offset is wrong(?) when size is larger than length
                # so the processing is different
                if row == self.focus_position:
                    self.dir_navigate('down')
                else:
                    self.list_navigate(size, to=row)
            else:
                if row == focus_offset:
                    self.dir_navigate('down')
                else:
                    self.list_navigate(size, to=self.focus_position - focus_offset + row)
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
            'down': 1,
            'up': -1,
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
            'right': 'down',
            'left':  'up',
            'enter': 'down',
        }
        if key in list_navigations:
            self.list_navigate(size, list_navigations[key])
        elif key in dir_navigations:
            self.dir_navigate(dir_navigations[key])
        elif key in ['d']:
            # dummy delete
            if len(self.body) > 0:
                self.body.pop(self.focus_position)
        elif key in ['a', 'i']:
            # dummy add
            self.body.insert(self.focus_position, PassNode('foonew'))
        elif key in ['A', 'I']:
            # dummy generate
            self.body.insert(self.focus_position, PassNode('foonew'))
        elif key in ['/']:
            passui.contents['footer'] = (passui.searchbox, None)
            passui.set_focus('footer')
        else:
            return super().keypress(size, key)

    def dir_navigate(self, direction):
        debug("body length: {}".format(len(self.body)))
        if self.body is None or len(self.body) == 0:
            return
        # record current position
        self._all_pass[self.root].pos = self.focus_position
        if direction in 'down':
            if self.focus.node in self._all_pass[self.root].dirs:
                self.root = os.path.join(self.root, self.focus.node)
        elif direction in 'up':
            self.root = os.path.dirname(self.root)
        # this way the list itself is not replaced
        self.body[:] = self._all_pass[self.root].nodelist()
        self._ui.update_view()
        self.focus_position = self._all_pass[self.root].pos

    def list_navigate(self, size, shift=0, to=None):
        if self.body is None or len(self.body) == 0:
            return
        offset = self.get_focus_offset_inset(size)[0]
        if to is None:
            new_focus = self.focus_position + shift
        else:
            new_focus = to
            shift = to - self.focus_position
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
        self._ui.update_view()


class Directory:
    def __init__(self, root, dirs, files):
        self.root = root
        self.dirs = sorted(dirs)
        self.files = sorted(files)
        self.pos = 0  # cursor position

    def nodelist(self):
        return [PassNode(d, True) for d in self.dirs] + [PassNode(f) for f in self.files]


class UI(urwid.Frame):
    def __init__(self, allpass=None):
        self._last_preview = None
        self._app_string = 'cPass'
        self._all_pass = allpass
        self.header_widget = urwid.AttrMap(urwid.Text(''), 'border')
        self.messagebox = urwid.Text('')
        self.indicator = urwid.AttrMap(urwid.Text('', align='right'), 'border')
        self.footer_widget = urwid.Columns([self.messagebox, ('pack', self.indicator)])
        self.divider = urwid.AttrMap(urwid.Divider('-'), 'border')
        self.preview = urwid.Filler(urwid.Text(''), valign='top')
        self.searchbox = SearchBox("/")

        self.walker = urwid.SimpleListWalker(self._all_pass[''].nodelist())
        self.listbox = PassList(self.walker, allpass=allpass, ui=self)
        if arg_preview in ['side', 'horizontal']:
            self.middle = urwid.Columns([self.listbox, self.preview], dividechars=1)
        elif arg_preview in ['bottom', 'vertical']:
            self.middle = urwid.Pile([self.listbox, ('pack', self.divider), self.preview])

        super().__init__(self.middle, self.header_widget, self.footer_widget)

    def message(self, message, alert=False):
        if alert:
            self.messagebox.set_text(('alert', message))
        else:
            self.messagebox.set_text(message)

    def update_view(self):
        self.contents['header'][0].original_widget.set_text('{}: {}'.format(
            self._app_string,
            os.path.join(Pass.PASS_DIR, self.listbox.root)
        ))
        if self.listbox.body is None or len(self.listbox.body) == 0:
            self.indicator.original_widget.set_text("0/0")
            return

        self.indicator.original_widget.set_text("{}/{}".format(
            self.listbox.focus_position + 1,
            len(self.listbox.body)
        ))

        text = self.listbox.focus.node
        node = os.path.join(self.listbox.root, text)

        if node == self._last_preview:
            return
        self._last_preview = node

        if text in self._all_pass[self.listbox.root].dirs:
            preview = "\n".join(['/' + d for d in self._all_pass[node].dirs]) + \
                      "\n".join([' ' + f for f in self._all_pass[node].files])
        else:
            preview = Pass.show(node)
        self.preview.original_widget.set_text(preview)


class Pass:
    FALLBACK_PASS_DIR = os.path.join(os.getenv("HOME"), ".password_store")
    PASS_DIR = os.getenv("PASSWORD_STORE_DIR", FALLBACK_PASS_DIR)

    @classmethod
    def extract_all(cls):
        """ pass files traversal """
        dir_contents = {}
        for root, dirs, files in os.walk(cls.PASS_DIR, topdown=True):
            if not root.startswith(os.path.join(cls.PASS_DIR, '.git')):
                root = os.path.normpath(os.path.relpath(root, cls.PASS_DIR))
                dirs = [os.path.join('', d) for d in dirs if d != '.git']
                files = [file.rstrip('.gpg') for file in files if file.endswith('.gpg')]
                if root == '.':
                    root = ''
                dir_contents[root] = Directory(root, dirs, files)
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
        # name          fg              bg              style
        ('border',      'light cyan',   'default'),
        ('dir',         'light green',  'default'),
        ('alert',       'light red',    'default'),
        ('focus',       'black',        'white'),
        ('focusdir',    'black',        'light green',  'bold'),
    ])
    # set no timeout after escape key
    loop.screen.set_input_timeouts(complete_wait=0)
    loop.run()
