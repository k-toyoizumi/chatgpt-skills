#!/usr/bin/env python3
"""Offline MULTI-PAGE Pandoc preview of the Quarto source; not a Quarto render.
Usage: python scripts/render_preview.py [/absolute/preview-dir]
"""
from pathlib import Path
from bs4 import BeautifulSoup
import base64, html, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'assets/quarto-book'
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'preview'
CHAPTERS=[BOOK/'index.qmd', *(BOOK/'chapters'/p for p in ('01-attention.qmd','02-attention-mechanics.qmd','03-attention-practice.qmd'))]
if not shutil.which('pandoc'):
    sys.exit('Pandoc CLI is required for offline preview; Quarto build is preferred.')

def to_html(path):
    raw=subprocess.check_output(['pandoc',str(path),'-f','markdown+tex_math_dollars+fenced_divs','-t','html5','--mathml','--wrap=none'],text=True)
    return BeautifulSoup(raw,'html.parser')

pages=[to_html(p) for p in CHAPTERS]
labels={}
for chapter_number,soup in enumerate(pages):
    fcount=tcount=0
    for f in soup.select('figure[id^="fig-"]'):
        fcount+=1;labels[f['id']]=(f'図{chapter_number}.{fcount}',chapter_number)
    for t in soup.select('table'):
        c=t.find('caption')
        if c:
            m=re.search(r'\{#(tbl-[a-z0-9-]+)\}',c.get_text())
            if m:
                tcount+=1;labels[m.group(1)]=(f'表{chapter_number}.{tcount}',chapter_number)

