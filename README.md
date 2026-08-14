# STRIDE — Qualitative Transition Comparisons (Anonymous Supplement)

Supplementary videos for a double-blind submission. Each clip shows the **same**
start→end transition rendered by four methods from identical boundary frames:
**Ours (STRIDE)** vs. DynamiCrafter, SEINE, and TVG. A GitHub Pages page
(`index.html`) plays them side-by-side in the browser.

> **Anonymity:** this repository contains no author names, affiliations, or
> identifying metadata. It must live on a **throwaway GitHub account** (fresh
> email, pseudonymous username) and be committed with an anonymized author —
> the included `setup_anon_repo.sh` enforces that automatically.

## Clip selection

The gallery shows **illustrative examples** from the 48-clip benchmark, not a uniform
sample. Selection is driven by the real 576-rating human study
(`PAPER/tvs48_stats_final/ratings_long.csv`): per-clip mean over 3 raters of
GHOSTING / SMOOTHNESS / SEMANTIC_COMMITMENT, compared against the **best** baseline on
that clip. Two tiers:

**Tier 1 — STRIDE rated at or above every baseline on every dimension (7 clips, all published).**
No weak link for a reviewer to click on.

| clip | ghosting | smoothness | commitment | overall |
|---|---|---|---|---|
| `scene_04` | +1.00 | +4.00 | +1.33 | **+2.22** |
| `scene_02` | +1.00 | +2.67 | +1.33 | **+2.00** |
| `scene_03` | +0.33 | +3.00 | +1.33 | **+1.89** |
| `morph_14` | 0.00 | +2.00 | +1.00 | **+1.33** |
| `morph_12` | 0.00 | +2.67 | +1.00 | **+1.22** |
| `morph_09` | 0.00 | +2.33 | +0.67 | **+1.00** |
| `scene_01` | +0.67 | +2.00 | 0.00 | **+1.00** |

**Tier 2 — published for reasons other than a clean sweep (1 clip).**

- `morph_06` — +0.56 overall (ghosting +1.00, smoothness +0.33, commitment −0.33, a
  near-tie).

**`cam_14` REMOVED (2026-08-14).** Was published as "a tie, not a win" (−0.22 overall,
smoothness +1.33) solely to have *some* camera-motion example, with the caveat spelled
out in this README. Advisor review of the live page flagged that, side-by-side, STRIDE
reads as visibly weaker than TVG on this clip — a reviewer skimming the grid would land
on it as evidence against the smoothness claim, which outweighs the value of covering
the category. **No camera-motion clip is currently published**; the page now shows only
`scene_*` and `morph_*` rows. See "Adding more camera-motion rows" below before
re-adding one — every other camera clip was already rejected for a visible artifact:

| clip | why not |
|---|---|
| `cam_12` | +0.56 overall, but **not actually camera motion** — a cat appears on a static chair, so the category caption would be false |
| `cam_06` | interior frames 4–10 show a **doubled, translucent ghost mushroom** (matches its −2.00 ghosting rating) |
| `cam_01` | interior goes **purple/magenta** (colour cast); 4× the baselines' flicker; `hold_frac 0.33` |
| `cam_03` / `cam_05` / `cam_08` | `hold_frac ≥ 0.33` — STRIDE holds nearly still, then jumps |
| `cam_04` / `cam_11` / `cam_15` | flicker 6.6–7.8, the highest in the set |
| `cam_09` / `cam_13` | rated far below all baselines (ghosting −2.33 / −3.00) |
| `cam_14` | tie not a win (−0.22 overall); reads weaker than TVG in the live grid (removed 2026-08-14) |

Also excluded: `scene_13` (+1.33 overall but ghosting −1.00), `scene_06` (ghosting −2.00,
commitment −1.00), `morph_11`, `scene_11`.

### Adding more camera-motion rows

The ratings above were collected on the **v3/raw** renders. The frozen final model is
**Stage-A EMA**, whose one kept win is reduced background flicker — which is exactly the
failure mode that sinks camera-motion clips (whole-frame background motion → VAE
breathing/jitter). So the camera ranking is stale, and re-scoring the Stage-A renders is
the legitimate way to find more publishable camera rows. Best flip candidates, by
smoothness margin and least-bad ghosting: `cam_14` (overall −0.22, smoothness +1.33,
ghosting −0.67 — the least-bad ghosting of all 15), then `cam_10` (−0.67) and `cam_06`
(−0.89). Baseline mp4s for those three are **not** in this repo's history; pull them from
the pod's per-method result roots via `PAPER/build_comparative_192.py`.

