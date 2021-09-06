# cpass: another console UI for pass

**!DISCLAIMER!**: Before the version 1.0.0, I do not guarantee that this program will always run as intended.
So it is recommended to back up your passwords or use git (by `pass git init`) to manage the password store, so that the changes can be reverted.
On my side, I only use `pass` commands to interact with the password store to minimize any possible damages.
So simply do `pass git reset --hard <some commit>` to revert any changes.

---

`cpass` is an [urwid](http://urwid.org/) based terminal user interface (TUI) for the standard unix password manager, [pass](https://www.passwordstore.org/).
`cpass` tries to achieve a minimal, clean interface and utilizes vim-like keybinding. Also, thanks to the urwid module, mouse is supported quite well.

## Features:

- Browse the local password store and preview the folder and password content
- Colors, key bindings and other customizability
- Pass operations, e.g., add, generate, edit, remove
- Copy password in various ways (also customizable)
- Search password within the current window, like in vim (smart case sensitivity)

Features todo list:

- More pass operations, e.g., find, copy, move, rename, git, otp

## Requirement

- [pass](https://www.passwordstore.org/)
- [urwid](http://urwid.org/) module
- [xclip](https://github.com/astrand/xclip) for copying passwords

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

There is an example configuration file [cpass.cfg](cpass.cfg) with all available options set to the default value, with detailed comments. You don't have to copy the whole file, because it does not change the default behavior of `cpass`.

Two sections, the `keys` and `color`, need some references:
- Key bindings in `keys` section:
  - For all actions available to bind, see the example configuration file.
  - For the format to specify keys, see the [urwid documentation](http://urwid.org/manual/userinput.html#keyboard-input).
- Colors in `color` section. The configuration is similar to (can be seen as) an urwid pallete consisting of multiple display attributes. In the example [cpass.cfg](cpass.cfg) I provided enough information to get started. If you want to know more:
  - See urwid documentation for [definition of a pallete](http://urwid.org/reference/display_modules.html#urwid.BaseScreen.register_palette_entry) and [a palette example](http://urwid.org/manual/displaymodules.html#setting-a-palette).
  - Also refer to documentation of the [available color names](http://urwid.org/reference/constants.html#foreground-and-background-colors) and general information on [display attributes](http://urwid.org/manual/displayattributes.html).

This is an overview of what can be customized through the configuration file, for the complete list of options, see [cpass.cfg](cpass.cfg):
```
[ui]
preview_layout = side/bottom/horizontal/vertical

[pass]
no_symbols = true/false

[keys]
down = j, down, ctrl n
up = k, up, ctrl p

[copy_fields]
login = l

[color]
normal   = default, default
dir      = light blue, default

[icon]
dir     = "󰉋 "
file    = "󰈤 "
```

## Screenshot

https://user-images.githubusercontent.com/12032219/123406878-f338b280-d5dd-11eb-951e-2a4fc185a65d.mp4
