<div align="center">

<img src="./headline.svg" width="860" alt="Hi, I'm Thanvanth. Aspiring Game Developer." />

<br><br>

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

<br>

<h3><code>thanvanth@github ~ $ cat projects/fresora-ai/README.md</code></h3>
<a href="https://github.com/thanvanthat/fresora-AI"><img src="./featured.svg" width="860" alt="Featured project: Fresora AI" /></a>
<p><a href="https://fresora-web.vercel.app">Live app</a> · <a href="https://github.com/thanvanthat/fresora-AI">Repository</a></p>

<br>

<h3><code>thanvanth@github ~ $ ls ~/projects</code></h3>
<!-- projects:start -->
<table>
  <tr>
    <td valign="top"><a href="https://github.com/thanvanthat/Gilli"><img src="./projects/Gilli.svg" width="420" alt="Gilli" /></a><br><sub><a href="https://gilli-rho.vercel.app">Play</a> · <a href="https://github.com/thanvanthat/Gilli">Repo</a></sub></td>
    <td valign="top"><a href="https://github.com/thanvanthat/snake-and-ladder-"><img src="./projects/snake-and-ladder-.svg" width="420" alt="Snakes &amp; Ladders 3D" /></a><br><sub><a href="https://snakes-and-ladders-3d-psi.vercel.app">Play</a> · <a href="https://github.com/thanvanthat/snake-and-ladder-">Repo</a></sub></td>
  </tr>
  <tr>
    <td valign="top"><a href="https://github.com/thanvanthat/fresora-AI"><img src="./projects/fresora-AI.svg" width="420" alt="Fresora AI" /></a><br><sub><a href="https://fresora-web.vercel.app">Live</a> · <a href="https://github.com/thanvanthat/fresora-AI">Repo</a></sub></td>
    <td valign="top"><a href="https://github.com/thanvanthat/GrantPilot-Frontend"><img src="./projects/GrantPilot-Frontend.svg" width="420" alt="GrantPilot AI" /></a><br><sub><a href="https://thanvanthat.github.io/GrantPilot-Frontend/">Live</a> · <a href="https://github.com/thanvanthat/GrantPilot-Frontend">Repo</a></sub></td>
  </tr>
  <tr>
    <td valign="top"><a href="https://github.com/thanvanthat/Patchpulse"><img src="./projects/Patchpulse.svg" width="420" alt="PatchPulse" /></a><br><sub><a href="https://github.com/thanvanthat/Patchpulse">Repo</a></sub></td>
    <td valign="top"><a href="https://github.com/thanvanthat/portfolio"><img src="./projects/portfolio.svg" width="420" alt="Portfolio" /></a><br><sub><a href="https://thanvanth.vercel.app">Live</a> · <a href="https://github.com/thanvanthat/portfolio">Repo</a></sub></td>
  </tr>
  <tr>
    <td valign="top"><a href="https://github.com/thanvanthat/cinimatic"><img src="./projects/cinimatic.svg" width="420" alt="cinimatic" /></a><br><sub><a href="https://github.com/thanvanthat/cinimatic">Repo</a></sub></td>
    <td valign="top"><a href="https://github.com/thanvanthat/job-Appliction"><img src="./projects/job-Appliction.svg" width="420" alt="Lumen Job Portal" /></a><br><sub><a href="https://github.com/thanvanthat/job-Appliction">Repo</a></sub></td>
  </tr>
  <tr>
    <td valign="top"><a href="https://github.com/thanvanthat/leetcode-solutions"><img src="./projects/leetcode-solutions.svg" width="420" alt="LeetCode Solutions" /></a><br><sub><a href="https://github.com/thanvanthat/leetcode-solutions">Repo</a></sub></td>
  </tr>
</table>
<!-- projects:end -->

<br>

<h3><code>thanvanth@github ~ $ cat stack.toml</code></h3>
<img src="./stack.svg" width="860" alt="Tech stack" />

<br><br>

<h3><code>thanvanth@github ~ $ ./connect.sh</code></h3>
<a href="https://github.com/thanvanthat"><img src="./badges/github.svg" height="28" alt="GitHub" /></a>&nbsp;
<a href="https://instagram.com/thanvanth_ox"><img src="./badges/instagram.svg" height="28" alt="Instagram" /></a>&nbsp;
<a href="mailto:thanvanthat24@gmail.com"><img src="./badges/email.svg" height="28" alt="Email" /></a>

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
| `featured.svg` | `scripts/make_featured.py` | by hand, when the project changes |
| `projects/*.svg` + README grid | `scripts/make_projects.py` | by hand, when projects change |
| `headline.svg` | `scripts/make_headline.py` | by hand, when the lines change |
| `stack.svg`, `badges/*.svg` | `scripts/make_badges.py` (icons: Simple Icons, `scripts/icons.json`) | by hand, when the stack or links change |

Names, info-card rows, headline lines, featured project, project cards, stack and social links all live in `scripts/config.py`.

```bash
python -m venv .venv && source .venv/bin/activate

# heatmap (what the workflow runs)
pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py && python scripts/render_heatmap_svg.py

# portrait from a photo (local only; without a photo the initials are drawn)
pip install -r scripts/requirements-portrait.txt
python scripts/prep_photo.py source-photo.jpg && python scripts/make_ascii_svg.py

# info card, headline, stack + connect badges, featured project, project cards
python scripts/make_info_card.py && python scripts/make_headline.py && python scripts/make_badges.py && python scripts/make_featured.py && python scripts/make_projects.py
```

`STATIC=1` on any generator emits a frozen frame for previews.

</details>
