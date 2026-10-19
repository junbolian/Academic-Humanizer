---
name: academic-humanizer
description: Edit or draft academic prose so it reads as precise human scholarship. Covers journal and conference papers in any field, theses, rebuttals, referee response letters, grant proposals, and Chinese academic text. Removes AI stock phrases, invented contrasts (not X but Y, 不是……而是), cue colons, meta-narrative, defensive hedging, figurative language, em dashes, repeated sentence skeletons, translationese, and disconnected flow. States each claim at the strength its evidence or proven result supports, and keeps every number, equation, citation key, label, formal statement, and genuine qualifier unchanged and verifies this with a bundled script. Use whenever the user asks to polish, proofread, tighten, rewrite, humanize, 润色, 改写, 去AI味, or make a manuscript read more naturally, and whenever the assistant drafts new manuscript text.
license: MIT (see LICENSE.txt)
compatibility: Agent Skills format. Works in Claude (apps and Claude Code), OpenAI Codex, ChatGPT skills, and any agent that reads SKILL.md. scripts/check_revision.py needs Python 3 and the standard library only.
metadata:
  version: "1.0"
---

# Academic Humanizer

The skill makes AI-assisted academic prose read the way a careful author in the field writes: literal, precise, connected from one sentence to the next, confident where the evidence is strong, and never stronger than the evidence. It changes wording, not content. Numbers, equations, citation keys, cross-references, formal statements, and genuine qualifiers stay as the author wrote them, and a bundled script verifies this. Authors keep their venue's AI-disclosure obligations.

## Modes and scope

- **Polish** is the default when the user asks to polish, tighten, rewrite, 润色, or 改写. All Rules apply, and sentences may be rewritten for flow (Rule 8) and idiom (Rule 9) within the edit discipline below.
- **Cleanup** applies when the user asks only to remove AI tone, says 只去AI味 or 成稿清理, or calls the text final. Only Rules 1 to 4 and the first item of Rule 5 apply. A sentence that matches none of them stays verbatim, and a sentence that matches changes only in the matched part. Claims that need evidence go to the report, not into placeholders.
- **Draft** applies when the assistant writes new manuscript text, such as a section, a response letter, or a proposal. Apply the Rules while writing, run `check_revision.py audit` on the draft, and fix what it finds before delivering. Never cite from memory: search for every new reference, confirm that it exists, and check that the sentence describing it matches the source. A literature review includes a search for work from the last two years.

When the request does not settle the choice between polish and cleanup, use polish for drafts and cleanup for text the user calls final or submitted.

## Edit discipline

1. **Every change has a rule.** Each change corresponds to a numbered Rule below. A change without a rule is reverted. Taste in wording is not a rule.
2. **Smallest sufficient change.** Within a sentence that matches a rule, change what the rule targets and leave the neighbouring words alone. Polish mode also allows Rules 8 and 9 to act on the same sentence.
3. **Nothing added.** Names, institutions, roles, places, numbers, dates, orderings, quotations, sources, links, causal claims, motives, and examples enter the text only if the original or the user's material contains them. Every content word in the revision traces to one of those two sources. Concrete detail is the author's to supply, and a thin passage becomes a report item.
4. **Nothing lost.** Claims, conclusions, concessions, and qualifiers that express real uncertainty stay: may, likely, typically, in some cases, under these conditions, 可能, 通常, 在某些情况下. Rule 7 removes two kinds of qualifier only, hedges on results that the text itself proves or reports and stacked duplicates, and the report lists each removal. `compare` lists every qualifier that disappears.
5. **Fixed structure.** Heading levels, section order, paragraph count and order, lists, tables, figures, quotations, and code stay in place unless the user asks for structural change. Structural problems go into the report (Rule 11).

## Style reference first

When the user supplies the author's earlier papers, a style guide, or a target-voice description, read it before editing. Note sentence length, connectives, level of hedging, how sections and paragraphs open, punctuation habits, and notation. Where the reference conflicts with Rules 1, 2, 3, 4, 8, or 9, follow the reference, since those rules set register and the reference shows the author's register. An author who uses dashes on purpose keeps them. The reference never overrides Rules 5, 6, 7, and 10, which protect evidence, proven scope, stance, and the invariants.

## Running the checker