chapter_titles=['はじめに','Self-Attentionの基礎とテンソル形状','Attentionの計算と主要な構成','Attentionの実装・解釈・確認問題']
css='''
:root{--ink:#22354c;--dark:#142d49;--muted:#647b90;--rule:#dde6ee;--blue:#246ba9;--bg:#f6f9fc}
*{box-sizing:border-box}html{scroll-padding-top:76px}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Noto Sans JP",sans-serif;font-size:16px;line-height:1.85}
a{color:var(--blue);text-underline-offset:3px}strong{color:var(--dark)}.header{position:sticky;top:0;z-index:10;min-height:64px;background:#fff;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;align-items:center;padding:10px 24px;gap:10px}.brand{font-weight:800;text-decoration:none;color:var(--dark)}
.shell{display:grid;grid-template-columns:225px minmax(0,800px) 190px;gap:34px;max-width:1330px;margin:auto;padding:0 18px}.sidebar,.toc{position:sticky;top:88px;max-height:calc(100vh - 105px);overflow-y:auto;padding:26px 0}.side-heading{font-size:12px;color:var(--muted);font-weight:800;letter-spacing:.04em}.group>summary{font-weight:750;cursor:pointer;font-size:13px;padding:12px 5px}.side-link{display:block;padding:10px 12px;margin:3px 0;color:#425d78;text-decoration:none;border-radius:8px;font-size:13px;line-height:1.6}.side-link[aria-current=page]{background:#e6f1fc;color:#14558d;font-weight:750}.side-link:hover{background:#eef4fb}.paper{background:white;min-width:0;padding:45px clamp(22px,4vw,54px) 70px;box-shadow:0 0 0 1px #e9eef4;min-height:100vh}.paper h1{font-size:clamp(26px,3vw,37px);line-height:1.4;margin:0 0 28px;color:var(--dark)}.paper h2{margin-top:45px;padding-bottom:12px;border-bottom:1px solid var(--rule);color:var(--dark);font-size:23px}.paper h3{margin-top:30px;color:var(--dark);font-size:18px}.paper p{margin:0 0 21px}.paper figure{margin:32px auto}.paper figure img{display:block;width:100%;height:auto;border:1px solid var(--rule);border-radius:12px;background:#f9fbfe;cursor:zoom-in}.paper figcaption{font-size:13px;color:var(--muted);margin-top:10px}.paper .table-scroll,.paper .tb-table-compact,.paper .tb-table-comparison,.paper .tb-table-wide{overflow-x:auto;max-width:100%;border:1px solid var(--rule);border-radius:9px;margin:22px 0}.paper table{min-width:0;width:auto;table-layout:auto;white-space:normal;border-collapse:collapse;font-size:13px}.paper .tb-table-compact table{width:max-content;min-width:0}.paper .tb-table-compact th,.paper .tb-table-compact td{white-space:nowrap}.paper .tb-table-compact th:not(:first-child),.paper .tb-table-compact td:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}.paper .tb-table-comparison table{width:100%;min-width:0}.paper .tb-table-comparison th,.paper .tb-table-comparison td{white-space:normal;overflow-wrap:anywhere}.paper .tb-table-wide table{min-width:680px}.paper table th,.paper table td{border-bottom:1px solid var(--rule);padding:10px;text-align:left;vertical-align:top}.paper table th{background:#eff5fb}.paper caption{caption-side:bottom;text-align:left;padding:12px;color:var(--muted)}.paper math[display=block]{display:block;max-width:100%;overflow-x:auto;padding:14px 3px;background:#f8fbff}.paper pre{overflow-x:auto;background:#f4f7fb;padding:18px;border-radius:10px;font-size:12px}.paper details.solution{padding:14px;background:#f7fbff;border:1px solid #dae5f0;border-radius:9px;margin:14px 0}.paper details.solution summary{cursor:pointer;font-weight:700}.callout-tip{background:#eff6fc;border-left:3px solid var(--blue);padding:10px 18px;border-radius:8px}.callout-tip h2{font-size:17px;margin:10px 0;border:none}.toc-link{display:block;font-size:12px;padding:8px;color:#586f83;text-decoration:none;border-left:2px solid transparent}.toc-link.h3{padding-left:20px}.toc-link:hover{color:var(--blue);border-left-color:var(--blue)}.chapter-nav{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--rule);margin-top:44px;padding-top:20px}.notice{font-size:11px;color:var(--muted);border-top:1px solid var(--rule);margin-top:30px;padding-top:14px}.mobile-nav{display:none}.mobile-nav summary{cursor:pointer;color:var(--dark);font-weight:750}.mobile-inner{padding:14px;background:#fff;border:1px solid var(--rule);position:absolute;top:60px;left:10px;right:10px;box-shadow:0 9px 28px #1b345c22;max-height:70vh;overflow-y:auto}.preview-zoom{max-width:95vw;width:950px;max-height:92vh;border-radius:12px;border:1px solid #abc;padding:12px;overflow:auto}.preview-zoom::backdrop{background:#10283bc4}.preview-zoom img{display:block;width:100%;min-width:640px}.preview-zoom button{position:sticky;left:100%;top:0;cursor:pointer}
@media(max-width:1199px){.shell{grid-template-columns:210px minmax(0,800px);max-width:1060px}.toc{display:none}}
@media(max-width:820px){.shell{display:block;padding:0}.sidebar{display:none}.mobile-nav{display:block}.header{min-height:60px;padding:10px 18px}.paper{min-height:0;padding:28px 22px 60px}.paper h1{font-size:29px}.paper h2{font-size:21px;margin-top:37px}.paper figure{margin:24px 0}}
@media(max-width:380px){.paper{padding:26px 16px}.brand{font-size:13px}body{font-size:15px}}
'''
script='''
(()=>{const zoom=document.getElementById('preview-zoom');const zoomImg=zoom.querySelector('img');
document.querySelectorAll('.paper figure img').forEach(img=>{img.tabIndex=0;img.setAttribute('role','button');img.addEventListener('click',()=>{zoomImg.src=img.src;zoom.showModal()});img.addEventListener('keydown',e=>{if(e.key==='Enter'){zoomImg.src=img.src;zoom.showModal()}})});
zoom.querySelector('button').addEventListener('click',()=>zoom.close());})();
'''

def link(src_idx,dest_idx):
    p0=Path('index.html') if src_idx==0 else Path('chapters')/(CHAPTERS[src_idx].stem+'.html')
    p1=Path('index.html') if dest_idx==0 else Path('chapters')/(CHAPTERS[dest_idx].stem+'.html')
    return ('../' if src_idx>0 else '')+str(p1) if src_idx==0 or dest_idx==0 else p1.name

