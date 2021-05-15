# cpass: another console UI for pass

[`pass`](https://www.passwordstore.org/) is the standard unix password manager. This program `cpass` is a [urwid](http://urwid.org/) based terminal user interface (TUI) for that password manager with mouse support and vim-like keybindings.

## Features:

- browse local password store

## Features to-be:

- pass operations, e.g., add, remove, generate, edit, search
- copy password or other information
- basic pass git operations and status

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/)

## Usage:

Make sure you are using a local password store compatible with [`pass`](https://www.passwordstore.org/), `cpass` will look in `$PASSWORD_STORE_DIR`, otherwise in `~/.password_store/`. `pass` is also required, although theoretically a `pass` compatible client does not need `pass` command (e.g., [qtpass](https://qtpass.org/) can work with `git` and `gpg`).

`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported very well.

### Start `cpass`

### Keybindings

Basic common keybindings just work as you would use in a lot of other programs:

`h`, `j`, `k`, `l`, `g`, `G`, `ctrl+d`, `ctrl+u`, `ctrl+f`, `ctrl+b`, `ctrl+n`, `ctrl+p`

For `pass` related operations (mostly todo):

- `d` will delete current password file or directory after user confirms
- `a` or `i` will add a new password in current directory
- `A` or `I` will generate a new password in current directory
- `/` will start a search

### Mouse

This is very intuitive.

- Scroll to navigate up and down in the current list.
- Left click on the current highlighted item will open it, while left click on other items will highlight it.
- Right click will go to the parent folder.
