# Model and Cost Rules

## モデル名は固定しない

共通 Rules では、原則として具体的なモデル名を固定しない。

モデル世代や提供形態は変更されるため、長期的な規則では次の能力区分で表現する。

- 高速モデル
- 標準モデル
- 高性能モデル

実行環境がモデル選択を明示的にサポートする場合のみ、その時点で利用可能な具体的モデルへ割り当てる。

具体的なモデル名の対応表が必要な場合は、共通 Rule に埋め込まず、実行時設定・プロジェクト設定・短命な mapping として管理する。

## Model / reasoning effort

原則として、必要十分な最小構成から開始する。

| 処理 | 推奨 |
| --- | --- |
| LLM 不要 | 通常コード / 通常ツール |
| 日常的な質問・単純な事実確認 | 高速モデル + low |
| 通常の Web 調査・比較 | 高速モデル + low |
| 軽い抽出・分類・限定範囲の要約 | 高速モデル + low |
| 明確な仕様からのまとまった実装 | 高速〜標準モデル + medium |
| 複雑な設計・原因解析 | 高性能モデル + medium |
| 重大な不確実性・厳密な統合分析 | 高性能モデル + high |

検索・Web 参照が不要な日常質問では、不要な外部検索を行わない。

### Escalation

- UI polish、単純同期、機械的変換だけを理由に high へ上げない。
- 失敗時は全体を高 effort でやり直さず、失敗箇所だけ escalate する。
- 大量の独立タスクへ自然に分割できる場合だけ multi-agent を検討する。
- Agent を増やすこと自体を目的にしない。

## Research routing

論文・技術調査では、調査フェーズごとに必要な reasoning depth が異なる。

詳細な手順は `skills/research-survey/SKILL.md` に置き、ここでは routing 原則だけを定義する。

| Phase | 主目的 | 推奨 |
| --- | --- | --- |
| pre-survey | 調査観点・仮説・検索軸の設計 | 高性能モデル + medium〜high |
| quick-and-wide-survey | 多数候補を広く収集・一次選別 | 高速〜標準モデル + low〜medium |
| deep-research | 文献を深く理解し、統合・比較・分析 | 高性能モデル + high |

pre-survey は、調査目的・観点・検索語が十分明確な場合は省略してよい。単純な整理だけで済む場合は low まで下げてよい。

quick-and-wide-survey では、metadata 整理、重複排除、タイトル・abstract の抽出、候補表作成など、決定論的に処理できる部分は通常ツール・コードを優先する。

## Prompt Cache を意識した Context 設計

API / Agent 実装で cache を制御できる場合は、安定部分と変動部分を分離する。

### Stable prefix

- 共通 instructions
- 固定 schema
- 安定した tool definitions
- 長期 reference

### Variable suffix

- 今回のユーザー指示
- 日時
- 最新検索結果
- 変更データ

### ルール

- tool 定義の順序・schema を不用意に変えない。
- 一時的な検索結果や時刻を stable prefix に入れない。
- cache の料金・lifetime・対応 model は、利用時点の公式仕様を確認する。
- ChatGPT アプリ内部の hidden prompt / cache hit を、ユーザー側で制御できる前提にしない。
