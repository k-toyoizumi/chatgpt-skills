#!/usr/bin/env python3
"""Test multipage offline preview in Chromium; does not validate Quarto rendering."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'preview'
files=[ROOT/'index.html',ROOT/'chapters/01-attention.html',ROOT/'chapters/02-attention-mechanics.html',ROOT/'chapters/03-attention-practice.html']
for file in files: assert file.is_file(),f'Preview missing: {file}'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    try:
        for width,height in [(320,740),(390,844),(768,1024),(1440,950)]:
            page=browser.new_page(viewport={'width':width,'height':height})
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            for ci,path in enumerate(files):
                page.set_content(path.read_text(encoding='utf8'),wait_until='load')
                metrics=page.evaluate('({cw:document.documentElement.clientWidth,sw:document.documentElement.scrollWidth})')
                assert metrics['cw']==metrics['sw'],(width,ci,metrics)
                assert page.locator('.paper h1').count()==1
                assert page.locator('.sidebar .side-link').count()==4
                assert page.locator('.sidebar .side-link[aria-current="page"]').count()==1
                assert page.locator('.mobile-nav .side-link[aria-current="page"]').count()==1
                page.locator('figure img').evaluate_all('async imgs => {for(const img of imgs){img.loading="eager";await img.decode()}}')
                for img in page.locator('figure img').all():
                    assert img.evaluate('(e)=>e.complete && e.naturalWidth>0'), (ci,'broken image')
                assert page.locator('figure').count()==[0,2,3,0][ci]
                assert page.locator('table[id^="tbl-"]').count()==[0,0,1,0][ci]
                for a in page.locator('a.crossref').all():
                    href=a.get_attribute('href');assert href and '#' in href
                    target=(path.parent/href.split('#')[0]).resolve() if href.split('#')[0] else path
                    assert target.is_file(),href
                    assert 'id="'+href.split('#')[1]+'"' in target.read_text(), href
                assert page.locator('.toc .toc-link').count()>0
                if width<=820:
                    assert page.locator('.mobile-nav').is_visible()
                    assert not page.locator('.sidebar').is_visible()
                    assert not page.locator('.toc').is_visible()
                    page.locator('.mobile-nav > summary').click()
                    assert page.locator('.mobile-inner').is_visible()
                    page.locator('.mobile-nav > summary').click()
                elif width==1440:
                    assert page.locator('.sidebar').is_visible()
                    assert page.locator('.toc').is_visible()
                    page.locator('.sidebar .group summary').click()
                    assert not page.locator('.sidebar .group').evaluate('(e)=>e.open')
                    page.locator('.sidebar .group summary').click()
                    assert page.locator('.sidebar .group').evaluate('(e)=>e.open')
                assert not errors,errors
            # Navigation targets are checked on disk because this browser cannot
            # navigate to local file:// or localhost URLs (administrator policy).
            page.set_content(files[0].read_text(encoding='utf8'),wait_until='load')
            links=page.locator('.sidebar .side-link')
            assert links.nth(2).get_attribute('href')=='chapters/02-attention-mechanics.html'
            assert files[2].is_file() and files[2].read_text(encoding='utf8').find('Attentionの計算')>=0
            if width==1440:
                page.set_content(files[2].read_text(encoding='utf8'),wait_until='load')
                page.screenshot(path=str(ROOT/'desktop-navigation.png'),full_page=False)
            if width==390:
                page.locator('.mobile-nav > summary').click()
                page.screenshot(path=str(ROOT/'mobile-navigation.png'),full_page=False)
            page.close()
            print(f'PASS {width}px: 4 pages, chapter links, responsive sidebar, collapsible part, TOC, figures and tables')
    finally:
        browser.close()
