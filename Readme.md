# cpass: another console UI for pass

[`pass`](https://www.passwordstore.org/) is the standard unix password manager. This program `cpass` is an [urwid](http://urwid.org/) based terminal user interface (TUI) for that password manager with mouse support and vim-like keybindings.

`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported very well.

## Features:

- browse local password store
- color, key binding and other customizations through configuration file
- pass operations, e.g., add, generate, edit, remove

## Features to-be:

- pass operations, e.g., copy, move, search
- copy password or other information
- basic pass git operations and status

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/)

## Usage:

Make sure you are using a local password store compatible with [`pass`](https://www.passwordstore.org/), `cpass` will look in `$PASSWORD_STORE_DIR`, otherwise in `~/.password_store/`. `pass` is also required, although theoretically a `pass` compatible client does not need `pass` command (e.g., [qtpass](https://qtpass.org/) can work with `git` and `gpg`).

### Start `cpass`

To be determined.

### Configuration file

Some appearances or behaviors in the program can be customized through a configuration file located at `$XDG_CONFIG_DIR/cpass/cpass.cfg` or `$HOME/.config/cpass/cpass.cfg`. Most importantly, the key bindings and colors can be changed. For more details see the comments in the example `cpass.cfg` provided in the repo.

### Keybindings

Basic common keybindings just work as you would use in a lot of other programs:

`h`, `j`, `k`, `l`, `g`, `G`, `ctrl+d`, `ctrl+u`, `ctrl+f`, `ctrl+b`, `ctrl+n`, `ctrl+p`

For `pass` related operations:
- `i` will add a new password in current directory
- `a` will generate a new password in current directory
- `d` will delete current password file or directory after user confirms
- `e` edit current password
- `z` toggle preview

To-do ones

- `I` to add multiline password
- `A` to generate with more options
- `r` rename the file
- `/` will start a search
- `D`, `Y`, `P` remove, copy and paste item
- `y` + `y/G/a/[0-9]` copy contents in password

### Mouse

This is very intuitive.

- Scroll to navigate up and down in the current list.
- Left-click on the current highlighted item will open it, while left click on other items will highlight it.
- Right-click will go to the parent folder.