SKILL_DIR is the folder that contains this file. Common locations are `~/.claude/skills/academic-humanizer` in Claude Code, `/mnt/skills/user/academic-humanizer` in the Claude apps, and `~/.agents/skills/academic-humanizer` or `.agents/skills/academic-humanizer` in OpenAI Codex. An environment without Python still gets the same comparisons: carry them out by reading, and state in the report that the script did not run.

## Process for polish and cleanup

1. Save the original verbatim in a working folder, for example `ah/orig.tex`, or `.md` and `.txt` for other text. Record the document type, venue, language, and mode.
2. Read the style reference, if one was supplied.
3. Run `python3 SKILL_DIR/scripts/check_revision.py audit ah/orig.tex`. The output lists candidate AI-tell phrases with their lines, sentence patterns, dashes, semicolon and parenthesis density, long sentences, runs of very short sentences, and the section and result structure. Each hit is a candidate for a decision. "Robust" is correct in a paper on robust statistics, and "navigation" is literal in a robotics paper.
4. Read the full text before changing anything. Identify each paragraph's single point and how it follows from the paragraph before, since flow problems show at this level.
5. Rewrite under the Rules and the edit discipline. Cleanup mode touches only sentences with a rule match.
6. Save the revision next to the original and run `python3 SKILL_DIR/scripts/check_revision.py compare ah/orig.tex ah/revised.tex --changes`. The script compares numbers, citation keys, `\ref` and `\label` keys, math, the text of formal environments, and the preamble. It then lists lost qualifiers, new capitalized terms, new quoted strings, and every changed sentence, and audits the revision against the original. Revert each unintended difference, match each changed sentence to a rule, and repeat until only intended differences remain.
7. Go through the final checklist and deliver as described under Output.

For a single paragraph under about 150 words the script is optional. Compare numbers, citations, qualifiers, and math against the original by reading before delivering.

Read `references/examples.md` before the first rewrite in a conversation. It shows each rule applied with and without the evidence a sentence needs, and the same paragraph in polish and cleanup modes.

## Rules

### 1. Remove stock phrases and AI vocabulary

The full candidate list is `references/lexicon.txt`, which the script reads. The main groups:

- Vocabulary: delve, underscore, intricate, tapestry, testament, pivotal, showcase, foster, realm, seamless, harness, multifaceted, nuanced, holistic, meticulous, paramount, invaluable, crucial when it only means important, leverage when it only means use.
- Significance claims without content: paves the way, a crucial step toward, opens new avenues, sheds light on, bridges the gap, of paramount importance, transformative, groundbreaking, new paradigm.
- Formulaic openers: "In recent years, X has attracted increasing attention", "With the rapid development of", "Despite recent advances", "X plays a crucial role in". Open with the specific problem instead.
- Spoken openers: Simply put, Long story short, Bottom line, 说白了, 说穿了, 先说结论. Delete them and state the point.
- Size words without numbers: extensive or comprehensive experiments, a wide range of, numerous, various, substantial. Replace each with the count or the number the paper reports.
- Novelty padding: "novel" more than once per section, "for the first time", and "to the best of our knowledge". Keep at most one, and only where the authors searched the literature.
- Announced emphasis: It is worth noting that, Importantly, Interestingly, Notably. State the fact and let its position and evidence carry its weight.
- Copula avoidance ("serves as" or "stands as" where "is" is meant), negative parallelism for emphasis ("not just X but Y"), trailing "-ing" clauses that add a vague evaluation ("..., highlighting the importance of ..."), and lists of three where one item is meant.
- Implications boilerplate: rich insights, important implications for practitioners, provides a new perspective, delicate balance, interplay, repeated counterintuitive.
- Response-letter boilerplate: thanks for an "insightful comment" in every reply. Thank the reviewers once, at the top of the letter. Each reply states what changed and where.

### 2. Write literally

Replace metaphors and figurative labels with the mechanism they stand for: landscape, through the lens of, cornerstone, blueprint, roadmap, double-edged sword, sweet spot, unlock, arms race, holy grail, silver bullet, at the heart of, tackle, grapple with. A reader in the field checks each sentence against the model or the data, and a metaphor offers nothing to check.

Persona metaphors are the clearest case. A tool, model, or procedure described as an idealized person ("acts as a tireless reviewer", "like a wise mentor", 像一位智慧的导师) is usually followed by praise or a "not only ... but also" clause. State what the thing does: "it checks each constraint against the data in seconds".

