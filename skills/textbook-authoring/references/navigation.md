# Navigation and page architecture (mandatory)

## Default for all books

- A **Quarto Book** must have an `index.qmd` landing page and **one `.qmd` file per substantive chapter**. No monolithic scrolling HTML for an entire multi-chapter course.
- Put all navigable pages in `book.chapters` in `_quarto.yml`; use a named `part` containing `chapters` to group related chapters. Do not list unpublished placeholders.
- Desktop layout: **left docked chapter sidebar**, center article, **right within-page table of contents**. Use Quarto native `book.sidebar`, `format.html.toc`, and `toc-location: right` rather than custom navigation JavaScript.
- With multiple chapters under a part, set `book.sidebar.collapse-level: 1` or another justified default so groups can be expanded/collapsed. Ensure the active chapter is distinguishable.
- Mobile: Quarto's responsive navigation collapses the left sidebar into a touch-friendly chapter menu. Do not force the desktop sidebar to remain visible on narrow viewports. Right TOC may collapse/hide at smaller widths.
- Enable `book.page-navigation: true` for next/previous chapter links. Preserve heading-anchor navigation and `@fig-*` / `@tbl-*` crossrefs **across pages**, not merely within a chapter.
- Each page should cover a coherent topic rather than mechanically cutting at a word count. If a chapter is extremely long, consider splitting it into pedagogically meaningful chapters only if chapter boundaries make sense.

## Quarto config example

```yaml
project:
  type: book
book:
  title: "図解で学ぶAIの理論"
  page-navigation: true
  sidebar:
    style: docked
    collapse-level: 1
    pinned: true
  chapters:
    - index.qmd
    - part: "Transformer と Attention"
      chapters:
        - chapters/01-attention.qmd
        - chapters/02-attention-mechanics.qmd
        - chapters/03-attention-practice.qmd
format:
  html:
    toc: true
    toc-location: right
    toc-title: "このページ"
    toc-depth: 3
```

## Quality requirements

1. `quarto render` yields one HTML page per listed `.qmd`; verify page count and navigation links from `index.html` to at least two chapters.
2. Test mobile menu open/close, active-page indication, part collapse/expand, chapter links and right-page TOC where the viewport allows it.
3. Check internal links, including refs across chapters, and next/previous page links.
4. The included `render_preview.py` is a **Pandoc-only offline approximation** for environments without Quarto, not evidence of Quarto-native behavior. Its UI can differ from Quarto's.
