# The house style — blocks and when to use them

`page-shell.html` is everything that goes **above** `<div class="wrap">`: the
title, the font links and the whole stylesheet. Copy it verbatim into every
page of this series, change only the `<title>`, then write the body inside
`<div class="wrap">…</div>`.

Do not invent a new palette per subject. The identity of these pages is the
**series**, not the topic — a reader should recognise one at a glance, the way
they recognise a runbook. This instruction overrides `artifact-design`'s
default of designing a fresh visual identity for each page; that skill's own
first rule is to apply an existing design system when there is one, and this
is one.

## Contents

- **Page skeleton** — the wrap, the entry block, the closing timeline
- **Blocks** — asides, tables, code, the `.legend` and its chips
- **The visual blocks** — reach for these before a diagram:
  `.concepts`, `.chain`, `.twocase`, `.anatomy`, `.timeline`, and a hand-built
  figure in plain HTML
- **Mermaid — how to draw one that reads** — eleven numbered rules. Rules 1 to
  9 are about mermaid; **rules 10 (one abstraction level, never static beside
  runtime) and 11 (the legend answers three questions) govern any diagram**,
  including the blocks above
- **Mermaid colours** — the palette, and the one-meaning-per-page rule

Two words used throughout, the same as in `SKILL.md`: a **block** is one of
the house HTML components; a **diagram** is anything drawn, mermaid or
hand-built.

## Page skeleton

```html
<div class="wrap">
  <header style="display:flex;flex-direction:column;gap:10px">
    <span class="eyebrow">Référence d'équipe · SUJET</span>
    <h1>…</h1>
    <p class="lead">Une phrase qui dit ce que le lecteur saura après.</p>
    <nav aria-label="Sommaire"><ul>
      <li><a href="#id">1. Titre de section</a></li>
    </ul></nav>
  </header>

  <section aria-label="Résumé">
    <div class="tldr">…</div>
  </section>

  <section id="id">
    <span class="eyebrow">1</span>
    <h2>…</h2>
    …
  </section>
</div>
```

Sections are numbered with a bare digit in `.eyebrow`, and the nav repeats the
numbers. Renumber both together when you insert a section.

## Blocks

| Block | What it is for |
| --- | --- |
| `.tldr` | The four cards under the title. `<strong>` headline, then one or two sentences, never more than four. What goes in them is an editorial call the skill makes (step 5, "open with an entry block"). |
| `.lead` | The one-sentence promise under the `h1`. |
| `.eyebrow` | The small caps label. Carries the section number, or a category word above a heading. |
| `.diagram` | Wraps a `<pre class="mermaid">`. Gives it a card, a border and horizontal scroll. |
| `.table-wrap` | **Always** wrap a `<table>` in one. It is what stops a wide table from widening the page on a phone. |
| `.note` | The amber aside: a caveat, a trap, a "what this means in practice". |
| `.note.ok` | Green: a correction of a common mistaken belief, or good news. |
| `.note.ko` | Red: something genuinely broken or a measured gap. |
| `.steps` | A tight `<ol>` or `<ul>` where the items are real steps or real alternatives. |
| `.layer` | The two-column label/description strip. For a short ordered taxonomy (three levels, three phases) where each entry has a name and a paragraph. |
| `.verdict` | A grid of 2–3 cards for options being weighed, or "what to do first". Use `.small` on the paragraphs inside. |
| `.gap` | A card with a red left border and a `<dl>` inside. For a catalogue of findings, each with the same fields (où / effet / correctif). Keeps them comparable. |
| `.catalogue` | A monospace block that reproduces real output verbatim — a log line, a listing. Use `.good` / `.bad` spans to mark lines inside it. |
| `.legend` + `.chip` | A colour key above a diagram. `.c-mono` `.c-pkg` `.c-api` match the three `classDef` colours below. |
| `.num` | On a `<strong>` holding a figure, so digits line up and read as data. |

## The visual blocks — reach for these before a diagram

These are the workhorses. They are plain HTML, so they can take the exact shape
of the content, which a generic flowchart never can. **Most of what an
explainer needs is one of these, not a mermaid diagram.**

### `.concepts` — 2 to 4 notions, posed at once

```html
<div class="concepts">
  <div class="concept"><span class="ico">🏠</span><h4>Host</h4>
    <p>Charge et affiche les remotes. Ici : le monolithe.</p></div>
  <div class="concept">…</div>
</div>
```

An icon, a two-word title, two lines. Replaces the paragraph that defines three
terms in a row — a reader can point at one.

### `.chain` — who calls whom, and why it goes one level down

