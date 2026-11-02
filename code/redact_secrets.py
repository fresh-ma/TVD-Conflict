#!/usr/bin/env python3
"""Remove API credentials from agent output before displaying or saving it."""
from __future__ import annotations

import os
import re
import sys


OPENROUTER_KEY = re.compile(r"sk-or-v1-[A-Za-z0-9_-]+")


def redact_secrets(text: str) -> str:
    # Also cover configured credentials whose format differs from OpenRouter's.
    secrets = {
        value for name, value in os.environ.items()
        if value and name.endswith(("API_KEY", "AUTH_TOKEN", "OAUTH_TOKEN"))
    }
    for secret in sorted(secrets, key=len, reverse=True):
        text = text.replace(secret, "[REDACTED]")
    return OPENROUTER_KEY.sub("[REDACTED]", text)


def main() -> None:
    # Process whole lines so a credential split across pipe writes stays intact.
    for line in sys.stdin.buffer:
        clean = redact_secrets(line.decode("utf-8", errors="surrogateescape"))
        sys.stdout.buffer.write(clean.encode("utf-8", errors="surrogateescape"))
        sys.stdout.buffer.flush()


if __name__ == "__main__":
    main()
