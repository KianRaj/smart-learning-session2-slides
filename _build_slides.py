#!/usr/bin/env python3
"""
Build the lecture slide deck for:

    Session 2 — Smart Learning with Google Gemini & NotebookLM

Content lives here (one place). Run this to regenerate the HTML:

    python _build_slides.py

Output:
    index.html                 <- the full presentation (open this / share this)
Shared look & behaviour:
    assets/slides.css , assets/slides.js
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Archivo:wght@700;800;900&"
         "family=IBM+Plex+Sans:wght@400;500;600&"
         "family=IBM+Plex+Mono:wght@400;500;600&display=swap")

# palette (kept in sync with assets/slides.css)
INK, PEN, RED, YEL, MUT, LINE, GRN = (
    "#17233B", "#2B4FD8", "#E4572E", "#FFE066", "#6E7688", "#E7E4DB", "#2E9E5B")

# ---------- render helpers (return HTML strings) ----------
def slide(*body, cls=""):
    return f'<section class="slide {cls}"><div class="inner">' + "".join(body) + "</div></section>"

def eyebrow(tag):   return f'<p class="eyebrow">Session 2 <span class="dot">•</span> {tag}</p>'
def h1(t):   return f"<h1>{t}</h1>"
def h2(t):   return f"<h2>{t}</h2>"
def lead(t): return f'<p class="lead">{t}</p>'
def p(t):    return f"<p>{t}</p>"
def muted(t):return f'<p class="muted">{t}</p>'

def cards(items, cols=3):
    inner = "".join(
        f'<div class="card">{("<span class=k>"+k+"</span>") if k else ""}'
        f'<h3>{t}</h3><p>{d}</p></div>' for k, t, d in items)
    return f'<div class="cards c{cols}">{inner}</div>'

def tick(items):
    return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def steps(items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def rows(pairs):
    r = "".join(f'<div class="row"><span class="lbl">{k}</span><span>{v}</span></div>' for k, v in pairs)
    return f'<div class="rows">{r}</div>'

def arch(txt):   return f'<div class="arch">{html.escape(txt)}</div>'
def flash(txt):  return f'<div class="flash">{txt}</div>'
def two(a, b):   return f'<div class="two"><div>{a}</div><div>{b}</div></div>'
def tags(items, on=()):
    return '<div class="tags">' + "".join(
        f'<span class="tag {"on" if t in on else ""}">{t}</span>' for t in items) + "</div>"

def prompt(text, tag="prompt"):
    return (f'<div class="prompt-box"><span class="pl">{tag}</span>'
            f'<span class="pt">{html.escape(text)}</span></div>')

def handoff(title, note, chip):
    return ('<div class="handoff"><p class="eyebrow">Now — hands-on</p>'
            f'<div class="big">{title}</div><p class="muted">{note}</p>'
            f'<span class="file">{chip}</span></div>')

# ---------- visualization helpers (inline SVG) ----------
def viz(svg, cap="", legend=None):
    leg = ""
    if legend:
        leg = '<div class="viz-legend">' + "".join(
            f'<span><i style="background:{c}"></i>{t}</span>' for c, t in legend) + "</div>"
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="viz">{svg}{cap}{leg}</div>'

def _chip(x, y, w, txt, fill, tc, h=34, r=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{LINE}"/>'
            f'<text x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle" font-size="13" fill="{tc}" class="mono">{txt}</text>')

def _arrow(x1, y1, x2, y2, color=MUT, mid="a"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#{mid})"/>'

def _defs():
    return (f'<defs>'
            f'<marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{MUT}"/></marker>'
            f'<marker id="ap" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{PEN}"/></marker>'
            f'<marker id="ag" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{GRN}"/></marker>'
            f'</defs>')

def viz_timesplit():
    # three activities; long "without AI" bar vs short "with AI" bar
    acts = [("Searching", 430, 120), ("Organizing", 380, 90), ("Revising", 460, 150)]
    y = 40; s = ""
    for name, wo, wi in acts:
        s += f'<text x="150" y="{y+14}" text-anchor="end" font-size="14" fill="{INK}">{name}</text>'
        s += f'<rect x="165" y="{y}" width="{wo}" height="20" rx="5" fill="#E7E2D6"/>'
        s += f'<rect x="165" y="{y}" width="{wi}" height="20" rx="5" fill="{PEN}"/>'
        s += f'<text x="{165+wo+10}" y="{y+15}" font-size="12" fill="{MUT}" class="mono">was hours</text>'
        y += 44
    svg = f'''<svg viewBox="0 0 720 170">{s}
      <text x="165" y="160" font-size="12" fill="{PEN}" class="mono">■ with AI</text>
      <text x="255" y="160" font-size="12" fill="{MUT}" class="mono">■ time you spend today</text></svg>'''
    return viz(svg, "AI compresses the searching / organizing / revising time — comprehension still happens in your head.")

def viz_compare():
    # Gemini (open world) vs NotebookLM (grounded)
    def panel(x, title, color, icon, lines):
        s = f'<rect x="{x}" y="20" width="300" height="230" rx="14" fill="#fff" stroke="{color}" stroke-width="2"/>'
        s += f'<text x="{x+24}" y="62" font-size="30">{icon}</text>'
        s += f'<text x="{x+70}" y="55" font-size="18" font-weight="700" fill="{INK}">{title}</text>'
        yy = 100
        for ln in lines:
            s += f'<circle cx="{x+28}" cy="{yy-4}" r="3" fill="{color}"/>'
            s += f'<text x="{x+42}" y="{yy}" font-size="13.5" fill="{INK}">{ln}</text>'
            yy += 34
        return s
    g = panel(30, "Gemini", PEN, "🌐",
              ["Open-world — broad knowledge", "Brainstorm, explain, code help",
               "File upload &amp; image understanding", "Great for ideas &amp; drafts"])
    n = panel(390, "NotebookLM", RED, "📚",
              ["Closed-world — your sources only", "Every answer is cited",
               "Won't invent outside facts", "Great for mastering your material"])
    svg = f'<svg viewBox="0 0 720 270">{g}{n}</svg>'
    return viz(svg, "Rule of thumb: Gemini for world ideas · NotebookLM for mastery of YOUR material.",
               [(PEN, "Gemini — open world"), (RED, "NotebookLM — grounded")])

def viz_gemini():
    ins = ["Text prompt", "PDF / DOCX", "Image / photo", "Code snippet"]
    outs = ["Explanations", "Summaries", "Project ideas", "Fixed code"]
    s = _defs()
    y = 30
    for t in ins:
        s += _chip(20, y, 150, t, "#fff", INK)
        s += _arrow(172, y+17, 268, 145, PEN, "ap")
        y += 46
    s += f'<rect x="270" y="110" width="150" height="70" rx="12" fill="{PEN}"/>'
    s += f'<text x="345" y="152" text-anchor="middle" font-size="18" fill="#fff" font-weight="700">Gemini</text>'
    y = 30
    for t in outs:
        s += _arrow(422, 145, 518, y+17, PEN, "ap")
        s += _chip(520, y, 160, t, "rgba(43,79,216,.10)", INK)
        y += 46
    svg = f'<svg viewBox="0 0 700 220">{s}</svg>'
    return viz(svg, "One assistant, many inputs → it reads text, files, images and code, and answers back.")

def viz_notebooklm():
    srcs = ["📄 PDF textbook", "📊 PPT slides", "🔬 Research paper", "📝 Class notes"]
    outs = ["Study guide", "FAQ", "Audio overview", "MCQs / quiz"]
    s = _defs()
    y = 24
    for t in srcs:
        s += _chip(16, y, 168, t, "#fff", INK)
        s += _arrow(186, y+17, 262, 130, MUT, "a")
        y += 44
    s += f'<rect x="264" y="96" width="164" height="74" rx="12" fill="{RED}"/>'
    s += f'<text x="346" y="130" text-anchor="middle" font-size="16" fill="#fff" font-weight="700">NotebookLM</text>'
    s += f'<text x="346" y="152" text-anchor="middle" font-size="11" fill="#ffdccb" class="mono">indexes your sources</text>'
    y = 24
    for t in outs:
        s += _arrow(430, 130, 506, y+17, RED, "a")
        s += _chip(508, y, 176, t, "rgba(228,87,46,.10)", INK)
        y += 44
    svg = f'<svg viewBox="0 0 700 210">{s}</svg>'
    return viz(svg, "Upload YOUR documents → NotebookLM turns them into study assets, every answer cited back to a page.")

def viz_grounding():
    s = _defs()
    s += _chip(20, 90, 190, "Your question", "#fff", INK, h=40)
    s += _arrow(212, 110, 288, 110, MUT, "a")
    s += f'<rect x="290" y="70" width="150" height="80" rx="12" fill="{RED}"/>'
    s += f'<text x="365" y="106" text-anchor="middle" font-size="15" fill="#fff" font-weight="700">NotebookLM</text>'
    s += f'<text x="365" y="126" text-anchor="middle" font-size="10.5" fill="#ffdccb" class="mono">reads sources</text>'
    s += _arrow(442, 110, 518, 110, RED, "a")
    s += f'<rect x="520" y="60" width="170" height="100" rx="12" fill="#fff" stroke="{LINE}"/>'
    s += f'<text x="605" y="92" text-anchor="middle" font-size="13" fill="{INK}">Answer</text>'
    for i, c in enumerate(["p.12", "p.30", "fig 4"]):
        s += f'<rect x="{535+i*50}" y="108" width="44" height="26" rx="13" fill="rgba(43,79,216,.12)" stroke="{PEN}"/>'
        s += f'<text x="{535+i*50+22}" y="125" text-anchor="middle" font-size="11" fill="{PEN}" class="mono">{c}</text>'
    svg = f'<svg viewBox="0 0 710 200">{s}</svg>'
    return viz(svg, "Ask → NotebookLM answers ONLY from your files, with clickable citations you can verify.")

def viz_prompt_anatomy():
    parts = [("role / context", "You are a strict examiner.", PEN),
             ("the task", "Write 5 MCQs", RED),
             ("the source", "from my uploaded notes only,", GRN),
             ("the format", "each with 4 options + answer.", INK)]
    s = ""; x = 20
    for _lbl, txt, col in parts:
        w = 8 + len(txt)*7.6
        s += f'<rect x="{x}" y="40" width="{w}" height="40" rx="8" fill="{col}" opacity="0.14"/>'
        s += f'<rect x="{x}" y="40" width="{w}" height="40" rx="8" fill="none" stroke="{col}"/>'
        s += f'<text x="{x+w/2}" y="65" text-anchor="middle" font-size="13.5" fill="{INK}" class="mono">{txt}</text>'
        s += f'<text x="{x+w/2}" y="105" text-anchor="middle" font-size="11.5" fill="{col}" class="mono">{_lbl}</text>'
        x += w + 10
    svg = f'<svg viewBox="0 0 {int(x)} 130">{s}</svg>'
    return viz(svg, "A good prompt = role + task + source + format. Name all four and the output gets sharper.")

def viz_taskflow():
    s = _defs()
    s += _chip(20, 70, 170, "1 document", "#fff", INK, h=50, r=10)
    s += f'<text x="105" y="140" text-anchor="middle" font-size="11" fill="{MUT}" class="mono">syllabus · paper · notes</text>'
    s += _arrow(192, 95, 250, 95, MUT, "a")
    s += f'<rect x="252" y="55" width="180" height="80" rx="12" fill="{RED}"/>'
    s += f'<text x="342" y="90" text-anchor="middle" font-size="15" fill="#fff" font-weight="700">NotebookLM</text>'
    s += f'<text x="342" y="112" text-anchor="middle" font-size="11" fill="#ffdccb" class="mono">10 outputs</text>'
    s += _arrow(434, 95, 492, 95, MUT, "a")
    s += f'<rect x="494" y="55" width="180" height="80" rx="12" fill="rgba(46,158,91,.14)" stroke="{GRN}" stroke-width="2"/>'
    s += f'<text x="584" y="90" text-anchor="middle" font-size="15" fill="{INK}" font-weight="700">1 PDF</text>'
    s += f'<text x="584" y="112" text-anchor="middle" font-size="11" fill="{GRN}" class="mono">11 items · submit</text>'
    svg = f'<svg viewBox="0 0 700 160">{s}</svg>'
    return viz(svg, "The whole lab in one line: one document in → ten AI-built study assets → one PDF submitted.")

# ============================================================
#  SLIDES
# ============================================================
SLIDES = [
  # 1 — title
  slide(
    eyebrow("Smart Learning Series"),
    h1("Smart Learning with<br>Gemini &amp; NotebookLM"),
    lead("Turn your syllabus, notes and research papers into summaries, MCQs, "
         "flashcards and study plans — <mark>in minutes, not hours</mark>."),
    tags(["Tools: Gemini + NotebookLM", "Mode: hands-on lab", "Deliverable: one PDF"], on=["Mode: hands-on lab"]),
    muted("Press → / Space to advance · ← to go back · F for fullscreen"),
  ),
  # 2 — motivation
  slide(
    eyebrow("Motivation"),
    h2("Where does your study time actually go?"),
    viz_timesplit(),
    cards([
      ("the pain", "Searching", "Hunting for material across PDFs, slides and websites."),
      ("the pain", "Organizing", "Re-writing content into notebooks and summaries."),
      ("the pain", "Revising", "Re-reading whole chapters with no condensed structure."),
    ], cols=3),
  ),
  # 3 — objectives
  slide(
    eyebrow("Objective"),
    h2("By the end of this session you can…"),
    tick([
      "Use <b>Gemini</b> for research, brainstorming, coding help and image understanding.",
      "Create a <b>NotebookLM</b> notebook from your own academic documents.",
      "Generate summaries, study guides, FAQs, audio overviews and revision notes.",
      "Ask questions that are <b>grounded in your uploaded sources</b> (with citations).",
      "Produce MCQs, viva questions, flashcards and a 7-day study plan.",
      "Compile everything into a <b>submission-ready PDF</b>.",
    ]),
  ),
  # 4 — toolkit / compare
  slide(
    eyebrow("The toolkit · visualize it"),
    h2("Two tools, two different jobs"),
    viz_compare(),
    muted("Gemini opens the whole world to you. NotebookLM locks onto YOUR documents so answers stay exam-safe."),
  ),
  # 5 — gemini features
  slide(
    eyebrow("Gemini · visualize it"),
    h2("Four Gemini features every student should use"),
    viz_gemini(),
    cards([
      ("1", "File upload", "Chat with a PDF, DOCX or slide deck."),
      ("2", "Coding help", "Write, fix and explain code line-by-line."),
      ("3", "Brainstorming", "Project ideas, seminar titles, outlines."),
      ("4", "Image understanding", "Read a diagram, hand-written note or photo."),
    ], cols=4),
  ),
  # 6 — gemini prompts
  slide(
    eyebrow("Gemini"),
    h2("Prompts you can steal today"),
    two(
      prompt("Suggest 10 mini-project ideas for a 2nd-year CSE student on machine "
             "learning. For each, list the dataset and difficulty level.", "brainstorm") +
      prompt("This Python code throws 'IndexError: list index out of range'. Explain "
             "why in simple terms, then show the fixed code. [paste code]", "coding help"),
      prompt("[attach chapter PDF] Explain the three hardest ideas in this chapter "
             "using everyday examples an 18-year-old would relate to.", "file upload") +
      prompt("[attach photo of a diagram] Identify this diagram, label each part, and "
             "explain the flow in 5 bullet points.", "image"),
    ),
    flash("<b>Good prompts have three parts:</b> role or context + a specific task + the output format."),
  ),
  # 7 — notebooklm intro
  slide(
    eyebrow("NotebookLM"),
    h2("Your personal, source-grounded research assistant"),
    two(
      tick([
        "Accepts PDFs, Google Docs &amp; Slides, websites, YouTube links, pasted text.",
        "Every answer includes <b>clickable citations</b> back to your documents.",
        "Won't invent facts from outside your sources.",
      ]),
      flash("Grounded answers are <b>safer for exam prep</b> — when the syllabus defines "
            "what's correct, you want answers that stay inside it.<br><br>"
            "Free with a Google account · works in the browser on laptop and phone."),
    ),
  ),
  # 8 — notebooklm workflow
  slide(
    eyebrow("NotebookLM · visualize it"),
    h2("How NotebookLM works"),
    viz_notebooklm(),
    muted("You bring the sources; NotebookLM does the reading and turns them into study material you can trust."),
  ),
  # 9 — create first notebook
  slide(
    eyebrow("NotebookLM"),
    h2("Create your first notebook"),
    two(
      steps([
        "Go to <code>notebooklm.google.com</code> and sign in.",
        "Click <b>Create new</b>.",
        "Add sources — drag-and-drop, a URL, or Google Drive.",
        "Wait for NotebookLM to <b>index</b> your sources.",
        "Start chatting, or use one-click tools in the <b>Studio</b> panel.",
      ]),
      flash("<b>Tips</b><br>• Name it by subject + unit — e.g. "
            "<i>DBMS – Unit 3 Normalization</i>.<br>• One notebook = one topic → "
            "sharper, better-cited answers."),
    ),
  ),
  # 10 — working with documents
  slide(
    eyebrow("NotebookLM"),
    h2("PDFs, PPTs &amp; research papers"),
    cards([
      ("textbook PDFs", "Upload directly", "Ask for unit breakdowns and worked examples on tough sections."),
      ("slides / PPT", "Via Google Slides or export to PDF", "Reconstruct the full lecture from the deck."),
      ("research paper", "Ask the 3 questions", "“What problem does it solve? What method? What results?”"),
    ], cols=3),
    flash("Mix source types in one notebook and ask a question <b>across all of them at once</b>."),
  ),
  # 11 — studio tools
  slide(
    eyebrow("NotebookLM"),
    h2("One click, four study assets"),
    cards([
      ("Studio", "Study guide", "Auto-outline: key topics, terms and short-answer questions."),
      ("Studio", "FAQ", "The questions a reader is most likely to ask — answered with citations."),
      ("Studio", "Audio overview", "A podcast-style discussion to revise while commuting."),
      ("Studio", "Briefing / notes", "Condensed summaries, timelines and mind maps."),
    ], cols=4),
    muted("Ask in chat for more: flashcards, a 7-day study plan, viva questions with model answers."),
  ),
  # 12 — question answering (grounding)
  slide(
    eyebrow("NotebookLM · visualize it"),
    h2("Ask your documents, get cited answers"),
    viz_grounding(),
    two(
      prompt("Define 'normalization' exactly as this document explains it, then give "
             "the example it uses.", "definition") +
      prompt("List anything in the syllabus PDF that is NOT covered in my class-notes "
             "PDF.", "gap finder"),
      flash("<b>Always click the citation</b> to check the passage before you memorise it. "
            "NotebookLM will also tell you when it <i>cannot</i> find something — that's a real gap."),
    ),
  ),
  # 13 — prompt anatomy
  slide(
    eyebrow("Skill · visualize it"),
    h2("Anatomy of a good prompt"),
    viz_prompt_anatomy(),
    p("Whether it's Gemini or NotebookLM, the same recipe works. For NotebookLM add "
      "<b>“from my sources only”</b> so the answer stays grounded."),
  ),
  # 14 — activity overview
  slide(
    eyebrow("Hands-on"),
    h2("Activity — your Smart Study Companion"),
    viz_taskflow(),
    cards([
      ("~10 min", "Task 1 · Create", "Upload one document and build a notebook."),
      ("~45 min", "Task 2 · Explore", "Generate all 10 study outputs from it."),
      ("~15 min", "Compile", "Paste everything into one PDF and submit."),
    ], cols=3),
  ),
  # 15 — task 1
  slide(
    eyebrow("Hands-on · Task 1"),
    h2("Create your notebook  (~10 min)"),
    two(
      p("Pick <b>one</b> document (4–5+ pages of real content) and upload it:") +
      tick([
        "Your branch <b>syllabus</b>",
        "An <b>AI-related article</b>",
        "A <b>research paper</b>",
        "A <b>college brochure</b>",
        "Your <b>class notes</b> or lecture slides",
      ]),
      flash("📸 <b>Screenshot the uploaded source</b> inside NotebookLM right away — "
            "that screenshot is the first item in your submission."),
    ),
  ),
  # 16 — task 2 part 1
  slide(
    eyebrow("Hands-on · Task 2"),
    h2("Explore the document — generate these"),
    two(
      steps([
        "A <b>100–150 word summary</b> of the document.",
        "The <b>five most important concepts</b> discussed.",
        "<b>Three difficult terms</b> explained in simple language.",
        "<b>Five MCQs</b> with answers.",
        "<b>Five flashcards</b> (question → answer) for revision.",
      ]),
      steps([
        "One-page <b>revision notes</b> for the whole document.",
        "<b>Five interview / viva questions</b> (with model answers).",
        "The key <b>learning outcomes</b>.",
        "A <b>mind map</b> or concept hierarchy (describe it if visuals aren't available).",
        "A <b>7-day study plan</b> to master the document.",
      ]),
    ),
    flash("<b>Prompt pattern:</b> “From my sources only, …” + the task + a word / format limit."),
  ),
  # 17 — sample 7-day plan
  slide(
    eyebrow("Hands-on · what 'good' looks like"),
    h2("A 7-day plan, done well"),
    rows([
      ("Day 1", "Read the summary + key concepts — skim the source with citations open."),
      ("Day 2–3", "Deep-dive the difficult terms &amp; core sections — ask “explain with an example”."),
      ("Day 4", "Active recall — flashcards, self-test without notes."),
      ("Day 5", "Practice — attempt the MCQs and viva questions aloud."),
      ("Day 6", "Consolidate — rewrite the one-page notes from memory."),
      ("Day 7", "Simulate — audio overview on the commute + a final gap check."),
    ]),
    muted("A good plan is document-specific and uses varied methods — not “read everything again”."),
  ),
  # 18 — submission checklist
  slide(
    eyebrow("Deliverable"),
    h2("One PDF, eleven items"),
    two(
      tick([
        "Screenshot of the uploaded document",
        "100–150 word summary",
        "Five key concepts",
        "Three simplified term explanations",
        "Five MCQs with answers",
        "Five flashcards",
      ]),
      tick([
        "One-page revision notes",
        "Five interview / viva questions",
        "Key learning outcomes",
        "Mind map or concept hierarchy",
        "7-day study plan",
      ]),
    ),
    flash("Paste into a Google Doc / Word in this order with headings, export as one PDF. "
          "Filename: <b>RollNo_Name_Session2.pdf</b>"),
  ),
  # 19 — best practices
  slide(
    eyebrow("Best practice"),
    h2("Use AI like a topper, not a shortcut"),
    two(
      cards([("do", "Verify &amp; rewrite", "Check answers against cited passages; rewrite key outputs in your own words; use flashcards for active recall; ask follow-ups until you can explain it to a friend.")], cols=1),
      cards([("don't", "Don't outsource thinking", "Don't submit text you haven't read; don't trust numbers / formulas without checking the source; don't upload confidential or copyrighted material; don't let tools replace practice problems.")], cols=1),
    ),
    flash("<b>Tools compress reading time — understanding still happens in your head.</b>"),
  ),
  # 20 — wrap up
  slide(
    handoff("Every document you own is now a study companion.",
            "Recap — Gemini for open-world help · NotebookLM for grounded mastery · "
            "one PDF with all 11 items.",
            "notebooklm.google.com  ·  gemini.google.com"),
    muted("Submission deadline as announced in class — ask your doubts now or during the lab."),
    cls="handoff-slide",
  ),
]

# ============================================================
#  PAGE SHELL + WRITE
# ============================================================
def page():
    body = "\n".join(SLIDES)
    nav = ('<div class="nav"><button class="up" title="Previous (↑)">↑</button>'
           '<button class="down" title="Next (↓)">↓</button></div>')
    chrome = ('<div class="margin-line"></div><div class="progress"></div>'
              '<div class="counter"></div>'
              '<div class="brand">KIET · Smart Learning · Session 2</div>' + nav)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Session 2 — Smart Learning with Gemini &amp; NotebookLM</title>
<meta name="description" content="Hands-on lecture slides: use Google Gemini and NotebookLM to study smarter.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/slides.css">
</head><body>
<div class="stage">
{body}
</div>
{chrome}
<script src="assets/slides.js"></script>
</body></html>"""

def main():
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page())
    print("wrote index.html  (", len(SLIDES), "slides )")
    print("Open index.html in a browser to present.")

if __name__ == "__main__":
    main()
