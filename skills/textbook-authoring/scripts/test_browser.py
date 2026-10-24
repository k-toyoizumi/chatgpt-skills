#!/usr/bin/env python3
"""Smoke test the Pandoc offline preview in local Chromium without file:// navigation."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
html=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'assets/quarto-book/attention-preview.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    try:
        for width,height in [(320,740),(390,844),(768,1024),(1440,950)]:
            page=browser.new_page(viewport={'width':width,'height':height})
            errors=[]
            page.on('pageerror', lambda err:errors.append(str(err)))
            page.set_content(html,wait_until='load')
            page.locator('figure img').evaluate_all('async imgs => {for(const img of imgs){img.loading="eager";await img.decode()}}')
            metrics=page.evaluate('({clientWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth})')
            assert metrics['scrollWidth']==metrics['clientWidth'], (width,metrics)
            assert page.locator('figure img').count()==5
            assert page.locator('figure figcaption').count()==5
            assert page.locator('table[id^=tbl-]').count()==1
            assert page.locator('table caption').first.inner_text().startswith('表1.1')
            assert page.locator('figure figcaption').first.inner_text().startswith('図1.1')
            assert page.locator('a.crossref[href^=\"#fig-\"]').count()==5
            assert page.locator('a.crossref[href^=\"#tbl-\"]').count()==1
            assert page.locator('.citation[data-cites^=fig-], .citation[data-cites^=tbl-]').count()==0
            assert page.locator('math').count()>20
            assert page.locator('details').count()==4
            assert page.locator('figure img').evaluate_all('(imgs)=>imgs.every(x=>x.naturalWidth>0)')
            assert not errors,errors
            page.locator('figure img').first.click()
            assert page.locator('#zoom-dialog').evaluate('(d)=>d.open')
            page.locator('.close-zoom').click()
            assert not page.locator('#zoom-dialog').evaluate('(d)=>d.open')
            page.locator('details summary').first.click()
            assert page.locator('details').first.evaluate('(d)=>d.open')
            print(f'PASS browser {width}px: numbered figures=5, numbered tables=1, links=6, overflow=0, exercises=4, zoom=works')
            page.close()
    finally:
        browser.close()