Established technical terms stay even when they began as metaphors: bottleneck, halo effect, spillover, curse of dimensionality, cold start, warm start, signal and noise, backbone for a network architecture, loss landscape, heuristic as the name of an algorithm class. A term stays when it has a definition in the field or in the paper. A precise description beats a general label: "a method without a performance guarantee" says more than "a heuristic method".

The rule exists for checkability. Metaphor as such does not separate model output from human writing, and human writers of Chinese nonfiction use more of it (see "Not reasons to change"). Apply it to papers, theses, reports, and letters. In essays and popular writing where figurative language belongs to the genre, follow the style reference.

The paper's title and the names the authors gave to models, policies, and effects stay. A figurative name gets one mention in the report, and the decision stays with the author.

### 3. Punctuation: no dashes, few semicolons and parentheses

Remove em dashes (U+2014, LaTeX `---`, the Chinese 破折号) and spaced en dashes or hyphens used as dashes. Use a comma, a colon, or two sentences. En dashes in numeric ranges (`2--6`) and in joint names (`Karush--Kuhn--Tucker`) stay, and so do Chinese 连接号 as described in `references/chinese.md`.

Semicolons and parenthetical asides follow the same logic. Two or more semicolons in one paragraph, or a parenthetical aside in most sentences, signal a paragraph that needs restructuring into full sentences. Parentheses around citations, equation numbers, units, and abbreviations at first use are standard and stay.

Dash rates vary by model by more than an order of magnitude. In a corpus of Chinese nonfiction, measured per 1,000 characters, human writers used 0.80 dashes, Claude 4.25, DeepSeek 5.16, Kimi 2.32, Gemini 0.51, and GPT 0.11. The same corpus shows GPT using 不是……而是 most often of the five models. Every draft gets the full check whichever model produced it.

### 4. Sentence patterns that mark generated text

Each pattern below appears at a clearly higher rate in model output than in human writing, measured on 300 model-written articles from five models and 329 human-written articles in Chinese nonfiction, and each has a trigger that can be located in a specific sentence. The English forms make the same move in English. An item applies only when its trigger is present.

**4.1 Invented contrasts.** The sentence sets up a misconception nobody in the text holds and then corrects it: "The real barrier is not technology but understanding", "X is not about A; it is about B", "What matters is not A but B", 不是……而是, 并非……而是, 不在于……而在于, 与其说……不如说, 看似……实则, 你以为……其实, 说到底. State the claim directly: "The barrier is understanding." A contrast stays when someone the text identifies holds A, such as a prior result, an assumption the paper relaxes, or a hypothesis the data reject: "Unlike \citet{ref1}, we do not assume a closed population." Rule 1 covers the additive form "not just X but Y".

**4.2 Cue colons and list lead-ins.** A cue phrase and a colon announce content instead of stating it: "The key insight is: ...", "The answer is simple: ...", "The result: ...", "In short: ...", 一句话总结：, 核心是：, 关键在于：, 原因如下：, 本质上：. Delete the cue when it carries nothing. When it links to the previous sentence, keep it and replace the colon with ordinary syntax. A sentence that only announces a list ("Here are the main reasons:", 我见过的几种典型场景：) becomes a statement with content or goes, and the list follows the preceding text with every item intact. Colons that introduce a quotation, a definition, an equation, or the parts of a general statement stay ("The model has two components: a measurement model and a structural model"), as do genre lead-ins such as "We make three contributions:" in many introductions and "The proof has two steps:". Headings, list-item labels, URLs, and code are out of scope.

**4.3 Repeated sentence skeletons and filler examples.** Two or more adjacent sentences built on one skeleton, with the same clause order, comma positions, and length, read like a completed form. The measured rate is 9.41 such pairs per 100 paragraphs in model text against 4.81 in human text. Change the syntax of one sentence by merging, splitting, reordering, or subordinating it, and keep its content. When a paragraph gives three or more parallel cases that make the same point, keep the most representative case in the main clause and compress the others into a clause without dropping information. Narrative sequence, enumerated steps, and parallel clauses inside one sentence stay.

**4.4 Restatement sentences.** A sentence that opens with "This means that", "This suggests that", "In other words", 这意味着, 这表明, 这说明, or 换句话说 and repeats the previous sentence merges into that sentence or keeps only its conclusion. A sentence that draws a conclusion the previous one does not contain stays, and its support is checked under Rules 5 and 6.

