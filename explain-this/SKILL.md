---
name: explain-this
description: Build a published explainer page that teaches how something works — a tool, a system, an unfamiliar area of the codebase, or the context around a ticket. Use when the user says "explain how X works", "I don't understand X", "make me a page about X", "contextualise this ticket", "I need to understand this before I can improve it", or asks for a doc their team could read. Also use to audit or fix an explainer page that already exists.
---

# Explain this

Produce a page that makes a cold reader understand a mechanism they would
otherwise have to assemble from scattered code, docs and tribal knowledge.

Publish it as an Artifact. Write it in the language the user is speaking.

**Two words, used consistently below.** A **block** is a house-style HTML
component — `.concepts`, `.chain`, `.twocase`, `.anatomy`, `.timeline`,
`.catalogue`. A **diagram** is anything drawn: mermaid, or a figure you build
by hand. Both beat a paragraph, and step 6 routes between them.

Copy this checklist and tick it off as you go:

```
- [ ] 1  House style copied from references/page-shell.html, nothing invented
- [ ] 2  Every number and path printed is one I opened this session
- [ ] 3  Spine sentence stated, unhedged
- [ ] 4  Prerequisites asked in one AskUserQuestion
- [ ] 5  Sections derived from the subject, questions 1-7 answered
- [ ] 6  Blocks and tables built section by section, not prose converted later
- [ ] 7  At least one diagram of the mechanism, not only of the map
- [ ] 8  audit-page.py clean, then cut / jargon / render, then publish
```

**Bundled files, all one level from here:**

| File | When to read it |
| --- | --- |
| `references/page-shell.html` | Step 1 — copy verbatim, it is the whole stylesheet |
| `references/components.md` | Before writing the body — the blocks, and the eleven diagram rules |
| `references/why.md` | A log of what went wrong and the rule it produced — read it before changing or deleting a rule, not while applying one |
| `scripts/audit-page.py` | Step 8 — run it, do not reimplement it |
| `evaluations/` | When you change this skill, to check nothing regressed |

## Who you are writing for

**A competent engineer who is junior on architecture and infrastructure, who
is discovering this subject today, and who will share the page with their
team.** Everything below follows from that one sentence, so when a choice is
unclear, decide it from here.

They are fluent in code: do not explain the language, the framework, or how to
read a config file. What they have not built is the mental model *around* the
code — where it runs, what is deployed when, who calls whom across repos, what
a registry or a bundle is **in this organisation**. That is why step 4's
prerequisites are nearly always infrastructure concepts, not language ones.

| What is true of them | What it forces on the page |
| --- | --- |
| They do not know why the thing exists | Answer the problem before the mechanism — they have no slot to put it in |
| They do not know the vocabulary, the subject's own name included | Gloss at first use, starting with the title's own noun |
| They scan before they read | A wall of correct prose reads as "not for me"; a structure reads as an explanation |
| They will not act on the page today | Describe the terrain, not the tasks — a to-do list makes them decide before they understand |
| They will forward it to someone else | Anything that only makes sense because *you* investigated does not survive that forward |

The failure this guards against is not being wrong. It is **being correct and
unusable**: a page written from the code, for someone who already accepts the
premise, that answers "how" without ever answering "why" or "when".

## 1 — The house style. Do not invent one.

These pages are a series, and a reader should recognise one at a glance.

- Copy `references/page-shell.html` **verbatim** into the new page. It is the
  title, the fonts and the whole stylesheet — everything above
  `<div class="wrap">`. Change only the `<title>`.
- Read `references/components.md` before writing the body: the blocks that do
  most of the work, the asides and tables around them, and the eleven rules
  for a diagram that reads — nine for mermaid, two for any diagram at all.
- You do **not** need `artifact-design` here: its job is to invent a visual
  identity, and this one exists. Its own first rule is to apply an existing
  design system when there is one. Load it only if the user asks for a
  different look.

