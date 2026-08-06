# STRIDE — Qualitative Transition Comparisons (Anonymous Supplement)

Supplementary videos for a double-blind submission. Each clip shows the **same**
start→end transition rendered by four methods from identical boundary frames:
**Ours (STRIDE)** vs. DynamiCrafter, SEINE, and TVG. A GitHub Pages page
(`index.html`) plays them side-by-side in the browser.

> **Anonymity:** this repository contains no author names, affiliations, or
> identifying metadata. It must live on a **throwaway GitHub account** (fresh
> email, pseudonymous username) and be committed with an anonymized author —
> the included `setup_anon_repo.sh` enforces that automatically.

## Layout

```
anon_supplement/
├── index.html          # side-by-side gallery (GitHub Pages entry point)
├── clips.json          # manifest that drives the gallery (24 clips × 4 methods)
├── captions.json       # per-clip titles/captions (category-derived)
├── gen_manifest.py     # scans videos/ → writes clips.json
├── make_captions.py    # scans videos/stride → writes captions.json
├── setup_anon_repo.sh  # anonymized git init + commit + push
└── videos/             # 24 clips per method, identical filenames across methods
    ├── stride/         # Ours (STRIDE)
    ├── dynamicrafter/
    ├── seine/
    └── tvg/
```

**Clip ids** are neutral, anonymity-safe, and encode only the transition
**category** (never a dataset path or identifying name):

| prefix | category | count |
|--------|----------|-------|
| `cam_NN`   | camera motion | 8 |
| `morph_NN` | object morph  | 8 |
| `scene_NN` | scene change  | 8 |

The **same filename** appears in all four method folders for a given clip, so the
filename stem (e.g. `cam_01`) is the clip id and one gallery row shows all four
renderings from identical boundary frames.

## Publish to the anonymous repo (3 steps)

The videos, `clips.json`, and `captions.json` are **already generated** in this
folder, so publishing is just: commit anonymously → push → enable Pages.

1. **Create the throwaway GitHub account + empty repo.** Use a fresh email and a
   pseudonymous username (`anon-stride-2026`). Create an **empty public** repo
   named `stride-transitions` (no auto-README). Do **not** reuse your real account.

2. **Build + push** (from this folder):
   ```bash
   ./setup_anon_repo.sh https://github.com/anon-stride-2026/stride-transitions.git
   ```
   The script regenerates `clips.json`, checks file sizes, commits as
   `Anonymous <anonymous@anon.review>` (never your real name), and pushes.

3. **Enable GitHub Pages** on the repo: *Settings → Pages → Deploy from
   branch → `main` / `(root)`*. The gallery goes live at
   `https://anon-stride-2026.github.io/stride-transitions/` — this is the URL
   already cited in the paper's supplementary footnote.

> To add/remove clips later: drop the new `.mp4` (same name) into each method
> folder, then re-run `python3 make_captions.py && python3 gen_manifest.py`.

## Notes

- **File size:** GitHub hard-rejects files > 100 MB. Keep clips short and
  compressed. The setup script blocks the push and prints an `ffmpeg` recipe if
  any clip is ≥ 90 MB. A safe recipe:
  ```bash
  ffmpeg -i in.mp4 -vf scale=256:-2 -crf 30 -an out.mp4
  ```
- **Anonymity checklist before you push:**
  - throwaway account, pseudonymous username, fresh email;
  - committed author reads `Anonymous` (the script prints it for you to verify);
  - no filenames or captions that leak your name, institution, or private paths.
- Regenerate the manifest any time you add/remove clips: `python3 gen_manifest.py`.