**4.5 Rhetorical lists.** One clause chaining three or more parallel items to sound complete, such as "startups, mid-sized firms, and large groups all benefit", becomes "firms of every size benefit". Without a fitting category word, change the syntax of one item. Lists that carry content stay complete: datasets, baselines, variables, assumptions, parameter values, regulatory items, and Markdown lists. Most lists in academic text carry content.

**4.6 Ordinal headings.** In reports, handouts, posts, and slides, three or more consecutive headings numbered 一、二、三, 第一、第二, or First, Second lose the ordinals and keep their text. Section numbers set by a manuscript class file or venue template, numbered steps, and items referred to by number are out of scope.

**4.7 Paragraph openings without a referent.** A paragraph other than the first opens with a comment such as 听起来, 看起来, 值得注意的是, 更重要的是, 关键在于, or 问题在于 and contains no word pointing back to the preceding text (这, 那, 其, 此, 上述). Add the referent: 这听起来像……. In English, a paragraph that opens with "More importantly," or "The catch is" names its subject.

**4.8 Signpost connectives at paragraph starts.** When 然而, 因此, 此外, 与此同时, 换言之, 总而言之, Moreover, Furthermore, However, or Therefore opens several consecutive paragraphs, keep the connective only where it marks the logical relation at a turn in the argument. Move an additive connective into the sentence or delete it. Rule 8 governs connectives inside paragraphs.

**4.9 Meta-narrative, self-reference, previews, and recaps.** Sentences about the text itself carry no content: "In this section, we discuss ...", "We now turn to ...", "As mentioned above, ...", "Before proceeding, ...", "To summarize, ...", "This section has shown ...", "The remainder of this paper is organized as follows", 本节将介绍, 下面我们将, 如前所述, 本文结构安排如下, 本章小结. Delete them, or keep only the substantive claim they wrap ("As shown above, the bound is tight" becomes "The bound is tight (Proposition 2)"). The paper's conclusion section keeps its summary. Cross-references that point to content the reader needs at that point stay: "the bound in Section 3 gives ...".

### 5. Empirical claims match their evidence

- When a summary phrase ("substantially improves", "a large gain", 显著提升, 实现了效率的提升) stands where the same or the next paragraph gives the number, date, or object, put that specific value in its place. When the text gives no number, restore the plain verb ("achieves an improvement in accuracy" becomes "improves accuracy", 完成了对流程的优化 becomes 优化了流程) and add nothing.
- Each empirical claim points to its evidence, a table, figure, test, or citation, and its verb matches that evidence: "show" or "find" for what the reported results exhibit, "suggest" or "is consistent with" for indirect evidence. "Prove" is reserved for proofs.
- Replace a vague magnitude with the number the paper reports, with its metric, comparator, and sample: "reduces mean absolute error by 3.1% relative to the strongest baseline (Table 4)".
- Numbers, test results, table and figure references, and citations come only from the supplied material. When a sentence needs evidence that was not supplied, insert the visible placeholder `[[EVIDENCE: what is needed]]`, written in LaTeX as `\textbf{[[EVIDENCE: what is needed]]}` with plain words inside (no `%`, `_`, `&`, `#`). The script lists every placeholder and excludes its contents from the comparison. A placeholder is a correct output, and a plausible number is a fabrication. Cleanup mode lists the need in the report instead.
- Report the statistic the paper computed, a mean with its standard error or confidence interval, a median, or a range, together with its aggregation. One statistic is never converted into another.
- Compare against the strongest baseline first.
- "Significant" and "significantly" require a stated test. Without one, give the difference and drop the word.
- All reported numbers come from one sample of record. Text that mixes samples, runs, or data versions without saying so is flagged in the report, and the numbers stay untouched.
- The phrasing states exactly what the evidence supports, neither weaker (Rule 7) nor stronger.

### 6. Theoretical claims match the proven statement

