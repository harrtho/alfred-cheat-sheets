# Cheat-Sheets Alfred Workflow

[![GitHub Version][shield-version]][gh-releases]
[![GitHub All Releases][shield-downloads]][gh-releases]
[![GitHub][shield-license]][license-mit]

Create your own cheat sheets and make them searchable with [Alfred][alfred].

![][preview]

## Download & Installation

Download the [latest workflow release][gh-latest-release] from GitHub. Open the workflow file to
install it in Alfred.

## Usage

This workflow requires some configuration before use. See the [Configuration](#configuration) section for details.

- `cheat [<query>]` - Show a list of your cheat sheets filtered by `<query>`
  - `↩` Paste selected cheat sheet entry into frontmost window
  - `⌘ + C` Copy selected cheat sheet entry into the clipboard
- `cheat -s [<keywords>]` or `cheat --search  [<keywords>]` - Search across all cheat sheet entries, filtered by `[<keywords>]`
  - `↩` Paste selected cheat sheet entry into frontmost window
  - `⌘ + c` Copy selected cheat sheet entry into the clipboard
- `cheatsettings` - Configure your cheat sheet directory

## Configuration

Before you can use this workflow, you need to configure a directory where the workflow will search for cheat sheets. Use the command `cheatsettings`.

The cheat sheets are markdown files. Create a new file in the configured folder and give it a descriptive name, such as `nmap.md`, `top.md`, or `tar.md`. For better organization, cheat sheets can be arranged in a hierarchical folder structure.
The folder structure is displayed as a subtitle in the result list and is included in the `[<query>]` filter.

Write your cheat sheet according to the [parsing rules](#parsing-rules).

**Note:** You can start with the cheat sheets provided by [cheat][gh-cheat].

**Note:** Hidden cheat sheets and hidden directories (those starting with a `.`) will be ignored.

### Parsing rules

A cheat sheet entry consists of one or more comment lines followed by a command line. Entries are separated by two line breaks (i.e., a blank line).

This example cheat sheet is called `demosheet.md`. Its content is the following:

```markdown
# This is a one line comment. 
command one goes here.

# This is a second comment for the second command
# Yes, we can have multi-line comments
# Note that only the last line is interpreted as the command.
command two goes here

#
command three: in rare cases you don't have any comment, keep an empty # above.

# Incorrectly formatted entries are ignored, e.g., if no corresponding command is present, like here

or this line because it's a single command line without comment.
```

## Bug Reports and Feature Requests

Please use [GitHub issues][gh-issues] to report bugs or request features.

## Contributors

This Alfred Workflow is a fork of the [original workflow][original-workflow] by [Wayne Yao][gh-wayneyaoo].

## License

Cheat-Sheets Alfred Workflow is licensed under the [MIT License][license-mit]

The workflow uses the following libraries:

- [Alfred-PyWorkflow][alfred-pyworkflow] ([MIT License][license-mit])

[alfred-pyworkflow]: https://github.com/harrtho/alfred-pyworkflow
[alfred]: https://www.alfredapp.com
[gh-cheat]: https://github.com/cheat/cheatsheets
[gh-issues]: https://github.com/harrtho/alfred-cheat-sheets/issues
[gh-latest-release]: https://github.com/harrtho/alfred-cheat-sheets/releases/latest
[gh-releases]: https://github.com/harrtho/alfred-cheat-sheets/releases
[gh-wayneyaoo]: https://github.com/wayneyaoo
[license-mit]: https://opensource.org/licenses/MIT
[original-workflow]: https://github.com/wayneyaoo/alfred-cheat
[preview]: img/preview.png
[shield-downloads]: https://img.shields.io/github/downloads/harrtho/alfred-cheat-sheets/total.svg
[shield-license]: https://img.shields.io/github/license/harrtho/alfred-cheat-sheets.svg
[shield-version]: https://img.shields.io/github/release/harrtho/alfred-cheat-sheets.svg
