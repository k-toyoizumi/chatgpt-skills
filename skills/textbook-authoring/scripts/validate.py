#!/usr/bin/env python3
"""Static textbook skill checks. Does not replace Quarto render or human fact checking."""
from pathlib import Path
import re, shutil, sys, xml.etree.ElementTree as ET
import yaml
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'assets/quarto-book'
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
check(skill.startswith('---\n'),'Skill frontmatter missing')
check(bool(re.search(r'^name: textbook-authoring\s*$',skill,re.M)), 'Skill name missing')
check(bool(re.search(r'^description:\s*\S+',skill,re.M)), 'Skill description missing')
for path in ['references/pedagogy.md','references/diagrams.md','references/tables.md','references/quality.md','assets/quarto-book/_quarto.yml','scripts/render_preview.py','scripts/test_numeric.py']:
    check((ROOT/path).is_file(), f'Missing {path}')
cfg=yaml.safe_load((BOOK/'_quarto.yml').read_text())
chapters=cfg['book']['chapters']
check('index.qmd' in chapters, 'index.qmd absent from book')
for f in BOOK.rglob('*.qmd'):
    check(f.relative_to(BOOK).as_posix() in chapters, f'chapter not listed: {f}')
    src=f.read_text(encoding='utf-8')
    check(src.count('```')%2==0,f'unbalanced code fences: {f}')
    check(src.count(':::')%2==0,f'unbalanced div fences: {f}')
    for dest in re.findall(r'!\[([^]]*)\]\(([^)]+)\)',src):
        alt,path=dest
        check(bool(alt.strip()),f'figure missing alt: {f}:{path}')
        check((f.parent/path).is_file(),f'broken image reference: {f}:{path}')
    # Check every referenced figure/table resolves; require use of numbered references.
    ids=re.findall(r'\{#((?:fig|tbl)-[a-z0-9-]+)\}',src)
    references=re.findall(r'(?<![\w-])@((?:fig|tbl)-[a-z0-9-]+)',src)
    check(len(ids)==len(set(ids)),f'duplicate figure/table labels: {f}')
    for target in references:
        check(target in ids, f'broken figure/table reference @{target}: {f}')
    for target in ids:
        check(target in references, f'unreferenced figure/table {target}: {f}')
    for line in re.findall(r'^: .+\{#tbl-[a-z0-9-]+\}\s*$',src,re.M):
        check(bool(line.strip()),f'table missing caption: {f}')
    if f.name=='01-attention.qmd':
        check(len(re.findall(r'^\*\*Q\d\.',src,re.M))>=4,'need 4 exercises')
        check(src.count('<details>')>=4,'answer disclosure missing')
        check(src.count('{#fig-')>=5,'expected at least 5 figure anchors')
        check(src.count('{#tbl-')>=1,'expected at least one numbered table')
        check('Attention is not Explanation' in src,'interpretability reference missing')
for f in BOOK.rglob('*.svg'):
    try:
        tree=ET.parse(f)
        check(bool(tree.getroot().find('{http://www.w3.org/2000/svg}title') is not None),f'SVG missing title: {f.name}')
    except ET.ParseError as ex:
        errors.append(f'invalid SVG: {f.name}:{ex}')
if errors:
    print('FAIL static checks:',*errors,sep='\n - ')
    sys.exit(1)
print('PASS: skill metadata, Quarto config, QMD sections, references, 5 labeled SVGs and linked fig/table refs')
if shutil.which('quarto'): print('AVAILABLE: Quarto CLI; run quarto render in assets/quarto-book')
else: print('NOT RUN: Quarto render (CLI not installed)')
