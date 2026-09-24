---
name: research-survey
description: 論文・技術文献を調査するときに、pre-survey、quick-and-wide-survey、deep-research の3段階で調査観点の設計、広い候補収集、深い統合分析を行う。研究動向、関連研究、新規性、技術比較、文献レビューで使用する。
metadata:
  short-description: 3段階で効率よく論文・技術調査を行う
---

# Research Survey

論文調査を、目的の異なる3段階に分けて実行する。

すべての段階を必ず実行する必要はない。調査目的・難易度・既知情報に応じて省略または軽量化する。

## Applicable rules

- `rules/core.md`
- `rules/model-and-cost.md`
- 長期研究の場合は `rules/context-and-state.md`

## Phase 1: pre-survey

### 目的

本格検索の前に、調査観点・仮説・検索軸を洗い出す。

### 実施内容

- 問題設定を分解する
- 主要概念・類義語・隣接分野を整理する
- 検索クエリ候補を設計する
- 比較観点・評価軸を定める
- 見落としやすい反証・代替仮説を洗い出す
- 必要なら対象期間・venue・分野を定める

### Model / effort

原則:

- 高性能モデル + medium〜high

ただし以下では軽量化してよい。

- 調査観点が既に明確 → 省略可能
- 単純な検索語整理だけ → low まで下げてよい

### Output

- research questions
- search axes / queries
- inclusion / exclusion criteria
- comparison dimensions
- preliminary hypotheses

## Phase 2: quick-and-wide-survey

### 目的

タイトル、abstract、必要に応じて introduction 程度を中心に、多数の候補を素早く集めて一次選別する。

### 実施内容

- 幅広く文献候補を検索する
- タイトル・abstract・metadata を確認する
- 必要な場合のみ introduction を確認する
- 重複を除去する
- relevance を一次判定する
- deep-research 対象候補を絞る
- 候補リストに選定理由を残す

### Model / effort

原則:

- 高速〜標準モデル + low〜medium

大量候補を扱う場合は、高性能モデルを全件に使わない。

### Tool / code priority

以下は可能な限り通常ツール・コードを使う。

- DOI / URL / title の重複排除
- metadata の正規化
- 年・venue・citation 等による sort / filter
- abstract 取得
- 候補表・JSON の生成
- 既読 / 未読・採否状態の管理

LLM は主に relevance 判定、曖昧な分類、短い要約に使う。

### Output

各候補について、最低限以下を持つ。

- title
- year
- source / venue
- URL / DOI
- task / problem
- core idea
- relevance
- selection status
- short reason

## Phase 3: deep-research

### 目的

選定した重要文献を深く理解し、複数文献を統合・比較・分析する。

### 実施内容

必要に応じて本文全体を読む。

- problem formulation
- assumptions
- method / architecture / algorithm
- objective / loss
- dataset
- evaluation protocol
- results
- limitations
- relationship to prior work

その後、複数文献について以下を統合する。

- 共通点・相違点
- 時系列的な発展
- trade-off
- contradictory findings
- unresolved gaps
- target research との関係
- novelty / positioning

### Model / effort

原則:

- 高性能モデル + high

ただし、単一文献の単純要約だけなら必要に応じて effort を下げてよい。

### Output

単なる論文ごとの要約集ではなく、調査目的に沿った統合結果を作る。

例:

- literature map
- comparison matrix
- historical development
- gaps / open questions
- research positioning
- key papers and why they matter

## Transition rules

- pre-survey の結果を quick-and-wide-survey の検索条件へ渡す。
- quick-and-wide-survey で全候補を深読みしない。
- deep-research へ渡す文献は、調査目的に対する重要度で絞る。
- deep-research 中に新しい重要キーワードや系統が見つかった場合は、必要な範囲だけ quick-and-wide-survey に戻る。
- 各段階で得た raw 検索結果を無制限に Context へ残さない。
