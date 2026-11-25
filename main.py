#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — make.fun entry.

Writes one two-part micro-confession to /output/entry.txt:
a To: line naming who it was meant for, and the unsent message
itself, one line written exactly as it was typed.

The gate requires UTF-8 text of 1 to 260 characters, not only
whitespace; the judge's brief caps the message line at 200
characters. This program is fully deterministic: same input,
same confession, every run.
"""

import os
import sys

ADDRESSEE = "Grandma"

MESSAGE = (
    "I sold your piano to pay the rent and never told you, and every "
    "time someone plays the song you taught me I leave the room "
    "before the chorus."
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def build_confession(addressee: str, message: str) -> str:
    """Assemble the two-part confession exactly as it was typed."""
    to_line = "To: " + addressee.strip()
    body = " ".join(message.split())
    return to_line + "\n" + body + "\n"


def check_confession(text: str) -> None:
    """Enforce the gate: 1-260 UTF-8 chars, message one line <= 200."""
    if not text.strip():
        raise ValueError("confession is empty or only whitespace")
    if len(text) > MAX_TOTAL_CHARS:
        raise ValueError(
            "confession is %d chars, over the 260-char gate" % len(text)
        )
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError("confession must be exactly two lines, got %d" % len(lines))
    if not lines[0].startswith("To: "):
        raise ValueError("first line must be a To: line")
    if len(lines[1]) > MAX_MESSAGE_CHARS:
        raise ValueError(
            "message line is %d chars, over the 200-char cap" % len(lines[1])
        )


def main() -> int:
    text = build_confession(ADDRESSEE, MESSAGE)
    check_confession(text)
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    lines = text.rstrip("\n").split("\n")
    print("wrote %s (%d chars total, message %d chars)"
          % (out_path, len(text), len(lines[1])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
