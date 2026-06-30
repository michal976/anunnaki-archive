#!/usr/bin/env python3
"""Fix the Anunnaki Archive MkDocs site:
1. Rename Czech filenames to English
2. Convert [[Obsidian wikilinks]] to [Markdown links](file.md)
3. Update mkdocs.yml nav
"""

import os
import re
import yaml
from pathlib import Path

DOCS = Path("/Users/michalplacek/projects/anunnaki-archive/web/docs")
MKDOCS_YML = Path("/Users/michalplacek/projects/anunnaki-archive/web/mkdocs.yml")

# ============================================================
# STEP 1: Build CZECH → ENGLISH filename mapping
# ============================================================

# All files that need renaming (relative to docs/)
CZECH_TO_ENGLISH = {
    # books
    "books/Kdyz-zapocal-cas-reference.md": "books/when-time-began-reference.md",
    "books/Schody-k-nebesům-reference.md": "books/stairway-to-heaven-reference.md",

    # characters
    "characters/Gilgameš.md": "characters/gilgamesh.md",

    # concepts
    "concepts/Nukleární-zničení.md": "concepts/nuclear-destruction.md",
    "concepts/NÉRU.md": "concepts/neru.md",
    "concepts/Potopa.md": "concepts/flood.md",
    "concepts/Pyramidové-války.md": "concepts/pyramid-wars.md",
    "concepts/Sinaj-kosmodrom.md": "concepts/sinai-spaceport.md",
    "concepts/Stěhování-bohů.md": "concepts/migration-of-gods.md",
    "concepts/Tabulka-osudů.md": "concepts/tablet-of-destinies.md",
    "concepts/Věž-Babylon.md": "concepts/tower-of-babel.md",
    "concepts/Šar.md": "concepts/shar.md",

    # criticism
    "criticism/Mainstream-asyriologie.md": "criticism/mainstream-assyriology.md",
    "criticism/Nibiru-kritika.md": "criticism/nibiru-critique.md",
    "criticism/Pseudohistorie.md": "criticism/pseudohistory.md",
    "criticism/Překlady-spory.md": "criticism/translation-disputes.md",
    "criticism/Sumerologové.md": "criticism/sumerologists.md",

    # modern-science
    "modern-science/Africké-doly.md": "modern-science/african-mines.md",
    "modern-science/Archeoastronomie-Gízy.md": "modern-science/archeoastronomy-of-giza.md",
    "modern-science/Megalitická-archeologie.md": "modern-science/megalithic-archaeology.md",
    "modern-science/Neandertálci-Denisovani.md": "modern-science/neanderthals-denisovans.md",
    "modern-science/Paleogenetika.md": "modern-science/paleogenetics.md",
    "modern-science/Panspermie.md": "modern-science/panspermia.md",
    "modern-science/Voda-na-planetách.md": "modern-science/water-on-planets.md",
    "modern-science/Vznik-Měsíce.md": "modern-science/origin-of-the-moon.md",

    # places
    "places/Gíza.md": "places/giza.md",
    "places/Jeruzalém.md": "places/jerusalem.md",
    "places/Sinaj.md": "places/sinai.md",

    # quotes
    "quotes/Anunnaki-a-bohové.md": "quotes/anunnaki-and-gods.md",
    "quotes/Bible-paralely.md": "quotes/bible-parallels.md",
    "quotes/Inanna-cyklus.md": "quotes/inanna-cycle.md",
    "quotes/Letadla-a-rakety.md": "quotes/aircraft-and-rockets.md",
    "quotes/Nukleární-zničení.md": "quotes/nuclear-destruction.md",
    "quotes/Potopa.md": "quotes/flood.md",
    "quotes/Pyramidové-války.md": "quotes/pyramid-wars.md",
    "quotes/Sitchinovy-klíčové.md": "quotes/sitchin-key-quotes.md",
    "quotes/Stvoření-vesmíru.md": "quotes/creation-of-the-universe.md",
    "quotes/Stvoření-člověka.md": "quotes/creation-of-humans.md",
    "quotes/Číselné-kódy.md": "quotes/numerical-codes.md",

    # religions
    "religions/Gnosticismus.md": "religions/gnosticism.md",
    "religions/Indie.md": "religions/india.md",
    "religions/Mezoamerika.md": "religions/mesoamerica.md",
    "religions/Nový-zákon.md": "religions/new-testament.md",
    "religions/Severská.md": "religions/norse.md",
    "religions/Starý-zákon.md": "religions/old-testament.md",
    "religions/Řecko.md": "religions/greece.md",

    # sources
    "sources/Dvanáctá-planeta.md": "sources/twelfth-planet.md",
    "sources/Enuma-Elíš.md": "sources/enuma-elish.md",
    "sources/Kdy-začal-čas.md": "sources/when-time-began.md",
    "sources/Konec-dnů.md": "sources/end-of-days.md",
    "sources/Kosmický-kód.md": "sources/cosmic-code.md",
    "sources/Návrat-ke-Genesis.md": "sources/return-to-genesis.md",
    "sources/Schody-do-nebes.md": "sources/stairway-to-heaven.md",
    "sources/Války-bohů-a-lidí.md": "sources/wars-of-gods-and-men.md",
    "sources/Ztracená-království.md": "sources/lost-realms.md",

    # themes
    "themes/Genetické-inženýrství.md": "themes/genetic-engineering.md",
    "themes/Jaderné-zbraně.md": "themes/nuclear-weapons.md",
    "themes/Kalendář.md": "themes/calendar.md",
    "themes/Kosmodromy.md": "themes/spaceports.md",
    "themes/Monoatomické-zlato.md": "themes/monatomic-gold.md",
    "themes/Navigační-majáky.md": "themes/navigation-beacons.md",
    "themes/Posvátná-čísla.md": "themes/sacred-numbers.md",
    "themes/Precese.md": "themes/precession.md",
    "themes/Pyramidy.md": "themes/pyramids.md",
    "themes/Smíšená-manželství.md": "themes/mixed-marriages.md",
    "themes/Vimány-a-letadla.md": "themes/vimanas-and-aircraft.md",

    # timeline
    "timeline/Enlilovo-velení.md": "timeline/enlil-command.md",
    "timeline/Mezopotámská-civilizace.md": "timeline/mesopotamian-civilization.md",
    "timeline/Nukleární-katastrofa.md": "timeline/nuclear-catastrophe.md",
    "timeline/Po-potopě.md": "timeline/after-the-flood.md",
    "timeline/Potopa.md": "timeline/flood.md",
    "timeline/Pyramidové-války.md": "timeline/pyramid-wars.md",
    "timeline/Přistání-v-Eridu.md": "timeline/landing-in-eridu.md",
    "timeline/Příchod-Anunnaků.md": "timeline/arrival-of-the-anunnaki.md",
    "timeline/Stvoření-člověka.md": "timeline/creation-of-humans.md",
    "timeline/Těžba-zlata.md": "timeline/gold-mining.md",
    "timeline/Ústup-bohů.md": "timeline/retreat-of-the-gods.md",
}

