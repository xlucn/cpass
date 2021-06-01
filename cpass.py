#!/usr/bin/env python3
# Author: Lu Xu <oliver_lew at outlook dot com>
# License: MIT License Copyright (c) 2021 Lu Xu
import os
import re
import urwid
import configparser
from subprocess import run, PIPE

version = "0.3.1"


def debug(message):
    if os.getenv('DEBUG'):
        open('log', 'a').write(message.rstrip('\n') + '\n')
        passui.message(message)


class PassNode(urwid.AttrMap):
    def __init__(self, node, root, isdir=False):
        """ node=None to represent empty node """
        self._selectable = True

        self.node = node
        self.isdir = isdir
        self.text = node if node else "-- EMPTY --"
        self.path = os.path.join(root, node) if node else ''
        self.icon = arg_icon_dir if isdir else arg_icon_file if node else ''
        # topdown option in os.walk makes this possible
        self.count = str(len(Pass.all_pass[self.path])) if isdir else ''

        super().__init__(urwid.Columns([
                ('pack', urwid.Text(self.icon)),
                urwid.Text(self.text, wrap='clip'),
                ('pack', urwid.Text(self.count))
            ]),
            'dir' if isdir else '' if node else 'bright',
            'focusdir' if isdir else 'focus' if node else 'bright',
        )

    def keypress(self, size, key):
        """ let the widget pass through the keys to parent widget """
        return key


class PassList(urwid.ListBox):
    def __init__(self, body, root='', ui=None):
        self._ui = ui
        self.root = root
        super().__init__(body)

    def mouse_event(self, size, event, button, col, row, focus):
        focus_offset = self.get_focus_offset_inset(size)[0]

        debug("passlist mouse event: {} {} {} {} {} {} {} {}".format(
            size, event, button, col, row, focus, self.focus_position, focus_offset
        ))

        if button == 1:
            if size[1] > len(self.body):
                # NOTE: offset is wrong(?) when size is larger than length
                # so the processing is different
                if row == self.focus_position:
                    self.dir_navigate('down')
                else:
                    self.list_navigate(size, new_focus=row)
            else:
                if row == focus_offset:
                    self.dir_navigate('down')
                else:
                    self.list_navigate(size, new_focus=self.focus_position - focus_offset + row)
        elif button == 3:
            self.dir_navigate('up')
        elif button == 4:
            self.list_navigate(size, -1)
        elif button == 5:
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
            self.body.insert(self.focus_position, PassNode('foonew', self.root))
        elif key in ['A', 'I']:
            # dummy generate
            self.body.insert(self.focus_position, PassNode('foonew', self.root))
        elif key in ['e']:
            if not self.focus.isdir:
                self._ui.message(Pass.edit(os.path.join(self.root, self.focus.node)))
        else:
            return super().keypress(size, key)

    def dir_navigate(self, direction):
        debug("body length: {}".format(len(self.body)))

        # record current position
        Pass.all_pass[self.root].pos = self.focus_position

        # change root position accordingly
        if direction in 'down' and self.focus.isdir:
            self.root = os.path.join(self.root, self.focus.node)
        elif direction in 'up':
            self.root = os.path.dirname(self.root)

        # update listbox content, this way the list itself is not replaced
        self.body[:] = Pass.all_pass[self.root]

        # restore cursor position of the new root
        self.focus_position = Pass.all_pass[self.root].pos

        self._ui.update_view()

    def list_navigate(self, size, shift=0, new_focus=None):
        offset = self.get_focus_offset_inset(size)[0]

        # either specify a shift offset, or an absolute position
        if new_focus is None:
            new_focus = self.focus_position + shift
        else:
            shift = new_focus - self.focus_position
        new_offset = offset + shift

        # border check
        new_focus = min(max(new_focus, 0), len(self.body) - 1)
        new_offset = min(max(new_offset, 0), size[1] - 1)

        self.change_focus(size, new_focus, offset_inset=new_offset)
        self._ui.update_view()


class FolderWalker(list):
    def __init__(self, root, dirs, files):
        self.pos = 0  # cursor position

        self[:] = [PassNode(f, root, f in dirs) for f in sorted(dirs) + sorted(files)]
        if len(self) == 0:
            self[:] = [PassNode(None, None)]


