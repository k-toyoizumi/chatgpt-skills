#!/usr/bin/env python3
"""Browser regression for textbook table CSS using semantic fixture tables.

This validates CSS in Chromium; it does NOT replace Quarto or Pandoc output QA.
"""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "assets/quarto-book/styles.css").read_text(encoding="utf-8")
assert "min-width:540px" not in CSS, "Legacy global minimum width still present"

HTML = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
* {box-sizing:border-box}
body {margin:0}
main {width:min(100%,760px);margin:0 auto;padding:16px}
</style></head><body><main id="quarto-document-content">
<div class="tb-table-compact" aria-label="短い利得行列">
<table><thead><tr><th>自分の行動</th><th>相手：防御</th><th>相手：仕掛け</th></tr></thead>
<tbody><tr><td>攻撃</td><td>+2</td><td>-1</td></tr>
<tr><td>待機</td><td>0</td><td>+1</td></tr></tbody></table>
<p>行＝自分、列＝相手の行動。数値は自分の利得（点）。</p></div>
<div class="tb-table-comparison" aria-label="文章の多い比較表">
<table><thead><tr><th>方式</th><th>強み</th><th>制約</th></tr></thead>
<tbody><tr><td>方式A</td>
<td>学習時に複数の情報源を統合することにより幅広い応用分野で一定の精度を得やすい</td>
<td>計算資源が限られると実装や推論のコストが高くなりやすい</td></tr></tbody></table></div>
<div class="tb-table-wide" aria-label="多列の表">
<table><thead><tr><th>ケース</th><th>列1</th><th>列2</th><th>列3</th><th>列4</th><th>列5</th><th>列6</th></tr></thead>
<tbody><tr><td>例</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr></tbody></table></div>
</main></body></html>"""
HTML = HTML.replace("</style>", "\n" + CSS + "\n</style>")

def check_column_boundaries(page, selector):
    sizes = page.locator(selector).evaluate("""table => {
      const head = [...table.tHead.rows[0].cells];
      const row = [...table.tBodies[0].rows[0].cells];
      return head.map((el,i) => {
        const h=el.getBoundingClientRect(), d=row[i].getBoundingClientRect();
        return {left:Math.abs(h.left-d.left),right:Math.abs(h.right-d.right)};
      });
    }""")
    assert all(x["left"] < 1.2 and x["right"] < 1.2 for x in sizes), sizes

with sync_playwright() as pw:
    executable = shutil.which("chromium") or shutil.which("chromium-browser")
    browser = pw.chromium.launch(
        headless=True, executable_path=executable, args=["--no-sandbox"]
    ) if executable else pw.chromium.launch(headless=True)
    try:
        for width in (375, 768, 1280):
            page = browser.new_page(viewport={"width":width,"height":850})
            page.set_content(HTML, wait_until="load")
            headings = page.locator(".tb-table-compact th").all_inner_texts()
            assert headings == ["自分の行動", "相手：防御", "相手：仕掛け"], headings
            check_column_boundaries(page, ".tb-table-compact table")
            check_column_boundaries(page, ".tb-table-comparison table")
            vals = page.evaluate("""() => {
                const main = document.querySelector('main');
                const compact = document.querySelector('.tb-table-compact table');
                const comp = document.querySelector('.tb-table-comparison table');
                const wide = document.querySelector('.tb-table-wide');
                return {
                    mainWidth:main.clientWidth,
                    compactWidth:compact.getBoundingClientRect().width,
                    compareWidth:comp.getBoundingClientRect().width,
                    wideOverflow:wide.scrollWidth>wide.clientWidth+1,
                    pageOverflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1
                };
            }""")
            assert not vals["pageOverflow"], (width, vals)
            if width == 1280:
                assert vals["compactWidth"] < vals["mainWidth"]*0.85, vals
                assert vals["compareWidth"] >= vals["mainWidth"]*0.90, vals
            if width == 375:
                assert vals["wideOverflow"], vals
            page.close()
            print(f"PASS table CSS {width}px: aligned boundaries; intrinsic/long/wide layouts")
    finally:
        browser.close()
print("NOTE: Quarto official rendering and alternative-renderer visual QA are separate checks.")
