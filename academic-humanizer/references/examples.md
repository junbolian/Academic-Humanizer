# Worked examples

Each example states the context the author supplied and the mode, which is polish unless stated. Every number, result, and reference in an "After" text comes from that context. Where the context lacks what a sentence needs, the "After" text carries a placeholder instead of a plausible value. Citation keys such as ref1 and ref2 are placeholders.

The running context for every example except Example 7: the paper estimates the size of a closed animal population from repeated capture surveys in which some animals are easier to catch than others. The stratified estimator divides the animals into strata by catchability, estimates the size of each stratum separately, and adds the estimates. Theorem 2 proves that the stratified estimator is consistent as the number of sampling rounds grows, for a closed population with equal catchability within each of at least two strata. Table 3 reports, over 1,200 simulated populations, a mean relative error of 0.8% (standard error 0.1%) for the stratified estimator and 2.9% for the best unstratified estimator. Its parameter grid varies the capture probability and the number of strata. No statistical test is reported, and the text does not state the largest error over the grid.

## 1. Introduction opening (Rules 1, 5, 6)

Before:
> In recent years, wildlife population monitoring has attracted increasing attention from both academia and practitioners. With the rapid development of sensing technologies, ecologists face intricate trade-offs between survey cost and precision, making the choice of estimator of paramount importance. In this paper, we propose a novel framework that sheds light on this pivotal problem and offers rich practical insights. Extensive numerical experiments demonstrate the effectiveness of our approach.

After:
> Capture surveys estimate the size of an animal population from repeated captures, and the estimate is biased when some animals are easier to catch than others. We study this problem for a closed population in which catchability is equal within each of at least two strata. We prove that the stratified estimator is consistent as the number of sampling rounds grows (Theorem 2). The estimator estimates the size of each stratum separately and adds the estimates. Across 1,200 simulated populations its mean relative error is 0.8% (standard error 0.1%), compared with 2.9% for the best unstratified estimator (Table 3).

What changed: the opening states the estimation problem instead of its popularity. "Novel", "sheds light", "pivotal", "rich practical insights", and "extensive" go, and "demonstrate the effectiveness" becomes the numbers from Table 3 with their comparator. "Prove" stays because Theorem 2 is proven in the paper, and the sentence carries the theorem's conditions.

## 2. Scope of a proven result (Rule 6)

Before:
> We prove that the stratified estimator is optimal, which provides a simple and robust solution for practitioners.

After:
> We prove that the stratified estimator is consistent as the number of sampling rounds grows, for a closed population with equal catchability within each of at least two strata (Theorem 2).

What changed: "prove" stays. "Optimal" becomes "consistent", which is what Theorem 2 states, with the theorem's conditions. "Robust" goes because the paper contains no robustness result, and "for practitioners" goes because no part of the paper concerns field use. The report offers a literal version of the simplicity point: the estimator needs only the stratum labels and the capture counts.

## 3. Numerical claims and placeholders (Rule 5)

Before:
> Extensive numerical experiments demonstrate that our estimator significantly outperforms existing benchmarks and remains robust across a wide range of settings.

After:
> Across the 1,200 simulated populations in Table 3, the mean relative error of the stratified estimator is 0.8% (standard error 0.1%), compared with 2.9% for the best unstratified estimator. Over the grid of capture probabilities and stratum counts in Table 3, the error does not exceed [[EVIDENCE: largest error over the grid in Table 3]].

What changed: "significantly" goes because no test is reported. The comparison is with the strongest benchmark in Table 3 and uses the statistic the table reports. "Robust across a wide range of settings" becomes the actual grid plus a placeholder for the one number the text does not supply. A plausible value such as "1.5%" in that place would be a fabrication.

## 4. Splitting a long sentence without fragmenting it (Rule 8)

Before:
> Existing population estimators, though effective in specific sampling regimes, lack theoretical guarantees underpinning their performance, which restricts their applicability and hinders further development.

Too fragmented, never the target:
> Existing estimators work in some regimes. They lack guarantees. That restricts applicability.

After:
> Existing population estimators perform well in specific sampling regimes, but they have no performance guarantee. Without a guarantee, it is unclear in which surveys an estimator will perform well, and this uncertainty limits both its application and its further development.

What changed: each sentence carries one step, and the logical relations stay explicit ("but", "Without a guarantee"). The fragmented version has short sentences and drops the relations, which leaves the reader to reconstruct the argument.