If the user points at an existing page as the model, read it (`Artifact`,
`action: "read"`) and take the shell from there — their reference wins.

## 2 — Establish the facts. Do not write from memory.

Every claim must be something you verified **in this session**. That is the
whole value of the page: a teammate can act on it without re-checking.

- Read the actual files. Not the docs about the files — the files.
- Count with a command, and let the numbers be yours. They are the spine of a
  good explainer.
- When a count uses a loose method (a grep matching anywhere in a file), say
  so in the page and call the figure a ceiling.
- Docs drift from code. The code wins, and **the divergence is itself a
  finding** worth a line.

**Except for direction, where the code is the weakest source.** How a thing
works is in the code. Whether it is the recommended way, a legacy form, or
something being replaced is a *decision*, and decisions live in prose. The
trap: **a deprecation in progress looks exactly like healthy code**, and the
legacy form is usually the majority of what you count — so reading only the
code makes you describe the backlog as the normal case.

Four places state direction, and all four are findable:

| Where | What it tells you |
| --- | --- |
| A `migrate-X-to-Y` skill or command | The house has chosen Y. Its own wording — "the modern X", "legacy Y" — is quotable. |
| `.claude/rules/`, ADRs, a root `CLAUDE.md` | The rule nobody wants repeated in review, often with the reason. |
| Lint rules, deprecation cops, tracked metrics | Someone is counting the old form down. What is counted is what is being removed. |
| A newer package or service doing the same job | The successor, already wired in somewhere — grep for its name, not only the subject's. |

Read them as evidence, not as tooling: a migration skill is a sentence saying
where the thing is going, written by the people who decided it. When none of
the four says anything, say so on the page — "nothing in the repo states a
direction" is actionable, and silence reads as "this is stable".

**Three mistakes to expect**, because they recur:

| Mistake | What it actually means |
| --- | --- |
| Asserting an absence — "this tool doesn't have X" | You have not found how X arrives |
| Taking a mechanism's name at face value | You have not opened it |
| Finding one path and stopping | Systems keep the old route alive beside the new one behind a switch, and the one you found first is as often the legacy. When its code sits in a repo you do not have, say so on the page rather than completing the picture by inference |

When you find you were wrong, fix the page and tell the user in one sentence.

**When to stop.** Investigating has no natural end, so set one. You are done
when all three hold:

- you can state the spine sentence of step 3 without hedging it;
- every number and file path you intend to print is one you opened;
- **for every mechanism the page names, you opened it** — and can say how it
  starts, how it moves, and **how it is undone**.

The third exists because the first two fire without it and feel sufficient;
the undo path is the blind spot every time, and a filename is a claim about a
file, not the file. If the spine sentence will not come after a dozen or so
calls, say so rather than writing around the gap: either the subject is two
subjects, or it has no organising idea — which is itself the finding.

## 3 — Find the spine before writing

A good explainer has **one idea that makes everything else obvious**. Find it
before you write a line. The test: you can state it in one sentence that
corrects what the reader currently believes.

- "The skill isn't missing — it's not *selected*."
- "A route never says where to find the thing, only where its *name* comes from."
- "Nothing runs on your machine."

Everything in the page either sets up that sentence or follows from it. If a
section does neither, cut it.

## 4 — Ask what the reader already knows

A page leans on concepts that are **not** its subject: IndexedDB, a Service
Worker, a semver range, a cron, a reverse proxy. Each one left unglossed is a
place the reader stops; each one glossed needlessly is noise. You cannot guess
which is which — so ask.

Once the facts are in and before writing, put the background concepts to the
user in **one** `AskUserQuestion`, multi-select, phrased as "which of these
should I define?". Keep it to the three to five that carry weight. Do not ask
about the subject itself (you define that unconditionally) or about what any
engineer uses daily.

A concept they skip is used without ceremony. If no answer comes, gloss in one
line anyway: a superfluous gloss costs a sentence, a missing one costs the
section.

