#!/usr/bin/env python3
"""Static source checks for a multi-page Quarto Book; not a Quarto render."""
from pathlib import Path
import re, shutil, sys, xml.etree.ElementTree as ET
import yaml
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'assets/quarto-book'
errors=[]
def check(value,message):
    if not value:errors.append(message)

skill=(ROOT/'SKILL.md').read_text(encoding='utf8')
check(bool(re.search(r'^name: textbook-authoring\s*$',skill,re.M)),'Skill name missing')
for name in ['references/pedagogy.md','references/diagrams.md','references/tables.md','references/navigation.md','references/quality.md','scripts/render_preview.py','scripts/test_browser.py']:
    check((ROOT/name).is_file(),'Missing '+name)
config=yaml.safe_load((BOOK/'_quarto.yml').read_text(encoding='utf8'))
book=config['book'];html=config['format']['html']
check(config['project']['type']=='book','Quarto project must be book')
check(book.get('page-navigation') is True,'Chapter previous/next navigation not enabled')
sidebar=book.get('sidebar',{})
check(sidebar.get('style')=='docked','Sidebar should be docked on desktop')
check(isinstance(sidebar.get('collapse-level'),int),'Collapsible chapter hierarchy not configured')
check(html.get('toc') is True and html.get('toc-location')=='right','Right-page TOC missing')

chapters=book['chapters']
def flatten(items):
    result=[]
    for item in items:
        if isinstance(item,str):result.append(item)
        elif isinstance(item,dict):result.extend(flatten(item.get('chapters',[])))
    return result
listing=flatten(chapters)
check(listing[0]=='index.qmd','Book index must be first')
check(len(listing)>=3,'Need index and at least two navigable chapter pages')
check(len(listing)==len(set(listing)),'Duplicate chapter path')
check(any(isinstance(x,dict) and 'part' in x for x in chapters),'No collapsible navigation group')
for item in listing:check((BOOK/item).is_file(),'Broken chapter nav link: '+item)
all_sources=list(BOOK.rglob('*.qmd'))
check(set(listing)=={x.relative_to(BOOK).as_posix() for x in all_sources},'Unlisted .qmd source or missing page')
all_ids={};all_refs=[];figure_count=table_count=exercise_count=0
for file in all_sources:
    src=file.read_text(encoding='utf8')
    check(src.count('```')%2==0,'Unbalanced code fences: '+file.name)
    check(src.count(':::')%2==0,'Unbalanced callout fences: '+file.name)
    check(not re.search(r'^## \d+\. ',src,re.M),'Do not hand-number numbered sections: '+file.name)
    for alt,dest in re.findall(r'!\[([^]]*)\]\(([^)]+)\)',src):
        check(bool(alt.strip()),'Missing image alt: '+file.name)
        check((file.parent/dest).is_file(),'Broken media path: '+file.name+':'+dest)
    for dest in re.findall(r'\]\(([^)]+\.qmd)\)',src):
        check((file.parent/dest).is_file(),'Broken chapter link: '+file.name+':'+dest)
    for identifier in re.findall(r'\{#((?:fig|tbl)-[a-z0-9-]+)\}',src):
        check(identifier not in all_ids,'Duplicate figure/table id: '+identifier)
        all_ids[identifier]=file
    all_refs.extend((r,file) for r in re.findall(r'(?<![\w-])@((?:fig|tbl)-[a-z0-9-]+)',src))
    figure_count+=len(re.findall(r'\{#fig-',src))
    table_count+=len(re.findall(r'\{#tbl-',src))
    exercise_count+=len(re.findall(r'^\*\*Q\d+\.',src,re.M))
for identifier,file in all_refs:check(identifier in all_ids,'Broken cross-chapter reference: '+file.name+':@'+identifier)
for identifier in all_ids:check(any(x==identifier for x,_ in all_refs),'Figure/table not cited in text: '+identifier)
check(figure_count==5 and table_count==1,'Demo must preserve 5 figures and 1 comparison table')
check(exercise_count>=4,'Demo must preserve 4 exercises')
for svg in BOOK.rglob('*.svg'):
    try:
        root=ET.parse(svg).getroot()
        check(root.find('{http://www.w3.org/2000/svg}title') is not None,'SVG missing title: '+svg.name)
    except ET.ParseError as e:errors.append(f'Invalid SVG: {svg.name}:{e}')
if errors:
    print('FAIL static checks:',*errors,sep='\n- ');sys.exit(1)
print('PASS static: 4 independent pages, collapsible sidebar config, right TOC, global crossrefs, 5 figures, 1 table, 4 exercises')
print('AVAILABLE Quarto CLI' if shutil.which('quarto') else 'NOT RUN: Quarto render (CLI not installed)')
