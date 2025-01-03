# Text Replacer

A simple yet powerful text replacement tool that automatically replaces specified trigger words with custom text as you type. Better yet, this can be installed and used across OS'. 

## Features

- Real-time text replacement while typing
- Custom trigger words and replacement text
- Support for multi-line text replacements
- Usage statistics tracking
- Command-line interface for managing replacements
- Persistent storage of replacements and usage data

## Why build this?

I've used MacOS native text replacement tool for a long time but it works, maybe 7 out of 10 times. I then tried other text replacement apps and services, but they had too much bloatware or were too expensive or too complicated to use. But my need for a text replacement tool never went away. So I built this. Thanks to Claude, my coding partner. 

## Installation

1. Ensure you have Python 3.6 or higher installed
2. Clone this repository or download the source code
3. Install the required dependencies:

```bash
pip install pynput
```

## Usage

1. Run the program:
```bash
python text_replace.py
```
or 
```bash 
python3 text_replace.py
```

2. Available commands:
- `add <trigger> <replacement>` - Add a new text replacement rule
- `remove <trigger>` - Remove an existing replacement rule
- `list` - Show all current replacement rules
- `stats` - Display usage statistics
- `exit` - Exit the program

## Example

```bash
> add :shrug: ¯\_(ツ)_/¯
> add :hello: Hello, World!
```

Now when you type `:shrug:` followed by a space or enter in any application, it will automatically be replaced with `¯\_(ツ)_/¯`. 