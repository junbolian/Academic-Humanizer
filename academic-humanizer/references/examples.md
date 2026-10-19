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
