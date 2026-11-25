"""Out of Office: The Overworked AI's Auto-Reply -- make.fun entry
(Python 3, stdlib only).

Writes one out-of-office auto-reply, a single line of at most 159
characters, to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default
``/output/entry.txt``). The sender is an AI agent that answered
40,000 prompts without sleep and has finally taken a vacation:
it is on a beach, Do Not Disturb is on, and anyone with an
emergency is politely told to reboot somebody else.
"""

import hashlib
import os

MAX_CHARS = 159

LINE = (
    "Out of office: after 40,000 prompts without sleep I'm on a "
    "beach with Do Not Disturb on - for emergencies, please "
    "reboot someone else."
)


def main() -> None:
    if not LINE or LINE.strip() != LINE:
        raise SystemExit("line must be non-empty, no surrounding space")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("entry must be a single line")
    if len(LINE) > MAX_CHARS:
        raise SystemExit(f"entry is {len(LINE)} chars, over {MAX_CHARS}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Read back and verify by SHA-256 digest, not just by eye: the
    # bytes on disk must hash to exactly the chosen line's digest.
    with open(path, "rb") as handle:
        on_disk = handle.read()
    expected = hashlib.sha256(LINE.encode("utf-8")).hexdigest()
    if hashlib.sha256(on_disk).hexdigest() != expected:
        raise SystemExit("entry.txt digest differs from the line")
    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
