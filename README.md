# Session 2 — Smart Learning with Google Gemini & NotebookLM

Presentation slides + hands-on lab for the **Smart Learning** series. Built as a
lightweight, self-contained slide deck (a web page, **not** a notebook) so you can
present the concepts first, then run the hands-on activity.

> **Live slides:** https://kianraj.github.io/smart-learning-session2-slides/
>
> **Present locally:** open [`index.html`](index.html) in any browser.

This is intentionally kept **separate from the course notebook templates** — it is a
teaching deck, not a fill-in-the-blanks exercise.

## All sessions in this series

| Session | Topic | Live slides |
|---------|-------|-------------|
| 2 | Smart Learning with Google Gemini & NotebookLM | https://kianraj.github.io/smart-learning-session2-slides/ |
| 3 | AI for Presentations & Design (Gamma & Figma AI) | https://kianraj.github.io/smart-learning-session3-slides/ |
| 4 | The Integrated AI Workflow — capstone & assessment | https://kianraj.github.io/smart-learning-session4-slides/ |

## What's inside

| Part | Slides | Content |
|------|--------|---------|
| Motivation & objectives | 1–2 | Where study time goes (visualized); session outcomes |
| The tools | 3–4 | Gemini vs NotebookLM compared; steal-these prompts + prompt anatomy |
| NotebookLM | 5–8 | How grounding works; create a notebook, Studio tools, cited answers — real in-app screens |
| Hands-on | 9–12 | Task 1 + Task 2 (all 10 outputs); drawn examples of good outputs + 7-day plan; where each output comes from in the tool |
| Submit & wrap | 13–14 | The 11-item PDF checklist; recap |

Every concept slide carries a **visualization** (inline SVG diagrams) so students can
*see* the workflow — sources → NotebookLM → study assets → one PDF — while they do it.

## Present it

- **Navigate:** `→` / `Space` next · `←` back · `Home` / `End` jump · `F` fullscreen.
- **Click:** right edge of the slide = next, left edge = back. Touch = swipe.
- **Deep-link:** `index.html#9` opens the activity directly.

## The hands-on activity (what students submit)

**Task 1 — Create your notebook.** Upload *one* document: branch syllabus, an AI
article, a research paper, a college brochure, or class notes / lecture slides.

**Task 2 — Explore the document.** Using NotebookLM, produce all ten:

1. 100–150 word summary
2. Five most important concepts
3. Three difficult terms explained simply
4. Five MCQs with answers
5. Five flashcards
6. One-page revision notes
7. Five interview / viva questions
8. Key learning outcomes
9. Mind map or concept hierarchy
10. 7-day study plan

**Submit** one PDF (`RollNo_Name_Session2.pdf`) containing a screenshot of the
uploaded document plus all of the above.

## Files

```
smart-learning-session2-slides/
├── index.html          <- the presentation (open / share this)
├── assets/
│   ├── slides.css       <- the "notebook aesthetic" theme
│   └── slides.js        <- keyboard / click / swipe navigation
├── _build_slides.py     <- all slide content lives here; regenerates index.html
└── README.md
```

## Editing the slides

All content lives in one place — [`_build_slides.py`](_build_slides.py). Edit the
`SLIDES` list or a `viz_*` diagram, then regenerate:

```bash
python _build_slides.py
```