## 5. Practical implication (Rules 1, 6)

Additional context: Proposition 4 shows that, under the conditions of Theorem 2, the number of sampling rounds needed to reach a target precision decreases in the capture probability and increases in the difference in catchability across strata.

Before:
> These results offer rich practical insights: practitioners should carefully balance survey effort and precision when designing monitoring programs.

After:
> The number of sampling rounds needed for a given precision decreases as the capture probability rises and increases with the difference in catchability across strata (Proposition 4). A survey whose strata differ more in catchability should therefore plan more rounds even when the capture probability does not change.

What changed: the implication is the comparative static of Proposition 4, with its direction and its source. The second sentence follows from the second half of the proposition and claims nothing beyond it.

## 6. Citation list (Rule 10)

Before:
> Population estimation has been widely studied \citep{ref1, ref2, ref3, ref4, ref5}.

After:
> Population estimation has a large literature \citep{ref1, ref2, ref3, ref4, ref5}.

Report entry: "Line 14 cites five works without saying how any of them differs from this paper. Consider naming the closest one and the difference."

What changed: all five keys stay, and no cited work is described beyond what the text already says.

## 7. Referee response (venue register)

Context: the authors added Section 5.2, which allows animals to move between strata. Proposition 6 extends Theorem 2 to this case, with the proof in Appendix C.3.

Before:
> We sincerely thank the reviewer for this insightful and valuable comment. Following the reviewer's excellent suggestion, we have carefully revised the manuscript accordingly to address this important point.

After:
> We added Section 5.2, which allows animals to move between strata. Proposition 6 extends Theorem 2 to this case, and its proof is in Appendix C.3.

What changed: the reply states the change and its location. Thanks appear once, at the top of the letter.

## 8. Invented contrast, cue colon, and restatement: polish versus cleanup (Rules 4, 6)

Before:
> The difficulty of estimating population size is not computational; it lies in unequal catchability. The key insight is simple: under the conditions of Theorem 2, stratifying by catchability loses little. This means that the estimator does not need a model of individual behavior.

After, polish mode:
> The difficulty of estimating population size lies in unequal catchability. Under the conditions of Theorem 2, the stratified estimator is consistent as the number of sampling rounds grows, so it does not need a model of individual behavior.

After, cleanup mode:
> The difficulty of estimating population size lies in unequal catchability. Under the conditions of Theorem 2, stratifying by catchability loses little, so the estimator does not need a model of individual behavior.

What changed: no one in the text claims the difficulty is computational, so the contrast goes (4.1) and the author's own claim stays. "The key insight is simple:" announces the sentence instead of stating it (4.2). The "This means that" sentence restates the previous one and merges into it with "so" (4.4). Polish mode also replaces "loses little" with the statement of Theorem 2 under Rule 6. Cleanup mode leaves the claim's strength alone, so "loses little" stays and the report says: "Line 3: 'loses little' is weaker and vaguer than Theorem 2. Consider stating the theorem's result."

## 9. Qualifiers survive the edit (edit discipline, Rules 7 and 10)

Context: Table 3 varies the capture probability, and the text reports no test of performance at low capture probabilities.

Before:
> Our results suggest that the stratified estimator may perform well when the capture probability is low. It is worth noting that this is a pivotal finding.

Wrong:
> Our results show that the stratified estimator performs well when the capture probability is low.

After:
> Our results suggest that the stratified estimator may perform well when the capture probability is low.

What changed: the second sentence carries only announced emphasis and a significance word (Rule 1) and goes, since it adds no claim. "Suggest" and "may" stay because the text has no direct evidence for low capture probabilities, so the uncertainty is real. The wrong version gains confidence by changing the claim, and `compare` lists both lost qualifiers. Example 10 shows the opposite case, where the evidence is in the text and the hedge goes.

## 10. Stance and meta-narrative (Rules 4.9, 7)

Before:
> In this section, we present our main numerical results. Although our approach is only a preliminary attempt and has several limitations, the results may potentially suggest that the stratified estimator could perform better than existing estimators: its mean relative error is 0.8% (standard error 0.1%), compared with 2.9% for the best unstratified estimator (Table 3). To summarize, the stratified estimator performs well.

After:
> Across 1,200 simulated populations, the stratified estimator has a mean relative error of 0.8% (standard error 0.1%), compared with 2.9% for the best unstratified estimator (Table 3).

