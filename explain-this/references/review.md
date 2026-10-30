# The three passes before publishing

Step 8 of `SKILL.md` runs these **after** `scripts/audit-page.py` exits clean.
The audit is objective; these are not, which is why each one below names the
trap it has — the thing that is obvious once said and invisible otherwise.

## Contents

- The cut pass — what to remove, and the short lines it strands
- The jargon pass — seven checks, starting with the subject's own name
- The render pass — what only shows on screen

### The cut pass

Read the page back with the spine sentence in mind and cut what does not serve
it. Step 3 said this, but by now every paragraph feels earned, so it takes a
second deliberate look.

- The usual casualty is the fact that is true, verified, interesting — and
  beside the point. It cost you a tool call, which is exactly why you want to
  keep it. Cut it anyway.
- A section that would survive being moved to a page about another subject was
  never about this one.
- Shorter is not the goal. Removing the one aside that competes with the spine
  is worth more than trimming ten sentences.
- **Then read the short lines, not the long ones.** This pass removes words,
  so it is also the pass that strands a line halfway: a card, a step or a
  table cell that names a thing and never says what it does. Step 6's "and
  so?" test applies here, line by line, on everything short enough to have
  escaped the cut.

### The jargon pass

The audit prints a candidate list — proper nouns, filenames and backticked
tokens, with the line of their first occurrence. For each: was it defined
there? Sit in the seat of someone who has never heard it.

| Check | The trap |
| --- | --- |
| **The subject's own name, first** | It is in the title, so it *feels* defined. A title names a thing; it never says what it **is** — a package the apps embed, a scheduled workflow, a file read at boot. You will skip this one every time, and it costs the reader the whole page |
| **The example you chose is a term you introduced** | Pulling a real class out of the repo makes its name a proper noun on your page. `AbstractAccessControlGuard` needs half a sentence before use — a class the framework runs before the controller, which lets the request through or refuses it |
| **Every path anchored to its repo** | `CLAUDE.md` at the root — of *what*? Where several repos are in play, group by repo so the location is the heading, not a column the reader carries in their head |
| **Two names for one thing** | A bug, not a style issue. Pick one |
| **The words you invented** | Fine when the thing has no name, and then introduced as yours. Not fine when it has one. Never fine when the coinage **collides** with a domain term — numbering paths "route A / route B" on a frontend page spends attention on a word that already means a react-router route |
| **Vocabulary imported from the last page you wrote** | A word that was the source material's own on one subject is an invention on the next |
| **People and examples the page has not established** | "Your colleague won't see it" invents a character to carry a point the facts already carry: say it is stored in your browser |

Gloss in place, in an aside. A glossary at the end is never read at the moment
it is needed.

### The render pass

Open the published page and look at it. Mermaid failures, overlapping labels
and stripped markup are invisible in the source and obvious on screen. Never
tell the user a page is done without having looked at it.

Diagrams need a second look even when they render cleanly, because the
renderer lays them out and you did not: arrows that cross, a diagram taller
than the screen, a label sitting on a line. The usual fix is the source, not
the layout — declare the nodes in reading order, or switch `TD` and `LR` — and
it takes one republish to see.