class UI(urwid.Frame):
    def __init__(self):
        self._last_preview = None
        self._app_string = 'cPass'
        self._preview_shown = True
        self._edit_type = None
        self._help_string = ' a/i:add e:edit z:toggle'

        # widgets
        self.path_indicator = urwid.Text('', wrap='clip')
        self.help_text = urwid.Text(self._help_string)
        self.header_widget = urwid.Columns([self.path_indicator, ('pack', self.help_text)])
        self.messagebox = urwid.Text('')
        self.count_indicator = urwid.Text('', align='right')
        self.footer_widget = urwid.Columns([
            self.messagebox,
            ('pack', urwid.AttrMap(self.count_indicator, 'border'))
        ])
        self.divider = urwid.AttrMap(urwid.Divider('-'), 'border')
        self.preview = urwid.Filler(urwid.Text(''), valign='top')
        self.editbox = urwid.Edit()

        self.walker = urwid.SimpleListWalker(Pass.all_pass[''])
        self.listbox = PassList(self.walker, ui=self)

        # use Columns for horizonal layout, and Pile for vertical
        if arg_preview in ['side', 'horizontal']:
            self.middle = urwid.Columns([], dividechars=1)
        elif arg_preview in ['bottom', 'vertical']:
            self.middle = urwid.Pile([])
        self.update_preview_layout()

        super().__init__(self.middle, self.header_widget, self.footer_widget)

    def message(self, message, alert=False):
        self.messagebox.set_text(('alert' if alert else 'normal', message))

    def update_preview_layout(self):
        if self._preview_shown:
            if arg_preview in ['side', 'horizontal']:
                self.middle.contents = [(self.listbox, ('weight', 1, False)),
                                           (self.preview, ('weight', 1, False))]
            if arg_preview in ['bottom', 'vertical']:
                self.middle.contents = [(self.listbox, ('weight', 1)),
                                           (self.divider, ('pack', 1)),
                                           (self.preview, ('weight', 1))]
        else:
            self.middle.contents = [(self.listbox, ('weight', 1, False))]
        self.middle.focus_position = 0
        self.update_preview()

    def keypress(self, size, key):
        debug("ui keypress: {} {}".format(key, size))
        if key in ['esc']:
            self.messagebox.set_text('')
            self.unfocus_edit()
        elif key in ['enter']:
            if self._edit_type == "search":
                # dummy search
                self.unfocus_edit()
            elif self._edit_type.startswith("insert"):
                self.insert()
        elif self._edit_type is not None:
            # pass through to edit widget
            # NOTE: is this the right way to do it?
            super().keypress(size, key)
        elif key in ['/']:
            self._edit_type = "search"
            self.editbox.set_caption('/')
            self.focus_edit()
        elif key in ['a', 'i']:
            self._edit_type = "insert"
            self.editbox.set_caption('Enter password filename: ')
            self.focus_edit()
        elif key in ['z']:
            self._preview_shown = not self._preview_shown
            self.update_preview_layout()
        else:
            return super().keypress(size, key)

    def unfocus_edit(self):
        self.contents['footer'] = (self.footer_widget, None)
        self.set_focus('body')
        self.editbox.set_mask(None)
        self._edit_type = None

    def focus_edit(self):
        self.contents['footer'] = (self.editbox, None)
        self.set_focus('footer')
        self.editbox.set_edit_text('')

    def insert(self):
        if self._edit_type == "insert":
            self._insert_path = os.path.join(self.listbox.root, self.editbox.edit_text)
            self._edit_type = "insert_password"
            self.editbox.set_caption('Enter password: ')
            self.editbox.set_mask("*")
            self.editbox.set_edit_text('')
        elif self._edit_type == "insert_password":
            self._insert_pass = self.editbox.edit_text
            self._edit_type = "insert_password_confirm"
            self.editbox.set_caption('Enter password again: ')
            self.editbox.set_mask("*")
            self.editbox.set_edit_text('')
        elif self._edit_type == "insert_password_confirm":
            self.insert_pass_again = self.editbox.edit_text
            self.editbox.set_mask(None)
            self.editbox.set_edit_text('')
            self.unfocus_edit()
            if self._insert_pass == self.insert_pass_again:
                Pass.insert(self._insert_path, self._insert_pass)
            else:
                self.message("Password is not the same", alert=True)

    def update_view(self):
        # update header
        self.path_indicator.set_text([
            ('border', '{}: '.format(self._app_string)),
            ('bright', '/{}'.format(self.listbox.root)),
        ])

        # update footer
        self.count_indicator.set_text("{}/{}".format(
            self.listbox.focus_position + 1,
            len(self.listbox.body)
        ) if self.listbox.focus.node else "0/0")

        if self._preview_shown:
            self.update_preview()

    def update_preview(self):
        node = self.listbox.focus.text
        path = os.path.join(self.listbox.root, node)

        if path == self._last_preview:
            return
        self._last_preview = path

        if self.listbox.focus.isdir:
            preview = "\n".join([(f.icon + f.text) for f in Pass.all_pass[path]])
        elif self.listbox.focus.node is None:
            preview = ""
        else:
            preview = Pass.show(path)
        self.preview.original_widget.set_text(preview)