# Build reverse: English → Czech (for reference)
ENGLISH_TO_CZECH = {v: k for k, v in CZECH_TO_ENGLISH.items()}

# Build mapping from basename (without path) to new path
# This is needed for wikilink resolution
BASENAME_TO_NEW_PATH = {}

# English basename → new relative path
ENGLISH_BASENAME_TO_PATH = {}

for old_rel, new_rel in CZECH_TO_ENGLISH.items():
    old_name = os.path.splitext(os.path.basename(old_rel))[0]
    new_name = os.path.splitext(os.path.basename(new_rel))[0]
    BASENAME_TO_NEW_PATH[old_name] = new_rel
    ENGLISH_BASENAME_TO_PATH[new_name] = new_rel

# Also add files that DON'T need renaming
ALL_MD_FILES = []
for root, dirs, files in os.walk(DOCS):
    for f in files:
        if f.endswith(".md"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, DOCS)
            ALL_MD_FILES.append(rel)
            if rel not in CZECH_TO_ENGLISH.values():
                basename = os.path.splitext(f)[0]
                ENGLISH_BASENAME_TO_PATH[basename] = rel

# Print mapping for verification
print("=== CZECH → ENGLISH filename mapping ===")
for old, new in sorted(CZECH_TO_ENGLISH.items()):
    print(f"  {old}  →  {new}")
print(f"\nTotal files to rename: {len(CZECH_TO_ENGLISH)}")

# ============================================================
# STEP 2: Rename all files
# ============================================================
print("\n=== STEP 2: Renaming files ===")
for old_rel, new_rel in sorted(CZECH_TO_ENGLISH.items()):
    old_path = DOCS / old_rel
    new_path = DOCS / new_rel
    if old_path.exists():
        # Ensure parent directory exists
        new_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.rename(new_path)
        print(f"  ✓ {old_rel} → {new_rel}")
    else:
        print(f"  ✗ NOT FOUND: {old_rel}")

# Update ALL_MD_FILES to reflect new names
ALL_MD_FILES_NEW = []
for rel in ALL_MD_FILES:
    if rel in CZECH_TO_ENGLISH:
        ALL_MD_FILES_NEW.append(CZECH_TO_ENGLISH[rel])
    else:
        ALL_MD_FILES_NEW.append(rel)
ALL_MD_FILES = ALL_MD_FILES_NEW

print("\n=== STEP 3: Converting [[wikilinks]] to Markdown links ===")

# Pattern for [[wikilinks]] - both simple [[Name]] and [[Name|display]]
# Also handle escaped pipes used in tables: [[Name\|display]]
WIKILINK_PATTERN = re.compile(r'\[\[([^\]]+?)(?:\|([^\]]*?))?\]\]')

# For each markdown file, find and replace wikilinks
files_processed = 0
links_converted = 0
unknown_links = set()

