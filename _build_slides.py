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

def shot(src, url, cap="", crop=False):
    """A real-website screenshot in a browser frame (image self-hosted in assets/img)."""
    dots = "".join(f'<i style="background:{c}"></i>' for c in ("#E4572E", "#FFC93C", "#2E9E5B"))
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    cls = "imgwrap crop" if crop else "imgwrap"
    return (f'<div class="shot"><div class="bar">{dots}<span class="url">{url}</span></div>'
            f'<div class="{cls}"><img src="assets/img/{src}" alt="{url} screenshot"></div>{cap}</div>')

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

def viz_samples():
    """Drawn examples of the three trickiest outputs: flashcard, MCQ, mind map."""
    s = ""
    # flashcard (front + back)
    s += f'<rect x="20" y="30" width="200" height="120" rx="10" fill="#fff" stroke="{PEN}" stroke-width="1.6" transform="rotate(-2 120 90)"/>'
    s += f'<text x="120" y="62" text-anchor="middle" font-size="11" fill="{PEN}" class="mono" transform="rotate(-2 120 90)">FLASHCARD · FRONT</text>'
    s += f'<text x="120" y="95" text-anchor="middle" font-size="13" fill="{INK}" font-weight="600" transform="rotate(-2 120 90)">What does ACID</text>'
    s += f'<text x="120" y="112" text-anchor="middle" font-size="13" fill="{INK}" font-weight="600" transform="rotate(-2 120 90)">stand for?</text>'
    s += f'<rect x="60" y="120" width="200" height="90" rx="10" fill="{YEL}" stroke="#EAD98A" transform="rotate(2 160 165)"/>'
    s += f'<text x="160" y="150" text-anchor="middle" font-size="11" fill="{INK}" class="mono" transform="rotate(2 160 165)">BACK</text>'
    s += f'<text x="160" y="172" text-anchor="middle" font-size="12" fill="{INK}" transform="rotate(2 160 165)">Atomicity · Consistency</text>'
    s += f'<text x="160" y="188" text-anchor="middle" font-size="12" fill="{INK}" transform="rotate(2 160 165)">Isolation · Durability</text>'
    # MCQ card
    s += f'<rect x="300" y="30" width="220" height="180" rx="10" fill="#fff" stroke="{LINE}"/>'
    s += f'<text x="316" y="56" font-size="11" fill="{RED}" class="mono">MCQ · Q3</text>'
    s += f'<text x="316" y="78" font-size="12.5" fill="{INK}" font-weight="600">Which normal form removes</text>'
    s += f'<text x="316" y="94" font-size="12.5" fill="{INK}" font-weight="600">partial dependency?</text>'
    opts = [("A) 1NF", False), ("B) 2NF", True), ("C) 3NF", False), ("D) BCNF", False)]
    yy = 116
    for t, right in opts:
        if right:
            s += f'<rect x="310" y="{yy-13}" width="90" height="19" rx="9" fill="rgba(46,158,91,.18)"/>'
        s += f'<text x="318" y="{yy}" font-size="12" fill="{GRN if right else INK}" font-weight="{700 if right else 400}">{t}{" ✓" if right else ""}</text>'
        yy += 23
    # mind map
    cx, cy = 660, 110
    import math
    for i, b in enumerate(["unit 1", "terms", "uses", "limits", "people"]):
        ang = -90 + i*72
        bx = cx + 95*math.cos(math.radians(ang)); by = cy + 78*math.sin(math.radians(ang))
        s += f'<line x1="{cx}" y1="{cy}" x2="{bx}" y2="{by}" stroke="{LINE}" stroke-width="2"/>'
        s += f'<rect x="{bx-32}" y="{by-13}" width="64" height="26" rx="13" fill="#fff" stroke="{RED}"/>'
        s += f'<text x="{bx}" y="{by+4}" text-anchor="middle" font-size="10.5" fill="{INK}" class="mono">{b}</text>'
    s += f'<circle cx="{cx}" cy="{cy}" r="34" fill="{RED}"/>'
    s += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11.5" fill="#fff" font-weight="700">TOPIC</text>'
    s += f'<text x="120" y="232" text-anchor="middle" font-size="11.5" fill="{MUT}" class="mono">flashcards (output 5)</text>'
    s += f'<text x="410" y="232" text-anchor="middle" font-size="11.5" fill="{MUT}" class="mono">MCQs (output 4)</text>'
    s += f'<text x="{cx}" y="232" text-anchor="middle" font-size="11.5" fill="{MUT}" class="mono">mind map (output 9)</text>'
    svg = f'<svg viewBox="0 0 790 240">{s}</svg>'
    return viz(svg)

