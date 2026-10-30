#!/usr/bin/env python3
"""Audit an explain-this page against step 6's budget.

Usage:  python3 audit-page.py page.html [--jargon]

Counts, per <h2> section: body paragraphs, house blocks, diagrams, tables.
Then applies the signals in step 6 of SKILL.md and prints a verdict each.

Why this exists rather than a fresh one-liner each time: the definition of
"a visual" is the part that gets it wrong. The entry block (.tldr) is a
visual. A <p> inside an aside is not a body paragraph. Both of those were
miscounted once, which is the whole reason this file is checked in.

Exit status: 0 when no section FAILs, 1 otherwise. WARNs do not fail the run;
they are judgement calls the author keeps or fixes deliberately.
"""

import html
import re
import sys
from collections import Counter

# A house block is structure: it shows something a paragraph would have
# narrated. Keep this list in sync with references/components.md.
BLOCK_CLASSES = {
    "tldr", "concepts", "concept", "chain", "twocase", "anatomy", "timeline",
    "catalogue", "gap", "layer", "verdict", "legend", "legend-rows", "steps",
    "table-wrap", "cards", "grid",
}
# A diagram is anything drawn, mermaid or hand-built.
DIAGRAM_CLASSES = {"mermaid", "diagram"}
# An aside carries a gloss or a trap. Its <p> is not body prose.
ASIDE_CLASSES = {"note", "ok", "ko", "good", "bad", "small", "lead", "eyebrow"}

# Step 6's budget. Measured across the first four pages of the series:
# sections that read badly sat at 10-25 paragraphs, ones that read well at
# 2-9. Eight is the line between "dense" and "an essay nobody asked for".
PARA_BUDGET = 8
# Tables per section. "Far fewer tables than sections" is the signal; below a
# third is not a judgement call, between a third and a half is one.
TABLE_RATIO_FAIL = 1 / 3
TABLE_RATIO_WARN = 0.5


def strip_comments(doc):
    return re.sub(r"<!--.*?-->", "", doc, flags=re.S)


def classes_of(tag_text):
    m = re.search(r'class="([^"]*)"', tag_text)
    return set(m.group(1).split()) if m else set()


def split_sections(body):
    """Return [(title, html)] split on <h2>. Text before the first <h2> is the
    entry block and is reported as a section so its visuals are counted."""
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", body, flags=re.S | re.I)
    sections, title, buf = [], "(entry block)", parts[0] if parts else ""
    for i in range(1, len(parts), 2):
        sections.append((title, buf))
        title = re.sub(r"<[^>]+>", "", parts[i]).strip()
        title = html.unescape(re.sub(r"\s+", " ", title))
        buf = parts[i + 1] if i + 1 < len(parts) else ""
    sections.append((title, buf))
    return sections


def drop_nested(frag, classes):
    """Remove every element carrying one of `classes`, with its full subtree.

    Hand-written pages nest <div> inside <div>; a non-greedy regex closes on
    the first </div> and leaves the block's own content behind to be counted
    as body prose. This tracks depth per tag name instead.
    """
    out, skip_tag, depth, pos = [], None, 0, 0
    for m in re.finditer(r"</?(\w+)([^>]*)>", frag):
        tag, closing = m.group(1), m.group(0).startswith("</")
        if skip_tag is None:
            if not closing and classes_of(m.group(0)) & classes:
                out.append(frag[pos:m.start()])
                skip_tag, depth = tag, 1
            continue
        if tag != skip_tag:
            continue
        if closing:
            depth -= 1
            if depth == 0:
                skip_tag, pos = None, m.end()
        elif not m.group(0).endswith("/>"):
            depth += 1
    if skip_tag is None:
        out.append(frag[pos:])
    return " ".join(out)


def count_section(sec):
    """Count what a reader sees, not what a regex finds."""
    # Blocks and diagrams, by the class on any element.
    blocks = diagrams = 0
    aside_spans = []
    for m in re.finditer(r"<(\w+)([^>]*)>", sec):
        cls = classes_of(m.group(0))
        if cls & DIAGRAM_CLASSES:
            diagrams += 1
        elif cls & BLOCK_CLASSES:
            blocks += 1
        if cls & ASIDE_CLASSES:
            aside_spans.append(m.start())
    diagrams += len(re.findall(r"<svg\b", sec, re.I))

    tables = len(re.findall(r"<table\b", sec, re.I))

    # Body paragraphs: a <p> that is not inside an aside, a block or a table.
    # Nesting matters here - a .timeline holds seven <p> that are block content,
    # not body prose - so this walks tags and tracks depth instead of using a
    # non-greedy regex, which stops at the first </div> of a nested block.
    stripped = drop_nested(sec, ASIDE_CLASSES | BLOCK_CLASSES | DIAGRAM_CLASSES)
    paras = [p for p in re.findall(r"<p\b[^>]*>(.*?)</p>", stripped, re.S)
             if len(re.sub(r"<[^>]+>", "", p).strip()) > 40]
    return len(paras), blocks, diagrams, tables


