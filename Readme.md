# cpass: another console UI for pass

**!DISCLAIMER!**: Before the version 1.0.0, I do not guarantee that this program will always run as intended.
So it is recommended to back up your passwords or use git (by `pass git init`) to manage the password store, so that the changes can be reverted.
On my side, I only use `pass` commands to interact with the password store to minimise any possible damages.
So simply do `pass git reset --hard <some commit>` to revert any changes.

`cpass` is an [urwid](http://urwid.org/) based terminal user interface (TUI) for the standard unix password manager, [pass](https://www.passwordstore.org/).
`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported quite well.

![](https://github.com/OliverLew/oliverlew.github.io/blob/pictures/cpass.png?raw=true)

## Features:

- Browse the local password store
- Preview the folder and password content in a preview window
- Colors, key bindings and other customizations through a configuration file
- Password file operations, e.g., add, generate, edit, remove
- Copy password in various ways, e.g., first line, all lines, specific field (also customizable)

Features to-be:

- Search password files
- Basic pass git operations and status indicator
- Password file operations, e.g., copy, move, rename (low priority, since can be done with file managers, but it is worth implementing since `pass` commands will create git commits which protect the data)

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/)

Make sure you are using a local password store created/compatible with [`pass`](https://www.passwordstore.org/), which `cpass` will look for in `$PASSWORD_STORE_DIR`, otherwise in `~/.password_store/`.
`pass` is also required, although theoretically a `pass` compatible client does not need `pass` command (e.g., [qtpass](https://qtpass.org/) can work with `git` and `gpg`).
However, `pass` does a lot of things to assure the robustness and security of password management, there is no need to reinvent the wheels.

## Install

- As python package:
  ```
  pip install --user cpass
  ```

- Clone the repo or download the single script file.

## Usage:

### Start `cpass`

For now, just run `cpass`.

### Keybindings

Basic common keybindings just work as you would use in a lot of other programs:

`h`, `j`, `k`, `l`, `g`, `G`, `ctrl+d`, `ctrl+u`, `ctrl+f`, `ctrl+b`, `ctrl+n`, `ctrl+p`

For `pass` related operations:
- `i` add a new password in current directory
- `a` generate a new password in current directory
- `d` delete current password file or directory after user confirms
- `e` edit current password
- `z` toggle preview
- `y` + `y/a/[0-9]` copy contents in password

To-do ones

- `I` to add multiline password
- `A` to generate with more options
- `r` rename the file
- `/` will start a search
- `D`, `Y`, `P` remove, copy and paste item

### Mouse

This is very intuitive.

- Scroll to navigate up and down in the current list.
- Left-click on the current highlighted item will open it, while left click on other items will highlight it.
- Right-click will go to the parent folder.

## Configuration

Some appearances or behaviors in the program can be customized through a configuration file located at `$XDG_CONFIG_DIR/cpass/cpass.cfg` or `$HOME/.config/cpass/cpass.cfg`.
Most importantly, the key bindings and colors can be changed. For more details see the comments in the example `cpass.cfg` provided in the repo.

There are different sections in the configuration file for different type of options, as listed below.

- `ui`: UI layout.

  Control the preview window layout, either vertical or horizontal split.
  ```
  [ui]
  preview_layout = side/bottom/horizontal/vertical
  ```

- `pass`: `pass` related options.

  Whether use `--no-symbols` option in `pass generate`.
  ```
  [pass]
  no_symbols = true/false
  ```

- `keys`: Key bindings.

  For all actions available, see the example configuration file. For the format to specify keys, see the [urwid documentation](http://urwid.org/manual/userinput.html#keyboard-input)
  ```
  [keys]
  down = j, down, ctrl n
  up = k, up, ctrl p
  ```

- `copy_fields`: Copy key bindings.

  The copy behavior can be customized by specifying a key for any field. So at the copy prompt, pressing that key will copy the corresponding field.
  ```
  [copy_fields]
  login = l
  ```

- `color`: Colors.

  See urwid documentation for [definition](http://urwid.org/reference/display_modules.html#urwid.BaseScreen.register_palette_entry), [an palette example](http://urwid.org/manual/displaymodules.html#setting-a-palette) and [available color names](http://urwid.org/reference/constants.html#foreground-and-background-colors)
  ```
  [color]
  normal   = default, default
  dir      = light blue, default
  ```

- `icon`: Icons for folder and files.

  You can specify fancy icons like (below is the Meterial Design Icons I use, they are not default)
  ```
  [icon]
  dir     = "󰉋 "
  file    = "󰈤 "
  ```