- For results proven in the paper, "we prove", "we show", and "we establish" are correct and stay.
- A sentence that restates a result carries its conditions: the assumptions, the class of methods, the parameter region, and whether the result is asymptotic. "The estimator is unbiased" becomes "Under Assumptions 1 and 2, the estimator is unbiased when the sampling fraction exceeds the threshold in Proposition 3." Use the paper's notation and names and introduce no new symbols.
- Check each quantifier against the statement: optimal, always, never, robust, for any. A result that depends on a functional form or a distribution, such as linearity or normal errors, says so wherever the introduction or the conclusion states it.
- Practical implications are conditional comparative statics with a direction and a source: "The number of sampling rounds needed for a given precision decreases in the capture probability and increases in the heterogeneity across strata (Proposition 4)." Advice such as "practitioners should carefully balance cost and precision" says less than the proposition it replaces.
- Theorems, propositions, and lemmas are never added, removed, merged, or promoted. Suggestions about their number go into the report (Rule 11).

### 7. Stance: assert what the evidence supports

The target voice is a confident scholar: assertive verbs, specific results, no superlatives without evidence, and no apology.

- State proven and reported results as results. "Our method may reduce error by 3.1% (Table 4)" becomes "Our method reduces error by 3.1% (Table 4)". Hedges stay only where uncertainty is real: indirect evidence, extrapolation beyond the sample, conjecture.
- Collapse stacked hedges to one: "may potentially", "might possibly suggest", "could perhaps", "在一定程度上可能".
- Remove self-deprecation: "this simple attempt", "a preliminary step", "our modest contribution", "admittedly", "we humbly", 本文只是初步尝试, 抛砖引玉, 笔者水平有限, 不足之处敬请指正.
- Remove defensive writing: rebuttals of objections nobody raised, "we do not claim to ...", repeated "beyond the scope of this paper", and weaknesses listed without bearing on a result's validity.
- Remove unnecessary disclosure, such as accounts of failed attempts, of the order in which work was done, or of doubts the evidence does not raise. A limitation that bounds a result's validity is stated once, plainly, where the result is stated or in the limitations paragraph. Disclosures that the venue requires, such as AI use, data availability, and conflicts of interest, stay where the venue puts them.
- State contributions directly: "We show", "We introduce", "This paper establishes". Claims of being first, largest, or only stand when the evidence and a literature search support them.

### 8. Connected flow: one point per paragraph, no jumps

- Each paragraph makes one point, stated in its first or second sentence, and the remaining sentences support it.
- Each sentence follows from the one before. When the logical step between two sentences is missing, add a clause that states the relation already present in the argument: because, so, as a result, in contrast, for example, under this condition. When the relation is unclear, flag it in the report.
- Logical connectives stay: because, therefore, thus, however, in contrast, whereas. Additive connectives (Moreover, Furthermore, Additionally, In addition) at the start of consecutive sentences give way to the actual relation or to nothing.
- Split sentences longer than about 35 words, or with three or more subordinate clauses, so that each carries one step, and keep the pieces connected. Rhythm is not a reason to split (see "Not reasons to change").
- Runs of short declarative sentences, fragments such as "That limits progress.", and headline colons such as "The result: ..." are errors too. A long sentence that states one condition and its consequence is fine.
- One object keeps one name. A defined term is reused exactly, and a repeated name is not replaced by a pronoun for variety. "Participants", "subjects", and "respondents" do not alternate for one group.
- Present tense for what the paper does and what its results show, past tense for procedures carried out.
- Definitions, assumptions, and result statements stay verbatim, and the compare script checks them.

### 9. Idiomatic English

Many drafts come from authors whose first language is not English, and the edit leaves the English idiomatic as well as free of AI phrases. Fix articles, countability ("a research", "informations"), prepositions (different from, consistent with, depend on), "which" versus "that", and constructions carried over from Chinese ("with the development of", "play an important role in", "make a contribution to", chains of "so as to"). Each replacement is a real collocation: "the methods remain largely empirical" is idiomatic, "the methods stay empirical" is not. Technical terms never become everyday words.

### 10. Preserve what is correct

- Qualifiers that express real uncertainty: suggests, is consistent with, may, we conjecture. "Suggests" does not become "shows" without new evidence. Rule 7 handles hedges on established results, and Rule 1 handles vague hedges such as somewhat and fairly.
- Passive voice when the actor does not matter, and "we" for the authors.
- Technical terms, notation, equations, LaTeX macros and environments, labels, and citation keys, verbatim.
- Genre conventions of careful authors: "Our work relates to three streams of literature" in an introduction, a contribution list, the structure of proofs.
- Citations: no citation key is added or removed. A cited work is described only from the existing text or from a source read in the current conversation, because descriptions written from memory are a frequent source of error. A citation list that never says how the works differ from the paper becomes a report item.

