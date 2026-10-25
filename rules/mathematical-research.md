# Mathematical research: evidence, verification, and publication

Applies to mathematical discovery, conjectures, computational searches, proof audits, and eventual publication.

For exploration versus rigorous verification, follow `rules/research.md`. During discovery, prioritize questions, definitions, examples and conjectures; choose formalization work when it helps select a direction or verify an agreed claim. Preserve the claim and evidence standards below in every phase.

- Separate **precise mathematical correctness**, **formal verification**, **novelty**, and **publication significance**. Never infer one from another.
- State the exact quantified proposition, domain, assumptions, definitions, and whether it is conjectural.
- Keep reproducible experiments, bounded search results, failed approaches, and literature citations. Finite checks do not prove universal statements.
- Do not label a mathematical claim **Lean-verified** without checking the actual Lean source and a successful compiler/CI run for the corresponding commit. No `sorry`, `admit`, or unsupported extra axioms in the relevant proof. Check imported assumptions and trusted axioms when important.
- A formally verified transcription of an equation does **not** establish that a published paper contains that equation: inspect the source and context independently.
- A detected error in an example does not automatically refute the theorem or conjecture.
- Compare prior literature and possible errata before claiming novelty or alleging an error.
- Preserve unsuccessful attempts with an explanation; do not present provisional hypotheses as theorems.
- When a result is significant, promote it to a paper candidate only after correctness, novelty and relevance have been assessed independently.
- Cite exact code revisions, successful CI run URLs, and sources. If a tool is unavailable or execution failed, report the limitation rather than inventing completion.
- Store project-specific research notes, paper drafts, repository URLs and ongoing status **in the project repository**, not this reusable rule.
- Follow the user's explicit instructions and the existing shared interaction rules for major decisions.
