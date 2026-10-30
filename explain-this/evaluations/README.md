# Evaluations

Three scenarios, each a real subject this skill was run on. Run one by giving
Claude the `query` with the skill available, in a checkout of the repo named,
then score the run against `expected_behavior` — every line is pass/fail, not
a judgement.

**Use them when you change `SKILL.md`.** A rule added to fix one page has a
habit of breaking a behaviour two pages back: questions 1 and 2 of step 5 were
dropped twice, and the prerequisites question has been skipped whenever the
subject felt self-explanatory.

| File | Subject | What it mainly tests |
| --- | --- | --- |
| `01-background-migrations.json` | `db/migrate-background` in the monolith | Steps 3, 5 and 6 — spine, question order, tables over prose |
| `02-feature-switches.json` | `config/feature_switches.yml` | Step 2's direction sources and step 5's question 7 |
| `03-audit-existing-page.json` | An existing page handed back for review | The reverse mode: audit, report, change nothing without agreement |

A run that produces a correct page while failing three expectations is still a
failed run. The expectations are the behaviours that make pages good across
subjects, which a single good page does not demonstrate.