for idx,(path,soup) in enumerate(zip(CHAPTERS,pages)):
    for fig in soup.select('figure[id^="fig-"]'):
        number=labels[fig['id']][0]
        cap=fig.find('figcaption')
        if cap:cap.insert(0,number+'：')
    for t in soup.select('table'):
        cap=t.find('caption')
        if not cap: continue
        m=re.search(r'\{#(tbl-[a-z0-9-]+)\}',cap.get_text())
        if not m:continue
        key=m.group(1);t['id']=key
        cap.string=labels[key][0]+'：'+cap.get_text().replace('{#'+key+'}','').strip()
        wrap=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'表（左右にスクロール可能）'})
        t.wrap(wrap)
    for c in soup.select('.citation[data-cites]'):
        keys=c.get('data-cites','').split()
        if len(keys)!=1 or keys[0] not in labels:continue
        number,dest=labels[keys[0]]
        a=soup.new_tag('a',href=link(idx,dest)+'#'+keys[0],attrs={'class':'crossref'})
        a.string=number
        c.replace_with(a)
    for img in soup.find_all('img'):
        f=(path.parent/img.get('src','')).resolve()
        if not f.is_relative_to(BOOK.resolve()) or not f.is_file():raise ValueError(f'broken media: {f}')
        img['src']='data:image/svg+xml;base64,'+base64.b64encode(f.read_bytes()).decode()
        img['loading']='lazy'
    for a in soup.select('a[href$=".qmd"]'):
        dest=a.get('href')
        dest_path=(path.parent/dest).resolve()
        if dest_path not in [p.resolve() for p in CHAPTERS]:raise ValueError(f'unlisted QMD link {dest}')
        a['href']=link(idx,[p.resolve() for p in CHAPTERS].index(dest_path))
    for d in soup.select('details'):d['class']='solution'
    sections=[]
    for h in soup.select('h2,h3'):
        if h.find_parent(class_='callout-tip'):continue
        if not h.get('id'):h['id']='heading-'+str(len(sections)+1)
        sections.append((h.get_text(' ',strip=True),h['id'],h.name))
    toc=''.join(f'<a class="toc-link {typ}" href="#{html.escape(anchor,quote=True)}">{html.escape(name)}</a>' for name,anchor,typ in sections)
    side_links=''.join(f'<a class="side-link" {"aria-current=page" if j==idx else ""} href="{link(idx,j)}">{j}. {html.escape(title)}</a>' for j,title in enumerate(chapter_titles) if j>0)
    nav=f'<a class="side-link" {"aria-current=page" if idx==0 else ""} href="{link(idx,0)}">はじめに</a><details class="group" open><summary>Transformer と Attention</summary>{side_links}</details>'
    prev=f'<a href="{link(idx,idx-1)}">← 前の章</a>' if idx else '<span></span>'
    nxt=f'<a href="{link(idx,idx+1)}">次の章 →</a>' if idx<len(CHAPTERS)-1 else '<span></span>'
    if soup.h1:soup.h1.decompose()
    body=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(chapter_titles[idx])} — 図解で学ぶAIの理論</title><style>{css}</style></head><body>
<header class="header"><a class="brand" href="{link(idx,0)}">図解で学ぶAIの理論</a><details class="mobile-nav"><summary>☰ 章を選択</summary><nav class="mobile-inner" aria-label="スマホの章一覧">{nav}</nav></details></header>
<div class="shell"><aside class="sidebar" aria-label="章一覧"><p class="side-heading">章を選択</p>{nav}</aside>
<main class="paper"><h1>{html.escape(chapter_titles[idx])}</h1><article>{soup}</article><div class="chapter-nav">{prev}{nxt}</div><div class="notice">これはPandocによる複数ページ試作です。Quartoの正式なレンダリングではありません。</div></main>
<aside class="toc" aria-label="現在のページ内目次"><p class="side-heading">このページ</p>{toc}</aside></div>
<dialog class="preview-zoom" id="preview-zoom" aria-label="図を拡大"><button type="button" aria-label="閉じる">閉じる ×</button><img alt="拡大図"></dialog><script>{script}</script></body></html>'''
    out=OUT/('index.html' if idx==0 else f'chapters/{path.stem}.html')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(body,encoding='utf8')
    print('WROTE',out,len(soup.select('figure')),len(soup.select('table')))
print('OFFLINE MULTI-PAGE PREVIEW ONLY. Quarto render has not been tested.')
