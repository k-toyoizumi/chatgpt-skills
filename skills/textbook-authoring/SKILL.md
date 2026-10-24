---
name: textbook-authoring
description: 日本語のHTML教科書・学習教材をQuartoで計画、制作、改訂、検証する。概念の静的な図解、研究者向けの数式と手計算例、実装、理解度問題、章構成と品質チェックを含む依頼に使う。
---

# Textbook Authoring — v0.3

## Mission
Generate **accurate, diagram-led, low-motion** Japanese HTML textbooks, with Quarto as canonical source and a consistent educational structure. Apply in ChatGPT or Codex; avoid environment-specific commands inside the Skill itself.

## Before writing
1. Read `references/pedagogy.md`, `references/diagrams.md`, `references/tables.md`, and `references/quality.md`.
2. Reuse already-agreed preferences: audience, theme, depth, project format, diagram style, scope. Ask only about decisions that genuinely change the output; obey the user's preferred interview workflow if choices remain.
3. Define learning outcomes for each chapter; choose the smallest set of figures that materially improves conceptual comprehension. For each figure write its **learning purpose**, **what it omits**, and **caption**, before constructing it.

## Authoring workflow
1. Use `assets/quarto-book/` as the source template. The editable source is `.qmd`; book navigation lives in `_quarto.yml`.
2. Structure the chapter: why this matters → mental model and diagrams → formal notation/equations → verified worked numerical example → relevant implementation → misconceptions/boundaries → exercises with explanations → primary references.
3. Use static SVG for tensor geometry, ratios, numerical weights, and detailed conceptual illustrations. Use Mermaid for small, simple graphs if that helps. Only use generated illustrations if precise SVG would obscure a genuinely spatial/visual concept; **no automatic decorative animations**.
4. Number every figure/table automatically with Quarto IDs (`fig-...` / `tbl-...`) and cite it through `@fig-...` / `@tbl-...` in prose. Do not manually hardcode numbers. Use comparison tables when axes and assumptions are aligned.
5. Ensure figure accessibility: distinct visible labels (not color alone), alt, caption, reference from text, accuracy and limitations. Narrow viewport must keep labels legible; zoom or scroll is preferable to minuscule labels.
6. Expand technical acronyms on first mention. Each important formula needs symbol dimensions, assumptions, row/column orientation, and an explicit connection to at least one diagram or worked calculation. For claims, cite reliable primary sources; don't invent results or dates.
7. Include at least two exercises with answers and likely misconceptions. Distinguish toy examples from actual trained-model observations. Avoid asserting that attention weights are necessarily causal explanations.

## Build and validation
1. Run `python scripts/validate.py`, `python scripts/test_numeric.py` when scientific dependencies are present.
2. Prefer `quarto render` in `assets/quarto-book` when Quarto CLI is available; inspect the generated book in Chromium/Playwright at desktop and 390px mobile width. Record whether it *actually* succeeded.
3. If Quarto is not present, `python scripts/render_preview.py /path/to/preview.html` can produce a Pandoc-generated, offline **single-file preview**, but this is **not proof of Quarto rendering**. Run browser visual tests on the preview, note this distinction in the report.
4. Verify equations, figure values, numbered figure/table captions, clickable figure/table cross-references, source links, no broken media, no unwanted page overflow, and figure/table readability. Browser tests cannot replace technical fact checking.
5. Report PASS / FAIL / NOT RUN separately for static checks, numerical checks, HTML preview rendering, browser QA, and Quarto rendering.

## Composition with optional external Skills
- `frontend-design`: style, typography, responsive CSS; can be omitted.
- `visual-explainer`: exceptional complicated diagrams; can be omitted.
- Source/language/tool licensing must be checked before copying code. Skill works without installing these.
- ChatGPT automatic custom-Skill registration depends on supported product features; if unavailable, the SKILL.md and references can be supplied manually to ChatGPT, while Codex reads `.agents/skills/textbook-authoring/`.

## Outputs
- Editable `.qmd`, config, CSS, SVGs; plus built HTML or clearly labeled offline preview.
- Source evidence, QA report, unresolved limitations.
- Preserve source files and git-friendly structure; don't modify user's repository without explicit authorization.
