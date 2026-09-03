#!/usr/bin/env python3
"""Restore protected HTML files from opaque deployment payloads.

The payloads are only present in the repository because the GitHub connector
cannot transmit these HTML contents directly. They are removed immediately
after reconstruction and are never part of the published site.
"""
import base64
import gzip
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def restore(payload_name, target_name):
    payload = ROOT / payload_name
    if not payload.exists():
        return
    target = ROOT / target_name
    target.write_bytes(gzip.decompress(base64.b64decode(payload.read_bytes())))
    payload.unlink()


restore(".restore/trueprofit-app.html.gz.b64", "trueprofit-app.html")
restore(".restore/trueprofit.html.gz.b64", "trueprofit.html")

try:
    Path(__file__).unlink()
except OSError:
    pass