from pathlib import Path
from html import escape
import math
import numpy as np
DIR=Path(__file__).resolve().parents[1]/'assets/quarto-book/figures'
DIR.mkdir(parents=True,exist_ok=True)
NAVY='#18314e'; INK='#25394e'; MUTED='#64778a'; BLUE='#2569ac'; TEAL='#14877c'; AMBER='#b9751e'; BG='#f7fafc'; LINE='#d8e3ed'; WHITE='#ffffff'
header='''<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#8297ad"/></marker></defs>'''
def text(x,y,s,size=19,color=INK,weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Noto Sans CJK JP,Noto Sans JP,Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill=WHITE,stroke=LINE,rx=13,sw=1.7):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,color='#8297ad',width=2.5,arrow=False,dash=''):
 return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" {"stroke-dasharray="+repr(dash) if dash else ""} {"marker-end=\"url(#arr)\"" if arrow else ""}/>'
def svg(w,h,body,title,subtitle=''):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle or title)}</desc>{header}<rect width="{w}" height="{h}" rx="20" fill="{BG}"/>{body}</svg>'''
def save(name,w,h,body,title,subtitle=''):
 (DIR/name).write_text(svg(w,h,body,title,subtitle),encoding='utf-8')
# 1 pipeline
b=text(38,48,'1｜照合の計算と情報の集約',25,NAVY,700)+text(38,78,'Q・Kが重みを決め、Vが集約される。矢印はデータの流れ。',15,MUTED)
for yy,k,small,col in [(116,'Query：Q','何を照合するか',BLUE),(201,'Key：K','照合される手掛かり',TEAL),(286,'Value：V','集約する内容',AMBER)]:
 b+=rect(38,yy,242,66,WHITE,col)+text(57,yy+27,k,20,col,700)+text(57,yy+51,small,14,MUTED)
b+=rect(338,149,186,114,'#e8f0fa','#a9c5df')+text(431,190,'QKᵀ / √dₖ',25,BLUE,700,'middle')+text(431,223,'位置間のスコア',16,MUTED,400,'middle')
b+=rect(586,149,178,114,'#e4f5f1','#a1d5ca')+text(675,193,'Softmax',23,TEAL,700,'middle')+text(675,225,'Attention重み',15,MUTED,400,'middle')
b+=rect(822,149,224,114,'#fff4e5','#efcf96')+text(934,193,'重み付き和',23,AMBER,700,'middle')+text(934,226,'出力 Z = AV',16,INK,400,'middle')
b+=line(280,147,338,178,arrow=True)+line(280,233,338,233,arrow=True)+line(524,207,586,207,arrow=True)+line(764,207,822,207,arrow=True)
b+=line(280,319,807,319)+line(807,319,807,246)+line(807,246,822,246,arrow=True)
b+=text(481,301,'Vはスコアではなく最後の集約に使う',15,MUTED,400,'middle')
save('01-qkv-pipeline.svg',1084,383,b,'Self-Attentionの処理の流れ','QとKの照合、Softmax、Vの重み付き和を区別する模式図')
# 2 matrix shapes
b=text(34,44,'2｜行列の形状を追う',25,NAVY,700)+text(34,72,'同じ n でも、注意行列と特徴表現は別の次元を持つ。',15,MUTED)
blocks=[('Q','n × dₖ',BLUE),('Kᵀ','dₖ × n',BLUE),('A','n × n',TEAL),('V','n × dᵥ',AMBER),('Z','n × dᵥ',NAVY)]
xs=[34,240,449,665,874]
for i,((name,shape,c),x) in enumerate(zip(blocks,xs)):
 b+=rect(x,120,178,121,WHITE,LINE)+rect(x+12,133,154,8,c,c,5,0)
 b+=text(x+89,183,name,28,c,700,'middle')+text(x+89,213,shape,18,MUTED,500,'middle')
 if i<4:
  b+=text(x+193,186,['×','→','×','='][i],25,MUTED,600,'middle')
b+=rect(105,286,855,51,'#e8f1f9','#c6d9ea')+text(532,318,'A の各行は「ある Query が、どの Key を参照するか」の分布',17,BLUE,500,'middle')
save('02-shapes.svg',1088,365,b,'Attention計算のテンソル形状','Qはn掛けるdk、K転置はdk掛けるn、Aはn掛けるn、VとZはn掛けるdv')
# 3 heatmap
Q=np.array([[1,0],[0,1],[1,1]],dtype=float);score=Q@Q.T/math.sqrt(2)
AA=np.exp(score-score.max(axis=1,keepdims=True));AA=AA/AA.sum(axis=1,keepdims=True)
b=text(36,44,'3｜実際に計算した Attention 重み',25,NAVY,700)+text(36,73,'各行でSoftmax：同じQueryに対する参照先の重みは合計1',15,MUTED)
b+=text(435,120,'Key（参照先） →',18,INK,600,'middle')
for j in range(3): b+=text(290+j*146,151,f'K{j+1}',17,MUTED,700,'middle')
for i in range(3):
 b+=text(153,200+i*74,f'Q{i+1}',19,BLUE,700,'middle')
 for j in range(3):
  v=float(AA[i,j]);c=f'#{int(238-62*v):02x}{int(247-48*v):02x}{int(252-10*v):02x}'
  x=222+j*146;y=168+i*74
  b+=rect(x,y,135,66,c,'#c7d9e8',10,1.2)+text(x+67.5,y+40,f'{v:.3f}',23,NAVY,700,'middle')
b+=rect(706,167,332,213,WHITE,LINE)+text(731,201,'第1行の計算',21,NAVY,700)
b+=text(731,240,'scores = (0.707, 0, 0.707)',17,MUTED)+text(731,276,'softmax → (0.401, 0.198, 0.401)',16,BLUE,600)+text(731,315,'z₁ = Σⱼ a₁ⱼvⱼ',21,TEAL,700)+text(731,349,'= (1.604, 1.198)',20,NAVY,700)
save('03-weight-matrix.svg',1084,413,b,'数値例によるAttention重みのヒートマップ','3トークンのQuery Keyから計算した重み行列。各行の合計が1である')
# 4 causal
b=text(36,45,'4｜因果マスク：未来の Key を見せない',25,NAVY,700)+text(36,75,'Query i は Key j ≤ i のみを参照。灰色×はスコアに −∞ を加える位置。',15,MUTED)
for j in range(4):b+=text(351+j*112,135,f'K{j+1}',18,MUTED,700,'middle')
for i in range(4):
 b+=text(219,192+i*57,f'Q{i+1}',18,BLUE,700,'middle')
 for j in range(4):
  allowed=j<=i;x=301+j*112;y=152+i*57
  b+=rect(x,y,101,49,'#e1f3ed' if allowed else '#f0f1f3','#b2d5c9' if allowed else '#dae0e7',8,1.2)
  b+=text(x+50,y+33,'✓' if allowed else '×',25,TEAL if allowed else '#a1aab7',700,'middle')
b+=rect(806,167,238,125,WHITE,LINE)+text(825,200,'Softmaxの前に',18,NAVY,700)+text(825,230,'禁止位置 = −∞',18,BLUE,600)+text(825,262,'→ 重みは 0',17,MUTED)
save('04-causal-mask.svg',1084,419,b,'4トークンの因果マスク','Queryごとに未来のKeyを参照禁止とする下三角行列')
# 5 multi
b=text(35,45,'5｜Multi-Head は射影の異なる Attention を並列化',24,NAVY,700)+text(35,74,'役割があらかじめ固定されているのではなく、各ヘッドの射影行列が学習される。',15,MUTED)
b+=rect(36,171,137,87,'#e8eff9','#aac6e0')+text(105,205,'入力 X',24,BLUE,700,'middle')+text(105,234,'n × dmodel',15,MUTED,400,'middle')
for i,(yy,t,c) in enumerate([(100,'head 1',BLUE),(209,'head 2',TEAL),(318,'head H',AMBER)]):
 b+=rect(263,yy,223,74,WHITE,c)+text(282,yy+30,t,20,c,700)+text(282,yy+56,'各ヘッドで Q, K, V → A V',13,MUTED)
 b+=line(173,213,222,213)+line(222,213,222,yy+37)+line(222,yy+37,263,yy+37,arrow=True)
 b+=line(486,yy+37,565,yy+37)+line(565,yy+37,565,224)
b+=rect(613,174,175,99,'#e8f3f0','#a3cec4')+text(700,210,'Concat',22,TEAL,700,'middle')+text(700,239,'n × (H dᵥ)',17,MUTED,400,'middle')
b+=line(565,224,613,224,arrow=True)
b+=rect(846,174,197,99,'#eef2f8','#b1c5d9')+text(944,210,'出力射影 Wₒ',20,NAVY,700,'middle')+text(944,241,'n × dmodel',16,MUTED,400,'middle')
b+=line(788,224,846,224,arrow=True)
save('05-multi-head.svg',1084,419,b,'Multi-Head Attentionの概念図','入力が異なる射影による複数ヘッドへ分岐し、結合後に出力射影される')
print('Figures generated',len(list(DIR.glob('*.svg'))))