for rel_path in sorted(ALL_MD_FILES):
    full_path = DOCS / rel_path
    if not full_path.exists() or not full_path.is_file():
        continue

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine the directory of this file (for relative path calculations)
    file_dir = os.path.dirname(rel_path)

    def replace_wikilink(match):
        global links_converted
        target = match.group(1).strip()
        display = match.group(2)

        # Handle escaped pipes (used in table syntax)
        target = target.replace('\\|', '|')

        # Determine if this is a path-based link (contains /)
        if '/' in target:
            # It's a path like "Concepts/Sinaj-kosmodrom" or "Folder/File"
            parts = target.split('/')
            page_name = parts[-1]  # The file name (without extension)
            # Reconstruct the old relative path
            old_rel_path = os.path.join(*parts) + ".md"
            # Normalize the path
            old_rel_path = os.path.normpath(old_rel_path)

            # Check if this old path is in our mapping
            if old_rel_path in CZECH_TO_ENGLISH:
                new_rel_path = CZECH_TO_ENGLISH[old_rel_path]
            elif os.path.splitext(os.path.basename(old_rel_path))[0] in ENGLISH_BASENAME_TO_PATH:
                # Try looking up by the page name
                bn = os.path.splitext(os.path.basename(old_rel_path))[0]
                new_rel_path = ENGLISH_BASENAME_TO_PATH[bn]
            else:
                # Try looking up the filename in our basename mapping
                bn = os.path.splitext(os.path.basename(old_rel_path))[0]
                if bn in BASENAME_TO_NEW_PATH:
                    new_rel_path = BASENAME_TO_NEW_PATH[bn]
                else:
                    unknown_links.add(target)
                    return match.group(0)  # Return unchanged
        else:
            # Simple page name - look up in basename mapping
            if target in BASENAME_TO_NEW_PATH:
                new_rel_path = BASENAME_TO_NEW_PATH[target]
            elif target in ENGLISH_BASENAME_TO_PATH:
                new_rel_path = ENGLISH_BASENAME_TO_PATH[target]
            else:
                unknown_links.add(target)
                return match.group(0)  # Return unchanged

        # Compute relative path from current file to target file
        # Both paths are relative to docs/
        rel_link = os.path.relpath(new_rel_path, file_dir)

        # Determine display text
        if display is not None and display.strip():
            display_text = display.strip()
        else:
            # Use the English page name without extension
            display_text = os.path.splitext(os.path.basename(new_rel_path))[0]
            # Convert hyphens to spaces and capitalize
            display_text = display_text.replace('-', ' ').title()
            # Special cases
            display_overrides = {
                "Dur.An.Ki": "DUR.AN.KI",
                "Me": "ME",
                "Neru": "NÉRU",
                "Shar": "Šar",
                "Shem": "SHEM",
                "Edin": "E.DIN",
                "E Din": "E.DIN",
                "M E": "ME",
                "N É R U": "NÉRU",
            }
            if display_text in display_overrides:
                display_text = display_overrides[display_text]

        links_converted += 1
        return f"[{display_text}]({rel_link})"

    new_content = re.sub(WIKILINK_PATTERN, replace_wikilink, content)

    if new_content != content:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        files_processed += 1

print(f"  Files modified: {files_processed}")
print(f"  Links converted: {links_converted}")
if unknown_links:
    print(f"\n  Unknown (unresolved) wikilinks ({len(unknown_links)}):")
    for link in sorted(unknown_links):
        print(f"    [[{link}]]")

print("\n=== STEP 4: Update mkdocs.yml nav ===")

# Read mkdocs.yml
with open(MKDOCS_YML, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix nav paths - replace old Czech paths with new English ones
nav_fixes = 0
for old_rel, new_rel in sorted(CZECH_TO_ENGLISH.items(), key=lambda x: -len(x[0])):
    # Replace the old path reference in mkdocs.yml
    old_count = content.count(old_rel)
    if old_count > 0:
        content = content.replace(old_rel, new_rel)
        nav_fixes += old_count
        print(f"  nav: {old_rel} → {new_rel} ({old_count}x)")

with open(MKDOCS_YML, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n  Nav paths updated: {nav_fixes} replacements")

print("\n=== STEP 5: Check for remaining Czech diacritics ===")

# Check for Czech characters in file content
czech_chars = set('ěščřžýáíéůňťďó')
files_with_czech = []

for rel_path in sorted(ALL_MD_FILES):
    full_path = DOCS / rel_path
    if not full_path.exists() or not full_path.is_file():
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
        except:
            continue
    # Check for Czech characters
    found_chars = set()
    for i, ch in enumerate(content):
        if ch in czech_chars:
            # Skip the BOM character
            if ord(ch) < 128:
                continue
            found_chars.add(ch)

    if found_chars:
        files_with_czech.append((rel_path, found_chars))

if files_with_czech:
    print(f"  Found {len(files_with_czech)} files with Czech diacritics:")
    for path, chars in files_with_czech:
        print(f"    {path}: {''.join(sorted(chars))}")
else:
    print("  ✓ No files with Czech diacritics found")

print("\n=== Done! ===")
print(f"Files renamed: {len(CZECH_TO_ENGLISH)}")
print(f"Files with wikilink changes: {files_processed}")
print(f"Total wikilinks converted: {links_converted}")
print(f"Nav replacements: {nav_fixes}")
