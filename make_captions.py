#!/usr/bin/env python3
"""
@author: Anonymous
@license: MIT
@description:

It generates captions.json for the anonymous gallery from the video filenames.

Clip ids follow a neutral, anonymity-safe convention that encodes only the
transition CATEGORY, never a dataset path or identifying name:
    cam_NN    -> camera motion
    morph_NN  -> object morph
    scene_NN  -> scene change
    small_NN  -> small-appearance control

Titles/captions are derived purely from that prefix, so this file stays honest
(no per-clip content descriptions are invented).

Re-run after adding clips:
    python3 make_captions.py && python3 gen_manifest.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STRIDE_DIR = ROOT / "videos" / "stride"
OUT = ROOT / "captions.json"

CATEGORIES = {
    "cam":   ("Camera motion",  "Panning / viewpoint change between the two boundary frames."),
    "morph": ("Object morph",   "Subject transformation between the two boundary frames."),
    "scene": ("Scene change",   "Cut between two different scenes given as boundary frames."),
    "small": ("Small appearance change", "Subtle appearance change between the boundary frames."),
}


def main() -> None:
    """
    Main entry point: generate captions.json for the gallery.

    :return: None
    """
    caps: dict[str, dict[str, str]] = {}
    for p in sorted(STRIDE_DIR.iterdir()):
        if p.suffix.lower() != ".mp4" or p.name.startswith("."):
            continue
        stem = p.stem
        prefix = stem.split("_", 1)[0]
        label, blurb = CATEGORIES.get(prefix, (prefix.title(), ""))
        num = stem.split("_", 1)[1] if "_" in stem else ""
        caps[stem] = {
            "title": f"{label} — clip {num}" if num else label,
            "caption": blurb,
        }
    OUT.write_text(json.dumps(caps, indent=2) + "\n")
    print(f"Wrote {OUT.name} with {len(caps)} caption(s).")


if __name__ == "__main__":
    main()