def verdict(paras, blocks, diagrams, tables, is_entry):
    """Returns (level, message). Mirrors step 6's signal table exactly."""
    if is_entry:
        return "OK", ""
    if paras > PARA_BUDGET:
        return "FAIL", (
            "%d paragraphs, budget is %d - something with a shape was written "
            "as prose. Extract the table; the section usually splits in two."
            % (paras, PARA_BUDGET))
    if blocks + diagrams + tables == 0:
        return "FAIL", (
            "no block, diagram or table - this section was written, not built. "
            "It is rare that nothing had a shape; look again.")
    if paras > PARA_BUDGET - 2:
        return "WARN", "%d paragraphs, close to the budget of %d" % (
            paras, PARA_BUDGET)
    return "OK", ""


def jargon_candidates(body, limit=30):
    """Proper nouns, filenames and backticked/<code> tokens, with the line of
    first occurrence. The jargon pass checks each was defined there."""
    text_lines = body.split("\n")
    first = {}
    pat = re.compile(
        r"<code[^>]*>([^<]{2,60})</code>"           # code spans
        r"|\b([A-Za-z0-9_.-]+\.(?:rb|ts|tsx|js|py|yml|yaml|json|md|sql|html))\b"
        r"|\b((?:[A-Z][a-z0-9]+){2,}(?:::[A-Z][A-Za-z0-9]+)*)\b"  # CamelCase
        r"|\b([A-Z]{3,})\b")                        # acronyms
    for n, line in enumerate(text_lines, 1):
        for m in pat.finditer(line):
            tok = next(g for g in m.groups() if g)
            tok = html.unescape(tok).strip()
            if tok and tok not in first:
                first[tok] = n
    return sorted(first.items(), key=lambda kv: kv[1])[:limit]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    want_jargon = "--jargon" in sys.argv
    if not args:
        print(__doc__)
        return 2
    try:
        doc = open(args[0], encoding="utf-8").read()
    except OSError as exc:
        print("cannot read %s: %s" % (args[0], exc))
        return 2

    doc = strip_comments(doc)
    m = re.search(r'<div class="wrap">(.*)</div>', doc, re.S)
    body = m.group(1) if m else doc

    sections = split_sections(body)
    levels = Counter()
    print("%-44s %5s %6s %8s %6s  %s"
          % ("SECTION", "PARA", "BLOCK", "DIAGRAM", "TABLE", "VERDICT"))
    print("-" * 100)
    prose_only_run = 0
    rows = []
    for title, sec in sections:
        is_entry = title == "(entry block)"
        p, b, d, t = count_section(sec)
        lvl, msg = verdict(p, b, d, t, is_entry)
        if not is_entry:
            if b + d + t == 0:
                prose_only_run += 1
                if prose_only_run >= 2 and lvl != "FAIL":
                    lvl, msg = "FAIL", ("second prose-only section in a row - "
                                        "the page drifted back to text")
            else:
                prose_only_run = 0
        rows.append((title, p, b, d, t))
        levels[lvl] += 1
        print("%-44s %5d %6d %8d %6d  %s %s"
              % (title[:44], p, b, d, t, lvl, msg))

    body_sections = [r for r in rows if r[0] != "(entry block)"]
    n_sec = len(body_sections)
    n_tab = sum(r[4] for r in body_sections)
    n_dia = sum(r[3] for r in body_sections)
    print("-" * 100)
    print("%d sections, %d tables, %d diagrams, %d paragraphs"
          % (n_sec, n_tab, n_dia, sum(r[1] for r in body_sections)))

    page_fail = False
    if n_sec and n_tab < n_sec * TABLE_RATIO_FAIL:
        page_fail = True
        print("FAIL  %d tables for %d sections - enumerations are living in "
              "prose, the most common gap. The fix is step 6's table row, not "
              "trimming." % (n_tab, n_sec))
    elif n_sec and n_tab < n_sec * TABLE_RATIO_WARN:
        print("WARN  %d tables for %d sections - check each prose-only section "
              "for an enumeration that wanted a table." % (n_tab, n_sec))
    if n_dia == 0:
        page_fail = True
        print("FAIL  no diagram at all - step 7 asks for at least one of the "
              "mechanism, not only of the map.")

    if want_jargon:
        print("\nJARGON CANDIDATES (check each was defined at this line)")
        for tok, line in jargon_candidates(body):
            print("  line %-5d %s" % (line, tok))

    failed = levels["FAIL"] or page_fail
    print("\n%s" % ("FAILED - fix and run again, do not publish yet"
                    if failed else "clean - proceed to the three passes"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