class Pass:
    FALLBACK_PASS_DIR = os.path.join(os.getenv("HOME"), ".password_store")
    PASS_DIR = os.getenv("PASSWORD_STORE_DIR", FALLBACK_PASS_DIR)
    all_pass = {}

    @classmethod
    def extract_all(cls):
        # pass files traversal, topdown option is essential, see PassNode
        for root, dirs, files in os.walk(cls.PASS_DIR, topdown=False):
            if not root.startswith(os.path.join(cls.PASS_DIR, '.git')):
                root = os.path.normpath(os.path.relpath(root, cls.PASS_DIR))
                dirs = [os.path.join('', d) for d in dirs if d != '.git']
                files = [file[:-4] for file in files if file.endswith('.gpg')]
                if root == '.':
                    root = ''
                cls.all_pass[root] = FolderWalker(root, dirs, files)

    @staticmethod
    def show(node):
        result = run(['pass', 'show', node], stdout=PIPE, stderr=PIPE, text=True)
        main.screen.clear()
        return result.stderr if result.returncode else result.stdout

    @staticmethod
    def edit(node):
        # can not pipe stdout because this will start vim
        result = run(['pass', 'edit', node], stderr=PIPE, text=True)
        main.screen.clear()
        return result.stderr

    @staticmethod
    def insert(node, password):
        pw = password + '\n' + password + '\n'
        result = run(['pass', 'insert', node], input=pw, stderr=PIPE, text=True)
        main.screen.clear()
        return result.stderr


def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop


class MyConfigParser(configparser.RawConfigParser):
    def __init__(self):
        DEFAULT_CONFIG_DIR = os.path.join(os.getenv("HOME"), ".config")
        CONFIG_DIR = os.getenv("XDG_CONFIG_DIR", DEFAULT_CONFIG_DIR)
        CONFIG = os.path.join(CONFIG_DIR, "cpass", "cpass.cfg")
        super().__init__()
        if os.path.exists(CONFIG):
            self.read(CONFIG)

    def get(self, section, option, fallback=None):
        try:
            return super().get(section, option).strip("\"\'")
        except (configparser.NoOptionError, configparser.NoSectionError):
            return fallback


if __name__ == '__main__':
    config = MyConfigParser()
    arg_preview = config.get('ui', 'preview', 'side')
    arg_icon_dir = config.get('icon', 'dir', '/')
    arg_icon_file = config.get('icon', 'file', ' ')

    Pass.extract_all()
    # UI
    passui = UI()

    palette = [
        # name          fg              bg              style
        ('normal',      'default',      'default'),
        ('border',      'light green',  'default'),
        ('dir',         'light blue',   'default'),
        ('alert',       'light red',    'default'),
        ('bright',      'white',        'default'),
        ('focus',       'black',        'white'),
        ('focusdir',    'black',        'light blue',   'bold'),
    ]
    # update from configuration file
    for attr in palette:
        colors = config.get('color', attr[0])
        if colors:
            palette[palette.index(attr)] = (attr[0], *re.split(',\\s*', colors))

    # main loop
    main = urwid.MainLoop(passui, unhandled_input=unhandled_input, palette=palette)
    # set no timeout after escape key
    main.screen.set_input_timeouts(complete_wait=0)
    main.run()
