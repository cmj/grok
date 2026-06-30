# grok.py

A small CLI for talking to Grok (X/Twitter AI) from the terminal, with conversation threading and Markdown output.

## Setup

```bash
mkdir -p ~/.config/grok
cp config ~/.config/grok/config
chmod 600 ~/.config/grok/config
```

Edit `~/.config/grok/config` and set `auth_token` and `x_csrf_token` (`ct0`) from your logged-in x.com session cookies.

## Usage

```bash
grok.py what is the meaning of life    # full Markdown response
grok.py --short what is TCP            # short, plain-text answer
grok.py --conv music recommend albums  # separate named conversation thread
grok.py --new                          # reset the current conversation
grok.py --list                         # show all conversation slots
grok.py --rentry top albums of 2012    # also upload the response to rentry.co
```

Conversation slots persist in `~/.config/grok/convs/`, so you can keep multiple ongoing topics threaded separately.

## grok2md.py

Standalone helper to convert a saved Grok NDJSON response (`.json` file, e.g. from `--save`) into clean Markdown.

```bash
grok2md.py response.out output.md
cat response.out | grok2md.py > output.md
```
