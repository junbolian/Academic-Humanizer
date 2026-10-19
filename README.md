# Academic Humanizer

**Remove the AI tone from academic writing and keep every number, equation, citation, and theorem exactly as you wrote it.**

[中文说明](docs/zh-CN/README.md) · [PDF guide](docs/academic-humanizer-v1.0-en.pdf) · v1.0 · MIT License

Academic Humanizer is an agent skill for editing and drafting manuscripts, theses, referee responses, and grant proposals in English and Chinese. It runs in Claude, OpenAI Codex, ChatGPT, and any agent that reads `SKILL.md`. A bundled checker verifies every edit, so the science in the text stays the science you wrote.

## What it removes

- **Stock phrases and AI vocabulary.** delve, pivotal, sheds light on, "In recent years, X has attracted increasing attention", 近年来, 具有重要的理论意义和现实意义.
- **Sentence patterns typical of model output.** Invented contrasts ("The barrier is not technology but understanding", 不是……而是), cue colons ("The key insight is:", 一句话总结：), restatement sentences ("This means that", 这意味着), adjacent sentences built on one skeleton, rhetorical lists, and ordinal headings.
- **Meta-narrative and defensive writing.** "In this section, we ...", "To summarize, ...", 本节将介绍, self-deprecation ("only a preliminary attempt", 抛砖引玉), and stacked hedges ("may potentially suggest").
- **Figurative language and dashes.** Persona metaphors ("acts as a tireless reviewer"), figurative labels, and dashes used as punctuation.
- **Claims that miss their evidence.** "Significantly" without a test, "optimal" where the theorem proves consistency, a vague "large gain" where the paper reports 3.1%, and hedges on results the paper itself proves.

## What it keeps

Numbers, equations, citation keys, `\ref` and `\label` keys, the text of definitions, assumptions, and theorems, the LaTeX preamble, and every qualifier that expresses real uncertainty. Edits add no names, numbers, quotations, sources, or examples. A claim that needs evidence the text lacks receives a visible `[[EVIDENCE: ...]]` placeholder for the author to fill.

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
- "只去 AI 味，不要改内容。"
- "Draft a reply to Reviewer 2, comment 3. We added Section 5.2."

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
docs/zh-CN/                  中文说明, SKILL.md 中文译本, 中文 PDF
```

## License

MIT. See [LICENSE](LICENSE).
