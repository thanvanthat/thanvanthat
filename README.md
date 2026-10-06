<div align="center">

<h3><code>thanvanth@github ~ $ ./contributions.sh</code></h3>
<img src="./contrib-heatmap.svg" width="860" alt="Contribution heatmap" />

<br><br>

<h3><code>thanvanth@github ~ $ whoami</code></h3>
<table>
  <tr>
    <td valign="top"><img src="./ascii-portrait.svg" width="370" alt="ASCII portrait" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" alt="neofetch-style info card" /></td>
  </tr>
</table>

</div>

<br>

<details>
<summary><code>$ cat HOW_IT_WORKS.md</code></summary>

<br>

Everything above is a self-contained animated SVG (SMIL / CSS keyframes) — GitHub strips
`<script>` and inline styles from READMEs, but it plays animations inside SVGs loaded via `<img>`.
No token, no third-party stats service.

| File | Made by | Refreshed |
| --- | --- | --- |
| `contrib-heatmap.svg` | `scripts/fetch_contributions.py` → `scripts/render_heatmap_svg.py` | daily, by `.github/workflows/update-profile-art.yml` |
| `ascii-portrait.svg` | `scripts/prep_photo.py` → `scripts/make_ascii_svg.py` | by hand, when the photo changes |
| `info-card.svg` | `scripts/make_info_card.py` | by hand, when details change |

Names, the info-card rows and the GitHub username all live in `scripts/config.py`.

```bash
python -m venv .venv && source .venv/bin/activate

# heatmap (what the workflow runs)
pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py && python scripts/render_heatmap_svg.py

# portrait from a photo (local only; without a photo the initials are drawn)
pip install -r scripts/requirements-portrait.txt
python scripts/prep_photo.py source-photo.jpg && python scripts/make_ascii_svg.py

# info card
python scripts/make_info_card.py
```

`STATIC=1` on any generator emits a frozen frame for previews.

</details>
