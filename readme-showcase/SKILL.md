---
name: readme-showcase
description: Turn a project's README into a product introduction that gets across in seconds - hero image or demo animation, real screenshots, architecture diagram, badges, short quick start - and produce the media files for it. Use this whenever the user wants to present, showcase, introduce, promote or "make look professional" a repository; asks for a demo GIF, hero image, banner, screenshots or architecture diagram for a README; says their README is plain, text-only or has no pictures; points at popular / high-star repositories as the look they want; or is preparing a repo for a release, launch or open-sourcing. Also triggers on 專案介紹, 項目演示, README 美化, 示範動畫, 架構圖, 展示圖. Use it even when the user only says "improve my README" if the repo has something visual to show.
---

# README showcase

A README is the product page of a repository. Most visitors decide within the first screen whether to keep reading, so the job is to make that screen answer three questions without scrolling: what is this, what does it look like when it works, and how do I try it. Everything in this skill serves that.

Two things make this harder than "add a GIF":

- **The right media depends on what the project can show**, not on its language or framework. A CLI, a browser extension, a desktop app and a library each have a different honest way of being seen. Work that out from the repo; do not apply one template to everything.
- **The media must be true.** A recording of the real thing working is worth more than a polished mock, and a mock presented as the product is a lie the first user will discover. If something cannot be captured automatically, hand the user a shot list rather than faking it.

## Workflow

### 1. Survey the project

Read the existing README, the entry points, the release assets and the licence. Write down, in plain words:

- What it does for the person using it (one sentence, no technology names).
- Who that person is: end user, developer, operator, researcher.
- Its **surfaces** - every place where the project is visible: terminal output, a web page, a browser extension overlay or popup, a desktop window, a mobile screen, an API response, a generated file, numbers in a benchmark. A project often has several.
- How someone gets it running, counted in steps, and what they need first.
- What is already there: logo, screenshots, docs site, existing media folder, localized READMEs.
- Limits a newcomer will hit: platform, hardware, manual steps, unsigned binaries, preview status.

If the README in the working tree differs from the published one, work from the working tree and say so.

### 2. Decide the one picture

Before touching any tool, decide what a visitor should understand in five seconds and which single image or clip shows it. State it as a sentence: "a video is playing and translated subtitles appear over it as people speak". That sentence is the brief for the hero and usually the seed of the tagline.

If the value is not visible (a library, a protocol, a cost saving), the picture is whatever makes the result concrete: input next to output, before next to after, a number with its measurement, or a diagram of what talks to what.

### 3. Choose the style and the media

Read `references/readme-patterns.md` and pick the style archetype from the project's characteristics (visible UI or not, value seen in seconds or only in numbers, audience, number of surfaces, install effort). Then choose media per surface from `references/media-recipes.md`.

Prefer the cheapest thing that carries the message. A sharp static screenshot beats a blurry, heavy animation; an animation earns its weight only when the value is in the change over time. Several well-known READMEs have no animation at all.

Tell the user the plan before producing anything expensive: the archetype, the hero, the list of other media, and which items you can capture yourself versus which need them.

### 4. Capture

Follow `references/media-recipes.md` for the chosen surfaces. Rules that apply to every capture:

- Record the real product doing real work. Use sample content that is safe to publish: no personal accounts, private paths, API keys, other people's copyrighted video frames or faces in the shot.
- Script the capture when possible (a tape file, a browser script, a render script) and keep the script in the repo next to the media, so the asset can be regenerated when the UI changes.
- When a capture needs a human (a permission prompt, a user gesture, hardware, a login), write a **shot list**: what to open, the window size, what to do second by second, how long, what format to save, where to put the file. Then do the trimming, cropping and compression yourself.
- Put media in one folder inside the repo (`docs/media/` unless the project already has a convention) and reference it with relative paths, so the README works in forks, on mirrors and offline.

### 5. Restructure the README

Order, top to bottom. `references/readme-patterns.md` has the details and the HTML that GitHub accepts.

1. Title block: name, one-line tagline in the words the project's users would use (offer two or three candidates and let the user pick; it is the most-read line and a matter of taste), badges that are true and useful (licence, latest release, platform, build), language switcher if translations exist.
2. Hero media.
3. Two or three sentences: what it is, why it is different.
4. Quick start in as few steps as the project honestly allows. If there is an easy path and a source path, show the easy one and fold the other. Start from where the reader actually is: on the repository page with nothing installed. The first step is however this kind of project is obtained (a release download, a package install, a store link, a clone), so do not open with a command that assumes the files are already on their machine.
5. Features, written as outcomes ("Subtitles appear over any tab") rather than mechanisms ("Streams Opus over WebSocket"), with media where a feature is visual.
6. How it works: one diagram.
7. Known limits and project status, stated plainly.
8. Everything else - configuration, internals, project layout - folded with `<details>` or moved to `docs/` and linked.
9. Contributing, licence, credits.

Keep what already works in the existing README; move it rather than rewrite it. Keep every factual claim the project can back and drop adjectives it cannot. Do not invent numbers: a latency, accuracy or speed-up figure needs a measurement the user can point to, otherwise leave it out.

If the project has localized READMEs, apply the same structure and the same media to each, and keep them in step. Write each language the way its readers would say it rather than translating sentence by sentence; a phrase that is natural in one language is often odd in another.

The words a visitor reads follow the rules in "Writing the words" in `references/readme-patterns.md`. In particular, this skill's working vocabulary (hero, surface, first screen, archetype, shot list) is for planning, not for the page.

### 6. Verify

Run the bundled check from the repo root:

```bash
python <skill-dir>/scripts/check_readme_assets.py README.md
```

It reports missing local files, broken relative links, images without alt text, oversized media and whether any image appears in the first screen. Fix what it finds, then look at the result with your own eyes: render the README (GitHub preview, or a local Markdown preview) in both light and dark themes and at a narrow width. A check that passes on file names says nothing about whether the hero is legible.

The script cannot read, so do two more passes yourself:

- **Read it as a visitor.** Go through the first screen and the quick start as someone who has only the repository URL and has never seen the project. Every step must be possible from that starting point, and every term must be one they already know.
- **Check every step against the real interface.** Each button name, menu, option and file name in the quick start must exist in the current code or the running app. Search the source for each label; a plausible-sounding step that the UI does not offer is worse than no step.
- **Tone pass.** Re-read the tagline, intro, feature list and captions against "Prose that reads as machine-written" in `references/readme-patterns.md`, in every language version. In particular: bold labels are plain noun phrases, the main promise appears at most twice, and second-person pronouns are not in every sentence.
- **Look at the rendered page.** Diagrams, line breaks inside diagram labels, tables, image widths and folds can all differ from what the source suggests. If the README is already pushed, open the repository page in a browser; if not, use a local preview and check again after the push.

Finish by telling the user what was produced, which claims or captures are still waiting on them, and how to regenerate each asset. Name any check you could not do (for example, the page was never viewed on GitHub) instead of letting a passed script stand in for it.

## Boundaries

- Changing a README and adding files is local work. Committing, pushing, editing the repository's About/social preview or publishing a release needs the user's go-ahead.
- Do not add trackers, third-party hosted images that can disappear, or badges for services the project does not use.
- Do not copy another project's artwork, logo or screenshots. Their structure is fair to learn from; their assets are not.
