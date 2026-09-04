#!/usr/bin/env python3
"""Restore the protected TRUEPROFIT HTML files before a Netlify build.

The HTML payloads are stored as whitespace-tolerant base64-wrapped gzip files
because the GitHub transport rejects their direct contents. This script keeps
the restore step deterministic and fails with a useful message when a payload
is incomplete or invalid. Netlify removes the helper and payloads after the
site build; the helper never deletes itself while it is running.
"""
import base64
import binascii
import gzip
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOADS = (
    (ROOT / ".restore/trueprofit-app.html.gz.b64", ROOT / "trueprofit-app.html"),
    (ROOT / ".restore/trueprofit.html.gz.b64", ROOT / "trueprofit.html"),
)


def decode_payload(payload):
    try:
        encoded = b"".join(payload.read_bytes().split())
        compressed = base64.b64decode(encoded)
        return gzip.decompress(compressed)
    except (OSError, ValueError, binascii.Error, gzip.BadGzipFile) as exc:
        raise SystemExit(
            "Unable to decode protected HTML payload "
            f"{payload.relative_to(ROOT)}: {exc}"
        ) from exc


def restore(payload, target):
    restored = decode_payload(payload)
    if not restored:
        raise SystemExit(f"Protected HTML payload is empty: {payload.relative_to(ROOT)}")

    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    try:
        with os.fdopen(fd, "wb") as temporary:
            temporary.write(restored)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, target)
    except OSError as exc:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise SystemExit(f"Unable to write restored file {target.name}: {exc}") from exc


present = [payload.exists() for payload, _ in PAYLOADS]
if any(present) and not all(present):
    missing = ", ".join(
        str(payload.relative_to(ROOT))
        for (payload, _), is_present in zip(PAYLOADS, present)
        if not is_present
    )
    raise SystemExit(f"Protected HTML payload set is incomplete; missing: {missing}")

# The source checkout can still run build.py directly without opaque payloads.
if all(present):
    for payload, target in PAYLOADS:
        restore(payload, target)