def viz_week():
    """The 7-day study plan as a calendar strip."""
    days = [("D1", "read summary +\\nkey concepts", PEN),
            ("D2", "deep-dive\\nhard terms", PEN),
            ("D3", "deep-dive\\ncore sections", PEN),
            ("D4", "active recall:\\nflashcards", RED),
            ("D5", "practice: MCQs\\n+ viva aloud", RED),
            ("D6", "rewrite notes\\nfrom memory", GRN),
            ("D7", "audio overview\\n+ gap check", GRN)]
    s = ""; x = 14; w = 104
    for d, txt, col in days:
        s += f'<rect x="{x}" y="34" width="{w-8}" height="120" rx="10" fill="#fff" stroke="{LINE}"/>'
        s += f'<rect x="{x}" y="34" width="{w-8}" height="30" rx="10" fill="{col}"/>'
        s += f'<rect x="{x}" y="52" width="{w-8}" height="12" fill="{col}"/>'
        s += f'<text x="{x+(w-8)/2}" y="55" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">{d}</text>'
        l1, l2 = txt.split("\\n")
        s += f'<text x="{x+(w-8)/2}" y="95" text-anchor="middle" font-size="10.5" fill="{INK}">{l1}</text>'
        s += f'<text x="{x+(w-8)/2}" y="110" text-anchor="middle" font-size="10.5" fill="{INK}">{l2}</text>'
        x += w
    svg = f'<svg viewBox="0 0 {x+10} 168">{s}</svg>'
    return viz(svg, "Days 1–3 understand · days 4–5 recall &amp; practice · days 6–7 consolidate. Ask NotebookLM to build your plan like this.",
               [(PEN, "understand"), (RED, "recall &amp; practice"), (GRN, "consolidate")])

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
  # 2 — why + objectives (merged)
  slide(
    eyebrow("Why &amp; what · visualize it"),
    h2("Where your study time goes"),
    viz_timesplit(),
    two(
      p("Searching, organizing, revising — that's where your hours go. "
        "AI does the slow parts fast. <b>Understanding is still your job.</b>"),
      tick([
        "Use <b>Gemini</b> for research, brainstorming, code &amp; images.",
        "Build a <b>NotebookLM</b> notebook from your own documents.",
        "Generate summaries, MCQs, flashcards &amp; a study plan — <b>cited</b>.",
        "Compile everything into one <b>submission-ready PDF</b>.",
      ]),
    ),
  ),
  # 3 — toolkit compare
  slide(
    eyebrow("The toolkit · visualize it"),
    h2("Two tools, two different jobs"),
    viz_compare(),
    muted("Gemini opens the whole world to you. NotebookLM locks onto YOUR documents so answers stay exam-safe."),
  ),
  # 4 — gemini prompts + anatomy
  slide(
    eyebrow("Gemini"),
    h2("Prompts you can steal today"),
    two(
      prompt("Suggest 10 mini-project ideas for a 2nd-year CSE student on machine "
             "learning. For each, list the dataset and difficulty level.", "brainstorm"),
      prompt("[attach chapter PDF] Explain the three hardest ideas in this chapter "
             "using everyday examples an 18-year-old would relate to.", "file upload"),
    ),
    viz_prompt_anatomy(),
    tags(["file upload", "coding help", "brainstorming", "image understanding"]),
  ),
  # 5 — notebooklm intro + workflow (merged)
  slide(
    eyebrow("NotebookLM · visualize it"),
    h2("Answers from YOUR documents only"),
    viz_notebooklm(),
    two(
      tick([
        "Give it PDFs, Docs, Slides, websites, YouTube links or pasted text.",
        "Every answer shows <b>where it came from</b> — click the citation to see the exact page.",
      ]),
      flash("<b>Safer for exams:</b> answers come only from what you uploaded — nothing made up. "
            "Free with your Google account, works in the browser."),
    ),
  ),
  # 6 — create notebook (real UI)
  slide(
    eyebrow("NotebookLM · inside the tool"),
    h2("Create your first notebook"),
    two(
      steps([
        "Go to <code>notebooklm.google.com</code> and sign in.",
        "Click <b>Create new</b>.",
        "Add sources — drag-and-drop, a URL, or Google Drive.",
        "Wait for NotebookLM to <b>index</b> your sources.",
        "Start chatting, or use one-click tools in the <b>Studio</b> panel.",
      ]),
      shot("nblm_upload.jpg", "notebooklm.google.com → your notebook",
           "The real thing — sources added, and you just ask: “Can you summarize…”") +
      flash("<b>Tips</b> · name it subject + unit (e.g. <i>DBMS – Unit 3</i>) · "
            "one notebook = one topic → sharper, better-cited answers."),
    ),
  ),
  # 7 — studio tools + document types (merged, real UI)
  slide(
    eyebrow("NotebookLM · inside the tool"),
    h2("One click, four study assets"),
    two(
      shot("nblm_studio.jpg", "notebooklm.google.com → Studio panel",
           "The real Studio buttons — Study guide, Briefing doc, FAQ, Timeline."),
      tick([
        "<b>Study guide</b> — key topics, terms &amp; short-answer questions.",
        "<b>FAQ</b> — likely questions, answered with citations.",
        "<b>Audio overview</b> — podcast-style revision on the go.",
        "<b>Briefing / notes</b> — summaries, timelines, mind maps.",
      ]),
    ),
    muted("Works on textbook PDFs, exported PPTs and research papers — mix them in one notebook "
          "and ask across all of them. Chat gives you more: flashcards, study plans, viva questions."),
  ),
  # 8 — cited answers (real UI)
  slide(
    eyebrow("NotebookLM · inside the tool"),
    h2("Ask your documents, get cited answers"),
    two(
      shot("nblm_citations.jpg", "notebooklm.google.com → chat",
           "A real grounded answer — the highlight links straight back to the source passage."),
      prompt("Define 'normalization' exactly as this document explains it, then give "
             "the example it uses.", "definition") +
      prompt("List anything in the syllabus PDF that is NOT covered in my class-notes "
             "PDF.", "gap finder"),
    ),
    flash("<b>Always click the citation</b> to check the passage before you memorise it. "
          "NotebookLM also tells you when it <i>cannot</i> find something — that's a real gap."),
  ),
  # 9 — activity + task 1 (merged)
  slide(
    eyebrow("Hands-on · Task 1"),
    h2("Activity — your Smart Study Companion"),
    viz_taskflow(),
    two(
      p("<b>Task 1 (~10 min):</b> pick ONE document (4–5+ pages) and upload it:") +
      tags(["branch syllabus", "AI article", "research paper", "college brochure", "class notes / slides"]),
      flash("📸 <b>Screenshot the uploaded source</b> inside NotebookLM right away — "
            "it's the first item in your submission. Then Task 2: ~45 min · Compile: ~15 min."),
    ),
  ),
  # 10 — task 2: the ten outputs
  slide(
    eyebrow("Hands-on · Task 2"),
    h2("Explore the document — generate these ten"),
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
  # 11 — what good outputs look like (drawn)
  slide(
    eyebrow("Hands-on · visualize the outputs"),
    h2("What “good” looks like"),
    viz_samples(),
    viz_week(),
  ),
  # 12 — where each output comes from (real UI)
  slide(
    eyebrow("Hands-on · Task 2 in the tool"),
    h2("Where each output comes from"),
    '<div class="cards c3">'
    + shot("nblm_studio.jpg", "Studio panel",
           "Outputs 1, 6, 8 — summary, revision notes &amp; learning outcomes start from Study guide / Briefing doc.")
    + shot("nblm_citations.jpg", "chat with citations",
           "Outputs 2–5, 7 — concepts, simplified terms, MCQs, flashcards &amp; viva questions: ask in chat, verify the citations.")
    + shot("nblm_audio.jpg", "Audio overview",
           "Outputs 9–10 — generate the mind map in Studio; use the Audio overview while following your 7-day plan.")
    + '</div>',
    muted("Real NotebookLM screens — Studio for one-click assets, chat for everything custom, audio for revision on the go."),
  ),
  # 13 — submission
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
  # 14 — wrap
  slide(
    handoff("Every document you own is now a study companion.",
            "Recap — Gemini for open-world help · NotebookLM for grounded mastery · "
            "one PDF with all 11 items. Verify citations, rewrite in your own words, "
            "never submit what you haven't read.",
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
