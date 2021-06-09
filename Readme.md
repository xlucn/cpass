# cpass: another console UI for pass

DISCLAIMER: I do not guarantee that this program always runs as intended, so back up your passwords or use git (by `pass git init`) to manage the password store, that way the changes can be reverted. I will only use `pass` command in the program to avoid incorrect operations on the password files as much as possible.

`cpass` is an [urwid](http://urwid.org/) based terminal user interface (TUI) for the standard unix password manager, [`pass`](https://www.passwordstore.org/), with mouse support and vim-like keybindings.

`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported quite well.

![](https://github.com/OliverLew/oliverlew.github.io/blob/pictures/cpass.png?raw=true)

## Features:

- Browse the local password store
- Preview the folder and password content in a preview window
- Colors, key bindings and other customizations through a configuration file
- Password file operations, e.g., add, generate, edit, remove

## Features to-be:

- Copy password in various ways, e.g., first line, all lines, specific field (also customizable)
- Search password files
- Basic pass git operations and status indicator
- Password file operations, e.g., copy, move, rename (low priority, since can be done with file managers)

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/)

Make sure you are using a local password store created/compatible with [`pass`](https://www.passwordstore.org/), which `cpass` will look for in `$PASSWORD_STORE_DIR`, otherwise in `~/.password_store/`. `pass` is also required, although theoretically a `pass` compatible client does not need `pass` command (e.g., [qtpass](https://qtpass.org/) can work with `git` and `gpg`). However, `pass` does a lot of things to assure the robustness and security of password management, there is no need to reinvent the wheels.

## Usage:

### Start `cpass`

For now, just start the python script.

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