Objective re-ranking on the Stage-A renders (all three tools take a directory of mp4s,
so run them on the STRIDE dir and on each baseline dir):

```bash
# background flicker — detrended flick_idx, LOWER is better
python PAPER/build_static_scores.py --score_videos <dir> --flick_csv <dir>_flick.csv
# semantic roughness (CLIP-RS) + pixel-accel, paired per clip; run once per baseline
python PAPER/compare_smoothness.py --stage_a_dir <baseline_dir> --stage_b_dir <stride_dir> \
    --out_csv smooth_stride_vs_<baseline>.csv --gpu_id 0
# ghosting proxy — LOWER is better; ignore rows with endpoint_dist < 0.05
python PAPER/ghost_index.py --input_dir <dir> --out_dir <stats> --config_name <name> --gpu_id 0
```

These are proxies, and the human study said STRIDE loses camera motion — so the final
gate is your own eye, not the CSVs. If nothing flips, publish `cam_12` alone: one honest
camera row beats padding the category with a clip that visibly loses.

The page is framed around **smoothness / temporal continuity** because that is the
dimension the study validates broadly (STRIDE beats the best baseline on smoothness in
35/48 clips, versus 5/48 on ghosting and 21/48 on overall preference). The header keeps
a one-line note that these are selected examples and that the full 48-clip results are
in the paper — **keep it**: an undisclosed favorable subset is the one thing here a
reviewer could hold against the submission, and the paper's own Limitations section
already reports the ghosting loss.

### Playback: no looping (deliberate)

Clips **do not loop**. Every STRIDE render has a 3–7× spike in frame-to-frame change at
the *first and last* transition — the anchor-to-first-generated-frame seam (e.g.
`scene_04`: 20.7 / interior 4–10 / 17.2 on a 0–255 grey scale; `cam_12`: 15.0 / 2–5 /
13.3). On a looping video that seam repeats every two seconds and is the first thing the
eye locks onto, which works directly against the smoothness claim the page is making.
So each clip autoplays **once** when its row scrolls into view (IntersectionObserver,
60% threshold), with a per-row *Replay this comparison* button that restarts all four
videos in sync. Nothing about the videos themselves is altered — this is playback only.

### Re-rendering the STRIDE column

All eight STRIDE clips currently published come from one **Stage-A EMA** batch (the
`af`-config render, confirmed 2026-08-13); `morph_09` and `morph_06` were 640×360 and
were stretched to 512² to match the baseline framing. The human ratings were collected
on the earlier v3/raw renders, so the ranking above is a prior, not a guarantee —
eyeball each Stage-A render before publishing. To regenerate, on the pod:

```bash
python PAPER/generate_tvs48_configs.py \
  --stats_csv PAPER/tvs48_selection/tvs48_selection.csv \
  --checkpoint <stage_A_ema.pt> --output_root <dir> \
  --configs af --af_decay_steps 18 --cfg_scale 3.0 --device cuda:0
```

Then normalize to match the baseline framing and browser requirements — **H.264
(libx264, yuv420p), 512×512, 8 fps, 16 frames** (mpeg4 silently fails to play in
`<video>`; see `PAPER/reencode_h264.sh`), copy into `videos/stride/`, and re-run
`python3 gen_manifest.py`. `setup_anon_repo.sh` aborts if any row is missing a method.

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
   pseudonymous username (`anonstride2026`). Create an **empty public** repo
   named `stride-transitions` (no auto-README). Do **not** reuse your real account.

2. **Build + push** (from this folder):
   ```bash
   ./setup_anon_repo.sh https://github.com/anonstride2026/stride-transitions.git
   ```
   The script regenerates `clips.json`, checks file sizes, commits as
   `Anonymous <anonymous@anon.review>` (never your real name), and pushes.

3. **Enable GitHub Pages** on the repo: *Settings → Pages → Deploy from
   branch → `main` / `(root)`*. The gallery goes live at
   `https://anonstride2026.github.io/stride-transitions/` — this is the URL
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
