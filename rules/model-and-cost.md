# Model and Cost Rules

## Model / reasoning effort

実行環境が model 選択を明示的にサポートする場合のみ model を指定する。サポートしない場合は現在の model を使い、主に reasoning effort を調整する。

| 処理 | 方針 | 例 |
| --- | --- | --- |
| LLM 不要 | 通常コード / 通常ツール | hash、diff、sort、schema 検証、JSON 変換、healthcheck |
| 軽い定型処理 | 高速 model + low effort | 抽出、分類、小さな編集、限定範囲の要約 |
| 明確な仕様からの実装 | 高速 model + medium effort | 複数ファイル更新、明確な brief からの生成 |
| 複雑な設計・原因解析 | 高性能 model + medium effort | architecture、難しい debug、研究統合、security review |
| 重大な不確実性 | 高性能 model + high effort 以上 | 重要設計、複数仮説の厳密検証 |

### Escalation

- UI polish、単純同期、機械的変換だけを理由に high effort へ上げない。
- 失敗時は全体を高 effort でやり直さず、失敗箇所だけ escalate する。
- 大量の独立タスクへ自然に分割できる場合だけ multi-agent を検討する。
- Agent を増やすこと自体を目的にしない。

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