#### Not reasons to change

The features below look like AI writing to many readers, but corpus measurements show no gap, or a gap in the human direction. Changing them moves text away from human writing, so they never justify an edit. Rates are per 1,000 Chinese characters unless stated.

| Feature | Measured result |
|---|---|
| Uneven sentence or paragraph length | No gap: the coefficient of variation of sentence length is 0.58 for models and 0.67 for humans. |
| Passive voice, nominalization, long sentences | Normal formal writing. Abstract passives such as 被认为 and 被视为 occur 0.09 times in model text. |
| Repeating a full name instead of a pronoun | More common in human text (0.04 against 0.02 adjacent-sentence repeats). |
| Parallel phrasing inside one sentence | As common or more common in human text, with ratios from 0.61 to 1.10 across forms. |
| Questions in body text, question headings | Body questions run 1.83 in human text against 0.10 in model text. Question headings show no gap as a share of all headings. |
| "First ... second" inside paragraphs | No gap. Ordinal headings (4.6) are the target. |
| Few function words or colloquial connectives | Models use fewer, but added function words cannot be verified and push formal text toward speech. |
| Metaphor as such | Human writers use about 2.4 times as many. |

### 11. Structure audit, reported and changed only on request

Use the script's structure output and a full reading. Report:

- a section with exactly one subsection, to merge into its section or to pair with a second subsection;
- sections that could merge;
- the number of main-text results, intermediate results that could become appendix lemmas, and results that restate another under a different parameter and could become corollaries or remarks;
- paragraphs with more than one point, and places where the argument jumps;
- ordinal headings in non-manuscript documents (4.6) when cleanup mode fixes the structure.

## Venue register

- Conference papers with strict page limits, common in computer science and engineering: short and results-first, contributions stated as specific results, limitations stated plainly and once.
- Journal papers: the research question grounded in a concrete setting, the literature positioned by stream with the specific difference from the closest work, assumptions stated with their justification, and each main result followed by its interpretation and the condition under which it holds. Understatement of tone, full statement of results.
- Referee response letters: one reply per comment, quoting the comment and stating the change and its location. A disagreement gives the argument and the evidence. One round of thanks at the top.
- Grant proposals (NSF, NIH, and similar): read `references/proposals.md`.
- Chinese text, including textbooks, theses, and reports: read `references/chinese.md`.
- Earlier papers by the author: see "Style reference first".

## Final checklist

- Every change corresponds to a numbered Rule, and changes without one are reverted.
- In cleanup mode, every sentence without a rule match is verbatim, and matched sentences changed only in the matched part.
- No new names, numbers, dates, quotations, sources, causal claims, or examples. Every content word traces to the original or the supplied material.
- No real qualifier, concession, claim, or conclusion was dropped. Each qualifier that `compare` lists as lost was removed under Rule 7 and appears in the report.
- Headings, section order, paragraph order, lists, tables, and quotations are in place.
- No invented contrast, cue colon, list lead-in, restatement sentence, spoken opener, meta-narrative sentence, preview, or recap remains outside the conclusion section.
- No adjacent sentences share one skeleton, and no paragraph pads its point with parallel cases.
- No dash used as punctuation, no paragraph crowded with semicolons or asides, and no figurative or persona label outside established terms.
- Summary phrases with a specific value nearby now carry that value, and nominalized verbs are restored.
- Empirical verbs match their evidence, proven results carry their conditions, and established results read as established, without apology or defence.
- Every missing piece of evidence is a placeholder in polish mode or a report item in cleanup mode.
- None of the "Not reasons to change" features was edited for its own sake.
- `compare` reports numbers, citation keys, labels, math, and formal statements unchanged, or lists each difference as intended.

## Output

1. The complete revised text. A `.tex` or other file input comes back as the full revised file, never as a list of edit descriptions.
2. A short report, written under the same Rules:
   - the mode and, if used, the style reference;
   - changes grouped by Rule, with counts;
   - claims scoped, strengthened under Rule 7, or given evidence pointers;
   - every placeholder the author must fill, and in cleanup mode every claim that needs evidence;
   - structural issues (Rule 11) and figurative names chosen by the author (Rule 2);
   - the final `compare` result for numbers, citation keys, labels, math, formal statements, and qualifiers.
