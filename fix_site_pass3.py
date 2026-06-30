#!/usr/bin/env python3
"""Pass 3: Fix broken markdown links referencing old Czech filenames,
clean up Czech headings, and update mkdocs.yml."""
import os
import re

DOCS = "/Users/michalplacek/projects/anunnaki-archive/web/docs"
MKDOCS_YML = "/Users/michalplacek/projects/anunnaki-archive/web/mkdocs.yml"

# Mapping of old Czech paths to new English paths (for markdown links)
OLD_TO_NEW = {
    "Příchod-Anunnaků.md": "arrival-of-the-anunnaki.md",
    "Přistání-v-Eridu.md": "landing-in-eridu.md",
    "Těžba-zlata.md": "gold-mining.md",
    "Stvoření-člověka.md": "creation-of-humans.md",
    "Potopa.md": "flood.md",
    "Po-potopě.md": "after-the-flood.md",
    "Mezopotámská-civilizace.md": "mesopotamian-civilization.md",
    "Pyramidové-války.md": "pyramid-wars.md",
    "Nukleární-katastrofa.md": "nuclear-catastrophe.md",
    "Ústup-bohů.md": "retreat-of-the-gods.md",
    "Enlilovo-velení.md": "enlil-command.md",
    "Nukleární-zničení.md": "nuclear-destruction.md",
    "Stěhování-bohů.md": "migration-of-gods.md",
    "Sinaj-kosmodrom.md": "sinai-spaceport.md",
    "Věž-Babylon.md": "tower-of-babel.md",
    "Tabulka-osudů.md": "tablet-of-destinies.md",
    "NÉRU.md": "neru.md",
    "Šar.md": "shar.md",
    "Schody-do-nebes.md": "stairway-to-heaven.md",
    "Dvanáctá-planeta.md": "twelfth-planet.md",
    "Kdy-začal-čas.md": "when-time-began.md",
    "Konec-dnů.md": "end-of-days.md",
    "Kosmický-kód.md": "cosmic-code.md",
    "Návrat-ke-Genesis.md": "return-to-genesis.md",
    "Války-bohů-a-lidí.md": "wars-of-gods-and-men.md",
    "Ztracená-království.md": "lost-realms.md",
    "Enuma-Elíš.md": "enuma-elish.md",
    "Gíza.md": "giza.md",
    "Jeruzalém.md": "jerusalem.md",
    "Sinaj.md": "sinai.md",
    "Gilgameš.md": "gilgamesh.md",
}

# Fix broken markdown links (these reference old filenames)
print("=== Fixing broken markdown links ===")
fixed = 0
for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        old_content = content
        for old_name, new_name in OLD_TO_NEW.items():
            # Replace in markdown links: (Příchod-Anunnaků.md) -> (arrival-of-the-anunnaki.md)
            content = content.replace(f'({old_name})', f'({new_name})')
            content = content.replace(f'({old_name} ', f'({new_name} ')
            content = content.replace(f'({old_name})', f'({new_name})')
        if content != old_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            if fname == 'index.md':
                print(f"  Fixed: {os.path.relpath(fpath, DOCS)}")

print(f"Files with fixed links: {fixed}")

# Fix Czech headings with parenthetical English
print("\n=== Fixing Czech headings ===")
heading_fixes = {
    "# Ústup bohů (Departure of the Gods)": "# Departure of the Gods",
    "# Potopa (The Great Flood)": "# The Great Flood",
    "# Potopa (The Flood)": "# The Flood",
    "# Pyramidové války (Pyramid Wars)": "# Pyramid Wars",
    "# Nukleární katastrofa (Nuclear Catastrophe)": "# Nuclear Catastrophe",
    "# Těžba zlata (Gold Mining)": "# Gold Mining",
    "# Stvoření člověka (Creation of Humanity)": "# Creation of Humanity",
    "# Stvoření člověka (Creation of Man)": "# Creation of Man",
    "# Přistání v Eridu (Landing at Eridu)": "# Landing at Eridu",
    "# Nukleární zničení (Nuclear Destruction)": "# Nuclear Destruction",
    "# Stvoření vesmíru (Creation of the Universe)": "# Creation of the Universe",
    "# Enlilovo velení (Enlil's Command)": "# Enlil's Command",
    "# Enlilovo velení": "# Enlil's Command",
    "# Stěhování bohů (Migration of the Gods)": "# Migration of the Gods",
    "# Stěhování bohů": "# Migration of the Gods",
}

fixed_headings = 0
for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        old_content = content
        for old_h, new_h in heading_fixes.items():
            content = content.replace(old_h, new_h)
        if content != old_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_headings += 1

print(f"Files with fixed headings: {fixed_headings}")

# Now handle remaining Czech text more aggressively
print("\n=== More Czech text cleanup ===")

# Scan for remaining long Czech text
for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        old_content = content

        # Replace Czech refs in the quotes section pages
        # These files have Czech in their content as quotes from Sitchin's books
        # The Czech words are proper names/titles

        if content != old_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

# Update mkdocs.yml - fix remaining nav entries with Czech chars
print("\n=== Updating mkdocs.yml nav ===")
# Now fix the timeline section
with open(MKDOCS_YML, 'r', encoding='utf-8') as f:
    content = f.read()

# Add timeline sub-items with proper English filenames
# The timeline section currently just has "timeline/index.md" without sub-items
# We need to add them, or check if they're already there
if "timeline/index.md" in content:
    print("  Timeline section: checking nav entries")
    # Let me read the full yml to see if other nav entries need fixing

with open(MKDOCS_YML, 'w', encoding='utf-8') as f:
    f.write(content)

# Check for any remaining markdown links with Czech paths
print("\n=== Checking for remaining broken links ===")
for root, dirs, files in os.walk(DOCS):
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find markdown links that point to .md files
        links = re.findall(r'\]\(([^)]+\.md)\)', content)
        for link in links:
            # Resolve relative to the file's directory
            link_path = os.path.normpath(os.path.join(os.path.dirname(fpath), link))
            if not os.path.exists(link_path):
                print(f"  BROKEN: {os.path.relpath(fpath, DOCS)} -> {link}")
