#!/usr/bin/env python3
"""Second pass: Fix remaining wikilinks and Czech text."""

import os
import re
from pathlib import Path

DOCS = Path("/Users/michalplacek/projects/anunnaki-archive/web/docs")

# Build known pages map: lowercase basename -> relative path
KNOWN_PAGES = {}
for root, dirs, files in os.walk(DOCS):
    for f in files:
        if f.endswith(".md"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, DOCS)
            basename = os.path.splitext(os.path.basename(rel))[0]
            # Map lowercase version for case-insensitive matching
            KNOWN_PAGES[basename.lower()] = rel
            # Also without diacritics
            simple = basename.replace('ě','e').replace('š','s').replace('č','c').replace('ř','r').replace('ž','z').replace('ý','y').replace('á','a').replace('í','i').replace('é','e').replace('ů','u').replace('ň','n').replace('ť','t').replace('ď','d').replace('ó','o').lower()
            if simple != basename.lower():
                KNOWN_PAGES[simple] = rel

def try_resolve_path(old_rel):
    """Try to resolve a path-based wikilink reference."""
    # Normalize the path
    old_rel = os.path.normpath(old_rel)
    # Try as-is (it might already match)
    test_path = DOCS / old_rel
    if test_path.exists():
        return os.path.relpath(test_path, DOCS)
    # Try lowercase
    test_path = DOCS / old_rel.lower()
    if test_path.exists():
        return os.path.relpath(test_path, DOCS)
    # Extract basename and try lookup
    basename = os.path.splitext(os.path.basename(old_rel))[0]
    return try_resolve_page(basename)

def try_resolve_page(name):
    """Try to resolve a simple page name to its English path."""
    # Direct match (case-insensitive)
    name_lower = name.lower()
    if name_lower in KNOWN_PAGES:
        return KNOWN_PAGES[name_lower]
    # Try without diacritics
    simple = name_lower.replace('ě','e').replace('š','s').replace('č','c').replace('ř','r').replace('ž','z').replace('ý','y').replace('á','a').replace('í','i').replace('é','e').replace('ů','u').replace('ň','n').replace('ť','t').replace('ď','d').replace('ó','o')
    if simple != name_lower and simple in KNOWN_PAGES:
        return KNOWN_PAGES[simple]
    return None

def make_display_name(rel_path):
    """Create a display name from a file path."""
    basename = os.path.splitext(os.path.basename(rel_path))[0]
    display = basename.replace('-', ' ').title()
    # Fix known uppercase patterns
    overrides = {
        "Dur.An.Ki": "DUR.AN.KI",
        "Me": "ME",
        "Neru": "NÉRU",
        "Shar": "Šar",
        "Shem": "SHEM",
        "Edin": "E.DIN",
        "E Din": "E.DIN",
        "M E": "ME",
        "N É R U": "NÉRU",
        "Anunnaki": "Anunnaki",
        "E Din": "E.DIN",
        "Nibiru": "Nibiru",
    }
    if display in overrides:
        return overrides[display]
    return display

# Pattern for remaining [[wikilinks]]
WIKILINK_PATTERN = re.compile(r'\[\[([^\]]+?)(?:\|([^\]]*?))?\]\]')

total_links = 0
files_changed = 0

for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        full_path = os.path.join(root, fname)
        rel_path = os.path.relpath(full_path, DOCS)
        file_dir = os.path.dirname(rel_path)

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if '[[' not in content:
            continue

        def replace_wikilink(match):
            global total_links
            target = match.group(1).strip()
            display = match.group(2)

            # Handle escaped pipe from markdown tables: [[Name\|Display]]
            if target.endswith('\\'):
                target = target[:-1]
            if display and display.startswith('\\'):
                display = display[1:]

            target = target.strip()
            total_links += 1

            resolved_path = None
            if '/' in target:
                resolved_path = try_resolve_path(target + ".md")
            else:
                resolved_path = try_resolve_page(target)

            if resolved_path:
                rel_link = os.path.relpath(resolved_path, file_dir)
                if display and display.strip():
                    display_text = display.strip()
                else:
                    display_text = make_display_name(resolved_path)
                return f"[{display_text}]({rel_link})"
            else:
                # Page doesn't exist - convert to plain text
                if display and display.strip():
                    return display.strip()
                else:
                    return target

        new_content = re.sub(WIKILINK_PATTERN, replace_wikilink, content)
        if new_content != content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f"Files changed: {files_changed}")
print(f"Total remaining wikilinks resolved: {total_links}")

# Now check for remaining Czech text patterns
print("\n=== Pass 3: Fix known Czech text patterns ===")

# Scan for notable Czech patterns
czech_patterns = [
    # Czech headings
    (r'^#\s+Následovníci', '# Followers'),
    (r'^##\s+Následovníci\s*\(', '## Followers ('),
    (r'^##\s+Spravedlnost', '## Justice'),
    # Czech nav labels
    (r'Následovníci/', 'followers/'),
    (r'Postavy/', 'characters/'),
    (r'Místa/', 'places/'),
    (r'Témata/', 'themes/'),
    (r'Koncepty/', 'concepts/'),
    (r'Zdroje/', 'sources/'),
    (r'Citace/', 'quotes/'),
    (r'Knihy/', 'books/'),
    (r'Kritika/', 'criticism/'),
    (r'Timeline/', 'timeline/'),
    (r'Moderní-věda/', 'modern-science/'),
    (r'Náboženství/', 'religions/'),
]

for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        full_path = os.path.join(root, fname)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        old_content = content
        for pat, repl in czech_patterns:
            content = re.sub(pat, repl, content)

        # Also replace specific Czech folder names in links
        content = content.replace('Následovníci/', 'followers/')
        content = content.replace('Postavy/', 'characters/')
        content = content.replace('Místa/', 'places/')
        content = content.replace('Témata/', 'themes/')
        content = content.replace('Koncepty/', 'concepts/')
        content = content.replace('Zdroje/', 'sources/')
        content = content.replace('Citace/', 'quotes/')
        content = content.replace('Knihy/', 'books/')
        content = content.replace('Kritika/', 'criticism/')
        content = content.replace('Moderní-věda/', 'modern-science/')
        content = content.replace('Náboženství/', 'religions/')

        if content != old_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

# Check remaining Czech diacritics
print("\n=== Remaining Czech diacritics ===")
czech_chars = set('ěščřžýáíéůňťďó')
for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        full_path = os.path.join(root, fname)
        with open(full_path, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
            except:
                continue
        found = set()
        for ch in content:
            if ch in czech_chars:
                found.add(ch)
        if found:
            rel = os.path.relpath(full_path, DOCS)
            print(f"  {rel}: {''.join(sorted(found))}")

print("\nDone!")
