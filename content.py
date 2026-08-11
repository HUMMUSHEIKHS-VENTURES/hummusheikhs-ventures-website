#!/usr/bin/env python3
"""
HUMMUSHEIKHS VENTURES -- content loader.

This file no longer holds the content itself. All editable content now
lives in the /content folder as plain JSON files, so it can be edited
through the visual CMS at /admin (see CONTENT-GUIDE.md), through GitHub's
web editor, or by hand in any text editor.

This file just reads those JSON files into the shapes build.py expects.
You should not normally need to edit this file.
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_CONTENT = os.path.join(_HERE, "content")


def _load(name):
    with open(os.path.join(_CONTENT, name), encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- BUSINESS INFO
_site = _load("site.json")
SITE_URL = _site["site_url"]
BIZ = _site["biz"]
TAGLINE = _site["tagline"]
AUTHOR = _site["author"]
EMAIL = _site["email"]
WHATSAPP_URL = _site["whatsapp_url"]
WHATSAPP_DISPLAY = _site["whatsapp_display"]
LOGO = _site.get("logo", "logo-hummusheikhs-ventures.jpg")
AUTHOR_PHOTO = _site.get("author_photo", "author-bio-card.jpg")

# ---------------------------------------------------------------- BOOKS
_books_dir = os.path.join(_CONTENT, "books")
BOOKS = sorted(
    (
        _load(os.path.join("books", fname))
        for fname in os.listdir(_books_dir)
        if fname.endswith(".json")
    ),
    key=lambda b: b.get("order", 999),
)

# ---------------------------------------------------------------- CATEGORIES
CATEGORIES = [(c["key"], c["label"]) for c in _load("categories.json")["categories"]]

# ---------------------------------------------------------------- FAQS
FAQS = [(f["question"], f["answer"]) for f in _load("faqs.json")["faqs"]]

# ---------------------------------------------------------------- VENTURES
VENTURES = _load("ventures.json")["ventures"]
