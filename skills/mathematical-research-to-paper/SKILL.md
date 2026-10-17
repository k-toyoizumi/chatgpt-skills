---
name: mathematical-research-to-paper
description: Use for sustained mathematical research where hypotheses, Lean proofs, computational evidence, literature novelty checks, and potential papers should be accumulated reproducibly.
metadata:
  short-description: 数学研究の記録・形式検証・論文化
---

# Mathematical research → research notebook → paper candidate

Read [mathematical-research rule](../../rules/mathematical-research.md) and, for open research-direction choices, the existing `research-dialogue` skill. Use `research-survey` for literature searches. Do not repeat interview questions already settled.

## 1. Research record
Create a dated note **in the relevant project repository**, with: research question, precise claim and quantifiers, assumptions, motivation, derivation, status, experimental bounds, references, failed attempts, limitations and next test. Do not erase failed work.

## 2. Independent verification
- Reproduce arithmetic and computational experiments with explicit commands and versions.
- For important new proofs or alleged errors, write a Lean 4 proof, include it in the project CI build, and inspect the **successful CI log** at the relevant commit.
- Record exact Lean file, commit SHA, CI run URL and proof scope. If not compiled, label **not Lean-verified**.
- Check for `sorry`, `admit`, custom axioms, hidden assumptions, and mismatches between natural-language statements and Lean formalization.
- For audits of papers, check transcription, definitions, equation numbers, errata, and intended meaning separately.

## 3. Novelty and significance
Search authoritative original literature and related results. Record what is already known, what differs, and uncertainty. A correct proof may be previously known or too small for a standalone paper.

## 4. Promotion to a paper candidate
Only promote when a complete precise result, trustworthy proof, literature comparison and meaningful contribution exist. Draft a LaTeX paper with: introduction, related work, notation, main theorem, proof, examples or computation, limitations, references and reproducibility appendix. The user decides whether to submit or publicly announce.

## 5. Completion report
Report independently: (a) verified mathematics, (b) Lean CI status, (c) novelty review, (d) paper readiness, (e) next unresolved question. Link actual artifacts and never claim external writes or successful builds without evidence.

## Suggested project layout (not a fixed requirement)
`research/` dated notes and templates; `proofs/` Lean files; `experiments/` reproducible code; `paper-candidates/` mature outlines and LaTeX drafts.

## Publication safety
Do not treat numerical anomalies alone as a refutation. Clearly distinguish an internal audit from a publicly established correction, and preserve accurate attribution.
