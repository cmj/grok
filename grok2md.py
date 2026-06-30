#!/usr/bin/env python3
"""
grok2md.py - Extract and clean Markdown text from a raw Grok NDJSON log file.

Usage:
    ./grok2md.py <input_json_file> <output_md_file>
    ./grok2md.py -h | --help

Arguments:
    input_json_file  Path to the raw NDJSON log file saved by grok.py
    output_md_file   Path to save the cleaned Markdown (use "-" for stdout)

Example:
    ./grok2md.py ~/.local/state/grok/logs/1711800000.json output.md
    ./grok2md.py ~/.local/state/grok/logs/1711800000.json -
"""

import json
import re
import sys

if len(sys.argv) in [1, 2] or sys.argv[1] in ("-h", "--help"):
    print(__doc__.strip())
    sys.exit(0)

if len(sys.argv) != 3:
    print("Error: Invalid arguments.", file=sys.stderr)
    print("Usage: ./grok2md.py <input_json_file> <output_md_file>", file=sys.stderr)
    print("Run with --help for more details.", file=sys.stderr)
    sys.exit(1)

infile  = sys.argv[1]
outfile = sys.argv[2]

chunks = []
try:
    with open(infile) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = obj.get("result", {})
            if r.get("postIds") is not None:
                continue
            msg      = r.get("message", "")
            tag      = r.get("messageTag", "")
            thinking = r.get("isThinking", False)
            card     = r.get("cardAttachment")
            if not msg:
                continue
            if tag == "final" or (not thinking and card is None):
                chunks.append(msg)
except FileNotFoundError:
    print(f"Error: Input file '{infile}' not found.", file=sys.stderr)
    sys.exit(1)

text = "".join(chunks)

text = re.sub(r'<grok:render\b[^>]*>.*?</grok:render>', '', text, flags=re.DOTALL)
text = re.sub(r'</?(?:grok|xai):[^>]*>', '', text)
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
text = text.strip() + '\n'

if outfile == "-":
    sys.stdout.write(text)
else:
    with open(outfile, "w") as f:
        f.write(text)
    print(f"Wrote {len(text)} bytes to {outfile}", file=sys.stderr)