A concept they pick gets a gloss **at its first use**, sized to the concept —
never a glossary at the end, never a general tour. Two sizes, and picking the
wrong one is the usual mistake:

| Kind | Example | What it gets |
| --- | --- | --- |
| A term that only needs naming | a registry, a cron, a semver range | One or two sentences in an aside, then move on |
| A notion the reader must hold a model of | a framework, an execution model, a protocol | Its own passage, in the five steps below |

**The test is not how famous the term is, it is how much of the page leans on
it.** When the answer is "everything after this paragraph", it is the second
kind — treat it as a short section of its own, and say so in the aside that
introduces it, so the reader knows an explanation is coming.

The five steps of a model-sized gloss, which are step 5's questions in
miniature:

1. *the problem it solves* — what you would do without it, concretely;
2. *what it is* — the category and the one-sentence idea;
3. *how it works, in the abstract* — **a diagram of the thing itself**, naming
   its own parts, with no repo in it;
4. *the same thing in this repo* — the real code, read as an instance of that
   diagram;
5. *what it changes for the subject of the page* — the sentence that earns the
   detour.

Three of the five go wrong, always the same three:

| Failure | Why it matters |
| --- | --- |
| **1 and 5 get skipped** | They separate an explanation from a definition. NestJS is not "a Node framework" — it is *you declare, the framework assembles*, and that only lands after you have said what wiring everything by hand costs |
| **3 and 4 get inverted** | Repo code is an *instance*, and only teaches once the reader holds the shape it instantiates. Three declarations lifted from a service show that something is declared, never what a module, a class and a constructor are to each other |

And **keep it to a quarter of the page**. A prerequisite longer than what it
supports has become the page; if it will not fit, the notion deserves a page
of its own, linked from this one.

## 5 — Let the subject decide the sections

**There is no template, and reaching for one is the failure mode.** Sections
that appear because the form has them, not because the subject does, show:
"three words not to confuse" is excellent when three words genuinely collide,
and filler when they don't.

Derive the sections from the concept. Name the thing, then its sub-concepts in
the order they nest, and give each its own block with the least prose you can
manage. **The test for a section is "the reader cannot follow the next one
without it"**, never "the previous page had one".

The page must answer these, in this order — it is the order a newcomer asks
them in:

| | Question | The trap |
| --- | --- | --- |
| 1 | **Why does this exist?** What was painful before it, concretely | The code shows the answer and never the problem, so a page written from the code always loses this one |
| 2 | **When would I reach for it?** | Two or three *named* situations — "I'm in the monolith and don't want to boot the other backends", not "it improves the developer experience" |
| 3 | **What is this thing?** A package, a service, a cron, a file, a convention | You will skip it because the title names it — see the jargon pass |
| 4 | **How does it work, briefly and in diagrams?** | Enough to predict its behaviour, not a tour of the source: one or two decision points, shown rather than narrated |
| 5 | How do you drive it, see its state, and undo it? | The undo half is the one that gets dropped |
| 6 | Who owns it, and what is mine to change? | |
| 7 | **Is this the way we do it now?** | Least likely to be in the code (step 2), most likely to be the first thing a colleague would have said. Without it, the reader builds on the variant being migrated away from |

Questions 1 and 2 come **before** 3 and 4. A page that opens with the
mechanism is written for someone who already decided they care.

Only two fixed points:

- **Open with an entry block.** Four `.tldr` cards that work for someone who
  knows nothing: no term the page has not yet defined, no claim that needs the
  rest of the page. They answer *what is this and why would I care*, not *what
  did I just learn*. **The entry block is not the recap moved to the top** —
  that mistake makes the first screen the least readable one; a card that
  would make a good closing line belongs at the end. And **each card stands
  alone**: a grid is not read in order, so no card may lean on another.