What changed: the opening sentence describes the section instead of stating a result, and the closing sentence recaps it (4.9). "Only a preliminary attempt" and "has several limitations" apologize without naming a limitation that bounds this result (Rule 7). "May potentially suggest ... could perform better" stacks three hedges on numbers the paper itself reports, so the result reads as a result (Rule 7). The population count comes from Table 3 in the running context. `compare` lists "may" and "suggest" as lost qualifiers and the new number 1,200, and the report records each as intended.

## 11. Coined labels (Rules 2, 6)

Context: Section 4.2 states that each heuristic solution is checked for feasibility and that its objective is recomputed with the exact solver. The text says nothing more about the "robustness layer", and no proposition covers it.

Before:
> Each heuristic solution then passes through our rigorous certification protocol, and a robustness layer filters the remaining candidates, ensuring trustworthy decisions.

After:
> We then check each heuristic solution for feasibility and recompute its objective with the exact solver (Section 4.2). A robustness layer filters the remaining candidates.

Report item: "robustness layer" appears once and is never defined. State the filtering rule it applies, or name the step plainly ("a second filter"). "Robust" asserts a property that no result in the text supports (Rule 6).

What changed: the text states what the "certification protocol" does, so the label becomes those two steps, and "rigorous" goes with it (Rule 1). "Certification" also promised a guarantee the procedure does not give (Rule 6). The text never says what the "robustness layer" does, so the label stays and the report asks the author to define it. Inventing a filtering rule would add content. "Ensuring trustworthy decisions" is a trailing evaluation (Rule 1) and goes. The section number comes from the running context, so the report records the new number 4.2 that `compare` lists as intended. `audit` lists both labels under "no definition or citation", and `compare` on a revision that added a label such as "validation pipeline" would list it as new.

## 12. A proof written as a work log (Rule 11)

Context: the proof of Theorem 2 needs $g(x) \ge 0.37$ on $[0,1]$, where $g$ is defined in (12). The text does not say whether the bound was computed exactly or in floating point. Table 2 reports estimation errors averaged over 200 replications with $n = 500$, and no reported number depends on the solver settings.

Before:
> Our verification pipeline proceeds in three stages. A sanity check confirms that $g(x) > 0$ on $[0,1]$, the residual was below $10^{-12}$, and the certified bound $g(x) \ge 0.37$ holds. We ran `verify_bound.py` with seed 42 for the first run and seed 7 for the second. A jitter of $10^{-8}$ was added to the diagonal, and the safeguard against singular matrices never triggered. The solver tolerance was $10^{-9}$ with an iteration cap of 5000. We report the mean over 200 replications with sample size $n = 500$ (Table 2).

After:
> **Lemma 4.** For all $x \in [0,1]$, $g(x) \ge 0.37$.
>
> *Proof.* We evaluate $g$ on $[0,1]$ by [[EVIDENCE: exact (interval or rational arithmetic) or floating-point computation, and the software used]].
>
> We report the mean over 200 replications with sample size $n = 500$ (Table 2).

Report items:
- Not ready to submit: the placeholder in the proof of Lemma 4 must say how $g$ was evaluated. With exact arithmetic, Lemma 4 is proven. With floating point, it becomes a numerical statement, and Theorem 2 then rests on numerical evidence, which its statement must say.
- Deleted under Rule 11 as intended changes: the residual bound $10^{-12}$ (second sentence), the seeds 42 and 7 and the script name `verify_bound.py` (third), the jitter $10^{-8}$ and the safeguard that never triggered (fourth), and the solver tolerance $10^{-9}$ and iteration cap 5000 (fifth). These belong in the code repository or a reproducibility appendix if the venue asks for them.
- Kept for reproduction: 200 replications and $n = 500$, since Table 2 depends on both.
- Lemma 4 is new. Its statement is the bound the original text asserts. `compare` lists its number and its math as added, and in a `.tex` file it also lists the new lemma environment.

What changed: "verification pipeline", "sanity check", and "certified bound" framed the proof as a run of code (Rule 11), so the bound becomes a lemma with a proof. "Certified" goes because nothing in the text shows an exact computation. "$g(x) > 0$" goes because Lemma 4 implies it. The seeds, jitter, safeguard, tolerance, iteration cap, residual, and script name describe how the code ran, and no reported result depends on them, so each is deleted and listed with its number.