```html
<div class="chain">
  <div class="chain-node"><span class="who">Monolithe · BMSApp.tsx</span>Le routeur</div>
  <div class="chain-arrow">▼ délègue le reste de l'URL</div>
  <div class="chain-node accent"><span class="who">pro-frontend</span>Le shell des onglets</div>
</div>
```

`.who` is the actor in monospace, the rest is what it does. **The arrow carries
the reason**, not just a direction. Variants `.accent` `.ok` `.ko` on a node.

**Not for a flow that crosses systems.** A `.chain` is a single column: it can
name an actor per node, but it cannot group them, so three services and one
service look identical. The moment two or more systems are involved, the
reader's first question is which box belongs to whom, and that is a flowchart
with a `subgraph` per system and the page's colour code (rules 1 and 4).
Keep `.chain` for a sequence inside one system, or where the actor is not the
information — the reason in each arrow is then what the block is for.

### `.twocase` — two cases side by side

Before / after, two paths that diverge, the broken version and the fixed one.
`.case.ko` and `.case.ok` give the red and green borders; `.case-tag` is the
label at the top. The point is that the difference is **seen**, not described.

### `.anatomy` — cut a real string into labelled segments

For a URL, an identifier, a version, a file path. The segments in `.segs`
(`.seg.s1` `.s2` `.s3`), then `.legend-rows` underneath with a coloured `.dot`
per segment saying what it is and where it comes from. Nothing else explains a
URL this fast.

For a step-by-step resolution (how `../x` resolves, how a version is picked),
use `.catalogue` with one line per step.

### `.timeline` — a numbered sequence with a rail

```html
<div class="timeline">
  <div class="tl-step"><div class="tl-dot">1</div>
    <div class="tl-body"><h4>Publier</h4><p>…</p></div></div>
</div>
```

For a real sequence, and for the **final recap** — "the N key ideas" — which is
what people re-read three weeks later. `.tl-dot.ko` for a step that is the bug.

### A one-off figure in plain HTML

When none of the blocks above fits and mermaid would make grey rectangles,
**build the figure by hand** — nested `<div>`s with the shell's own tokens
(`--surface`, `--line`, `--accent`, `--pkg`, `--api`), or an inline `<svg>`.
This is the right answer for the diagrams mermaid is worst at: something
*containing* something else (a module holding its providers, a topic holding
its partitions), a before/after of one structure, anything where position on
the page carries meaning.

Keep it to the page's palette and type scale, give it the same legend any
other diagram gets (rule 11 below), and keep it under about forty lines —
past that, it is a drawing you will not be able to change later. Mark it with
`class="diagram"` so it sits in the same card as the rest.

## Mermaid — how to draw one that reads

