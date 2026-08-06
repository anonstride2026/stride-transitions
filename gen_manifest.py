#!/usr/bin/env python3
"""Generate clips.json that drives index.html (the side-by-side gallery).

Convention: put the SAME filename in each method folder for a given clip, e.g.
    videos/stride/clip01.mp4
    videos/dynamicrafter/clip01.mp4
    videos/seine/clip01.mp4
    videos/tvg/clip01.mp4
The clip id is the filename stem ("clip01"). Rows are ordered by the STRIDE
folder (falling back to the union of all folders). Optional per-clip titles /
captions can be supplied in captions.json:
    { "clip01": {"title": "Object morph — cat to dog", "caption": "..."} }

Run from the repo root:  python3 gen_manifest.py
No third-party dependencies; strips any identifying metadata by design.
"""
from __future__ import annotations

import json
from pathlib import Path

METHODS = ["stride", "dynamicrafter", "seine", "tvg"]
VIDEO_EXTS = {".mp4", ".webm", ".mov"}
ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
CAPTIONS_FILE = ROOT / "captions.json"
OUT = ROOT / "clips.json"


def stems_in(method: str) -> dict[str, str]:
    """Map clip stem -> repo-relative source path for one method folder."""
    d = VIDEOS / method
    found: dict[str, str] = {}
    if not d.is_dir():
        return found
    for p in sorted(d.iterdir()):
        if p.suffix.lower() in VIDEO_EXTS and not p.name.startswith("."):
            found[p.stem] = f"videos/{method}/{p.name}"
    return found


def main() -> None:
    per_method = {m: stems_in(m) for m in METHODS}

    # Row order: STRIDE first, then any clip that appears in another method only.
    ordered: list[str] = list(per_method["stride"].keys())
    for m in METHODS:
        for stem in per_method[m]:
            if stem not in ordered:
                ordered.append(stem)

    captions = {}
    if CAPTIONS_FILE.is_file():
        captions = json.loads(CAPTIONS_FILE.read_text())

    clips = []
    for stem in ordered:
        sources = {m: per_method[m][stem] for m in METHODS if stem in per_method[m]}
        meta = captions.get(stem, {})
        clips.append({
            "id": stem,
            "title": meta.get("title", stem),
            "caption": meta.get("caption", ""),
            "sources": sources,
        })

    OUT.write_text(json.dumps(clips, indent=2) + "\n")

    print(f"Wrote {OUT.relative_to(ROOT)} with {len(clips)} clip(s).")
    for c in clips:
        have = "".join("+" if m in c["sources"] else "-" for m in METHODS)
        print(f"  {c['id']:<24} [{have}]  ({''.join(m[0].upper() for m in METHODS)})")
    incomplete = [c["id"] for c in clips if len(c["sources"]) < len(METHODS)]
    if incomplete:
        print(f"\n  NOTE: {len(incomplete)} clip(s) are missing one or more methods: "
              + ", ".join(incomplete))
        print("  Gallery will show a placeholder for any missing method.")


if __name__ == "__main__":
    main()