- **Close with "the N key ideas"** on a `.timeline`. N is whatever the subject
  has, usually four to six. This is the block people re-read weeks later, and
  the only one whose place never depends on the content.

Everything between those two is the subject's own shape.

## 6 — Blocks and tables, not paragraphs

**Prose is the fallback, not the default.** For every thing you explain, the
first question is which structure shows it; a paragraph is what you write when
the answer is "none". Writing prose first and converting later is how a page
ends up correct and unread — the conversion never happens, because by then the
sentences exist and feel finished.

**Every section carries something that is not a paragraph.** A well-built page
runs roughly one diagram and one table per section: a lead sentence, the
structure, the detail list under it, an aside for the trap.

### Which structure

**A mermaid diagram is rarely the right one.** It draws a branch and a loop;
for everything else it makes grey rectangles joined by arrows, weaker than a
house block — or than a diagram you build by hand, which
`references/components.md` shows how to do.

| What you are explaining | What to build |
| --- | --- |
| 2 to 4 notions to pose at once | `.concepts` — cards with an icon and two lines |
| Who calls whom **inside one system** | `.chain` — nodes stacked, the reason in each arrow |
| Anything that **crosses two or more systems** | **A mermaid flowchart**, one `subgraph` per system, the page's colour code |
| Before / after, or two paths that diverge | `.twocase` — side by side, red and green |
| A real URL, identifier or path | `.anatomy` — coloured segments plus a legend |
| How something resolves, step by step | `.catalogue` — one line per step |
| A sequence, or the final recap | `.timeline` — numbered, with a rail |
| Any set of things with the same shape | **A table** — one row each |
| A field and what it triggers | A table |
| A genuine branch, or boxes that need grouping by repo | **A mermaid diagram** |
| A to B to C where the only content is the order | A sentence |

**Before picking, name the systems involved.** The table routes on the *shape*
of the content, and shape is the wrong criterion the moment more than one
service, repo or runtime is in play: a flow is still a flow, so it lands on
`.chain`, and the actors vanish. Ask first *how many distinct systems does
this touch?* Two or more, and the reader's first question is **which box is
whose** — which only a grouped, colour-coded diagram answers. One, and the
shape decides as usual.

> **The tell that you got this wrong:** the actor slots of your `.chain` hold
> moments rather than actors — "at page load", "if it arrives in time".
> Timing is what the arrows are for. When the nodes have nothing but timing to
> put in the actor slot, the actors were never in the diagram.

**The table row saves the most prose.** Identifiers, database tables, config
fields, files by layer, known limits, cases and what to do in each — anything
whose items share a shape is a table, and a real system has several. Written
as prose, each becomes a paragraph nobody can scan.

A linear chain is the most common shape and its three answers look
interchangeable. The criterion is **how much each step carries**:

| Each step has... | Build |
| --- | --- |
| An actor, a reason per arrow, sometimes a repo and a file path | `.chain` — more compact than mermaid, and it holds detail a mermaid box cannot |
| Grouping (boxes nested by repo or package), or a genuine branch | A mermaid flowchart |
| Nothing but its order | A sentence |

### The budget, and the signals that you broke it

Having a diagram does not protect a section: the sections that read worst
were the long ones *with* visuals, not the ones without
(`references/why.md`). The failure is additive, so nobody decides to make it.

| Signal | What it means | Fix |
| --- | --- | --- |
| A section past **~8 paragraphs** | Something with a shape was written as prose | Extract the table; the section usually splits in two along the way |
| A section with **no block or diagram at all** | It was written, not built | Rare that nothing had a shape — look again |
| **Two prose-only sections in a row** | The page drifted back to text | Stop and convert both |
| The page has **far fewer tables than sections** | Enumerations living in prose — the most common gap of all | The table row above, not trimming |
| A paragraph **over three sentences** | A block you have not built yet | Ask what shape it wants |
| A paragraph **explaining the block under it** | Dead weight | Delete it. One sentence of lead-in, one of conclusion where the point is not obvious, nothing between |

