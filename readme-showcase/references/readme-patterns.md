# README patterns

Drawn from a read of 24 popular repositories' READMEs in November 2026. The examples are there to look at, not to copy; star counts and layouts change, so open a couple of live examples of the chosen style before writing.

## Contents

- [Style archetypes](#style-archetypes)
- [Choosing a style](#choosing-a-style)
- [What the first screen holds](#what-the-first-screen-holds)
- [HTML that GitHub renders](#html-that-github-renders)
- [Writing the words](#writing-the-words)
- [What carries a README with no media](#what-carries-a-readme-with-no-media)
- [Common mistakes](#common-mistakes)

## Style archetypes

Styles combine. Most good READMEs are one hero style plus one body style.

| Style | What leads | Suits | Needs | Poor fit when | Look at |
|---|---|---|---|---|---|
| **Demo-first loop** | A short silent recording of the product doing its main thing | Value appears in motion within about 10 s; terminal or web UI | A scripted recording, re-recorded when the UI changes | The flow is long, sound matters, or the clip must work in both themes | charmbracelet/gum, open-webui/open-webui, agharsallah/esp-labs-web |
| **Video hero** | An embedded clip with room for sound or a longer flow | Audio, subtitle and consumer tools; browser extensions | A clip uploaded to GitHub (it cannot live in the repo and still play inline), plus a still as fallback | Developer libraries; readers who will not press play | immersive-translate/immersive-translate, m-bain/whisperX (before/after clips) |
| **Screenshot-led** | One real screenshot, then bold-led feature bullets and a short install | The value shows in a single frame; apps with several screens | One hero shot and three to seven supporting shots | The value is in change over time, or there is no UI | Stirling-Tools/Stirling-PDF, n8n-io/n8n, chidiwilliams/buzz, Niko1221/Strata, morluto/rea |
| **Per-feature media** | Each feature heading has its own captioned shot or loop | Several distinct features that each look different | One asset per feature, kept current | Few features; features that look alike | sharkdp/bat, SakiRinn/LiveCaptions-Translator, agharsallah/esp-labs-web |
| **Code as demo** | A copy-paste command, a terminal transcript or a ten-line snippet | Libraries, CLIs with text output, APIs | Nothing but real, tested commands | The output is visual and the reader is an end user | ollama/ollama, astral-sh/uv, tldraw/tldraw |
| **Matrix-led** | Tables: features by platform, downloads by platform, engines by capability | Several platforms or surfaces; readers who compare capabilities | An accurate capability list, maintained | Few features; a table would bury the one thing that matters | immich-app/immich, localsend/localsend, gorhill/uBlock |
| **Evidence-led** | A measured number, a chart, a paper | Tools chosen on speed, cost or accuracy against alternatives | A reproducible measurement and a link to the method | There is no measurement. Unsupported numbers cost more trust than they buy | astral-sh/uv, microsoft/TokenEconomizer, m-bain/whisperX, QuentinFuxa/WhisperLiveKit |
| **Showcase-led** | Named things built or done with the project | Tools whose value is what they enable | Real cases, with permission where they are other people's | The project is new and has no cases yet | morluto/rea, excalidraw/excalidraw ("who's integrating") |
| **Pointer** | Logo, one line, link to the site or docs | Established names; products with a live demo one click away | A reputation or a site that does the explaining | Anything a visitor has not heard of | zed-industries/zed, shadcn-ui/ui |
| **Reference manual** | A table of contents and a section per option | Tools with many options and expert users | Ongoing upkeep | Used alone. It works only below a first screen that already has a pitch, a picture and an install line | junegunn/fzf, sharkdp/bat |

## Choosing a style

Decide from the project's characteristics, in this order. The technology stack is not one of them.

1. **Is the value in something changing over time** - output streaming in, a UI reacting, something appearing as audio plays? The hero has to move. Silent and under about 10 s: demo-first loop. Needs sound or a longer story: video hero, with a still that makes sense on its own.
2. **Is there a UI, and does one frame show the value?** Screenshot-led. A still is sharper, lighter and easier to keep current than a loop.
3. **Is the value a number people compare?** Evidence-led, only with the project's own reproducible measurement. Otherwise pick another style and leave numbers out.
4. **Is nothing visible** (library, protocol, backend)? Code as demo, with a diagram of where it sits.
5. **Several surfaces or platforms, each installed separately?** Show the whole thing working once in the hero, then give each surface its own short install step or a matrix. Do not make the first screen a table.
6. **Several distinct features that look different?** Add per-feature media below the quick start.
7. **Does someone else already vouch for it** - a known author, a live site, real adopters? Say so in one line near the top. Without that, a pointer-style README leaves a stranger with nothing.
8. **Audience.** End users: lead with the outcome in everyday words and a download. Developers: lead with the install command and a snippet.
9. **Install effort.** One command goes straight under the hero. Several paths go in a table or `<details>` folds, with the easiest shown open.
10. **Many options?** Keep them in `docs/` or below a fold; a newcomer needs the first run, not the manual.

Motion is less common than it looks: in the sample, most product images were static, and animated heroes were the minority. Choose motion because the product needs it, not because popular repos seem to have it.

## What the first screen holds

In the order most of the sample uses:

1. Logo or name, centered.
2. Tagline: one line, the outcome for the user, no technology names.
3. Badges, three to six, each true and each telling the visitor something: licence, latest release, platform, build status. Skip vanity counters on a young repo.
4. Optional row of links or anchors (Install, Docs, Releases) and a language switcher when translations exist.
5. Hero media, 600-900 px wide for screenshots and loops; logos much smaller (80-300 px).
6. Two or three sentences, or the quick start, immediately after.

A caution or status note (preview, unsigned binary, hardware needed) belongs near the top too, as a GitHub alert. Projects that state limits early read as more trustworthy, not less.

## HTML that GitHub renders

GitHub strips `<style>`, `<script>`, inline `style` attributes and most layout CSS from READMEs. These survive:

```html
<!-- centered title block -->
<div align="center">
  <img src="docs/media/logo.png" alt="Project logo" width="120">
  <h1>Project name</h1>
  <p><strong>One-line tagline in the user's words.</strong></p>
  <p>
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/OWNER/REPO"></a>
    <a href="../../releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/OWNER/REPO"></a>
  </p>
  <p><a href="#quick-start">Quick start</a> · <a href="docs/">Docs</a> · <a href="README.zh-TW.md">繁體中文</a></p>
</div>

<!-- hero -->
<p align="center">
  <img src="docs/media/hero.gif" alt="Describe what happens, not 'demo'" width="800">
</p>

<!-- theme-aware image -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/media/shot-dark.png">
  <img src="docs/media/shot-light.png" alt="Settings page" width="800">
</picture>

<!-- two images side by side -->
<table>
  <tr>
    <td width="60%"><img src="docs/media/a.png" alt="..."></td>
    <td width="40%"><img src="docs/media/b.png" alt="..."></td>
  </tr>
</table>

<!-- captioned feature shot -->
<p align="center">
  <img src="docs/media/overlay.png" alt="..." width="700"><br>
  <em>Caption: what the reader is looking at.</em>
</p>

<!-- fold for the long path -->
<details>
<summary>Run from source</summary>

Steps here. Leave a blank line after the summary so Markdown inside renders.

</details>
```

Alerts: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]` on the first line of a blockquote.

Video: paste the `https://github.com/user-attachments/assets/...` URL on a line of its own. It only exists after the file is uploaded through GitHub's web editor or an issue comment, which is a publishing step for the user to do.

Width: set `width` on `<img>` rather than relying on file dimensions, so a 2x capture stays sharp without filling the page.

## Writing the words

- **Tagline**: what the user gets. "Live translated subtitles for any browser tab, running on your own PC" rather than "A FastAPI and Manifest V3 speech pipeline".
- **Features as outcomes**: a bold lead-in naming the result, then one sentence. Mechanisms, formats and protocol names go under "How it works".
- **Lead with the differentiator**: the one thing that makes this project the right choice (local-only, no account, free, fastest, works offline) belongs in the first three lines, not in section nine.
- **Quick start**: numbered, each step one action, the command in a copyable block, and what the user should see at the end. State prerequisites before step one.
- **Limits**: platform, hardware, manual steps, unsigned binaries, preview status - near the top, plainly.
- **Translations**: keep section order and media identical across languages; only the text differs.

## What carries a README with no media

Several very popular READMEs have little or no product imagery. Each has something else doing the work:

- **A known name or author** stated in the first sentence (zed).
- **An install that is one line and works**, followed by real, runnable examples (ollama, uv).
- **A live site that is the demo** (shadcn-ui).
- **Store badges and an established user base** (darkreader).

A new or small project has none of these yet, which is why it needs the picture more than they do. Do not take a famous project's bare README as evidence that media is optional.

## Common mistakes

- A hero that needs explaining: a settings page, an architecture diagram or a logo where the working product should be.
- Mock-ups or generated art shown as the product.
- A feature list of technologies.
- Install instructions below pages of configuration.
- Numbers with no measurement behind them.
- A wall of badges, or badges for things the project does not have.
- Media hosted somewhere that can vanish (image hosts, a personal site) when the repo could hold it.
- A GIF so large or fast that the result cannot be read; a loop with no pause on the final state.
- Screenshots containing personal paths, account names, other people's content or keys.
- A light-only screenshot with a transparent background that disappears in dark mode.
- Translated READMEs that drift from the main one.
