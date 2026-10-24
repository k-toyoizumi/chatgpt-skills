#!/usr/bin/env python3
"""Build an offline, single-file, static preview using Pandoc when Quarto isn't installed.
This is *not* a Quarto render and does not validate Quarto-specific build behavior.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import base64, html, re, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT/'assets/quarto-book'
CHAPTER = BOOK/'chapters/01-attention.qmd'
OUT= Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BOOK/'attention-preview.html'
if not shutil.which('pandoc'):
    sys.exit('Pandoc CLI required for offline preview')
raw = subprocess.check_output(['pandoc',str(CHAPTER),'-f','markdown+tex_math_dollars+fenced_divs','-t','html5','--mathml','--wrap=none'], text=True)
soup=BeautifulSoup(raw,'html.parser')
# The standalone preview has its own hero; suppress duplicated QMD heading and metadata.
if soup.h1: soup.h1.decompose()
first_para=soup.find('p')
if first_para and '想定学習時間' in first_para.get_text(): first_para.decompose()
# Quarto handles auto-numbering, but Pandoc alone does not. Simulate it only
# for the offline preview. Keep Quarto-source refs canonical and never hardcode.
number_map = {}
for i, fig in enumerate(soup.find_all('figure'), start=1):
    fid = fig.get('id', '')
    if not fid.startswith('fig-'):
        raise ValueError(f'figure lacks Quarto label: {fid!r}')
    number_map[fid] = f'図1.{i}'
    caption = fig.find('figcaption')
    if caption:
        caption['aria-hidden'] = 'false'
        caption.insert(0, number_map[fid] + '：')
for i, table in enumerate(soup.find_all('table'), start=1):
    caption = table.find('caption')
    if not caption:
        raise ValueError('table caption missing')
    label = re.search(r'\s*\{#(tbl-[a-z0-9-]+)\}\s*$', caption.get_text())
    if not label:
        raise ValueError('table lacks Quarto tbl-* label')
    table_id = label.group(1)
    caption.string = re.sub(r'\s*\{#tbl-[a-z0-9-]+\}\s*$', '', caption.get_text()).strip()
    table['id'] = table_id
    number_map[table_id] = f'表1.{i}'
    caption.insert(0, number_map[table_id] + '：')
    # Horizontal scroll only within the table, never at page level.
    wrap = soup.new_tag('div', attrs={'class':'table-scroll','role':'region', 'aria-label':number_map[table_id] + ' 比較表', 'tabindex':'0'})
    table.wrap(wrap)
for cite in soup.select('.citation[data-cites]'):
    ids = cite.get('data-cites', '').split()
    if len(ids) == 1 and ids[0].startswith(('fig-', 'tbl-')):
        target = ids[0]
        if target not in number_map:
            raise ValueError(f'broken cross-reference: {target}')
        a = soup.new_tag('a', href='#'+target, attrs={'class':'crossref'})
        a.string = number_map[target]
        cite.replace_with(a)
# Embed SVG as data URIs for fully portable offline HTML.
for img in soup.find_all('img'):
    path=(CHAPTER.parent/img['src']).resolve()
    if not path.is_relative_to(BOOK.resolve()) or not path.exists():
        raise ValueError(f'bad image: {path}')
    if path.suffix=='.svg':
        img['src']='data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode()
    img['loading']='lazy'
# Improve a11y: figure descriptions are intrinsic SVG titles, with visible captions.
for figure in soup.find_all('figure'):
    img=figure.find('img')
    if img:
        img['class']='zoomable'
        img['tabindex']='0'
        img['role']='button'
        img['aria-label']='図を拡大表示：'+img.get('alt','図')
        img['title']='クリックすると拡大表示します'

for details in soup.select('details'):
    details['class']='solution'
sections=[]
for h in soup.find_all(['h2','h3']):
    if h.find_parent('section', class_='callout-tip'):
        continue
    if not h.get('id'):
        h['id']=f'section-{len(sections)+1}'
    sections.append(dict(title=h.get_text(' ',strip=True), id=h['id'],level=h.name))
items='\n'.join(f'<a class="toc-link level-{s["level"]}" href="#{html.escape(s["id"],quote=True)}">{html.escape(s["title"])}</a>' for s in sections)
content=str(soup)
css='''
:root{--ink:#22354c;--dark:#142d49;--muted:#6b7c8c;--rule:#dde6ef;--blue:#246ba9;--nav:#52677f;--paper:#fff;--bg:#f5f8fb}
*{box-sizing:border-box}html{scroll-behavior:auto;scroll-padding-top:42px}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Noto Sans JP","Noto Sans CJK JP",sans-serif;font-size:16px;line-height:1.91;-webkit-font-smoothing:antialiased;letter-spacing:.005em}
a{color:var(--blue);text-underline-offset:3px;text-decoration-thickness:1px}a:hover{text-decoration-thickness:2px}strong{color:#193653}
.sitehead{background:#fff;border-bottom:1px solid var(--rule);height:68px;padding:0 clamp(20px,3.2vw,52px);display:flex;align-items:center;justify-content:space-between;gap:16px;position:sticky;top:0;z-index:10}
.logo{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--dark);font-weight:800;font-size:15px;letter-spacing:-.01em}.logo-mark{display:grid;place-items:center;background:#1d527e;color:#fff;font-size:16px;width:34px;height:34px;border-radius:9px}.headmeta{font-size:12px;color:var(--muted);border:1px solid var(--rule);padding:6px 12px;border-radius:99px}
.shell{display:grid;grid-template-columns:230px minmax(0,840px) 216px;column-gap:clamp(22px,2.7vw,48px);max-width:1438px;margin:auto;padding:0 25px;justify-content:center}.leftnav,.rightnav{position:sticky;top:100px;height:calc(100vh - 130px);overflow:auto;padding-top:38px;scrollbar-width:thin}.leftnav{padding-right:14px}.rightnav{padding-left:8px}.navlabel{font-size:11px;font-weight:800;color:#8292a0;letter-spacing:.1em;margin:0 0 18px;text-transform:uppercase}.sideintro{font-size:13px;line-height:1.7;color:var(--muted);margin-bottom:26px}.sideitem{display:block;padding:11px 12px;font-size:13px;color:#51677c;text-decoration:none;border-radius:9px;margin:4px 0}.sideitem.active{background:#e6f0fa;font-weight:750;color:#205e96}.sidenote{margin-top:28px;border-top:1px solid var(--rule);padding-top:18px;font-size:12px;color:var(--muted);line-height:1.7}
.paper{min-width:0;background:#fff;padding:52px clamp(23px,4vw,61px) 100px;box-shadow:0 0 0 1px #e8edf3;min-height:100vh}.eyebrow{color:#2c6b9a;letter-spacing:.15em;font-size:11px;font-weight:800;margin-bottom:20px;text-transform:uppercase}.chapterhead{border-bottom:1px solid var(--rule);margin-bottom:30px;padding-bottom:29px}.paper h1{font-size:clamp(29px,3vw,40px);line-height:1.35;letter-spacing:-.035em;font-weight:790;margin:0 0 18px;color:var(--dark)}.lead{font-size:14px;line-height:1.8;color:var(--muted)}.article h1{display:none}.article h2{font-size:clamp(21px,2vw,25px);line-height:1.52;margin:67px 0 23px;color:var(--dark);letter-spacing:-.025em;font-weight:780;padding-bottom:12px;border-bottom:1px solid var(--rule)}.article h3{font-size:19px;margin:42px 0 17px;color:var(--dark);line-height:1.5}.article p{margin:0 0 22px}.article ul,.article ol{padding-left:1.6em;margin:0 0 20px}.article li{padding-left:4px;margin:7px 0}.article figure{margin:30px 0 37px}.article figure img{display:block;width:100%;height:auto;cursor:zoom-in;border:1px solid #e4ebf2;border-radius:13px;background:#f7fafc}.article figcaption{color:#748598;font-size:12px;line-height:1.7;margin-top:11px}/* Numbered comparison tables */
.article .table-scroll{width:100%;overflow-x:auto;margin:28px 0 34px;border:1px solid #e0e7ef;border-radius:11px;overscroll-behavior-x:contain}
.article table{width:100%;min-width:590px;border-collapse:collapse;font-size:13px;line-height:1.65;margin:0}
.article table caption{caption-side:bottom;text-align:left;padding:10px 13px;color:#64788b;font-size:12px;line-height:1.5}
.article th,.article td{padding:11px 12px;border-bottom:1px solid #e2e9f0;vertical-align:top}
.article thead th{font-weight:750;background:#ecf3fa;color:#183853;text-align:left}
.article tbody tr:nth-child(even){background:#f7fafc}
.article tbody tr:last-child td{border-bottom:0}
.article .crossref{white-space:nowrap;font-weight:650}
.article .callout-tip{background:#eef5fb;border:1px solid #d5e5f2;border-left:4px solid #4f91c8;padding:18px 24px;border-radius:11px;margin:28px 0 34px}.article .callout-tip h2{border:0;margin:0 0 11px;padding:0;font-size:16px}.article .callout-tip ul{margin:0;font-size:14px}.article .callout-tip li{margin:4px 0}
.article math[display=block]{display:block;overflow-x:auto;overflow-y:hidden;max-width:100%;padding:19px 10px;margin:12px 0 25px;background:#f8fafc;border-radius:9px}.article math[display=inline]{font-size:1.05em}.article .sourceCode{margin:20px 0}.article pre{overflow-x:auto;background:#f1f5fa;color:#18334c;border:1px solid #e0e7ef;border-radius:12px;padding:18px;font-size:12.5px;line-height:1.75;tab-size:4}.article code{font-family:ui-monospace,SFMono-Regular,Consolas,"Noto Sans Mono CJK JP",monospace}.article p code{background:#edf3f8;padding:2px 5px;border-radius:5px}.article details{padding:13px 18px;margin:10px 0 20px;background:#f7fbff;border:1px solid #d8e5f2;border-radius:11px}.article details summary{font-weight:700;color:#246ba9;cursor:pointer}.article details[open] summary{margin-bottom:14px}.article details p:last-child{margin-bottom:0}.toc-link{display:block;text-decoration:none;color:#718093;font-size:12px;line-height:1.55;padding:9px 12px;border-left:2px solid transparent}.toc-link:hover{color:var(--blue);background:#ecf3f9}.toc-link.level-h3{padding-left:23px;font-size:11px}.toc-link.on{border-left-color:#357bae;color:#266699;font-weight:750}.foot{border-top:1px solid var(--rule);margin-top:45px;padding-top:25px;font-size:12px;color:var(--muted)}dialog.figure-dialog{width:min(96vw,1150px);max-width:96vw;max-height:92vh;padding:13px;border:1px solid #aebfcd;border-radius:12px;background:white;box-shadow:0 18px 50px #0b243e44;overflow:auto}dialog.figure-dialog::backdrop{background:#14283ccb}dialog.figure-dialog img{display:block;width:100%;min-width:650px;height:auto}dialog.figure-dialog .close-zoom{position:sticky;left:100%;top:0;padding:8px 12px;background:#17385b;color:#fff;border:0;border-radius:7px;cursor:pointer;font-size:14px;z-index:2}.zoomhint{color:var(--muted);font-size:11px;margin-top:-14px;margin-bottom:24px}.mobile-nav{display:none}
@media(max-width:1230px){.shell{grid-template-columns:204px minmax(0,840px);max-width:1120px}.rightnav{display:none}}
@media(max-width:820px){.shell{display:block;margin:0;padding:0}.leftnav{display:none}.paper{box-shadow:none;padding:37px clamp(20px,5vw,40px) 75px;min-height:0}.mobile-nav{display:block}.sitehead{height:60px;padding:0 20px}.headmeta{display:none}.paper h1{font-size:30px}.article h2{margin-top:49px}.article figure{margin:26px 0}.article .callout-tip{padding:16px 19px}}
@media(max-width:480px){body{font-size:15px;line-height:1.84}.paper{padding:28px 18px 65px}.paper h1{font-size:27px}.article h2{font-size:21px}.article h3{font-size:17px}.article math[display=block]{padding:12px 5px}.article pre{font-size:11px;padding:12px}.article figcaption{font-size:11px}}
@media print{.sitehead,.leftnav,.rightnav{display:none!important}.shell{display:block;padding:0}.paper{box-shadow:none;padding:0}.article details{break-inside:avoid}.article figure{break-inside:avoid}body{background:white}}
'''
# Decorative motion absent. This JS only highlights the active section; site works without it.
js='''
(()=>{const d=document.getElementById('zoom-dialog');const dest=d.querySelector('img');
function enlarge(img){dest.src=img.src;dest.alt=img.alt;d.showModal();}
document.querySelectorAll('img.zoomable').forEach(img=>{img.addEventListener('click',()=>enlarge(img));img.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();enlarge(img)}})});
d.querySelector('.close-zoom').addEventListener('click',()=>d.close());d.addEventListener('click',e=>{if(e.target===d)d.close()});
const hs=[...document.querySelectorAll('.article h2,.article h3')].filter(x=>x.id);
const items=[...document.querySelectorAll('.rightnav .toc-link')];if(!('IntersectionObserver' in window))return;
const ob=new IntersectionObserver(e=>{const visible=e.filter(x=>x.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);if(!visible.length)return;let target=visible[0].target.id;items.forEach(a=>a.classList.toggle('on',a.hash.slice(1)===target));},{rootMargin:'-78px 0px -76% 0px'});hs.forEach(h=>ob.observe(h));})();
'''
page=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="研究者向けSelf-Attention教材。直感、行列計算、静的図解、数値例、実装、演習まで。"><title>Self-Attentionを行列演算として理解する — 図解で学ぶAIの理論</title><style>{css}</style></head><body>
<header class="sitehead"><a href="#top" class="logo"><span class="logo-mark" aria-hidden="true">∑</span><span>図解で学ぶAIの理論</span></a><span class="headmeta">RESEARCH NOTES · CHAPTER 01</span></header>
<div class="shell" id="top"><aside class="leftnav" aria-label="教材の章一覧"><p class="navlabel">COURSE CONTENTS</p><p class="sideintro">研究者のための<br>数式・概念図・実装</p><a class="sideitem" href="#top">はじめに</a><a class="sideitem active" href="#top" aria-current="page">01　Self-Attention</a><p class="sidenote">静的な図解を中心に、導出・数値検証と限界を理解するための試作教材。</p></aside>
<main class="paper" id="main"><div class="eyebrow">CHAPTER 01 / TRANSFORMER</div><div class="chapterhead"><h1>Self-Attentionを<br>行列演算として理解する</h1><div class="lead">図解で直感をつかみ、テンソル形状・スケーリング・マスク・Multi-Head・実装へ。<br>研究者向け／40〜60分</div></div><article class="article">{content}</article><footer class="foot">textbook-authoring v0.3 · HTML preview generated offline by Pandoc (not Quarto). 図解はすべて新規作成。</footer></main>
<aside class="rightnav" aria-label="ページ内目次"><p class="navlabel">ON THIS PAGE</p>{items}</aside></div>
<dialog class="figure-dialog" id="zoom-dialog" aria-label="図の拡大表示"><button class="close-zoom" type="button" aria-label="拡大図を閉じる">閉じる ×</button><img alt=""></dialog><script>{js}</script></body></html>'''
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(page,encoding='utf-8')
print(f'WROTE {OUT} ({OUT.stat().st_size:,} bytes), {len(soup.find_all("figure"))} diagrams, {len(sections)} headings')
