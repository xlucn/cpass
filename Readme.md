# cpass: another console UI for pass

**!DISCLAIMER!**: Before the version 1.0.0, I do not guarantee that this program will always run as intended.
So it is recommended to back up your passwords or use git (by `pass git init`) to manage the password store, so that the changes can be reverted.
On my side, I only use `pass` commands to interact with the password store to minimize any possible damages.
So simply do `pass git reset --hard <some commit>` to revert any changes.

`cpass` is an [urwid](http://urwid.org/) based terminal user interface (TUI) for the standard unix password manager, [pass](https://www.passwordstore.org/).
`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported quite well.

https://user-images.githubusercontent.com/12032219/123406878-f338b280-d5dd-11eb-951e-2a4fc185a65d.mp4

## Features:

- Browse the local password store
- Preview the folder and password content in a preview window
- Colors, key bindings and other customizations through a configuration file
- Password file operations, e.g., add, generate, edit, remove
- Copy password in various ways, e.g., first line, all lines, specific field (also customizable)
- Search keywords within the current window, the general vim-like operation. The searching is smart in case sensitivity, i.e., ignore case when the search keywords contains upper case characters.

Features todo list:

- Find passwords globally in the password store, the pass find operation
- Basic pass git operations and status indicator
- Password file operations, e.g., copy, move, rename (low priority, since can be done with file managers, but it is worth implementing since `pass` commands will create git commits which protect the data)
- QR code, maybe?
- Asynchronous preview, or/and cache preview results
- OTP support

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/) module
- `xclip` for copy passwords

Make sure you are using a local password store created/compatible with [`pass`](https://www.passwordstore.org/), which `cpass` will look for in `$PASSWORD_STORE_DIR`, otherwise in `~/.password_store/`.
`pass` is also required, although theoretically a `pass` compatible client does not need `pass` command (e.g., [qtpass](https://qtpass.org/) can work with `git` and `gpg`).
However, `pass` does a lot of things to assure the robustness and security of password management, there is no need to reinvent the wheels.

## Install

- As python package:
  ```
  pip install --user cpass
  ```
  
- Install with GNU Guix

  The [GuixRUs](https://git.sr.ht/~whereiseveryone/guixrus) channel also provides `cpass`.

  After [adding](https://git.sr.ht/~whereiseveryone/guixrus#subscribing) `GuixRUs` to your [channels.scm](https://guix.gnu.org/manual/en/html_node/Using-a-Custom-Guix-Channel.html), run the following two commands:

  ```
  guix pull
  guix install cpass
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
- `y` + `y/a/[0-9]` copy contents in password ('0' to copy the 10th line)
- `/` or `?` will start a search (forward/backward)
- `n` or `N` go to next or previous search result

To-do ones (might change)

- `I` to add multiline password
- `A` to generate with more options
- `r` rename the file
- `D`, `Y`, `P` remove, copy and paste item

### Mouse

This is very intuitive.

- Scroll to navigate up and down in the current list.
- Left-click on the current highlighted item will open it, while left click on other items will highlight it.
- Right-click will go to the parent folder.

## Configuration

Some appearances or behaviors in the program can be customized through a configuration file located at `$XDG_CONFIG_DIR/cpass/cpass.cfg` or `$HOME/.config/cpass/cpass.cfg`.
Most importantly, the key bindings and colors can be changed.

There is an example configuration file [cpass.cfg](cpass.cfg) with all available options set to the default value, with detailed comments. You don't have to copy the whole file, because it does not change the default behavior of `cpass`. The different sections in the configuration file corresponds to different types of options, as listed below.

- `ui`: UI layout.

  Control the preview window layout, either vertical or horizontal split.
  ```
  [ui]
  preview_layout = side/bottom/horizontal/vertical
  ```

- `pass`: `pass` related options.

  Whether to use `--no-symbols` option in `pass generate`.
  ```
  [pass]
  no_symbols = true/false
  ```

- `keys`: Key bindings.

  For all actions available, see the example configuration file. For the format to specify keys, see the [urwid documentation](http://urwid.org/manual/userinput.html#keyboard-input).
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

  See urwid documentation for [definition](http://urwid.org/reference/display_modules.html#urwid.BaseScreen.register_palette_entry), [a palette example](http://urwid.org/manual/displaymodules.html#setting-a-palette) and [available color names](http://urwid.org/reference/constants.html#foreground-and-background-colors)
  ```
  [color]
  normal   = default, default
  dir      = light blue, default
  ```

- `icon`: Icons for folder and files.

  You can specify fancy icons like (below is the Material Design Icons I use, they are not default)
  ```
  [icon]
  dir     = "󰉋 "
  file    = "󰈤 "
  ```