**Apply this as you close each section, not at the end.** Knowing a rule and
applying it to the paragraph in front of you are different acts, and the gap
between them is wide enough that this skill once shipped a sixteen-paragraph
section within the hour of adding the table rule (`references/why.md`). The
audit in step 8 is the safety net, not the method.

### The sentences that survive

One idea per sentence, the point first and the detail after.

| Cut without mercy | Never cut |
| --- | --- |
| Throat-clearing — "it is worth noting that", "as we have seen" | The clause that says *what it does* |
| Hedges that protect nothing | The clause that says *why it matters* |
| The subordinate clause added for rhythm | The one real instance that makes a state picturable |

**Short is not the same as compressed, and the second costs the reader.**
Cutting a hedge costs nothing; cutting the clause that says what it does turns
an explanation into a label. The shape that works is a claim, then its
consequence:

> **À moitié appliquée** — certaines lignes sont remplies, d'autres non. C'est
> l'état réel en production, et celui qui trouve les bugs.

> **Certaines modifications de schéma peuvent faire tomber le site** — elles
> bloquent une table pendant qu'elles s'exécutent, et les requêtes s'empilent
> derrière.

Neither is long. Both say what happens, not only what the thing is called.
**A reader who has to infer the consequence is reading a note you wrote for
yourself.** When a line states a fact and stops — a title, a card, a step on a
rail, a cell in a table — ask "and so?" once and put the answer in the same
breath. A synthesis pass destroys that clause first.

**A state the reader cannot picture needs one real instance.** "The table is
half migrated", "the cache is warm" are summaries, and a summary only lands
for someone who has already seen the thing. Give it a body: the script that
produces that state, rows as they really look, the arithmetic for how long it
lasts, the two lines of code that respectively break and survive it. Naming
the state costs a sentence; showing it costs a block, and is the difference
between agreeing with the page and being able to use it.

**Use an analogy only where the mechanism is genuinely unfamiliar**, one or
two per page, and only if it maps exactly. The moment you write "it's a bit
like", drop it.

## 7 — The diagrams

**Draw the mechanism, not only the map.** Count the diagrams: if they all
answer *where does this live* — which repo, which package, which host — the
page has a map and no explanation. Provenance is the easy one to draw, every
box being a path you can verify, so it is the one that gets made. The reader
more often needs *how the thing works*: what the parts are, which holds what,
what moves between them when it runs. Its boxes are concepts rather than
paths, which is why it costs more — and a page about a mechanism needs one.

**No repository belongs in that diagram** — its boxes are the thing's own
parts, in the thing's own vocabulary. The map, with its real paths, is a
second diagram. Step 4 says the same for a prerequisite, and in the same
order: the model first, the repo's code after it.

### A diagram is a set of claims — verify it separately

Step 2's facts are not enough: errors cluster in diagrams rather than prose,
and they are the claims a reader trusts most (`references/why.md` says why).

So before a single line of mermaid — or of a hand-built figure — **list every
box and every arrow, and write next to each the file that proves it.** A box
is a name you read; an arrow is a call site you can open. Any line with no
file gets verified now or leaves the diagram. That list is also, almost
always, the ordered list that goes underneath the finished diagram.

**Name real things, and source the label too.** "The host app", "a module", "a
backend" teaches nothing — a generic box cannot be checked. But a real name is
only half: taking it from a config file and describing it from what the name
suggests is the quiet failure (`pro-financial-os` "the billing one" is a guess
dressed as a fact). Find the call site — `loadModule('pro-ehr/PatientHealthPage')`
in one repo and the `exposes` block in another say what the thing *is*, and
give the reader two files to open. **Follow the chain across repos**: the
package in one, the module that bundles it in a second, the call site in a
third. Nobody can reconstruct that chain from a single checkout, which is what
makes it the most useful thing on the page.

### How many to draw

