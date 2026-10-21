<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/banner-en-dark.svg">
  <img src="docs/assets/banner-en-light.svg" width="100%" alt="Academic Humanizer edits AI-assisted academic prose until it reads as human scholarship. Removes: 'In recent years, X has attracted increasing attention.', 'The real barrier is not data but trust.', delve, pivotal, 'It is worth noting that', 'may potentially', 'sheds light on', 'paves the way', 'In this section, we', 'This means that', 'novel framework', 'only a preliminary attempt', 'certification protocol', dashes. Keeps and verifies: 3.1%, n = 500, p &lt; 0.05, Eq. (4), Table 4, Fig. 2, citation keys, Theorem 2, Assumption 1, labels, the theorem statement 'Under Assumption 1, the estimator is unbiased.', and genuine qualifiers such as may and suggests. Every edit is checked against your original, so the science stays yours.">
</picture>

<img src="https://img.shields.io/badge/license-MIT-0F5C7A" alt="License: MIT">
<img src="https://img.shields.io/badge/version-1.1-0F5C7A" alt="Version 1.1">
<img src="https://img.shields.io/badge/runs%20in-Claude%20%C2%B7%20Codex%20%C2%B7%20ChatGPT-0F5C7A" alt="Runs in Claude, Codex, and ChatGPT">
<img src="https://img.shields.io/badge/checker-Python%203%2C%20stdlib%20only-0F5C7A" alt="Checker: Python 3, standard library only">
<img src="https://img.shields.io/badge/for-papers%20%C2%B7%20theses%20%C2%B7%20rebuttals%20%C2%B7%20grants-0F5C7A" alt="For papers, theses, rebuttals, and grants">

**English** · [简体中文](README.zh-CN.md) · [PDF guide](docs/academic-humanizer-v1.1-en.pdf)

</div>

**Remove the AI tone from academic writing and keep every number, equation, citation, and theorem exactly as you wrote it.**

Academic Humanizer is an agent skill for editing and drafting manuscripts, theses, referee responses, and grant proposals in English and Chinese. It runs in Claude, OpenAI Codex, ChatGPT, and any agent that reads `SKILL.md`. A bundled checker verifies every edit, so the science in the text stays the science you wrote.

## What it removes

- **Stock phrases and AI vocabulary.** delve, pivotal, sheds light on, "In recent years, X has attracted increasing attention", "has important theoretical and practical significance", and their Chinese counterparts.
- **Sentence patterns typical of model output.** Invented contrasts ("The barrier is not technology but understanding"), cue colons ("The key insight is:"), restatement sentences ("This means that"), adjacent sentences built on one skeleton, rhetorical lists, and ordinal headings.
- **Meta-narrative and defensive writing.** "In this section, we ...", "To summarize, ...", self-deprecation ("only a preliminary attempt"), and stacked hedges ("may potentially suggest").
- **Figurative language and dashes.** Persona metaphors ("acts as a tireless reviewer"), figurative labels, and dashes used as punctuation.
- **Coined labels.** An abstract modifier plus a system noun that the text never defines or cites, such as "certification protocol", "verification layer", or "safeguard mechanism". Each becomes what the text says it does. When the text never says, the report suggests what the author should state. Established terms such as "attention mechanism" stay.
- **Methods and proofs written as work logs.** "Verification pipeline", "sanity check", "audit", "certified bound", solver tolerances, random seeds, guards that never triggered, and script names. Computer-assisted proof steps become lemmas that say whether the computation is exact or numerical. Every value a reported result depends on stays, and every deleted number is listed in the report.
- **Claims that miss their evidence.** "Significantly" without a test, "optimal" where the theorem proves consistency, a vague "large gain" where the paper reports 3.1%, and hedges on results the paper itself proves.

## What it keeps

Numbers, equations, citation keys, `\ref` and `\label` keys, the text of definitions, assumptions, and theorems, the LaTeX preamble, and every qualifier that expresses real uncertainty. Edits add no names, numbers, quotations, sources, or examples. A claim that needs evidence the text lacks receives a visible `[[EVIDENCE: ...]]` placeholder for the author to fill. While any placeholder remains, the report opens with a warning that the text is not ready to submit, and the checker ends its output with a `NOT READY TO SUBMIT` line.

Results that the evidence supports read as results. The voice the skill produces is that of a confident scholar: specific, assertive, and exact about scope.

## Three modes

| Mode | Use it for | What changes |
|---|---|---|
| Polish | drafts | Wording, flow, idiomatic English, and claim scope |
| Cleanup | final or submitted text | Only sentences that match a listed pattern, and only the matched part |
| Draft | new sections, letters, proposals | New text written under the same rules, with every reference searched and confirmed |

## Install

**Claude Code**

```bash
git clone https://github.com/junbolian/Academic-Humanizer.git
cp -r Academic-Humanizer/academic-humanizer ~/.claude/skills/
```

**Claude apps.** Zip the `academic-humanizer` folder and upload it as a custom skill.

**OpenAI Codex.** Copy the folder to `~/.agents/skills/` for all projects, or to `.agents/skills/` inside one repository. Invoke it with `$academic-humanizer`, or let Codex select it from the task.

**ChatGPT.** On Business, Enterprise, and Edu plans, upload the zipped folder under Plugins, Skills, Create, Upload from your computer. On other plans, create a GPT or a project, paste [`platforms/chatgpt-instructions.md`](platforms/chatgpt-instructions.md) into its instructions, attach the files of the `academic-humanizer` folder, and turn on code execution.

**Any other agent.** Load `SKILL.md` as instructions and give the agent access to `references/` and `scripts/`.

## Use

Plain requests trigger the skill.

- "Polish the introduction in `paper.tex`."
- "This abstract is final. Remove the AI tone only."
- "Draft a reply to Reviewer 2, comment 3. We added Section 5.2."

Requests written in Chinese work the same way.

The agent returns the full revised text and a short report: changes grouped by rule, claims rescoped, placeholders to fill, structural notes, and the checker's verdict.

## The checker

```bash
python3 academic-humanizer/scripts/check_revision.py audit paper.tex
python3 academic-humanizer/scripts/check_revision.py compare paper.tex revised.tex --changes
```

`audit` lists candidate phrases and patterns by line. `compare` exits with status 1 when any number, citation key, label, math segment, formal statement, or the preamble changes. It also lists every qualifier that disappeared, every new capitalized term and quotation, and every changed sentence, so each edit maps to a rule. The script needs Python 3 and nothing else.

An excerpt from a real run on a results paragraph:

```text
== Invariants (must be unchanged unless the change is intended and reported) ==
  numbers                            unchanged (3)
  cross-references and labels        unchanged (1)
  RESULT: all invariants hold

== Conservation warnings (do not affect the exit status) ==
  qualifiers and concessions: 3 -> 0
    LOST (each one strengthens a claim unless it was intended):
      may x1  original line 2: ...the results >>may<< potentially suggest that the stratified...
```

The three removed qualifiers hedged numbers that the paper reports in its own table, so the report records them as intended stance edits. A removed qualifier on unsupported evidence goes back in.

## Repository

```text
academic-humanizer/          the skill: SKILL.md, references/, scripts/, agents/openai.yaml
platforms/                   instructions for ChatGPT GPTs and projects
docs/                        English PDF guide
docs/assets/                 README banners (light and dark, English and Chinese)
docs/zh-CN/                  Chinese translation of SKILL.md and Chinese PDF guide
README.zh-CN.md              Chinese README
```

## License

MIT. See [LICENSE](LICENSE).
