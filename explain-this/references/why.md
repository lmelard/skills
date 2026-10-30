# What went wrong, and the rule it produced

Every rule in `SKILL.md` was paid for by a page that failed. This file is that
log — one row per incident, the rule it produced, and the evidence behind any
number the rule names.

**Read it before you change or delete a rule**, never while applying one. A
rule whose cost you cannot see looks arbitrary and gets dropped, and the same
page fails again. If you are looking for *how* to do something, it is in
`SKILL.md`; nothing here repeats it.

## The log

| What happened | The rule it produced |
| --- | --- |
| A page described a mechanism correctly and never said the house recommends cohorts, nor that the organisation is moving to feature flags — both facts were in files already open that session | Step 5's question 7, and step 2's four-source table for direction |
| On that same page, the 1751 cohort-less switches were nearly reported as the legacy backlog. The legacy was two entirely different files | Step 2: **a deprecation in progress looks exactly like healthy code**, and the legacy form is usually the majority of what you count |
| A section ran to sixteen paragraphs with no table — written within the hour of the table rule being added, by the author who had just written it | Step 6: apply the budget **as you close each section**, not at the end. Step 8's audit is the safety net, not the method |
| "The table is half migrated" was on a page; the reader could not picture it and said it deserved an example | Step 6: a state the reader cannot picture needs one real instance — the script that produces it, rows as they look, the arithmetic for how long it lasts |
| A sequence diagram had a passive participant and invented dialogue. "Ton schéma n'est pas clair du tout" | Rule 9's two tests in `components.md`: every participant must act, every message must be a real call |
| A diagram mixed a framework with the repos using it. "NestJS est dans MDP, ton découpage est faux et incompréhensible" | Rule 10: one abstraction level per diagram, never static beside runtime, and a framework is not a place |
| A legend chip named a colour that appeared nowhere in the diagram | Rule 11: the legend answers three questions, or the diagram is not ready |
| A diagram rendered with crossing arrows from `LR` nesting | The render pass: fix the source — node order, `TD` versus `LR` — not the layout |
| A multi-service flow was drawn as a `.chain`, so the services became invisible | Step 6: **name the systems before picking a block.** See below |
| An ad-hoc counting script reported four false empty sections, because it did not count `.tldr` as a visual | `scripts/audit-page.py` exists, and step 8 says to run it rather than write one |
| A page's prose was compressed until lines named a thing without saying what it did. "Parfois à vouloir trop synthétiser on perd en compréhension" | Step 6: short is not compressed — the claim, then its consequence, asked with "and so?" |

## The two numbers, and where they come from

**The paragraph budget was measured, not chosen.** Across the first four pages
of this series, the sections that read badly were **not** the ones without
visuals — they were the ones at **ten to twenty-five paragraphs *with*
visuals**. The ones that read well sat between **two and nine**. Eight is the
line between those two groups.

That is why the budget is phrased as it is: having a diagram feels like having
done the work, so a section that already has one stops being audited. The
failure is additive — a diagram, then a paragraph of nuance, then a caveat,
then a second example. Each addition is reasonable; none of them is the moment
anyone decided to write an essay.

**Errors cluster in diagrams rather than prose**, for three reasons that
compound:

| Reason | Consequence |
| --- | --- |
| A box and an arrow *look* like drawing | They escape the scrutiny a sentence gets, while being the claims a reader trusts most |
| A diagram needs more facts per square centimetre | Prose can say "the monolith loads some modules"; a diagram must say which, from where, in which order |
| You draw it after the investigation | From memory, at the point where you are most confident and least checked |

Which is why step 7 asks for the box-and-arrow list, with a file beside each
line, *before* any mermaid — rather than treating step 2's facts as enough.

## The one rule whose failure is invisible

`.chain` deserves its own note, because the bug was in the routing and not in
the block.

Step 6's table originally chose on the **shape** of the content: "who calls
whom, level by level" sent you to `.chain`. A flow is a flow whether it
touches one service or four, so every multi-service flow landed there — and
`.chain` is a single column. It can name an actor per node, but it cannot
group them, so three services and one service look identical. The rules about
`subgraph` per system and one colour per system existed, but only inside the
mermaid section, so they never fired: the table never routed anything to
mermaid.

The fix put *how many systems does this touch* **before** the shape question.
The tell that the old failure is happening: the actor slots of a `.chain` hold
moments rather than actors — "at page load", "if it arrives in time". Timing
is what the arrows are for. When the nodes have nothing but timing to put in
the actor slot, the actors were never in the diagram.

## Sources

Rules 10 and 11 of `components.md` come from two articles the user supplied:
InfoQ's *Crafting Architectural Diagrams*, and ProcessOn's guide to technical
architecture diagrams. Both name these exact mistakes.