A mermaid diagram is rarely the right block (see the skill's steps 6 and 7).
When you do draw one, these eleven rules are what separate a readable diagram
from the grey-rectangle soup people skip.

Rules 1 to 9 are mermaid mechanics. **Rules 10 and 11 govern any diagram on
the page** — a `.chain`, a `.twocase` and an `.anatomy` each carry an
abstraction level and an implicit legend too, and they fail the same way.

**1. Group with `subgraph`, one per system or repo.** This is the single
biggest gain. The reader sees the boundaries first, the contents second.

```
subgraph MONO["Monolithe"]
  PAGE["La page du praticien"]
  LOADER["patient_health"]
end
subgraph MDP["MDP"]
  EHR["pro-ehr"]
end
```

**2. A group's name is not also a node inside it, and its members are
peers.** Two defects appear the moment you add a `subgraph`, and both survive
a proofread because the diagram still looks fine:

- *The duplicated container.* You drew a node for the system, then wrapped it
  in a subgraph of the same name — `subgraph MONO["Monolithe"]` containing a
  box called "the host application", when the monolith **is** the host
  application. Adding a container means re-reading the nodes you already drew
  and deleting the one it replaces.
- *The false sibling.* Everything inside a group reads as being at the same
  level. If one of your nodes contains the others, it is the group, not a
  member of it.

**3. Every arrow on a diagram means the same thing, and the label says which
one.** Mixing "calls", "contributes to" and "is served by" under one arrow
shape is why a diagram feels vaguely wrong without the reader being able to
say why. Pick the single relation the diagram is about — usually *loads*,
*calls*, or *writes to* — and if a piece of the diagram needs a different
relation, it belongs in a second diagram or in the prose.

**4. Colour means one thing per page, declared once and reused on every
diagram.** Usually that one thing is the system or the repository a box
belongs to; it can be something else — the deterministic machinery against
what a model does, say — as long as the whole page uses the same code. Put a
`.legend` of `.chip`s above the first diagram saying what it is, and keep the
`classDef` lines identical across diagrams. A reader learns the code once and
reads every later diagram for free. (Rule 11 is the test this must pass.)

**5. Number the edges, and mirror them in an ordered list underneath.**
`A -- "1. sauvegarde" --> B`. The numbers give a reading order; the list
carries the detail the boxes cannot hold.

**6. One short line per label — never `<br/>`.** It is stripped by the
renderer and the words end up glued: `ModalevaccinationVaccineInjectionModal`.
This is the most common defect in diagrams that otherwise look fine, and it is
invisible in the source. So the box gets the **human name only**; the file
path and the code identifier go in the ordered list below it.

**7. Let the shape say what the thing is.** `[( )]` for a datastore or a
database, `([ ])` for what the user sees, `{ }` for a decision, plain `[ ]`
for everything else.

**8. Eight nodes maximum.** The renderer scales a wide diagram down to fit,
so a big one arrives as unreadable small text. Two diagrams of six nodes beat
one of twelve.

**9. A sequence over time is a `sequenceDiagram`, not a flowchart.** With
`autonumber`, and `actor` for the human. Use a flowchart for topology — who
sits where — and a sequence for what happens in what order.

The trap is reaching for a sequence because the mechanism *happens* in an
order, when the claim is really about where things sit. Two tests, and
failing either means you want a flowchart:

- **Every participant must be something that acts.** A config file, a list,
  a manifest does not send messages. If one of your participants is a passive
  artifact, the diagram is about provenance, not conversation.
- **Every message must be a real call you can point at.** The moment you
  write a label like "what do you provide?", you are inventing dialogue to
  fill a lifeline, and the reader learns a conversation that never happens.

A sequence also spreads its participants across the full width, so arrows
travel far and cross each other. A flowchart with `subgraph`s per system says
the same thing in a quarter of the space — and it can group by repository,
which a lifeline cannot.

**10. One abstraction level per diagram, and never static beside runtime.**
The mistake that makes a diagram feel wrong without the reader being able to
name it, and the one that survives every proofread.

- *Static* is what exists in a checkout: repositories, packages, folders,
  classes, types.
- *Runtime* is what exists only once the thing runs: a process, a container,
  an injector, a connection pool, a request.

Put a runtime actor beside three repositories and the reader asks where it
lives — and there is no answer, because it lives in none of them. Split the
diagram in two, or keep the runtime half in prose. The same goes for mixing a
repository with a class, or a service with a function: pick the altitude the
claim needs and hold it for every box.

**A framework or a language is not a place.** NestJS, Rails and Spring do not
sit next to your repositories — they are what the code is written *with*,
everywhere at once. A box or a colour for one puts a technology on the same
footing as a location, which is how a legend ends up mixing "where the code
lives" with "what it is built on". Name the framework in the prose; keep the
diagram to things that have an address.

**11. The legend answers three questions, or the diagram is not ready.** What
is a box? What does an arrow mean? What does a colour mean? Write the three
lines out; if one of them will not come in a short sentence, the diagram is
still confused and no amount of layout will fix it.

- A dependency arrow must say which way it points — dependant towards
  dependency, or the reverse. Both conventions exist, and a reader cannot
  guess yours.
- Every box connects to something. An isolated box means the diagram is
  incomplete, or that the box belongs to another diagram.
- Few colours, each meaning one kind of thing. Two locations and a framework
  under three chips is not a colour code, it is two codes sharing a row.

(Rules 10 and 11 come from the checklists in InfoQ's *Crafting Architectural
Diagrams* and ProcessOn's guide to technical architecture diagrams, which
name both defects explicitly.)

## Mermaid colours

Every diagram uses the same three `classDef` lines, so colours mean the same
thing across the whole page and across pages:

```
classDef mono fill:#dbe4f5,stroke:#4a5d8f,color:#1c222b
classDef pkg  fill:#d7f0e4,stroke:#2f8a63,color:#1c222b
classDef api  fill:#ffe8cc,stroke:#c98024,color:#1c222b
```

Pick one meaning per page and state it in a `.legend` when a diagram has more
than one family. In a page about an automated system, a useful convention is:
blue for the deterministic machinery, green for what a model does, amber for
what a human writes. For a red "this is broken / dead end" node, add
`classDef bad fill:#fdeaea,stroke:#d06b6b,color:#1c222b`.

The colours are hard-coded in the diagrams rather than taken from the CSS
tokens, because the mermaid runtime renders before the page's variables
resolve. They are chosen to stay legible on the dark background too.

**Never put `<br/>` in a label.** It is stripped, and the words on either side
end up glued together.