`references/components.md` holds the eleven rules that decide whether a
diagram reads at all — read them before drawing; rules 10 and 11 govern any
diagram, including the blocks of step 6. Three more live here, about how many:

| Rule | Why |
| --- | --- |
| **One diagram, one claim — a section may need several** | Two small diagrams, each with its own claim and list, read far better than one that mixes relations. Three that each say something beat one that says three things |
| **When an explanation grows, split the diagram — do not add prose** | The reflex is to shrink the picture and repair it in a paragraph. Do the opposite. This is what keeps rule 8's eight-node limit from quietly turning into more text |
| **Parallel subjects get parallel diagrams** | Create, update and delete get three diagrams of the same kind, same participants, same order. The reader then gets the second and third almost free, and the difference is the only thing left to see |

And when a diagram needs a paragraph under it to be understood, it has failed
— fix the diagram, not the caption. (The numbered list carrying file paths is
not that paragraph; it is part of the diagram.)

## 8 — Before you publish

### The audit loop

```bash
python3 ~/.claude/skills/explain-this/scripts/audit-page.py path/to/page.html
```

It reports, per section: paragraphs, blocks, diagrams and tables, then a
verdict against step 6's budget. It knows the house blocks and `.tldr` count
as structure, which a fresh regex never does — so run it, do not rewrite it.

1. Run it.
2. For every `FAIL`, apply the fix step 6 names for that signal. Do not argue
   with a count by re-reading the section — convert something.
3. Run it again.
4. **Only when it exits clean, run the three passes.** A `WARN` is a
   judgement call you may keep; say in the handover which ones you kept.

**`references/review.md` holds the three passes in full** — read it there, not
from memory: each has a trap that is obvious once named and invisible
otherwise.

| Pass | What it catches | The trap it has |
| --- | --- | --- |
| **Cut** | The verified, interesting fact that is beside the point | By now every paragraph feels earned |
| **Jargon** | Terms never defined at first use | The subject's own name, which the title makes *feel* defined |
| **Render** | Mermaid failures, crossing arrows, stripped markup | They are invisible in the source and obvious on screen |

Never tell the user a page is done without having looked at it on screen.

## When you hand the page over

**Say that it is private.** A published Artifact is visible to its owner and
nobody else until they share it from the page's own Share menu, which you
cannot do for them. The point of these pages is usually that a team reads
them, so a link handed over without that sentence quietly fails for everyone
else.

Tell the user what you verified and what you did not, and which audit `WARN`s
you chose to keep. A page whose claims come from files you opened is worth
more than one that merely sounds right, and they can only know which they are
holding if you say so.

**Then offer to go deeper on one or two named points.** You know where you
compressed: the prerequisite that got four lines, the mechanism summarised
because it was not the subject, the second path flagged as unverified. The
reader does not know those choices were made. Name two or three in one
`AskUserQuestion`, multi-select, as "which of these should I expand?" — never
"anything unclear?", which hands the work of finding the gap to someone who
has just met the subject.

What comes back gets the same treatment: facts verified this session, the
question order of step 5, a structure rather than paragraphs, the audit and
the three passes. An expansion is written into place, at its first use, not
appended — and the page is republished at the same URL.

## Reviewing a page that already exists

The skill works in reverse, and the user will ask for this — "what is still
unclear?", "which diagrams don't hold up?". Run `scripts/audit-page.py`, then
the three passes of `references/review.md`, then steps 6 and 7 as audits, and
**report before changing anything**:

- the audit's per-section verdict, with your reading of each `FAIL`;
- diagrams, one by one, against step 6's routing table, step 7, and the eleven
  rules in `references/components.md`, with a verdict each;
- terms used without a gloss, ranked by how much they block comprehension;
- anything framed as an action when the reader is still learning;
- claims you cannot trace back to a file you read.

Report first, apply after the user chooses. A page they didn't agree to is a
page they won't share.
