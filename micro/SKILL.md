---
name: micro
description: Expert reference for the micro terminal-based text editor (github.com/zyedidia/micro) — the `micro` command. Use this skill whenever the user asks about micro the editor: configuring it, keybindings and rebinding keys, the command bar and commands, options/settings, colorschemes and syntax highlighting, writing or managing plugins, copy/paste (including over SSH), or how any micro feature works. Trigger it even when the user does not say "skill" — any question about using or configuring the micro editor qualifies.
---
# micro editor expert reference

This skill turns you into an expert on the [micro](https://github.com/zyedidia/micro)
terminal-based text editor. The complete text of micro's built-in help topics
(everything reachable via `> help <topic>` inside the editor) and the
project README are inlined below, copied verbatim from the micro source tree.

Read the relevant sections before answering, then advise the user precisely.

## How to use this reference

- Answer from the inlined docs below, not from memory. When micro's behavior is
  in question, the text here is authoritative.
- Use exact names: micro's key names (e.g. `Ctrl-e`, `Alt-g`), command
  names, option keys, and colorscheme group names are precise. Quote them exactly
  as written in the docs.
- When the user wants to change behavior, point them at the concrete mechanism:
  a `bindings.json` entry, a `settings.json` option, a
  `> command`, or an `init.lua` snippet — with the exact syntax
  from the docs.
- Distinguish default keybindings (see the defaultkeys topic) from the full
  rebinding system (the keybindings topic).
- For anything the docs do not cover, say so plainly rather than guessing.

## Contents

The following documents are reproduced verbatim below, in order:

1. `README.md` — project overview and feature summary
2. `runtime/help/help.md`
3. `runtime/help/tutorial.md`
4. `runtime/help/defaultkeys.md`
5. `runtime/help/keybindings.md`
6. `runtime/help/commands.md`
7. `runtime/help/options.md`
8. `runtime/help/copypaste.md`
9. `runtime/help/colors.md`
10. `runtime/help/plugins.md`


---

<!-- Verbatim copy of README.md from the micro source tree. -->

<img alt="micro logo" src="./assets/micro-logo-drop.svg" width="500px"/>

![Test Workflow](https://github.com/micro-editor/micro/actions/workflows/test.yaml/badge.svg)
[![Go Report Card](https://goreportcard.com/badge/github.com/micro-editor/micro/v2)](https://goreportcard.com/report/github.com/micro-editor/micro/v2)
[![Release](https://img.shields.io/github/release/micro-editor/micro.svg?label=Release)](https://github.com/micro-editor/micro/releases)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/micro-editor/micro/blob/master/LICENSE)
[![Join the chat at https://gitter.im/zyedidia/micro](https://badges.gitter.im/zyedidia/micro.svg)](https://gitter.im/zyedidia/micro?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Snap Status](https://snapcraft.io/micro/badge.svg)](https://snapcraft.io/micro)

**micro** is a terminal-based text editor that aims to be easy to use and intuitive, while also taking advantage of the capabilities
of modern terminals. It comes as a single, batteries-included, static binary with no dependencies; you can download and use it right now!

As its name indicates, micro aims to be somewhat of a successor to the nano editor by being easy to install and use.
It strives to be enjoyable as a full-time editor for people who prefer to work in a terminal, or those who regularly edit files over SSH.

Here is a picture of micro editing its source code.

![Screenshot](./assets/micro-solarized.png)

To see more screenshots of micro, showcasing some of the default color schemes, see [here](https://micro-editor.github.io).

You can also check out the website for Micro at https://micro-editor.github.io.

- - -

## Features

- Easy to use and install.
- No dependencies or external files are needed — just the binary you can download further down the page.
- Multiple cursors.
- Common keybindings (<kbd>Ctrl-s</kbd>, <kbd>Ctrl-c</kbd>, <kbd>Ctrl-v</kbd>, <kbd>Ctrl-z</kbd>, …).
  - Keybindings can be rebound to your liking.
- Sane defaults.
  - You shouldn't have to configure much out of the box (and it is extremely easy to configure).
- Splits and tabs.
- nano-like menu to help you remember the keybindings.
- Extremely good mouse support.
  - This means mouse dragging to create a selection, double click to select by word, and triple click to select by line.
- Cross-platform (it should work on all the platforms Go runs on).
  - Note that while Windows is supported, Mingw/Cygwin is not (see below).
- Plugin system (plugins are written in Lua).
  - micro has a built-in plugin manager to automatically install, remove, and update plugins.
- Built-in diff gutter.
- Simple autocompletion.
- Persistent undo.
- Automatic linting and error notifications.
- Syntax highlighting for over [130 languages](runtime/syntax).
- Color scheme support.
  - By default, micro comes with 16, 256, and true color themes.
- True color support.
- Copy and paste with the system clipboard.
- Small and simple.
- Easily configurable.
- Macros.
- Smart highlighting of trailing whitespace and tab vs space errors.
- Common editor features such as undo/redo, line numbers, Unicode support, soft wrapping, …

## Installation

To install micro, you can download a [prebuilt binary](https://github.com/micro-editor/micro/releases), or you can build it from source.

If you want more information about ways to install micro, see this [wiki page](https://github.com/micro-editor/micro/wiki/Installing-Micro).

Use `micro -version` to get the version information after installing. It is only guaranteed that you are installing the most recent
stable version if you install from the prebuilt binaries, Homebrew, or Snap.

A desktop entry file and man page can be found in the [assets/packaging](https://github.com/micro-editor/micro/tree/master/assets/packaging) directory.

### Pre-built binaries

Pre-built binaries are distributed in [releases](https://github.com/micro-editor/micro/releases).

To uninstall micro, simply remove the binary, and the configuration directory at `~/.config/micro`.

#### Third-party quick-install script

```bash
curl https://getmic.ro | bash
```

The script will place the micro binary in the current directory. From there, you can move it to a directory on your path of your choosing (e.g. `sudo mv micro /usr/bin`). See its [GitHub repository](https://github.com/benweissmann/getmic.ro) for more information.

#### Eget

With [Eget](https://github.com/zyedidia/eget) installed, you can easily get a pre-built binary:

```
eget micro-editor/micro
```

Use `--tag VERSION` to download a specific tagged version.

```
eget --tag nightly micro-editor/micro # download the nightly version (compiled every day at midnight UTC)
eget --tag v2.0.8 micro-editor/micro  # download version 2.0.8 rather than the latest release
```

You can install `micro` by adding `--to /usr/local/bin` to the `eget` command, or move the binary manually to a directory on your `$PATH` after the download completes.

See [Eget](https://github.com/zyedidia/eget) for more information.

### Package managers

You can install micro using Homebrew on Mac:

```
brew install micro
```

**Note for Mac:** All micro keybindings use the control or alt (option) key, not the command
key. By default, macOS terminals do not forward alt key events. To fix this, please see
the section on [macOS terminals](https://github.com/micro-editor/micro#macos-terminal) further below.

On Linux, you can install micro through [snap](https://snapcraft.io/docs/core/install)

```
snap install micro --classic
```

Micro is also available through other package managers on Linux such as dnf, AUR, Nix, and package managers
for other operating systems. These packages are not guaranteed to be up-to-date.

<!-- * `apt install micro` (Ubuntu 20.04 `focal`, and Debian `unstable | testing | buster-backports`). At the moment, this package (2.0.1-1) is outdated and has a known bug where debug mode is enabled. -->

* Linux:
    * distro-specific package managers:
        * `dnf install micro` (Fedora).
        * `apt install micro` (Ubuntu and Debian).
        * `pacman -S micro` (Arch Linux).
        * `emerge app-editors/micro` (Gentoo).
        * `zypper install micro-editor` (SUSE)
        * `eopkg install micro` (Solus).
        * `pacstall -I micro` (Pacstall).
        * `apt-get install micro` (ALT Linux)
        * See [wiki](https://github.com/micro-editor/micro/wiki/Installing-Micro) for details about CRUX, Termux.
    * distro-agnostic package managers:
        * `nix profile install nixpkgs#micro` (with [Nix](https://nixos.org/) and flakes enabled)
        * `flox install micro` (with [Flox](https://flox.dev))
* Windows: [Chocolatey](https://chocolatey.org), [Scoop](https://scoop.sh/) and [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/).
    * `choco install micro`.
    * `scoop install micro`.
    * `winget install zyedidia.micro`
* OpenBSD: Available in the ports tree and also available as a binary package.
    * `pkg_add -v micro`.
* NetBSD, macOS, Linux, Illumos, etc. with [pkgsrc](https://www.pkgsrc.org/)-current:
    * `pkg_add micro`
* macOS: Available in package managers.
    * `sudo port install micro` (with [MacPorts](https://www.macports.org))
    * `brew install micro` (with [Homebrew](https://brew.sh/))
    * `nix profile install nixpkgs#micro` (with [Nix](https://nixos.org/) and flakes enabled)
    * `flox install micro` (with [Flox](https://flox.dev))

**Note for Linux desktop environments:**

For interfacing with the local system clipboard, the following tools need to be installed:
* For X11, `xclip` or `xsel`
* For [Wayland](https://wayland.freedesktop.org/), `wl-clipboard`

Without these tools installed, micro will use an internal clipboard for copy and paste, but it won't be accessible to external applications.

### Building from source

If your operating system does not have a binary release, but does run Go, you can build from source.

Make sure that you have Go version 1.19 or greater and Go modules are enabled.

```
git clone https://github.com/micro-editor/micro
cd micro
make build
sudo mv micro /usr/local/bin # optional
```

The binary will be placed in the current directory and can be moved to
anywhere you like (for example `/usr/local/bin`).

The command `make install` will install the binary to `$GOPATH/bin` or `$GOBIN`.

You can install directly with `go get` (`go get github.com/micro-editor/micro/cmd/micro`) but this isn't
recommended because it doesn't build micro with version information (necessary for the plugin manager),
and doesn't disable debug mode.

### Fully static or dynamically linked binary

By default, the micro binary is linked statically to increase the portability of the prebuilt binaries.
This behavior can simply be overriden by providing `CGO_ENABLED=1` to the build target.

```
CGO_ENABLED=1 make build
```

Afterwards the micro binary will dynamically link with the present core system libraries.

**Note for Mac:**
Native macOS builds are done with `CGO_ENABLED=1` forced set to support adding the "Information Property List" in the linker step.

### macOS terminal

If you are using macOS, you should consider using [iTerm2](https://iterm2.com/) instead of the default terminal (Terminal.app). The iTerm2 terminal has much better mouse support as well as better handling of key events. For best keybinding behavior, choose `xterm defaults` under `Preferences->Profiles->Keys->Presets...`, and select `Esc+` for `Left Option Key` in the same menu. The newest versions also support true color.

If you still insist on using the default Mac terminal, be sure to set `Use Option key as Meta key` under
`Preferences->Profiles->Keyboard` to use <kbd>option</kbd> as <kbd>alt</kbd>.

### WSL and Windows Console

If you use micro within WSL, it is highly recommended that you use the [Windows
Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=en-us&gl=us)
instead of the default Windows Console.

If you must use Windows Console for some reason, note that there is a bug in
Windows Console WSL that causes a font change whenever micro tries to access
the external clipboard via powershell. To fix this, use an internal clipboard
with `set clipboard internal` (though your system clipboard will no longer be
available in micro).

### Colors and syntax highlighting

If you open micro and it doesn't seem like syntax highlighting is working, this is probably because
you are using a terminal which does not support 256 color mode. Try changing the color scheme to `simple`
by pressing <kbd>Ctrl-e</kbd> in micro and typing `set colorscheme simple`.

If you are using the default Ubuntu terminal, to enable 256 color mode make sure your `TERM` variable is set
to `xterm-256color`.

Many of the Windows terminals don't support more than 16 colors, which means
that micro's default color scheme won't look very good. You can either set
the color scheme to `simple`, or download and configure a better terminal emulator
than the Windows default.

### Cygwin, Mingw, Plan9

Cygwin, Mingw, and Plan9 are unfortunately not officially supported. In Cygwin and Mingw, micro will often work when run using
the `winpty` utility:

```
winpty micro.exe ...
```

Micro uses the amazing [tcell library](https://github.com/gdamore/tcell), but this
means that micro is restricted to the platforms tcell supports. As a result, micro does not support
Plan9 or Cygwin (although this may change in the future). Micro also doesn't support NaCl (which is deprecated anyway).

## Usage

Once you have built the editor, start it by running `micro path/to/file.txt` or `micro` to open an empty buffer.

micro also supports creating buffers from `stdin`:

```sh
ip a | micro
```

You can move the cursor around with the arrow keys and mouse.

You can also use the mouse to manipulate the text. Simply clicking and dragging
will select text. You can also double click to enable word selection, and triple
click to enable line selection.

## Documentation and Help

micro has a built-in help system which you can access by pressing <kbd>Ctrl-e</kbd> and typing `help`. Additionally, you can
view the help files here:

- [main help](https://github.com/micro-editor/micro/tree/master/runtime/help/help.md)
- [keybindings](https://github.com/micro-editor/micro/tree/master/runtime/help/keybindings.md)
- [commands](https://github.com/micro-editor/micro/tree/master/runtime/help/commands.md)
- [colors](https://github.com/micro-editor/micro/tree/master/runtime/help/colors.md)
- [options](https://github.com/micro-editor/micro/tree/master/runtime/help/options.md)
- [plugins](https://github.com/micro-editor/micro/tree/master/runtime/help/plugins.md)

I also recommend reading the [tutorial](https://github.com/micro-editor/micro/tree/master/runtime/help/tutorial.md) for
a brief introduction to the more powerful configuration features micro offers.

There is also an unofficial Discord, which you can join at https://discord.gg/nhWR6armnR.

## Contributing

If you find any bugs, please report them! I am also happy to accept pull requests from anyone.

You can use the [GitHub issue tracker](https://github.com/micro-editor/micro/issues)
to report bugs, ask questions, or suggest new features.

For a more informal setting to discuss the editor, you can join the [Gitter chat](https://gitter.im/zyedidia/micro) or the [Discord](https://discord.gg/nhWR6armnR). You can also use the [Discussions](https://github.com/micro-editor/micro/discussions) section on GitHub for a forum-like setting or for Q&A.

Sometimes I am unresponsive, and I apologize! If that happens, please ping me.

---

<!-- Verbatim copy of runtime/help/help.md from the micro source tree. -->

# Micro help text

Micro is an easy to use, intuitive, text editor that takes advantage of the
full capabilities of modern terminals.

Micro can be controlled by commands entered on the command bar, or with
keybindings. To open the command bar, press `Ctrl-e`: the `>` prompt will
display. From now on, when the documentation shows a command to run (such as
`> help`), press `Ctrl-e` and type the command followed by enter.

For a list of the default keybindings, run `> help defaultkeys`.
For more information on keybindings, see `> help keybindings`.
To toggle a short list of important keybindings, press Alt-g.

## Quick-start

To quit, press `Ctrl-q`. Save by pressing `Ctrl-s`. Press `Ctrl-e`, as previously
mentioned, to start typing commands. To see which commands are available, at the
prompt, press tab, or view the help topic with `> help commands`.

Move the cursor around with the mouse or with the arrow keys. Enter text simply
by pressing character keys.

If the colorscheme doesn't look good, you can change it with
`> set colorscheme ...`. You can press tab to see the available colorschemes,
or see more information about colorschemes and syntax highlighting with `> help
colors`.

Press `Ctrl-w` to move between splits, and type `> vsplit filename` or
`> hsplit filename` to open a new split.

## Accessing more help

Micro has a built-in help system which can be accessed with the `> help` command.

To view help for the various available topics, press `Ctrl-e` to access command
mode and type in `> help` followed by a topic. Typing just `> help` will open
this page.

Here are the available help topics:

* `tutorial`: A brief tutorial which gives an overview of all the other help
   topics
* `keybindings`: Gives a full list of the default keybindings as well as how to
   rebind them
* `defaultkeys`: Gives a more straight-forward list of the hotkey commands and
   what they do
* `commands`: Gives a list of all the commands and what they do
* `options`: Gives a list of all the options you can customize
* `plugins`: Explains how micro's plugin system works and how to create your own
   plugins
* `colors`: Explains micro's colorscheme and syntax highlighting engine and how
   to create your own colorschemes or add new languages to the engine
* `copypaste`: Explains micro's copy and paste usage and configuration.
   It describes how copy and paste is working on different operating systems and
   setups.

For example, to open the help page on plugins you would run `> help plugins`.

I recommend looking at the `tutorial` help file because it is short for each
section and gives concrete examples of how to use the various configuration
options in micro. However, it does not give the in-depth documentation that the
other topics provide.

---

<!-- Verbatim copy of runtime/help/tutorial.md from the micro source tree. -->

# Tutorial

This is a brief intro to micro's configuration system that will give some
simple examples showing how to configure settings, rebind keys, and use
`init.lua` to configure micro to your liking.

Hopefully you'll find this useful.

See `> help defaultkeys` for a list an explanation of the default keybindings.

### Settings

In micro, your settings are stored in `~/.config/micro/settings.json`, a file
that is created the first time you run micro. It is a json file which holds all
the settings and their values. To change an option, you can either change the
value in the `settings.json` file, or you can type it in directly while using
micro.

Press Ctrl-e to go to command mode, and type `set option value` (in the
future, I will use `> set option value` to indicate pressing Ctrl-e). The change
will take effect immediately and will also be saved to the `settings.json` file
so that the setting will stick even after you close micro.

You can also set options locally which means that the setting will only have
the value you give it in the buffer you set it in. For example, if you have two
splits open, and you type `> setlocal tabsize 2`, the tabsize will only be 2 in
the current buffer. Also micro will not save this local change to the
`settings.json` file. However, you can still set options locally in the
`settings.json` file. For example, if you want the `tabsize` to be 2 only in
Ruby files, and 4 otherwise, you could put the following in `settings.json`:

```json
{
    "*.rb": {
        "tabsize": 2
    },
    "tabsize": 4
}
```

Micro will set the `tabsize` to 2 only in files which match the glob `*.rb`.

If you would like to know more about all the available options, see the
`options` topic (`> help options`).

### Keybindings

Keybindings work in much the same way as options. You configure them using the
`~/.config/micro/bindings.json` file.

For example if you would like to bind `Ctrl-r` to redo you could put the
following in `bindings.json`:

```json
{
    "Ctrl-r": "Redo"
}
```

Very simple.

You can also bind keys while in micro by using the `> bind key action` command,
but the bindings you make with the command won't be saved to the
`bindings.json` file.

For more information about keybindings, like which keys can be bound, and what
actions are available, see the `keybindings` help topic (`> help keybindings`).

### Configuration with Lua

If you need more power than the json files provide, you can use the `init.lua`
file. Create it in `~/.config/micro`. This file is a lua file that is run when
micro starts and is essentially a one-file plugin. The plugin name is
`initlua`.

This example will show you how to use the `init.lua` file by creating a binding
to `Ctrl-r` which will execute the bash command `go run` on the current file,
given that the current file is a Go file.

You can do that by putting the following in `init.lua`:

```lua
local config = import("micro/config")
local shell = import("micro/shell")

function init()
    -- true means overwrite any existing binding to Ctrl-r
    -- this will modify the bindings.json file
    config.TryBindKey("Ctrl-r", "lua:initlua.gorun", true)
end

function gorun(bp)
    local buf = bp.Buf
    if buf:FileType() == "go" then
        -- the true means run in the foreground
        -- the false means send output to stdout (instead of returning it)
        shell.RunInteractiveShell("go run " .. buf.Path, true, false)
    end
end
```

Alternatively, you could get rid of the `TryBindKey` line, and put this line in
the `bindings.json` file:

```json
{
    "Ctrl-r": "lua:initlua.gorun"
}
```

For more information about plugins and the lua system that micro uses, see the
`plugins` help topic (`> help plugins`).

---

<!-- Verbatim copy of runtime/help/defaultkeys.md from the micro source tree. -->

# Default Keys

Below are simple charts of the default hotkeys and their functions. For more
information about binding custom hotkeys or changing default bindings, please
run `> help keybindings`

Please remember that *all* keys here are rebindable! If you don't like it, you
can change it!

### Power user

| Key       | Description of function                                                                           |
|---------- |-------------------------------------------------------------------------------------------------- |
| Ctrl-e    | Open a command prompt for running commands (see `> help commands` for a list of valid commands).  |
| Tab       | In command prompt, it will autocomplete if possible.                                              |
| Ctrl-b    | Run a shell command (this will close micro while your command executes).                          |

### Navigation

| Key                         | Description of function                                                                   |
|---------------------------- |------------------------------------------------------------------------------------------ |
| Arrows                      | Move the cursor around                                                                    |
| Shift-arrows                | Move and select text                                                                      |
| Alt(Ctrl on Mac)-LeftArrow  | Move to the beginning of the current line                                                 |
| Alt(Ctrl on Mac)-RightArrow | Move to the end of the current line                                                       |
| Home                        | Move to the beginning of text on the current line                                         |
| End                         | Move to the end of the current line                                                       |
| Ctrl(Alt on Mac)-LeftArrow  | Move cursor one word left                                                                 |
| Ctrl(Alt on Mac)-RightArrow | Move cursor one word right                                                                |
| Alt-{                       | Move cursor to previous empty line, or beginning of document                              |
| Alt-}                       | Move cursor to next empty line, or end of document                                        |
| PageUp                      | Move cursor up one page                                                                   |
| PageDown                    | Move cursor down one page                                                                 |
| Ctrl-Home or Ctrl-UpArrow   | Move cursor to start of document                                                          |
| Ctrl-End or Ctrl-DownArrow  | Move cursor to end of document                                                            |
| Ctrl-l                      | Jump to a line in the file (prompts with #)                                               |
| Ctrl-w                      | Cycle between splits in the current tab (use `> vsplit` or `> hsplit` to create a split)  |

### Tabs

| Key     | Description of function   |
|-------- |-------------------------- |
| Ctrl-t  | Open a new tab            |
| Alt-,   | Previous tab              |
| Alt-.   | Next tab                  |

### Find Operations

| Key       | Description of function                   |
|---------- |------------------------------------------ |
| Ctrl-f    | Find (opens prompt)                       |
| Ctrl-n    | Find next instance of current search      |
| Ctrl-p    | Find previous instance of current search  |

Note: `Ctrl-n` and `Ctrl-p` should be used from the main buffer, not from inside
the search prompt. After `Ctrl-f`, press enter to complete the search and then
you can use `Ctrl-n` and `Ctrl-p` to cycle through matches.

### File Operations

| Key       | Description of function                                           |
|---------- |------------------------------------------------------------------ |
| Ctrl-q    | Close current file (quits micro if this is the last file open)    |
| Ctrl-o    | Open a file (prompts for filename)                                |
| Ctrl-s    | Save current file                                                 |

### Text operations

| Key                                 | Description of function                   |
|------------------------------------ |------------------------------------------ |
| Ctrl(Alt on Mac)-Shift-RightArrow   | Select word right                         |
| Ctrl(Alt on Mac)-Shift-LeftArrow    | Select word left                          |
| Alt(Ctrl on Mac)-Shift-LeftArrow    | Select to start of current line           |
| Alt(Ctrl on Mac)-Shift-RightArrow   | Select to end of current line             |
| Shift-Home                          | Select to start of current line           |
| Shift-End                           | Select to end of current line             |
| Ctrl-Shift-UpArrow                  | Select to start of file                   |
| Ctrl-Shift-DownArrow                | Select to end of file                     |
| Ctrl-x                              | Cut selected text                         |
| Ctrl-c                              | Copy selected text                        |
| Ctrl-v                              | Paste                                     |
| Ctrl-k                              | Cut current line                          |
| Ctrl-d                              | Duplicate current line                    |
| Ctrl-z                              | Undo                                      |
| Ctrl-y                              | Redo                                      |
| Alt-UpArrow                         | Move current line or selected lines up    |
| Alt-DownArrow                       | Move current line or selected lines down  |
| Alt-Backspace or Alt-Ctrl-h         | Delete word left                          |
| Ctrl-a                              | Select all                                |
| Tab                                 | Indent selected text                      |
| Shift-Tab                           | Unindent selected text                    |

### Macros

| Key       | Description of function                                                           |
|---------- |---------------------------------------------------------------------------------- |
| Ctrl-u    | Toggle macro recording (press Ctrl-u to start recording and press again to stop)  |
| Ctrl-j    | Run latest recorded macro                                                         |

### Multiple cursors

| Key               | Description of function                                                                       |
|------------------ |---------------------------------------------------------------------------------------------- |
| Alt-n             | Create new multiple cursor from selection (will select current word if no current selection)  |
| Alt-Shift-Up      | Spawn a new cursor on the line above the current one                                          |
| Alt-Shift-Down    | Spawn a new cursor on the line below the current one                                          |
| Alt-p             | Remove latest multiple cursor                                                                 |
| Alt-c             | Remove all multiple cursors (cancel)                                                          |
| Alt-x             | Skip multiple cursor selection                                                                |
| Alt-m             | Spawn a new cursor at the beginning of every line in the current selection                    |
| Ctrl-MouseLeft    | Place a multiple cursor at any location                                                       |

### Other

| Key       | Description of function                                                               |
|---------- |-------------------------------------------------------------------------------------- |
| Ctrl-g    | Open help file                                                                        |
| Ctrl-h    | Backspace (old terminals do not support the backspace key and use Ctrl+H instead)     |
| Ctrl-r    | Toggle the line number ruler                                                          |

### Emacs style actions

| Key       | Description of function   |
|---------- |-------------------------- |
| Alt-f     | Next word                 |
| Alt-b     | Previous word             |
| Alt-a     | Move to start of line     |
| Alt-e     | Move to end of line       |

### Function keys.

Warning! The function keys may not work in all terminals!

| Key   | Description of function   |
|------ |-------------------------- |
| F1    | Open help                 |
| F2    | Save                      |
| F3    | Find                      |
| F4    | Quit                      |
| F7    | Find                      |
| F10   | Quit                      |

---

<!-- Verbatim copy of runtime/help/keybindings.md from the micro source tree. -->

# Keybindings

Micro has a plethora of hotkeys that make it easy and powerful to use and all
hotkeys are fully customizable to your liking.

Custom keybindings are stored internally in micro if changed with the `> bind`
command or can also be added in the file `~/.config/micro/bindings.json` as
discussed below. For a list of the default keybindings in the json format used
by micro, please see the end of this file. For a more user-friendly list with
explanations of what the default hotkeys are and what they do, please see
`> help defaultkeys` (a json formatted list of default keys is included
at the end of this document).

If `~/.config/micro/bindings.json` does not exist, you can simply create it.
Micro will know what to do with it.

You can use Ctrl + arrows to move word by word (Alt + arrows for Mac). Alt + left and right
move the cursor to the start and end of the line (Ctrl + left/right for Mac), and Ctrl + up and down move the
cursor to the start and end of the buffer.

You can hold shift with all of these movement actions to select while moving.

## Rebinding keys

The bindings may be rebound using the `~/.config/micro/bindings.json` file.
Each key is bound to an action.

For example, to bind `Ctrl-y` to undo and `Ctrl-z` to redo, you could put the
following in the `bindings.json` file.

```json
{
    "Ctrl-y": "Undo",
    "Ctrl-z": "Redo"
}
```

**Note:** The syntax `<Modifier><key>` is equivalent to `<Modifier>-<key>`. In
addition, `Ctrl-Shift` bindings are not supported by terminals, and are the same
as simply `Ctrl` bindings. This means that `CtrlG`, `Ctrl-G`, and `Ctrl-g` all
mean the same thing. However, for `Alt` this is not the case: `AltG` and `Alt-G`
mean `Alt-Shift-g`, while `Alt-g` does not require the Shift modifier.

In addition to editing your `~/.config/micro/bindings.json`, you can run
`>bind <keycombo> <action>` For a list of bindable actions, see below.

You can also chain commands when rebinding. For example, if you want `Alt-s` to
save and quit you can bind it like so:

```json
{
    "Alt-s": "Save,Quit"
}
```

Each action will return a success flag. Actions can be chained such that
the chain only continues when there are successes, or failures, or either.
The `,` separator will always chain to the next action. The `|` separator
will abort the chain if the action preceding it succeeds, and the `&` will
abort the chain if the action preceding it fails. For example, in the default
bindings, tab is bound as

```
"Tab": "Autocomplete|IndentSelection|InsertTab"
```

This means that if the `Autocomplete` action is successful, the chain will
abort. Otherwise, it will try `IndentSelection`, and if that fails too, it
will execute `InsertTab`. To use `,`, `|` or `&` in an action (as an argument
to a command, for example), escape it with `\` or wrap it in single or double
quotes.

If the action has an `onAction` lua callback, for example `onAutocomplete` (see
`> help plugins`), then the action is only considered successful if the action
itself succeeded *and* the callback returned true. If there are multiple
`onAction` callbacks for this action, registered by multiple plugins, then the
action is only considered successful if the action itself succeeded and all the
callbacks returned true.

## Binding commands

You can also bind a key to execute a command in command mode (see
`help commands`). Simply prepend the binding with `command:`. For example:

```json
{
    "Alt-p": "command:pwd"
}
```

**Note for macOS**: By default, macOS terminals do not forward alt events and
instead insert unicode characters. To fix this, do the following:

* iTerm2: select `Esc+` for `Left Option Key` in `Preferences->Profiles->Keys`.
* Terminal.app: Enable `Use Option key as Meta key` in `Preferences->Profiles->Keyboard`.

Now when you press `Alt-p` the `pwd` command will be executed which will show
your working directory in the infobar.

You can also bind an "editable" command with `command-edit:`. This means that
micro won't immediately execute the command when you press the binding, but
instead just place the string in the infobar in command mode. For example,
you could rebind `Ctrl-g` to `> help`:

```json
{
    "Ctrl-g": "command-edit:help "
}
```

Now when you press `Ctrl-g`, `help` will appear in the command bar and your
cursor will be placed after it (note the space in the json that controls the
cursor placement).

## Binding Lua functions

You can also bind a key to a Lua function provided by a plugin, or by your own
`~/.config/micro/init.lua`. For example:

```json
{
    "Alt-q": "lua:foo.bar"
}
```

where `foo` is the name of the plugin and `bar` is the name of the lua function
in it, e.g.:

```lua
local micro = import("micro")

function bar(bp)
    micro.InfoBar():Message("Bar action triggered")
    return true
end
```

See `> help plugins` for more informations on how to write lua functions.

For `~/.config/micro/init.lua` the plugin name is `initlua` (so the keybinding
in this example would be `"Alt-q": "lua:initlua.bar"`).

The currently active bufpane is passed to the lua function as the argument. If
the key is a mouse button, e.g. `MouseLeft` or `MouseWheelUp`, the mouse event
info is passed to the lua function as the second argument, of type
`*tcell.EventMouse`. See https://pkg.go.dev/github.com/micro-editor/tcell/v2#EventMouse
for the description of this type and its methods.

The return value of the lua function defines whether the action has succeeded.
This is used when chaining lua functions with other actions. They can be chained
the same way as regular actions as described above, for example:

```
"Alt-q": "lua:initlua.bar|Quit"
```

## Binding raw escape sequences

Only read this section if you are interested in binding keys that aren't on the
list of supported keys for binding.

One of the drawbacks of using a terminal-based editor is that the editor must
get all of its information about key events through the terminal. The terminal
sends these events in the form of escape sequences often (but not always)
starting with `0x1b`.

For example, if micro reads `\x1b[1;5D`, on most terminals this will mean the
user pressed CtrlLeft.

For many key chords though, the terminal won't send any escape code or will
send an escape code already in use. For example for `CtrlBackspace`, my
terminal sends `\u007f` (note this doesn't start with `0x1b`), which it also
sends for `Backspace` meaning micro can't bind `CtrlBackspace`.

However, some terminals do allow you to bind keys to send specific escape
sequences you define. Then from micro you can directly bind those escape
sequences to actions. For example, to bind `CtrlBackspace` you can instruct
your terminal to send `\x1bctrlback` and then bind it in `bindings.json`:

```json
{
    "\u001bctrlback": "DeleteWordLeft"
}
```

Here are some instructions for sending raw escapes in different terminals

### iTerm2

In iTerm2, you can do this in  `Preferences->Profiles->Keys` then click the
`+`, input your keybinding, and for the `Action` select `Send Escape Sequence`.
For the above example your would type `ctrlback` into the box (the `\x1b`) is
automatically sent by iTerm2.

### Linux using loadkeys

You can do this in linux using the loadkeys program.

Coming soon!

## Unbinding keys

It is also possible to disable any of the default key bindings by use of the
`None` action in the user's `bindings.json` file.

## Bindable actions and bindable keys

The list of default keybindings contains most of the possible actions and keys
which you can use, but not all of them. Here is a full list of both.

Full list of possible actions:

```
CursorUp
CursorDown
CursorPageUp
CursorPageDown
CursorLeft
CursorRight
CursorStart
CursorEnd
CursorToViewTop
CursorToViewCenter
CursorToViewBottom
SelectToStart
SelectToEnd
SelectUp
SelectDown
SelectLeft
SelectRight
WordRight
WordLeft
SubWordRight
SubWordLeft
SelectWordRight
SelectWordLeft
SelectSubWordRight
SelectSubWordLeft
DeleteWordRight
DeleteWordLeft
DeleteSubWordRight
DeleteSubWordLeft
SelectLine
SelectToStartOfLine
SelectToStartOfText
SelectToStartOfTextToggle
SelectToEndOfLine
ParagraphPrevious
ParagraphNext
SelectToParagraphPrevious
SelectToParagraphNext
InsertNewline
Backspace
Delete
InsertTab
Save
SaveAll
SaveAs
Find
FindLiteral
FindNext
FindPrevious
DiffNext
DiffPrevious
Center
Undo
Redo
Copy
CopyLine
Cut
CutLine
Duplicate
DuplicateLine
DeleteLine
MoveLinesUp
MoveLinesDown
IndentSelection
OutdentSelection
Autocomplete
CycleAutocompleteBack
OutdentLine
IndentLine
Paste
PastePrimary
SelectAll
OpenFile
Start
End
PageUp
PageDown
SelectPageUp
SelectPageDown
HalfPageUp
HalfPageDown
StartOfText
StartOfTextToggle
StartOfLine
EndOfLine
ToggleHelp
ToggleKeyMenu
ToggleDiffGutter
ToggleRuler
ToggleHighlightSearch
UnhighlightSearch
ResetSearch
ClearStatus
ShellMode
CommandMode
ToggleOverwriteMode
Escape
Quit
QuitAll
ForceQuit
AddTab
PreviousTab
NextTab
FirstTab
LastTab
NextSplit
PreviousSplit
FirstSplit
LastSplit
Unsplit
VSplit
HSplit
ToggleMacro
PlayMacro
Suspend (Unix only)
ScrollUp
ScrollDown
SpawnMultiCursor
SpawnMultiCursorUp
SpawnMultiCursorDown
SpawnMultiCursorSelect
RemoveMultiCursor
RemoveAllMultiCursors
SkipMultiCursor
SkipMultiCursorBack
JumpToMatchingBrace
JumpLine
Deselect
ClearInfo
None
```

The `StartOfTextToggle` and `SelectToStartOfTextToggle` actions toggle between
jumping to the start of the text (first) and start of the line.

The `CutLine` action cuts the current line and adds it to the previously cut
lines in the clipboard since the last paste (rather than just replaces the
clipboard contents with this line). So you can cut multiple, not necessarily
consecutive lines to the clipboard just by pressing `Ctrl-k` multiple times,
without selecting them. If you want the more traditional behavior i.e. just
rewrite the clipboard every time, you can use `CopyLine,DeleteLine` action
instead of `CutLine`.

You can also bind some mouse actions (these must be bound to mouse buttons)

```
MousePress
MouseDrag
MouseRelease
MouseMultiCursor
```

Here is the list of all possible keys you can bind:

```
Up
Down
Right
Left
UpLeft
UpRight
DownLeft
DownRight
Center
PageUp
PageDown
Home
End
Insert
Delete
Help
Exit
Clear
Cancel
Print
Pause
Backtab
F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12
F13
F14
F15
F16
F17
F18
F19
F20
F21
F22
F23
F24
F25
F26
F27
F28
F29
F30
F31
F32
F33
F34
F35
F36
F37
F38
F39
F40
F41
F42
F43
F44
F45
F46
F47
F48
F49
F50
F51
F52
F53
F54
F55
F56
F57
F58
F59
F60
F61
F62
F63
F64
CtrlSpace
Ctrl-a
Ctrl-b
Ctrl-c
Ctrl-d
Ctrl-e
Ctrl-f
Ctrl-g
Ctrl-h
Ctrl-i
Ctrl-j
Ctrl-k
Ctrl-l
Ctrl-m
Ctrl-n
Ctrl-o
Ctrl-p
Ctrl-q
Ctrl-r
Ctrl-s
Ctrl-t
Ctrl-u
Ctrl-v
Ctrl-w
Ctrl-x
Ctrl-y
Ctrl-z
CtrlLeftSq
CtrlBackslash
CtrlRightSq
CtrlCarat
CtrlUnderscore
Backspace
OldBackspace
Tab
Esc
Escape
Enter
```

You can also bind some mouse buttons (they may be bound to normal actions or
mouse actions)

```
MouseLeft
MouseLeftDrag
MouseLeftRelease
MouseMiddle
MouseMiddleDrag
MouseMiddleRelease
MouseRight
MouseRightDrag
MouseRightRelease
MouseWheelUp
MouseWheelDown
MouseWheelLeft
MouseWheelRight
```

## Key sequences

Key sequences can be bound by specifying valid keys one after another in brackets, such
as `<Ctrl-x><Ctrl-c>`.

# Default keybinding configuration.

A select few keybindings are different on MacOS compared to other
operating systems. This is because different OSes have different
conventions for text editing defaults.

```json
{
    "Up":             "CursorUp",
    "Down":           "CursorDown",
    "Right":          "CursorRight",
    "Left":           "CursorLeft",
    "ShiftUp":        "SelectUp",
    "ShiftDown":      "SelectDown",
    "ShiftLeft":      "SelectLeft",
    "ShiftRight":     "SelectRight",
    "AltLeft":        "WordLeft", (Mac)
    "AltRight":       "WordRight", (Mac)
    "AltUp":          "MoveLinesUp",
    "AltDown":        "MoveLinesDown",
    "CtrlShiftRight": "SelectWordRight",
    "CtrlShiftLeft":  "SelectWordLeft",
    "AltLeft":        "StartOfTextToggle",
    "AltRight":       "EndOfLine",
    "AltShiftRight":  "SelectWordRight", (Mac)
    "AltShiftLeft":   "SelectWordLeft", (Mac)
    "CtrlLeft":       "StartOfText", (Mac)
    "CtrlRight":      "EndOfLine", (Mac)
    "AltShiftLeft":   "SelectToStartOfTextToggle",
    "CtrlShiftLeft":  "SelectToStartOfTextToggle", (Mac)
    "ShiftHome":      "SelectToStartOfTextToggle",
    "AltShiftRight":  "SelectToEndOfLine",
    "CtrlShiftRight": "SelectToEndOfLine", (Mac)
    "ShiftEnd":       "SelectToEndOfLine",
    "CtrlUp":         "CursorStart",
    "CtrlDown":       "CursorEnd",
    "CtrlShiftUp":    "SelectToStart",
    "CtrlShiftDown":  "SelectToEnd",
    "Alt-{":          "ParagraphPrevious",
    "Alt-}":          "ParagraphNext",
    "Enter":          "InsertNewline",
    "Ctrl-h":         "Backspace",
    "Backspace":      "Backspace",
    "Alt-CtrlH":      "DeleteWordLeft",
    "Alt-Backspace":  "DeleteWordLeft",
    "Tab":            "Autocomplete|IndentSelection|InsertTab",
    "Backtab":        "OutdentSelection|OutdentLine",
    "Ctrl-o":         "OpenFile",
    "Ctrl-s":         "Save",
    "Ctrl-f":         "Find",
    "Alt-F":          "FindLiteral",
    "Ctrl-n":         "FindNext",
    "Ctrl-p":         "FindPrevious",
    "Alt-[":          "DiffPrevious|CursorStart",
    "Alt-]":          "DiffNext|CursorEnd",
    "Ctrl-z":         "Undo",
    "Ctrl-y":         "Redo",
    "Ctrl-c":         "Copy|CopyLine",
    "Ctrl-x":         "Cut|CutLine",
    "Ctrl-k":         "CutLine",
    "Ctrl-d":         "Duplicate|DuplicateLine",
    "Ctrl-v":         "Paste",
    "Ctrl-a":         "SelectAll",
    "Ctrl-t":         "AddTab",
    "Alt-,":          "PreviousTab|LastTab",
    "Alt-.":          "NextTab|FirstTab",
    "Home":           "StartOfText",
    "End":            "EndOfLine",
    "CtrlHome":       "CursorStart",
    "CtrlEnd":        "CursorEnd",
    "PageUp":         "CursorPageUp",
    "PageDown":       "CursorPageDown",
    "CtrlPageUp":     "PreviousTab|LastTab",
    "CtrlPageDown":   "NextTab|FirstTab",
    "ShiftPageUp":    "SelectPageUp",
    "ShiftPageDown":  "SelectPageDown",
    "Ctrl-g":         "ToggleHelp",
    "Alt-g":          "ToggleKeyMenu",
    "Ctrl-r":         "ToggleRuler",
    "Ctrl-l":         "command-edit:goto ",
    "Delete":         "Delete",
    "Ctrl-b":         "ShellMode",
    "Ctrl-q":         "Quit",
    "Ctrl-e":         "CommandMode",
    "Ctrl-w":         "NextSplit|FirstSplit",
    "Ctrl-u":         "ToggleMacro",
    "Ctrl-j":         "PlayMacro",
    "Insert":         "ToggleOverwriteMode",

    // Emacs-style keybindings
    "Alt-f": "WordRight",
    "Alt-b": "WordLeft",
    "Alt-a": "StartOfLine",
    "Alt-e": "EndOfLine",

    // Integration with file managers
    "F2":  "Save",
    "F3":  "Find",
    "F4":  "Quit",
    "F7":  "Find",
    "F10": "Quit",
    "Esc": "Escape",

    // Mouse bindings
    "MouseWheelUp":     "ScrollUp",
    "MouseWheelDown":   "ScrollDown",
    "MouseLeft":        "MousePress",
    "MouseLeftDrag":    "MouseDrag",
    "MouseLeftRelease": "MouseRelease",
    "MouseMiddle":      "PastePrimary",
    "Ctrl-MouseLeft":   "MouseMultiCursor",

    // Multi-cursor bindings
    "Alt-n":        "SpawnMultiCursor",
    "AltShiftUp":   "SpawnMultiCursorUp",
    "AltShiftDown": "SpawnMultiCursorDown",
    "Alt-m":        "SpawnMultiCursorSelect",
    "Alt-p":        "RemoveMultiCursor",
    "Alt-c":        "RemoveAllMultiCursors",
    "Alt-x":        "SkipMultiCursor",
}
```

## Pane type bindings

Keybindings can be specified for different pane types as well. For example, to
make a binding that only affects the command bar, use the `command` subgroup:

```
{
    "command": {
        "Ctrl-w": "WordLeft"
    }
}
```

The possible pane types are `buffer` (normal buffer), `command` (command bar),
and `terminal` (terminal pane). The defaults for the command and terminal panes
are given below:

```
{
    "terminal": {
        "<Ctrl-q><Ctrl-q>": "Exit",
        "<Ctrl-e><Ctrl-e>": "CommandMode",
        "<Ctrl-w><Ctrl-w>": "NextSplit"
    },

    "command": {
        "Up":             "HistoryUp",
        "Down":           "HistoryDown",
        "Right":          "CursorRight",
        "Left":           "CursorLeft",
        "ShiftUp":        "SelectUp",
        "ShiftDown":      "SelectDown",
        "ShiftLeft":      "SelectLeft",
        "ShiftRight":     "SelectRight",
        "AltLeft":        "StartOfTextToggle",
        "AltRight":       "EndOfLine",
        "AltUp":          "CursorStart",
        "AltDown":        "CursorEnd",
        "AltShiftRight":  "SelectWordRight",
        "AltShiftLeft":   "SelectWordLeft",
        "CtrlLeft":       "WordLeft",
        "CtrlRight":      "WordRight",
        "CtrlShiftLeft":  "SelectToStartOfTextToggle",
        "ShiftHome":      "SelectToStartOfTextToggle",
        "CtrlShiftRight": "SelectToEndOfLine",
        "ShiftEnd":       "SelectToEndOfLine",
        "CtrlUp":         "CursorStart",
        "CtrlDown":       "CursorEnd",
        "CtrlShiftUp":    "SelectToStart",
        "CtrlShiftDown":  "SelectToEnd",
        "Enter":          "ExecuteCommand",
        "CtrlH":          "Backspace",
        "Backspace":      "Backspace",
        "OldBackspace":   "Backspace",
        "Alt-CtrlH":      "DeleteWordLeft",
        "Alt-Backspace":  "DeleteWordLeft",
        "Tab":            "CommandComplete",
        "Backtab":        "CycleAutocompleteBack",
        "Ctrl-z":         "Undo",
        "Ctrl-y":         "Redo",
        "Ctrl-c":         "Copy",
        "Ctrl-x":         "Cut",
        "Ctrl-k":         "CutLine",
        "Ctrl-v":         "Paste",
        "Home":           "StartOfTextToggle",
        "End":            "EndOfLine",
        "CtrlHome":       "CursorStart",
        "CtrlEnd":        "CursorEnd",
        "Delete":         "Delete",
        "Ctrl-q":         "AbortCommand",
        "Ctrl-e":         "EndOfLine",
        "Ctrl-a":         "StartOfLine",
        "Ctrl-w":         "DeleteWordLeft",
        "Insert":         "ToggleOverwriteMode",
        "Ctrl-b":         "WordLeft",
        "Ctrl-f":         "WordRight",
        "Ctrl-d":         "DeleteWordLeft",
        "Ctrl-m":         "ExecuteCommand",
        "Ctrl-n":         "HistoryDown",
        "Ctrl-p":         "HistoryUp",
        "Ctrl-u":         "SelectToStart",

        // Emacs-style keybindings
        "Alt-f": "WordRight",
        "Alt-b": "WordLeft",
        "Alt-a": "StartOfText",
        "Alt-e": "EndOfLine",

        // Integration with file managers
        "F10": "AbortCommand",
        "Esc": "AbortCommand",

        // Mouse bindings
        "MouseWheelUp":     "HistoryUp",
        "MouseWheelDown":   "HistoryDown",
        "MouseLeft":        "MousePress",
        "MouseLeftDrag":    "MouseDrag",
        "MouseLeftRelease": "MouseRelease",
        "MouseMiddle":      "PastePrimary"
    }
}
```

## Final notes

Note: On some old terminal emulators and on Windows machines, `Ctrl-h` should be
used for backspace.

Additionally, alt keys can be bound by using `Alt-key`. For example `Alt-a` or
`Alt-Up`. Micro supports an optional `-` between modifiers like `Alt` and
`Ctrl` so `Alt-a` could be rewritten as `Alta` (case matters for alt bindings).
This is why in the default keybindings you can see `AltShiftLeft` instead of
`Alt-ShiftLeft` (they are equivalent).

Please note that terminal emulators are strange applications and micro only
receives key events that the terminal decides to send. Some terminal emulators
may not send certain events even if this document says micro can receive the
event. To see exactly what micro receives from the terminal when you press a
key, run the `> raw` command.

---

<!-- Verbatim copy of runtime/help/commands.md from the micro source tree. -->

# Command bar

The command bar is opened by pressing `Ctrl-e`. It is a single-line buffer,
meaning that all keybindings from a normal buffer are supported (as well
as mouse and selection).

When running a command, you can use extra syntax that micro will expand before
running the command. To use an argument with a space in it, put it in
quotes. The command bar parser uses the same rules for parsing arguments that
`/bin/sh` would use (single quotes, double quotes, escaping). The command bar
does not look up environment variables.

# Commands

Micro provides the following commands that can be executed at the command-bar
by pressing `Ctrl-e` and entering the command. Arguments are placed in single
quotes here but these are not necessary when entering the command in micro.

* `bind 'key' 'action'`: creates a keybinding from key to action. See the
   `keybindings` documentation for more information about binding keys.
   This command will modify `bindings.json` and overwrite any bindings to
   `key` that already exist.

* `help ['topic'] ['flags']`: opens the corresponding help topics.
   If no topic is provided opens the default help screen. If multiple topics are
   provided (separated via ` `) they are opened all as splits.
   Help topics are stored as `.md` files in the `runtime/help` directory of
   the source tree, which is embedded in the final binary.
   The `flags` are optional.
   * `-hsplit`: Opens the help topic in a horizontal split
   * `-vsplit`: Opens the help topic in a vertical split

   The default split type is defined by the global `helpsplit` option.

* `save ['filename']`: saves the current buffer. If the file is provided it
   will 'save as' the filename.

* `quit`: quits micro.

* `goto 'line[:col]'`: goes to the given absolute line (and optional column)
   number.
   A negative number can be passed to go inward from the end of the file.
   Example: -5 goes to the 5th-last line in the file.

* `jump 'line[:col]'`: goes to the given relative number from the current
   line (and optional absolute column) number.
   Example: -5 jumps 5 lines up in the file, while (+)3 jumps 3 lines down.

* `replace 'search' 'value' ['flags']`: This will replace `search` with `value`.
   The `flags` are optional. Possible flags are:
   * `-a`: Replace all occurrences at once
   * `-l`: Do a literal search instead of a regex search

   Note that `search` must be a valid regex (unless `-l` is passed). If one
   of the arguments does not have any spaces in it, you may omit the quotes.

   In case the search is done non-literal (without `-l`), the 'value'
   is interpreted as a template:
   * `$3` or `${3}` substitutes the submatch of the 3rd (capturing group)
   * `$foo` or `${foo}` substitutes the submatch of the (?P<foo>named group)
   * You have to write `$$` to substitute a literal dollar.

* `replaceall 'search' 'value'`: this will replace all occurrences of `search`
   with `value` without user confirmation.

   See `replace` command for more information.

* `set 'option' 'value'`: sets the option to value. See the `options` help
   topic for a list of options you can set. This will modify your
   `settings.json` with the new value.

* `setlocal 'option' 'value'`: sets the option to value locally (only in the
   current buffer). This will *not* modify `settings.json`.

* `toggle 'option'`: toggles the option. Only works with options that accept
   exactly two values. This will modify your `settings.json` with the new value.

* `togglelocal 'option'`: toggles the option locally (only in the
   current buffer). Only works with options that accept exactly two values.
   This will *not* modify `settings.json`.

* `reset 'option'`: resets the given option to its default value.

* `show 'option'`: shows the current value of the given option.

* `showkey 'key'`: Show the action(s) bound to a given key. For example
   running `> showkey Ctrl-c` will display `Copy`.

* `run 'sh-command'`: runs the given shell command in the background. The
   command's output will be displayed in one line when it finishes running.

* `vsplit ['filename']`: opens a vertical split with `filename`. If no filename
   is provided, a vertical split is opened with an empty buffer. If multiple
   files are provided (separated via ` `) they are opened all as splits.

* `hsplit ['filename']`: same as `vsplit` but opens a horizontal split instead
   of a vertical split.

* `tab ['filename']`: opens the given file in a new tab. If no filename
   is provided, a tab is opened with an empty buffer. If multiple files are
   provided (separated via ` `) they are opened all as tabs.

* `tabmove '[-+]n'`: Moves the active tab to another slot. `n` is an integer.
   If `n` is prefixed with `-` or `+`, then it represents a relative position
   (e.g. `tabmove +2` moves the tab to the right by `2`). If `n` has no prefix,
   it represents an absolute position (e.g. `tabmove 2` moves the tab to slot `2`).

* `tabswitch 'tab'`: This command will switch to the specified tab. The `tab`
   can either be a tab number, or a name of a tab.

* `textfilter 'sh-command'`: filters the current selection through a shell
   command as standard input and replaces the selection with the stdout of
   the shell command.  For example, to sort a list of numbers, first select
   them, and then execute `> textfilter sort -n`.

* `log`: opens a log of all messages and debug statements.

* `plugin list`: lists all installed plugins.

* `plugin install 'pl'`: install a plugin.

* `plugin remove 'pl'`: remove a plugin.

* `plugin update ['pl']`: update a plugin (if no arguments are provided
   updates all plugins).

* `plugin search 'pl'`: search available plugins for a keyword.

* `plugin available`: show available plugins that can be installed.

* `reload`: reloads all runtime files (settings, keybindings, syntax files,
   colorschemes, plugins). All plugins will be unloaded by running their
   `deinit()` function (if it exists), and then loaded again by calling the
   `preinit()`, `init()` and `postinit()` functions (if they exist).

* `cd 'path'`: Change the working directory to the given `path`.

* `pwd`: Print the current working directory.

* `open 'filename'`: Open a file in the current buffer.

* `reopen`: Reopens the current file from disk.

* `retab`: Replaces all leading tabs with spaces or leading spaces with tabs
   depending on the value of `tabstospaces`.

* `raw`: micro will open a new tab and show the escape sequence for every event
   it receives from the terminal. This shows you what micro actually sees from
   the terminal and helps you see which bindings aren't possible and why. This
   is most useful for debugging keybindings.

* `term ['exec']`: Open a terminal emulator running the given executable. If no
   executable is given, this will open the default shell in the terminal
   emulator.

---

The following commands are provided by the default plugins:

* `lint`: Lint the current file for errors.
* `comment`: automatically comment or uncomment current selection or line.

---

<!-- Verbatim copy of runtime/help/options.md from the micro source tree. -->

# Options

Micro stores all of the user configuration in its configuration directory.

Micro uses `$MICRO_CONFIG_HOME` as the configuration directory. If this
environment variable is not set, it uses `$XDG_CONFIG_HOME/micro` instead. If
that environment variable is not set, it uses `~/.config/micro` as the
configuration directory. In the documentation, we use `~/.config/micro` to
refer to the configuration directory (even if it may in fact be somewhere else
if you have set either of the above environment variables).

Here are the available options:

* `autoindent`: when creating a new line, use the same indentation as the
   previous line.

    default value: `true`

* `autosave`: automatically save the buffer every n seconds, where n is the
   value of the autosave option. Also when quitting on a modified buffer, micro
   will automatically save and quit. Be warned, this option saves the buffer
   without prompting the user, so data may be overwritten. If this option is
   set to `0`, no autosaving is performed.

    default value: `0`

* `autosu`: When a file is saved that the user doesn't have permission to
   modify, micro will ask if the user would like to use super user
   privileges to save the file. If this option is enabled, micro will
   automatically attempt to use super user privileges to save without
   asking the user.

    default value: `false`

* `backup`: micro will automatically keep backups of all open buffers. Backups
   are stored in `~/.config/micro/backups` and are removed when the buffer is
   closed cleanly. In the case of a system crash or a micro crash, the contents
   of the buffer can be recovered automatically by opening the file that was
   being edited before the crash, or manually by searching for the backup in
   the backup directory. Backups are made in the background for newly modified
   buffers every 8 seconds, or when micro detects a crash.

    default value: `true`

* `backupdir`: the directory micro should place backups in. For the default
   value of `""` (empty string), the backup directory will be
   `ConfigDir/backups`, which is `~/.config/micro/backups` by default. The
   directory specified for backups will be created if it does not exist.

    default value: `""` (empty string)

* `basename`: in the infobar and tabbar, show only the basename of the file
   being edited rather than the full path.

    default value: `false`

* `clipboard`: specifies how micro should access the system clipboard.
   Possible values are:
    * `external`: accesses clipboard via an external tool, such as xclip/xsel
       or wl-clipboard on Linux, pbcopy/pbpaste on MacOS, and system calls on
       Windows. On Linux, if you do not have one of the tools installed, or if
       they are not working, micro will throw an error and use an internal
       clipboard.
    * `terminal`: accesses the clipboard via your terminal emulator. Note that
       there is limited support among terminal emulators for this feature
       (called OSC 52). Terminals that are known to work are Kitty (enable
       reading with `clipboard_control` setting), iTerm2 (only copying),
       st, rxvt-unicode and xterm if enabled (see `> help copypaste` for
       details). Note that Gnome-terminal does not support this feature. With
       this setting, copy-paste **will** work over ssh. See `> help copypaste`
       for details.
    * `internal`: micro will use an internal clipboard.

    default value: `external`

* `colorcolumn`: if this is not set to 0, it will display a column at the
   specified column. This is useful if you want column 80 to be highlighted
   special for example.

    default value: `0`

* `colorscheme`: use the given colorscheme. This setting is `global only`.
   The colorscheme can be either one of the colorschemes that micro comes with
   by default (such as `default`, `solarized` or `solarized-tc`) which are
   embedded in the micro binary, or a custom colorscheme stored in
   `~/.config/micro/colorschemes/$(option).micro` where `$(option)` is the
   option value. You can read more about micro's colorschemes and see the list
   of default colorschemes in `> help colors`.

    default value: `default`

* `cursorline`: highlight the line that the cursor is on in a different color
   (the color is defined by the colorscheme you are using).

    default value: `true`

* `detectlimit`: if this is not set to 0, it will limit the amount of first
   lines in a file that are matched to determine the filetype.
   A higher limit means better accuracy of guessing the filetype, but also
   taking more time.

   default value: `100`

* `diffgutter`: display diff indicators before lines.

    default value: `false`

* `divchars`: specifies the "divider" characters used for the dividing line
   between vertical/horizontal splits. The first character is for vertical
   dividers, and the second is for horizontal dividers. By default, for
   horizontal splits the statusline serves as a divider, but if the statusline
   is disabled the horizontal divider character will be used.

    default value: `|-`

* `divreverse`: colorschemes provide the color (foreground and background) for
   the characters displayed in split dividers. With this option enabled, the
   colors specified by the colorscheme will be reversed (foreground and
   background colors swapped).

    default value: `true`

* `encoding`: the encoding to open and save files with. Supported encodings
   are listed at https://www.w3.org/TR/encoding/.

    default value: `utf-8`

* `eofnewline`: micro will automatically add a newline to the end of the
   file if one does not exist.

    default value: `true`

* `fakecursor`: forces micro to render the cursor using terminal colors rather
   than the actual terminal cursor. This is useful when the terminal's cursor is
   slow or otherwise unavailable/undesirable to use.
   Note: This option defaults to `true` in case `micro` is used in the legacy
   Windows Console.

    default value: `false`

* `fastdirty`: this determines what kind of algorithm micro uses to determine
   if a buffer is modified or not. When `fastdirty` is on, micro just uses a
   boolean `modified` that is set to `true` as soon as the user makes an edit.
   This is fast, but can be inaccurate. If `fastdirty` is off, then micro will
   hash the current buffer against a hash of the original file (created when
   the buffer was loaded). This is more accurate but obviously more resource
   intensive. This option will be automatically enabled for the current buffer
   if the file size exceeds 50KB.

    default value: `false`

* `fileformat`: this determines what kind of line endings micro will use for
   the file. Unix line endings are just `\n` (linefeed) whereas dos line
   endings are `\r\n` (carriage return + linefeed). The two possible values for
   this option are `unix` and `dos`. The fileformat will be automatically
   detected (when you open an existing file) and displayed on the statusline,
   but this option is useful if you would like to change the line endings or if
   you are starting a new file. Changing this option while editing a file will
   change its line endings. Opening a file with this option set will only have
   an effect if the file is empty/newly created, because otherwise the fileformat
   will be automatically detected from the existing line endings.

    default value: `unix` on Unix systems, `dos` on Windows

* `filetype`: sets the filetype for the current buffer. Set this option to
   `off` to completely disable filetype detection.

    default value: `unknown`. This will be automatically overridden depending
    on the file you open.

* `helpsplit`: sets the split type to be used by the `help` command.
   Possible values:
    * `vsplit`: open help in a vertical split pane
    * `hsplit`: open help in a horizontal split pane

    default value: `hsplit`

* `hlsearch`: highlight all instances of the searched text after a successful
   search. This highlighting can be temporarily turned off via the
   `UnhighlightSearch` action (triggered by the Esc key by default) or toggled
   on/off via the `ToggleHighlightSearch` action. Note that these actions don't
   change the `hlsearch` setting. As long as `hlsearch` is set to true, the next
   search will have the highlighting turned on again.

    default value: `false`

* `hltaberrors`: highlight tabs when spaces are expected, and spaces when tabs
   are expected. More precisely: if `tabstospaces` option is on, highlight
   all tab characters; if `tabstospaces` is off, highlight space characters
   in the initial indent part of the line.

    default value: `false`

* `hltrailingws`: highlight trailing whitespaces at ends of lines. Note that
   it doesn't highlight newly added trailing whitespaces that naturally occur
   while typing text. It highlights only nasty forgotten trailing whitespaces.

    default value: `false`

* `ignorecase`: perform case-insensitive searches.

    default value: `true`

* `incsearch`: enable incremental search in "Find" prompt (matching as you type).

    default value: `true`

* `indentchar`: sets the character to be shown to display tab characters.
   This option is **deprecated**, use the `tab` key in `showchars` option instead.

    default value: ` ` (space)

* `infobar`: enables the line at the bottom of the editor where messages are
   printed. This option is `global only`.

    default value: `true`

* `keepautoindent`: when using autoindent, whitespace is added for you. This
   option determines if when you move to the next line without any insertions
   the whitespace that was added should be deleted to remove trailing
   whitespace. By default, the autoindent whitespace is deleted if the line
   was left empty.

    default value: `false`

* `keymenu`: display the nano-style key menu at the bottom of the screen. Note
   that ToggleKeyMenu is bound to `Alt-g` by default and this is displayed in
   the statusline. To disable the key binding, bind `Alt-g` to `None`.

    default value: `false`

* `lockbindings`: prevent plugins and lua scripts from binding any keys.
   Any custom actions must be binded manually either via commands like `bind`
   or by modifying the `bindings.json` file.

    default value: `false`

* `matchbrace`: show matching braces for '()', '{}', '[]' when the cursor
   is on a brace character or (if `matchbraceleft` is enabled) next to it.

    default value: `true`

* `matchbraceleft`: simulate I-beam cursor behavior (cursor located not on a
   character but "between" characters): when showing matching braces, if there
   is no brace character directly under the cursor, match the brace character
   to the left of the cursor instead. Also when jumping to the matching brace,
   move the cursor either to the matching brace character or to the character
   next to it, depending on whether the initial cursor position was on the
   brace character or next to it (i.e. "inside" or "outside" the braces).
   With `matchbraceleft` disabled, micro will only match the brace directly
   under the cursor and will only jump to precisely to the matching brace.

    default value: `true`

* `matchbracestyle`: whether to underline or highlight matching braces when
   `matchbrace` is enabled. The color of highlight is determined by the `match-brace`
   field in the current theme. Possible values:
    * `underline`: underline matching braces.
    * `highlight`: use `match-brace` style from the current theme.

    default value: `underline`

* `mkparents`: if a file is opened on a path that does not exist, the file
   cannot be saved because the parent directories don't exist. This option lets
   micro automatically create the parent directories in such a situation.

    default value: `false`

* `mouse`: mouse support. When mouse support is disabled,
   usually the terminal will be able to access mouse events which can be useful
   if you want to copy from the terminal instead of from micro (if over ssh for
   example, because the terminal has access to the local clipboard and micro
   does not).

    default value: `true`

* `multiopen`: specifies how to layout multiple files opened at startup.
   Most useful as a command-line option, like `-multiopen vsplit`. Possible
   values correspond to commands (see `> help commands`) that open files:
    * `tab`: open each file in a separate tab.
    * `vsplit`: open files side-by-side.
    * `hsplit`: open files stacked top to bottom.

    default value: `tab`

* `pageoverlap`: the number of lines from the current view to keep in view
   when paging up or down. If this is set to 2, for instance, and you page
   down, the last two lines of the previous page will be the first two lines
   of the next page.

    default value: `2`

* `parsecursor`: if enabled, this will cause micro to parse filenames such as
   `file.txt:10:5` as requesting to open `file.txt` with the cursor at line 10
   and column 5. The column number can also be dropped to open the file at a
   given line and column 0. Note that with this option enabled it is not possible
   to open a file such as `file.txt:10:5`, where `:10:5` is part of the filename.
   It is also possible to open a file with a certain cursor location by using the
   `+LINE:COL` flag syntax. See `micro -help` for the command line options.

    default value: `false`

* `paste`: treat characters sent from the terminal in a single chunk as a paste
   event rather than a series of manual key presses. If you are pasting using
   the terminal keybinding (not `Ctrl-v`, which is micro's default paste
   keybinding) then it is a good idea to enable this option during the paste
   and disable once the paste is over. See `> help copypaste` for details about
   copying and pasting in a terminal environment.

    default value: `false`

* `permbackup`: this option causes backups (see `backup` option) to be
   permanently saved. With permanent backups, micro will not remove backups when
   files are closed and will never apply them to existing files. Use this option
   if you are interested in manually managing your backup files.

    default value: `false`

* `pluginchannels`: list of URLs pointing to plugin channels for downloading and
   installing plugins. A plugin channel consists of a json file with links to
   plugin repos, which store information about plugin versions and download URLs.
   By default, this option points to the official plugin channel hosted on GitHub
   at https://github.com/micro-editor/plugin-channel.

    default value: `[https://raw.githubusercontent.com/micro-editor/plugin-channel/master/channel.json]`

* `pluginrepos`: a list of links to plugin repositories.

    default value: `[]` (empty list)

* `readonly`: when enabled, disallows edits to the buffer. It is recommended
   to only ever set this option locally using `setlocal`.

    default value: `false`

* `relativeruler`: make line numbers display relatively. If set to true, all
   lines except for the line that the cursor is located will display the distance
   from the cursor's line.

    default value: `false`

* `reload`: controls the reload behavior of the current buffer in case the file
   has changed. The available options are `prompt`, `auto` & `disabled`.

   default value: `prompt`

* `rmtrailingws`: micro will automatically trim trailing whitespaces at ends of
   lines.
   Note: This setting overrides `keepautoindent` and isn't used at timed `autosave`
   or forced `autosave` in case the buffer didn't change. A manual save will
   involve the action regardless if the buffer has been changed or not.

    default value: `false`

* `ruler`: display line numbers.

    default value: `true`

* `savecursor`: remember where the cursor was last time the file was opened and
   put it there when you open the file again. Information is saved to
   `~/.config/micro/buffers/`

    default value: `false`

* `savehistory`: remember command history between closing and re-opening
   micro. Information is saved to `~/.config/micro/buffers/history`.

    default value: `true`

* `saveundo`: when this option is on, undo is saved even after you close a file
   so if you close and reopen a file, you can keep undoing. Information is
   saved to `~/.config/micro/buffers/`.

    default value: `false`

* `scrollbar`: display a scroll bar

    default value: `false`

* `scrollbarchar`: specifies the character used for displaying the scrollbar

    default value: `|`

* `scrollmargin`: margin at which the view starts scrolling when the cursor
   approaches the edge of the view.

    default value: `3`

* `scrollspeed`: amount of lines to scroll for one scroll event.

    default value: `2`

* `showchars`: sets what characters to be shown to display various invisible
   characters in the file. The characters shown will not be inserted into files.
   This option is specified in the form of `key1=value1,key2=value2,...`.

   Here are the list of keys:
   - `space`: space characters
   - `tab`: tab characters. If set, overrides the `indentchar` option.
   - `ispace`: space characters at indent position before the first visible
               character in a line. If this is not set, `space` will be shown
               instead.
   - `itab`: tab characters before the first visible character in a line.
             If this is not set, `tab` will be shown instead.

   Only `tab` and `itab` can display multiple characters (if possible),
   otherwise only the first character will be displayed.

   An example of this option value could be `tab=>,space=.,itab=|>,ispace=|`

   The color of the shown character is determined by the `indent-char`
   field in the current theme rather than the default text color.

    default value: `""` (empty string)

* `smartpaste`: add leading whitespace when pasting multiple lines.
   This will attempt to preserve the current indentation level when pasting an
   unindented block.

    default value: `true`

* `softwrap`: wrap lines that are too long to fit on the screen.

    default value: `false`

* `splitbottom`: when a horizontal split is created, create it below the
   current split.

    default value: `true`

* `splitright`: when a vertical split is created, create it to the right of the
   current split.

    default value: `true`

* `statusformatl`: format string definition for the left-justified part of the
   statusline. Special directives should be placed inside `$()`. Special
   directives include: `filename`, `modified`, `line`, `col`, `lines`,
   `percentage`, `opt`, `overwrite`, `bind`.
   The `opt` and `bind` directives take either an option or an action afterward
   and fill in the value of the option or the key bound to the action.

    default value: `$(filename) $(modified)$(overwrite)($(line),$(col)) $(status.paste)|
                    ft:$(opt:filetype) | $(opt:fileformat) | $(opt:encoding)`

* `statusformatr`: format string definition for the right-justified part of the
   statusline.

    default value: `$(bind:ToggleKeyMenu): bindings, $(bind:ToggleHelp): help`

* `statusline`: display the status line at the bottom of the screen.

    default value: `true`

* `sucmd`: specifies the super user command. On most systems this is "sudo" but
   on BSD it can be "doas." This option can be customized and is only used when
   saving with su.

    default value: `sudo`

* `syntax`: enables syntax highlighting.

    default value: `true`

* `tabalways`: always shows the tab bar, even when only one tab is open.

    default value: `false`

* `tabhighlight`: inverts the tab characters' (filename, save indicator, etc)
   colors with respect to the tab bar.

    default value: `false`

* `tabmovement`: navigate spaces at the beginning of lines as if they are tabs
   (e.g. move over 4 spaces at once). This option only does anything if
   `tabstospaces` is on.

    default value: `false`

* `tabreverse`: reverses the tab bar colors when active.

    default value: `true`

* `tabsize`: the size in spaces that a tab character should be displayed with.

    default value: `4`

* `tabstospaces`: use spaces instead of tabs. Note: This option will be
   overridden by [the `ftoptions` plugin](https://github.com/micro-editor/micro/blob/master/runtime/plugins/ftoptions/ftoptions.lua)
   for certain filetypes. To disable this behavior, add `"ftoptions": false` to
   your config. See [issue #2213](https://github.com/micro-editor/micro/issues/2213)
   for more details.

    default value: `false`

* `truecolor`: controls whether micro will use true colors (24-bit colors) when
   using a colorscheme with true colors, such as `solarized-tc` or `atom-dark`.
   * `auto`: enable usage of true color if micro detects that it is supported by
      the terminal, otherwise disable it.
   * `on`: force usage of true color even if micro does not detect its support
      by the terminal (of course this is not guaranteed to work well unless the
      terminal actually supports true color).
   * `off`: disable true color usage.

   Note: The change will take effect after the next start of `micro`.

   default value: `auto`

* `useprimary` (only useful on unix): defines whether or not micro will use the
   primary clipboard to copy selections in the background. This does not affect
   the normal clipboard using `Ctrl-c` and `Ctrl-v`.

    default value: `true`

* `wordwrap`: wrap long lines by words, i.e. break at spaces. This option
   only does anything if `softwrap` is on.

    default value: `false`

* `xterm`: micro will assume that the terminal it is running in conforms to
  `xterm-256color` regardless of what the `$TERM` variable actually contains.
   Enabling this option may cause unwanted effects if your terminal in fact
   does not conform to the `xterm-256color` standard.

    default value: `false`

---

Plugin options: all plugins come with a special option to enable or disable
them. The option is a boolean with the same name as the plugin itself.

By default, the following plugins are provided, each with an option to enable
or disable them:

* `autoclose`: automatically closes brackets, quotes, etc...
* `comment`: provides automatic commenting for a number of languages
* `ftoptions`: alters some default options depending on the filetype
* `linter`: provides extensible linting for many languages
* `literate`: provides advanced syntax highlighting for the Literate
   programming tool.
* `status`: provides some extensions to the status line (integration with
   Git and more).
* `diff`: integrates the `diffgutter` option with Git. If you are in a Git
   directory, the diff gutter will show changes with respect to the most
   recent Git commit rather than the diff since opening the file.

Any option you set in the editor will be saved to the file
`~/.config/micro/settings.json` so, in effect, your configuration file will be
created for you. If you'd like to take your configuration with you to another
machine, simply copy the `settings.json` to the other machine.

## Settings.json file

The `settings.json` file should go in your configuration directory (by default
at `~/.config/micro`), and should contain only options which have been modified
from their default setting. Here is the full list of options in json format,
so that you can see what the formatting should look like.

```json
{
    "autoclose": true,
    "autoindent": true,
    "autosave": 0,
    "autosu": false,
    "backup": true,
    "backupdir": "",
    "basename": false,
    "clipboard": "external",
    "colorcolumn": 0,
    "colorscheme": "default",
    "comment": true,
    "cursorline": true,
    "detectlimit": 100,
    "diff": true,
    "diffgutter": false,
    "divchars": "|-",
    "divreverse": true,
    "encoding": "utf-8",
    "eofnewline": true,
    "fakecursor": false,
    "fastdirty": false,
    "fileformat": "unix",
    "filetype": "unknown",
    "ftoptions": true,
    "helpsplit": "hsplit",
    "hlsearch": false,
    "hltaberrors": false,
    "hltrailingws": false,
    "ignorecase": true,
    "incsearch": true,
    "indentchar": " ",
    "infobar": true,
    "initlua": true,
    "keepautoindent": false,
    "keymenu": false,
    "linter": true,
    "literate": true,
    "matchbrace": true,
    "matchbraceleft": true,
    "matchbracestyle": "underline",
    "mkparents": false,
    "mouse": true,
    "multiopen": "tab",
    "pageoverlap": 2,
    "parsecursor": false,
    "paste": false,
    "permbackup": false,
    "pluginchannels": [
        "https://raw.githubusercontent.com/micro-editor/plugin-channel/master/channel.json"
    ],
    "pluginrepos": [],
    "readonly": false,
    "relativeruler": false,
    "reload": "prompt",
    "rmtrailingws": false,
    "ruler": true,
    "savecursor": false,
    "savehistory": true,
    "saveundo": false,
    "scrollbar": false,
    "scrollbarchar": "|",
    "scrollmargin": 3,
    "scrollspeed": 2,
    "showchars": "",
    "smartpaste": true,
    "softwrap": false,
    "splitbottom": true,
    "splitright": true,
    "status": true,
    "statusformatl": "$(filename) $(modified)$(overwrite)($(line),$(col)) $(status.paste)| ft:$(opt:filetype) | $(opt:fileformat) | $(opt:encoding)",
    "statusformatr": "$(bind:ToggleKeyMenu): bindings, $(bind:ToggleHelp): help",
    "statusline": true,
    "sucmd": "sudo",
    "syntax": true,
    "tabalways": false,
    "tabhighlight": true,
    "tabmovement": false,
    "tabreverse": false,
    "tabsize": 4,
    "tabstospaces": false,
    "useprimary": true,
    "wordwrap": false,
    "xterm": false
}
```

## Global and local settings

You can set these settings either globally or locally. Locally means that the
setting won't be saved to `~/.config/micro/settings.json` and that it will only
be set in the current buffer. Setting an option globally is the default, and
will set the option in all buffers. Use the `setlocal` command to set an option
locally rather than globally.

The `colorscheme` option is global only, and the `filetype` option is local
only. To set an option locally, use `setlocal` instead of `set`.

In the `settings.json` file you can also put set options locally by specifying
either a glob or a filetype. Here is an example which has `tabstospaces` on for
all files except Go files, and `tabsize` 4 for all files except Ruby files:

```json
{
    "ft:go": {
        "tabstospaces": false
    },
    "ft:ruby": {
        "tabsize": 2
    },
    "tabstospaces": true,
    "tabsize": 4
}
```

Or similarly you can match with globs:

```json
{
    "glob:*.go": {
        "tabstospaces": false
    },
    "glob:*.rb": {
        "tabsize": 2
    },
    "tabstospaces": true,
    "tabsize": 4
}
```

You can also omit the `glob:` prefix before globs:

```json
{
    "*.go": {
        "tabstospaces": false
    },
    "*.rb": {
        "tabsize": 2
    },
    "tabstospaces": true,
    "tabsize": 4
}
```

But it is generally more recommended to use the `glob:` prefix, as it avoids
potential conflicts with option names.

---

<!-- Verbatim copy of runtime/help/copypaste.md from the micro source tree. -->

Copy and paste are essential features in micro but can be
confusing to get right especially when running micro over SSH
because there are multiple methods. This help document will explain
the various methods for copying and pasting, how they work,
and the best methods for doing so over SSH.

# OSC 52 (terminal clipboard)

If possible, setting the `clipboard` option to `terminal` will give
best results because it will work over SSH and locally. However, there
is limited support among terminal emulators for the terminal clipboard
(which uses the OSC 52 protocol to communicate clipboard contents).
Here is a list of terminal emulators and their status:

* `Kitty`: supported, but only writing is enabled by default. To enable
   reading, add `read-primary` and `read-clipboard` to the
   `clipboard_control` option.

* `iTerm2`: only copying (writing to clipboard) is supported. Must be enabled in
   `Preferences->General-> Selection->Applications in terminal may access clipboard`.
   You can use `Command-v` to paste.

* `st`: supported.

* `rxvt-unicode`: not natively supported, but there is a Perl extension
   [here](https://anti.teamidiot.de/static/nei/*/Code/urxvt/).

* `xterm`: supported, but disabled by default. It can be enabled by putting
   the following in `.Xresources` or `.Xdefaults`:
   `XTerm*disallowedWindowOps: 20,21,SetXprop`.

* `gnome-terminal`: does not support OSC 52.

* `alacritty`: supported. Since 0.13.0, reading has been disabled by default.
   To reenable it, set the `terminal.osc52` option to `CopyPaste`.

* `foot`: supported.

* `wezterm`: only copying (writing to clipboard) is supported.


**Summary:** If you want copy and paste to work over SSH, then you
should set `clipboard` to `terminal`, and make sure your terminal
supports OSC 52.

# Pasting

## Recommendations (TL;DR)

The recommended method of pasting is the following:

* If you are not working over SSH, use the micro keybinding (`Ctrl-v`
  by default) to perform pastes. If on Linux, install `xclip` or
  `xsel` beforehand.

* If you are working over SSH, use the terminal keybinding
  (`Ctrl-Shift-v` or `Command-v`) to perform pastes. If your terminal
  does not support bracketed paste, when performing a paste first
  enable the `paste` option, and when finished disable the option.

## Micro paste events

Micro is an application that runs within the terminal. This means
that the terminal sends micro events, such as key events, mouse
events, resize events, and paste events. Micro's default keybinding
for paste is `Ctrl-v`. This means that when micro receives the key
event saying `Ctrl-v` has been pressed from the terminal, it will
attempt to access the system clipboard and effect a paste. The
system clipboard will be accessed through `pbpaste` on MacOS
(installed by default), `xclip` or `xsel` on Linux (these
applications must be installed by the user) or a system call on
Windows.

## Terminal paste events

For certain keypresses, the terminal will not send an event to
micro and will instead do something itself. In this document,
such keypresses will be called "terminal keybindings." Often
there will be a terminal keybinding for pasting and copying. On
MacOS these are Command-v and Command-c and on Linux `Ctrl-Shift-v`
and `Ctrl-Shift-c`. When the terminal keybinding for paste is
executed, your terminal will access the system clipboard, and send
micro either a paste event or a list of key events (one key for each
character in the paste), depending on whether or not your terminal
supports sending paste events (called bracketed paste).

If your terminal supports bracketed paste, then it will send a paste
event and everything will work well. However, if your terminal
sends a list of key events, this can cause issues because micro
will think you manually entered each character and may add closing
brackets or automatic indentation, which will mess up the pasted
text. To avoid this, you can temporarily enable the `paste` option
while you perform the paste. When paste option is on, micro will
aggregate lists of multiple key events into larger paste events.
It is a good idea to disable the `paste` option during normal use
as occasionally if you are typing quickly, the terminal will send
the key events as lists of characters that were in fact manually
entered.

## Pasting over SSH

When working over SSH, micro is running on the remote machine and
your terminal is running on your local machine. Therefore if you
would like to paste, using `Ctrl-v` (micro's keybinding) will not
work because when micro attempts to access the system clipboard,
it will access the remote machine's clipboard rather than the local
machine's clipboard. On the other hand, the terminal keybinding
for paste will access your local clipboard and send the text over
the network as a paste event, which is what you want.

# Copying

# Recommendations (TL;DR)

The recommended method of copying is the following:

* If you are not working over SSH, use the micro keybinding (`Ctrl-c` by
  default) to perform copies. If on Linux, install `xclip` or `xsel`
  beforehand.

* If you are working over SSH, use the terminal keybinding
  (`Ctrl-Shift-c` or `Command-c`) to perform copies. You must first disable
  the `mouse` option to perform a terminal selection, and you may wish
  to disable line numbers and diff indicators (`ruler` and `diffgutter`
  options) and close other splits. This method will only be able to copy
  characters that are displayed on the screen (you will not be able to
  copy more than one page's worth of characters).

Copying follows a similar discussion to the one above about pasting.
The primary difference is before performing a copy, the application
doing the copy must be told what text needs to be copied.

Micro has a keybinding (`Ctrl-c`) for copying and will access the system
clipboard to perform the copy. The text that micro will copy into is
the text that is currently selected in micro (usually such text is
displayed with a white background). When the `mouse` option is enabled,
the mouse can be used to select text, as well as other keybindings,
such as ShiftLeft, etc...

The terminal also has a keybinding (`Ctrl-Shift-c` or `Command-c`) to perform
a copy, and the text that it copies is the text selected by the terminal's
selection (*not* micro's selection). To select text with the terminal
selection, micro's mouse support must first be disabled by turning the
`mouse` option off. The terminal, unlike micro, has no sense of different
buffers/splits and what the different characters being displayed are. This
means that for copying multiple lines using the terminal selection, you
should first disable line numbers and diff indicators (turn off the `ruler`
and `diffgutter` options), otherwise they might be part of your selection
and copied.

---

<!-- Verbatim copy of runtime/help/colors.md from the micro source tree. -->

# Colors

This help page aims to cover two aspects of micro's syntax highlighting engine:

* How to create colorschemes and use them.
* How to create syntax files to add to the list of languages micro can
  highlight.

## Colorschemes

To change your colorscheme, press `Ctrl-e` in micro to bring up the command
prompt, and type:

```
set colorscheme twilight
```

(or whichever colorscheme you choose).

Micro comes with a number of colorschemes by default. The colorschemes that you
can display will depend on what kind of color support your terminal has.

Omit color-link default "[fg color],[bg color]" will make the background color match the terminal's, and transparency if set.

Modern terminals tend to have a palette of 16 user-configurable colors (these
colors can often be configured in the terminal preferences), and additional
color support comes in three flavors.

* 16-color: A colorscheme that uses the 16 default colors will always work but
  will only look good if the 16 default colors have been configured to the
  user's liking. Using a colorscheme that only uses the 16 colors from the
  terminal palette will also preserve the terminal's theme from other
  applications since the terminal will often use those same colors for other
  applications. Default colorschemes of this type include `simple` and
  `solarized`.

* 256-color: Almost all terminals support displaying an additional 240 colors
  on top of the 16 user-configurable colors (creating 256 colors total).
  Colorschemes which use 256-color are portable because they will look the
  same regardless of the configured 16-color palette. However, the color
  range is fairly limited due to the small number of colors available.
  Default 256-color colorschemes include `monokai`, `twilight`, `zenburn`,
  `darcula` and more.

* true-color: Some terminals support displaying "true color" with 16 million
  colors using standard RGB values. This mode will be able to support
  displaying any colorscheme, but it should be noted that the user-configured
  16-color palette is ignored when using true-color mode (this means the
  colors while using the terminal emulator will be slightly off). Not all
  terminals support true color but at this point most do (see below).
  True-color colorschemes in micro typically end with `-tc`, such as
  `solarized-tc`, `atom-dark`, `material-tc`, etc... If true color is not
  enabled but a true color colorscheme is used, micro will do its best to
  approximate the colors to the available 256 colors.

Here is the list of colorschemes:

### 256 color

These should work and look nice in most terminals. I recommend these
themes the most.

* `monokai` (also the `default` colorscheme)
* `zenburn`
* `gruvbox`
* `darcula`
* `twilight`
* `railscast`
* `bubblegum` (light theme)

### 16 color

These may vary widely based on the 16 colors selected for your terminal.

* `simple`
* `solarized` (must have the solarized color palette in your terminal to use
   this colorscheme properly)
* `cmc-16`
* `cmc-paper`
* `geany`

### True color

Micro enables true color support by default as long as it detects that the
terminal supports it (which is usually indicated by the environment variable
`COLORTERM` being set to `truecolor`, `24bit` or `24-bit`). You can also force
enabling it unconditionally by setting the option `truecolor` to `on` (or
alternatively by setting the environment variable `MICRO_TRUECOLOR` to 1, which
is supported for backward compatibility).

* `solarized-tc`: this is the solarized colorscheme for true color.
* `atom-dark`: this colorscheme is based off of Atom's "dark" colorscheme.
* `cmc-tc`: A true colour variant of the cmc theme.  It requires true color to
   look its best. Use cmc-16 if your terminal doesn't support true color.
* `gruvbox-tc`: The true color version of the gruvbox colorscheme
* `material-tc`: Colorscheme based off of Google's Material Design palette

## Creating a Colorscheme

Micro's colorschemes are also extremely simple to create. The default ones can
be found
[here](https://github.com/micro-editor/micro/tree/master/runtime/colorschemes).

Custom colorschemes should be placed in the `~/.config/micro/colorschemes`
directory.

A number of custom directives are placed in a `.micro` file. Colorschemes are
typically only 18-30 lines in total.

To create the colorscheme you need to link highlight groups with
actual colors. This is done using the `color-link` command.

For example, to highlight all comments in green, you would use the command:

```
color-link comment "green"
```

Background colors can also be specified with a comma:

```
color-link comment "green,blue"
```

This will give the comments a blue background.

If you would like no foreground you can just use a comma with nothing in front:

```
color-link comment ",blue"
```

You can also put bold, italic, or underline in front of the color:

```
color-link comment "bold red"
```

---

There are three different ways to specify the color.

Color terminals usually have 16 colors that are preset by the user. This means
that you cannot depend on those colors always being the same. You can use those
colors with the names `black, red, green, yellow, blue, magenta, cyan, white`
and the bright variants of each one (brightblack, brightred...).

Then you can use the terminals 256 colors by using their numbers 1-256 (numbers
1-16 will refer to the named colors).

If the user's terminal supports true color, then you can also specify colors
exactly using their hex codes. If the terminal is not true color but micro is
told to use a true color colorscheme it will attempt to map the colors to the
available 256 colors.

Generally colorschemes which require true color terminals to look good are
marked with a `-tc` suffix and colorschemes which supply a white background are
marked with a `-paper` suffix.

---

Here is a list of the colorscheme groups that you can use:

* default (color of the background and foreground for unhighlighted text)
* comment
* identifier
* constant
* statement
* symbol
* preproc
* type
* special
* underlined
* error
* todo
* selection (Color of the text selection)
* statusline (Color of the statusline)
* statusline.inactive (Color of the statusline of inactive split panes)
* statusline.suggestions (Color of the autocomplete suggestions menu)
* tabbar (Color of the tabbar that lists open files)
* tabbar.active (Color of the active tab in the tabbar)
* indent-char (Color of the character which indicates tabs if the option is
  enabled)
* line-number
* gutter-info
* gutter-error
* gutter-warning
* diff-added
* diff-modified
* diff-deleted
* cursor-line
* current-line-number
* color-column
* ignore
* scrollbar
* divider (Color of the divider between vertical splits)
* message (Color of messages in the bottom line of the screen)
* error-message (Color of error messages in the bottom line of the screen)
* match-brace (Color of matching brackets when `matchbracestyle` is set to `highlight`)
* hlsearch (Color of highlighted search results when `hlsearch` is enabled)
* tab-error (Color of tab vs space errors when `hltaberrors` is enabled)
* trailingws (Color of trailing whitespaces when `hltrailingws` is enabled)

Colorschemes must be placed in the `~/.config/micro/colorschemes` directory to
be used.

---

In addition to the main colorscheme groups, there are subgroups that you can
specify by adding `.subgroup` to the group. If you're creating your own custom
syntax files, you can make use of your own subgroups.

If micro can't match the subgroup, it'll default to the root group, so  it's
safe and recommended to use subgroups in your custom syntax files.

For example if `constant.string` is found in your colorscheme, micro will us
that for highlighting strings. If it's not found, it will use constant instead.
Micro tries to match the largest set of groups it can find in the colorscheme
definitions, so if, for example `constant.bool.true` is found then micro will
use that. If `constant.bool.true` is not found but `constant.bool` is found
micro will use `constant.bool`. If not, it uses `constant`.

Here's a list of subgroups used in micro's built-in syntax files.

* comment.bright (Some filetypes have distinctions between types of comments)
* constant.bool
* constant.bool.true
* constant.bool.false
* constant.number
* constant.specialChar
* constant.string
* constant.string.url
* identifier.class (Also used for functions)
* identifier.macro
* identifier.var
* preproc.shebang (The #! at the beginning of a file that tells the os what
  script interpreter to use)
* symbol.brackets (`{}()[]` and sometimes `<>`)
* symbol.operator (Color operator symbols differently)
* symbol.tag (For html tags, among other things)
* type.keyword (If you want a special highlight for keywords like `private`)

In the future, plugins may also be able to use color groups for styling.

---

Last but not least it's even possible to use `include` followed by the
colorscheme name as string to include a different colorscheme within a new one.
Additionally the groups can then be extended or overwritten. The `default.micro`
theme can be seen as an example, which links to the chosen default colorscheme.

## Syntax files

The syntax files are written in yaml-format and specify how to highlight
languages.

Micro's builtin syntax highlighting tries very hard to be sane, sensible and
provide ample coverage of the meaningful elements of a language. Micro has
syntax files built in for over 100 languages now! However, there may be
situations where you find Micro's highlighting to be insufficient or not to
your liking. The good news is that you can create your own syntax files, and
place them in  `~/.config/micro/syntax` and Micro will use those instead.

### Filetype definition

You must start the syntax file by declaring the filetype:

```
filetype: go
```

### Detect definition

Then you must provide information about how to detect the filetype:

```
detect:
    filename: "\\.go$"
```

Micro will match this regex against a given filename to detect the filetype.

In addition to the `filename` regex (or even instead of it) you can provide
a `header` regex that will check the first line of the file. For example:

```
detect:
    filename: "\\.ya?ml$"
    header: "%YAML"
```

This is useful in cases when the given file name is not sufficient to determine
the filetype, e.g. with the above example, if a YAML file has no `.yaml`
extension but may contain a `%YAML` directive in its first line.

`filename` takes precedence over `header`, i.e. if there is a syntax file that
matches the file with a filetype by the `filename` and another syntax file that
matches the same file with another filetype by the `header`, the first filetype
will be used.

Finally, in addition to `filename` and/or `header` (but not instead of them)
you may also provide an optional `signature` regex which is useful for resolving
ambiguities when there are multiple syntax files matching the same file with
different filetypes. If a `signature` regex is given, micro will match a certain
amount of first lines in the file (this amount is determined by the `detectlimit`
option) against this regex, and if any of the lines match, this syntax file's
filetype will be preferred over other matching filetypes.

For example, to distinguish C++ header files from C and Objective-C header files
that have the same `.h` extension:

```
detect:
    filename: "\\.c(c|pp|xx)$|\\.h(h|pp|xx)?$"
    signature: "namespace|template|public|protected|private"
```

### Syntax rules

Next you must provide the syntax highlighting rules. There are two types of
rules: patterns and regions. A pattern is matched on a single line and usually
a single word as well. A region highlights between two patterns over multiple
lines and may have rules of its own inside the region.

Here are some example patterns in Go:

```
rules:
    - special: "\\b(break|case|continue|default|go|goto|range|return)\\b"
    - statement: "\\b(else|for|if|switch)\\b"
    - preproc: "\\b(package|import|const|var|type|struct|func|go|defer|iota)\\b"
```

The order of patterns does matter as patterns lower in the file will overwrite
the ones defined above them.

And here are some example regions for Go:

```
- constant.string:
    start: "\""
    end: "\""
    rules:
        - constant.specialChar: "%."
        - constant.specialChar: "\\\\[abfnrtv'\\\"\\\\]"
        - constant.specialChar: "\\\\([0-7]{3}|x[A-Fa-f0-9]{2}|u[A-Fa-f0-9]{4}|U[A-Fa-f0-9]{8})"

- comment:
    start: "//"
    end: "$"
    rules:
        - todo: "(TODO|XXX|FIXME):?"

- comment:
    start: "/\\*"
    end: "\\*/"
    rules:
        - todo: "(TODO|XXX|FIXME):?"
```

Notice how the regions may contain rules inside of them. Any inner rules that
are matched are then skipped when searching for the end of the region. For
example, when highlighting `"foo \" bar"`, since `\"` is matched by an inner
rule in the region, it is skipped. Likewise for `"foo \\" bar`, since `\\` is
matched by an inner rule, it is skipped, and then the `"` is found and the
string ends at the correct place.

You may also explicitly mark skip regexes if you don't want them to be
highlighted. For example:

```
- constant.string:
    start: "\""
    end: "\""
    skip: "\\."
```

#### Includes

You may also include rules from other syntax files as embedded languages. For
example, the following is possible for html:

```
- default:
    start: "<script.*?>"
    end: "</script.*?>"
    rules:
        - include: "javascript"

- default:
    start: "<style.*?>"
    end: "</style.*?>"
    rules:
        - include: "css"
```

Note that nested include (i.e. including syntax files that include other syntax
files) is not supported yet.

### Default syntax highlighting

If micro cannot detect the filetype of the file, it falls back to using the
default syntax highlighting for it, which highlights just the bare minimum:
email addresses, URLs etc.

Just like in other cases, you can override the default highlighting by adding
your own custom `default.yaml` file to `~/.config/micro/syntax`.

For example, if you work with various config files that use the `#` sign to mark
the beginning of a comment, you can use the following custom `default.yaml` to
highlight those comments by default:

```
filetype: unknown

detect:
    filename: ""

rules:
    - comment: "(^|\\s)#.*$"
```

---

<!-- Verbatim copy of runtime/help/plugins.md from the micro source tree. -->

# Plugins

This help topic is about creating plugins. If you need help installing or
managing plugins, look for `plugin` commands in `help commands`. If you want to
enable or disable a plugin, look for `Plugin options` in `help options`.

Micro supports creating plugins with a simple Lua system. Plugins are
folders containing Lua files and possibly other source files placed
in `~/.config/micro/plug`. The plugin directory (within `plug`) should
contain at least one Lua file and a `repo.json` file. The `repo.json` file
provides additional information such as the name of the plugin, the
plugin's website, dependencies, etc.
[Here is an example `repo.json` file](https://github.com/micro-editor/updated-plugins/blob/master/go-plugin/repo.json)
from the go plugin, which has the following file structure:

```
~/.config/micro/plug/go-plugin/
    go.lua
    repo.json
    help/
        go-plugin.md
```

The `go.lua` file contains the main code for the plugin, though the
code may be distributed across multiple Lua files. The `repo.json`
file contains information about the plugin, such as the website,
description, version, and any requirements. Plugins may also
have additional files that can be added to micro's runtime files,
of which there are 5 types:

* Colorschemes
* Syntax files
* Help files
* Plugin files
* Syntax header files

In most cases, a plugin will want to add help files, but in certain
cases a plugin may also want to add colorschemes or syntax files.
No directory structure is enforced, but keeping runtime files in their
own directories is good practice.

## Lua callbacks

Plugins use Lua but also have access to many functions, both from micro
and from the Go standard library. Plugins can also define functions that micro
will call when certain events happen. Here is the list of callbacks
that micro defines:

* `init()`: this function should be used for your plugin initialization.
   This function is called after buffers have been initialized.

* `preinit()`: initialization function called before buffers have been
   initialized.

* `postinit()`: initialization function called after the `init()` function of
   all plugins has been called.

* `deinit()`: cleanup function called when your plugin is unloaded or reloaded.

* `onBufferOpen(buf)`: runs when a buffer is opened. The input contains
   the buffer object.

* `onBufferOptionChanged(buf, option, old, new)`: runs when an option of the
   buffer has changed. The input contains the buffer object, the option name,
   the old and the new value.

* `onBufPaneOpen(bufpane)`: runs when a bufpane is opened. The input
   contains the bufpane object.

* `onSetActive(bufpane)`: runs when changing the currently active bufpane.

* `onAction(bufpane)`: runs when `Action` is triggered by the user, where
   `Action` is a bindable action (see `> help keybindings`). A bufpane
   is passed as input. The function should return a boolean defining
   whether the action was successful, which is used when the action is
   chained with other actions (see `> help keybindings`) to determine whether
   the next actions in the chain should be executed or not.

   If the action is a mouse action, e.g. `MousePress`, the mouse event info
   is passed to the callback as an extra argument of type `*tcell.EventMouse`.
   See https://pkg.go.dev/github.com/micro-editor/tcell/v2#EventMouse for the
   description of this type and its methods.

* `preAction(bufpane)`: runs immediately before `Action` is triggered
   by the user. Returns a boolean which defines whether the action should
   be canceled.

   Similarly to `onAction`, if the action is a mouse action, the mouse event
   info is passed to the callback as an extra argument of type
   `*tcell.EventMouse`.

* `onRune(bufpane, rune)`: runs when the composed rune has been inserted

* `preRune(bufpane, rune)`: runs before the composed rune will be inserted

* `onAnyEvent()`: runs when literally anything happens. It is useful for
   detecting various changes of micro's state that cannot be detected
   using other callbacks.

For example, a function that is run every time the user saves the buffer
would be:

```lua
function onSave(bp)
    ...
    return false
end
```

The `bp` variable is a reference to the bufpane the action is being executed
within. This is almost always the current bufpane.

All available actions are listed in the keybindings section of the help.

## Accessing micro functions

Some of micro's internal information is exposed in the form of packages, which
can be imported by Lua plugins. A package can be imported in Lua, and a value
within it can be accessed using the following syntax:

```lua
local micro = import("micro")
micro.Log("Hello")
```

The packages and their contents are listed below (in Go type signatures):

* `micro`
    - `TermMessage(msg any...)`: temporarily close micro and print a
       message

    - `TermError(filename string, lineNum int, err string)`: temporarily close
       micro and print an error formatted as `filename, lineNum: err`.

    - `InfoBar() *InfoPane`: return the infobar BufPane object.

    - `Log(msg any...)`: write a message to `log.txt` (requires
       `-debug` flag, or binary built with `build-dbg`).

    - `SetStatusInfoFn(fn string)`: register the given lua function as
       accessible from the statusline formatting options.

    - `CurPane() *BufPane`: returns the current BufPane, or nil if the
       current pane is not a BufPane.

    - `CurTab() *Tab`: returns the current tab.

    - `Tabs() *TabList`: returns the global tab list.

    - `After(t time.Duration, f func())`: run function `f` in the background
       after time `t` elapses. See https://pkg.go.dev/time#Duration for the
       usage of `time.Duration`.

    Relevant links:
    [Time](https://pkg.go.dev/time#Duration)
    [BufPane](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/action#BufPane)
    [InfoPane](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/action#InfoPane)
    [Tab](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/action#Tab)
    [TabList](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/action#TabList)

* `micro/config`
    - `MakeCommand(name string, action func(bp *BufPane, args[]string),
                   completer buffer.Completer)`:
       create a command with the given name, and lua callback function when
       the command is run. A completer may also be given to specify how
       autocompletion should work with the custom command. Any lua function
       that takes a Buffer argument and returns a pair of string arrays is a
       valid completer, as are the built in completers below:

    - `FileComplete`: autocomplete using files in the current directory
    - `HelpComplete`: autocomplete using names of help documents
    - `OptionComplete`: autocomplete using names of options
    - `OptionValueComplete`: autocomplete using names of options, and valid
       values afterwards
    - `NoComplete`: no autocompletion suggestions

    - `TryBindKey(k, v string, overwrite bool) (bool, error)`:
       bind the key `k` to the string `v`. If `overwrite` is true, this will
       overwrite any existing binding to key `k`.
       Returns true if the binding was made, and a possible error.
       This operation can be rejected by `lockbindings` to prevent undesired
       actions by the user.

    - `Reload()`: reload configuration files.

    - `AddRuntimeFileFromMemory(filetype RTFiletype, filename, data string)`:
       add a runtime file to the `filetype` runtime filetype, with name
       `filename` and data `data`.

    - `AddRuntimeFilesFromDirectory(plugin string, filetype RTFiletype,
                                    directory, pattern string)`:
       add runtime files for the given plugin with the given RTFiletype from
       a directory within the plugin root. Only adds files that match the
       pattern using Go's `filepath.Match`

    - `AddRuntimeFile(plugin string, filetype RTFiletype, filepath string)`:
       add a given file inside the plugin root directory as a runtime file
       to the given RTFiletype category.

    - `ListRuntimeFiles(fileType RTFiletype) []string`: returns a list of
       names of runtime files of the given type.

    - `ReadRuntimeFile(fileType RTFiletype, name string) string`: returns the
       contents of a given runtime file.

    - `NewRTFiletype() int`: creates a new RTFiletype, and returns its value.

    - `RTColorscheme`: runtime files for colorschemes.
    - `RTSyntax`: runtime files for syntax files.
    - `RTHelp`: runtime files for help documents.
    - `RTPlugin`: runtime files for plugin source code.

    - `RegisterCommonOption(pl string, name string, defaultvalue any)`:
       registers a new option for the given plugin. The name of the
       option will be `pl.name`, and will have the given default value. Since
       this registers a common option, the option will be modifiable on a
       per-buffer basis, while also having a global value (in the
       GlobalSettings map).

    - `RegisterGlobalOption(pl string, name string, defaultvalue any)`:
       same as `RegisterCommonOption`, but the option cannot be modified
       locally to each buffer.

    - `GetGlobalOption(name string) any`: returns the value of a
       given plugin in the `GlobalSettings` map.

    - `SetGlobalOption(option, value string) error`: sets an option to a
       given value. This will try to convert the value into the proper
       type for the option. Can return an error if the option name is not
       valid, or the value can not be converted.

    - `SetGlobalOptionNative(option string, value any) error`: sets
       an option to a given value, where the type of value is the actual
       type of the value internally. Can return an error if the provided value
       is not valid for the given option.

    - `ConfigDir`: the path to micro's currently active config directory.

    Relevant links:
    [Buffer](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/buffer#Buffer)
    [buffer.Completer](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/buffer#Completer)
    [Error](https://pkg.go.dev/builtin#error)
    [filepath.Match](https://pkg.go.dev/path/filepath#Match)

* `micro/shell`
    - `ExecCommand(name string, arg ...string) (string, error)`: runs an
       executable with the given arguments, and pipes the output (stderr
       and stdout) of the executable to an internal buffer, which is
       returned as a string, along with a possible error.

    - `RunCommand(input string) (string, error)`: same as `ExecCommand`,
       except this uses micro's argument parser to parse the arguments from
       the input. For example, `cat 'hello world.txt' file.txt`, will pass
       two arguments in the `ExecCommand` argument list (quoting arguments
       will preserve spaces).

    - `RunBackgroundShell(input string) (func() string, error)`: returns a
       function that will run the given shell command and return its output.

    - `RunInteractiveShell(input string, wait bool, getOutput bool)
                          (string, error)`:
       temporarily closes micro and runs the given command in the terminal.
       If `wait` is true, micro will wait for the user to press enter before
       returning to text editing. If `getOutput` is true, micro will redirect
       stdout from the command to the returned string.

    - `JobStart(cmd string, onStdout, onStderr,
                onExit func(string, []any), userargs ...any)
                *exec.Cmd`:
       Starts a background job by running the shell on the given command
       (using `sh -c`). Three callbacks can be provided which will be called
       when the command generates stdout, stderr, or exits. The userargs will
       be passed to the callbacks, along with the output as the first
       argument of the callback. Returns the started command.

    - `JobSpawn(cmd string, cmdArgs []string, onStdout, onStderr,
                onExit func(string, []any), userargs ...any)
                *exec.Cmd`:
       same as `JobStart`, except doesn't run the command through the shell
       and instead takes as inputs the list of arguments. Returns the started
       command.

    - `JobStop(cmd *exec.Cmd)`: kills a job.
    - `JobSend(cmd *exec.Cmd, data string)`: sends some data to a job's stdin.

    - `RunTermEmulator(h *BufPane, input string, wait bool, getOutput bool,
                       callback func(out string, userargs []any),
                       userargs []any) error`:
       starts a terminal emulator from a given BufPane with the input command.
       If `wait` is true, it will wait for the user to exit by pressing enter
       once the executable has terminated, and if `getOutput` is true, it will
       redirect the stdout of the process to a pipe, which will be passed to
       the callback, which is a function that takes a string and a list of
       optional user arguments. This function returns an error on systems
       where the terminal emulator is not supported.

    - `TermEmuSupported`: true on systems where the terminal emulator is
       supported and false otherwise. Supported systems:
        * Linux
        * MacOS
        * Dragonfly
        * OpenBSD
        * FreeBSD

    Relevant links:
    [Cmd](https://pkg.go.dev/os/exec#Cmd)
    [BufPane](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/action#BufPane)
    [Error](https://pkg.go.dev/builtin#error)

* `micro/buffer`
    - `NewMessage(owner string, msg string, start, end, Loc, kind MsgType)
                  *Message`:
       creates a new message with an owner over a range defined by the start
       and end locations.

    - `NewMessageAtLine(owner string, msg string, line int, kindMsgType)
                        *Message`:
       creates a new message with owner, type, and text at a given line.

    - `MTInfo`: info message.
    - `MTWarning`: warning message.
    - `MTError` error message.

    - `Loc(x, y int) Loc`: creates a new location struct.
    - `SLoc(line, row int) display.SLoc`: creates a new scrolling location struct.

    - `BTDefault`: default buffer type.
    - `BTHelp`: help buffer type.
    - `BTLog`: log buffer type.
    - `BTScratch`: scratch buffer type (cannot be saved).
    - `BTRaw`: raw buffer type.
    - `BTInfo`: info buffer type.

    - `NewBuffer(text, path string) *Buffer`: creates a new buffer with the
       given text at a certain path.

    - `NewBufferFromFile(path string) (*Buffer, error)`: creates a new
       buffer by reading the file at the given path from disk. Returns an error
       if the read operation fails (for example, due to the file not existing).

    - `ByteOffset(pos Loc, buf *Buffer) int`: returns the byte index of the
       given position in a buffer.

    - `Log(s string)`: writes a string to the log buffer.
    - `LogBuf() *Buffer`: returns the log buffer.

    Relevant links:
    [Message](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/buffer#Message)
    [Loc](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/buffer#Loc)
    [display.SLoc](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/display#SLoc)
    [Buffer](https://pkg.go.dev/github.com/micro-editor/micro/v2/internal/buffer#Buffer)
    [Error](https://pkg.go.dev/builtin#error)

* `micro/util`
    - `RuneAt(str string, idx int) string`: returns the utf8 rune at a
       given index within a string.
    - `GetLeadingWhitespace(s string) string`: returns the leading
       whitespace of a string.
    - `IsWordChar(s string) bool`: returns true if the first rune in a
       string is a word character.
    - `String(b []byte) string`: converts a byte array to a string.
    - `Unzip(src, dest string) error`: unzips a file to given folder.
    - `Version`: micro's version number or commit hash
    - `SemVersion`: micro's semantic version
    - `HttpRequest(method string, url string, headers []string)
                  (http.Response, error)`: makes a http request.
    - `CharacterCountInString(str string) int`: returns the number of
       characters in a string
    - `RuneStr(r rune) string`: converts a rune to a string.

    Relevant links:
    [Rune](https://pkg.go.dev/builtin#rune)

This may seem like a small list of available functions, but some of the objects
returned by the functions have many methods. The Lua plugin may access any
public methods of an object returned by any of the functions above.
Unfortunately, it is not possible to list all the available functions on this
page. Please go to the internal documentation at
https://pkg.go.dev/github.com/micro-editor/micro/v2/internal to see the full list
of available methods. Note that only methods of types that are available to
plugins via the functions above can be called from a plugin. For an even more
detailed reference, see the source code on Github.

For example, with a BufPane object called `bp`, you could call the `Save`
function in Lua with `bp:Save()`.

Note that Lua uses the `:` syntax to call a function rather than Go's `.`
syntax.

```go
micro.InfoBar().Message()
```

turns to

```lua
micro.InfoBar():Message()
```

## Accessing the Go standard library

It is possible for your lua code to access many of the functions in the Go
standard library.

Simply import the package you'd like, and then you can use it. For example:

```lua
local ioutil = import("io/ioutil")
local fmt = import("fmt")
local micro = import("micro")

local data, err = ioutil.ReadFile("SomeFile.txt")

if err ~= nil then
    micro.InfoBar():Error("Error reading file: SomeFile.txt")
else
    -- Data is returned as an array of bytes
    -- Using Sprintf will convert it to a string
    local str = fmt.Sprintf("%s", data)

    -- Do something with the file you just read!
    -- ...
end
```

Here are the packages from the Go standard library that you can access.
Nearly all functions from these packages are supported. For an exact
list of functions that are supported, you can look through `lua.go`
(which should be easy to understand).

* [fmt](https://pkg.go.dev/fmt)
* [io](https://pkg.go.dev/io)
* [io/ioutil](https://pkg.go.dev/io/ioutil)
* [net](https://pkg.go.dev/net)
* [math](https://pkg.go.dev/math)
* [math/rand](https://pkg.go.dev/math/rand)
* [os](https://pkg.go.dev/os)
* [runtime](https://pkg.go.dev/runtime)
* [path](https://pkg.go.dev/path)
* [filepath](https://pkg.go.dev/filepath)
* [strings](https://pkg.go.dev/strings)
* [regexp](https://pkg.go.dev/regexp)
* [errors](https://pkg.go.dev/errors)
* [time](https://pkg.go.dev/time)
* [unicode/utf8](https://pkg.go.dev/unicode/utf8)
* [archive/zip](https://pkg.go.dev/archive/zip)
* [net/http](https://pkg.go.dev/net/http)

The following functions from the go-humanize package are also available:

* `humanize`:
    - `Bytes(s uint64) string`: produces a human readable representation of
       an SI size.
    - `Ordinal(x int) string`: gives you the input number in a rank/ordinal
       format.

[The Lua standard library](https://www.lua.org/manual/5.1/manual.html#5) is also
available to plugins, though it is rather small.

## Adding help files, syntax files, or colorschemes in your plugin

You can use the `AddRuntimeFile(name string, type config.RTFiletype,
                                path string)`
function to add various kinds of files to your plugin. For example, if you'd
like to add a help topic to your plugin called `test`, you would create a
`test.md` file and call the function:

```lua
config = import("micro/config")
config.AddRuntimeFile("test", config.RTHelp, "test.md")
```

Use `AddRuntimeFilesFromDirectory(name, type, dir, pattern)` to add a number of
files to the runtime. To read the content of a runtime file, use
`ReadRuntimeFile(fileType, name string)` or `ListRuntimeFiles(fileType string)`
for all runtime files. In addition, there is `AddRuntimeFileFromMemory` which
adds a runtime file based on a string that may have been constructed at
runtime.

## Default plugins

The following plugins come pre-installed with micro:

* `autoclose`: automatically closes brackets, quotes, etc...
* `comment`: provides automatic commenting for a number of languages
* `ftoptions`: alters some default options (notably indentation) depending on
   the filetype
* `linter`: provides extensible linting for many languages
* `literate`: provides advanced syntax highlighting for the Literate
   programming tool.
* `status`: provides some extensions to the status line (integration with
   Git and more).
* `diff`: integrates the `diffgutter` option with Git. If you are in a Git
   directory, the diff gutter will show changes with respect to the most
   recent Git commit rather than the diff since opening the file.

See `> help linter`, `> help comment`, and `> help status` for additional
documentation specific to those plugins.

These are good examples for many use-cases if you are looking to write
your own plugins.

## Plugin Manager

Micro also has a built in plugin manager, which you can invoke with the
`> plugin ...` command, or in the shell with `micro -plugin ...`.

For the valid commands you can use, see the `commands` help topic.

The manager fetches plugins from the channels (which is simply a list of plugin
metadata) which it knows about. By default, micro only knows about the [official
channel](https://github.com/micro-editor/plugin-channel) but you can
add your own third-party channels using the `pluginchannels` option and you can
directly link third-party plugins to allow installation through the plugin
manager with the `pluginrepos` option.

If you'd like to publish a plugin you've made as an official plugin, you should
upload your plugin online (preferably to Github) and add a `repo.json` file.
This file will contain the metadata for your plugin. Here is an example:

```json
[{
  "Name": "pluginname",
  "Description": "Here is a nice concise description of my plugin",
  "Website": "https://github.com/user/plugin",
  "Tags": ["python", "linting"],
  "Versions": [
    {
      "Version": "1.0.0",
      "Url": "https://github.com/user/plugin/archive/v1.0.0.zip",
      "Require": {
        "micro": ">=1.0.3"
      }
    }
  ]
}]
```

Then open a pull request at the [official plugin channel](https://github.com/micro-editor/plugin-channel),
adding a link to the raw `repo.json` that is in your plugin repository.

To make updating the plugin work, the first line of your plugin's lua code
should contain the version of the plugin. (Like this: `VERSION = "1.0.0"`)
Please make sure to use [semver](https://semver.org/) for versioning.
