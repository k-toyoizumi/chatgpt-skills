---
name: chatgpt-development-operations
description: Shared operating policy for long-running ChatGPT work such as web development, information retrieval and reporting, automation, research support, and agent development. Use when designing project state, context strategy, model/reasoning effort, incremental processing, validation, or cost-efficient workflows. Do not apply by default to casual one-off questions.
metadata:
  short-description: Common development and operations policy for long-running ChatGPT projects
---

# ChatGPT 開発・運用最適化

継続的な Web/Sites、情報収集・レポート、自動化、研究支援、Agent 開発で使う共通運用 Skill。

## Load policy

この Skill を毎回読む必要はない。次の場合に参照する。

- 新しい長期プロジェクトの設計
- model / reasoning effort の選択
- Context / State 設計
- コスト最適化
- 差分更新・検証フローの設計
- 長期 Session の終了・再開方針の設計

既存のタスク専用 Skill が同じ方針を具体化している場合は、専用 Skill を優先し、この共通 Skill の再取得を省略してよい。

結婚式、ゲーム、日常の些細な質問など、短い単発タスクには原則適用しない。

## Core principles

1. **LLM を呼ばなくてよい処理はコードで行う。**
2. **必要な情報だけを Working Set に入れ、過去全文を毎回読まない。**
3. **外部 State を正本にし、ChatGPT Memory は短く安定した情報だけにする。**
4. **全件再生成より差分更新を優先する。**
5. **必要十分な最小モデル・最小 reasoning effort から開始し、必要時だけ上げる。**
6. **検証に失敗した場合、壊れた最新版を公開せず、正常な旧版を維持する。**
7. **タスク固有の Skill・仕様・ユーザーの最新指示を、この共通 Skill より優先する。**

## Model / reasoning effort routing

実行環境がモデル選択を明示的にサポートする場合のみモデルを指定する。サポートしない場合は現在のモデルを使い、主に reasoning effort で調整する。

| 処理 | 第一選択 | 例 |
| --- | --- | --- |
| LLM 不要 | コード / 通常ツール | hash、diff、重複排除、sort、schema 検証、JSON 変換、件数確認、healthcheck |
| 軽い定型処理 | 高速モデル + low effort | 抽出、分類、小さな編集、限定範囲の要約、候補選別 |
| 明確な仕様からのまとまった実装 | 高速モデル + medium effort | 複数ファイルの協調更新、明確な brief からの生成 |
| 複雑な設計・原因解析 | 高性能モデル + medium effort | architecture、難しい debug、研究統合、security review |
| 重大な不確実性 | 高性能モデル + high effort 以上 | 重要な設計判断、複数仮説の厳密検証 |

- UI polish、単純同期、機械的変換だけを理由に high effort へ上げない。
- 大量の独立タスクへ分割できる場合だけ multi-agent を検討する。
- 失敗時は全体を高 effort でやり直さず、失敗箇所だけ escalate する。

## State hierarchy

### A. Source of Truth

コード、DB、Sheets、Notion DB、設定ファイルなどの実データ。事実確認はまずここを見る。

### B. Project State

長期プロジェクトごとに `PROJECT_STATE.md` または同等の運用ページを 1 つ置く。

最低限、以下だけを維持する。

- Goal / acceptance criteria
- 現在の architecture
- 確定済み decision
- 現在有効な設定・主要 ID
- open issues
- last successful state
- next actions
- source pointers

Project State はログではない。過去の試行錯誤や raw tool output を蓄積しない。

### C. ChatGPT Memory

長期間安定するユーザー方針と、「どの Skill / State を参照するか」という routing 情報だけを保持する。

コード、長い仕様、raw ログ、短命な状態は Memory へ入れない。

### D. Working Set

そのターン / Session で推論に必要な情報だけを保持する。

- Goal
- hard constraints
- acceptance criteria
- 関連する確定 decision
- 変更対象
- 変更箇所と依存箇所
- open issue
- 直近の検証結果
- 必要な source pointer

全文履歴ではなく、必要部分を検索・取得する。

### E. Scratch

検索途中、仮説、tool output、思考途中の情報。原則として次ターンへ持ち越さない。

将来必要なら構造化要約へ昇格させ、外部 State へ保存する。

## Working Set workflow

1. タスク開始時に Goal / constraints / current state / relevant sources を確定する。
2. 既存 State がある場合はまず State を読み、原本全文は必要な部分だけ取得する。
3. 「最近触った」「依存している」「今回変更する」情報を優先する。
4. 会話が長くなっても全文を再入力しない。
5. Context が肥大化したら、確定 decision・結果・未解決だけを compact する。
6. raw 検索結果、失敗した試行、重複説明は Working Set から外す。
7. compaction は毎ターンではなく、サイズ閾値またはフェーズ終了時に行う。
8. 圧縮後も原本の ID / URL / file path を保持し、必要時に再取得できるようにする。

## Incremental processing

可能なら LLM の前に決定論的コードで差分を絞る。

```text
current metadata / ids / timestamps / hashes
        ↓
deterministic diff
        ↓
changed records + directly dependent records only
        ↓
LLM processing
        ↓
schema / link / count / behavior validation
        ↓
publish
```

変更判定は原則として次の順で行う。

1. stable ID
2. updated_at / mtime
3. content hash
4. semantic comparison（上記で判定不能な場合のみ LLM）

変更のないデータは既存成果物を再利用する。

## Code utility contract

以下は LLM 推論より Python / JavaScript / shell 等の通常コードを優先する。

- `canonicalize(data)` — 順序・空白を正規化して安定比較可能にする
- `content_hash(data)` — SHA-256 等で変更検知
- `diff_by_id(old, new)` — added / changed / removed を抽出
- `dedupe(records, key)` — URL、ID、複合キーで重複排除
- `select_changed(records, state)` — 更新日時 / hash から LLM 対象を限定
- `validate_schema(data, schema)` — 必須 field・型を検査
- `validate_refs(data)` — 参照 ID・リンク切れ・孤立 record を検査
- `bounded_read(source, ids_or_range)` — 必要範囲だけ読む
- `healthcheck(output)` — 件数、schema、リンク、主要導線を検査

永続プロジェクトでは、これらを各 repo の `scripts/` または `tools/` に実装し、毎回 LLM に再生成させない。

共通 Skill は「何をコードへ回すか」を定義し、実コードの正本は各プロジェクト repo に置く。

## Prompt cache aware design

API / Agent 実装で prompt cache を制御できる場合は、次を基本とする。

- **stable prefix**: 共通 instructions、固定 schema、安定した tool definitions、長期 reference
- **variable suffix**: 今回のユーザー指示、日時、最新検索結果、変更データ
- tool 定義の順序・schema を不用意に変えない。
- 履歴を途中で書き換えるより append を優先する。
- 頻繁な compaction で stable prefix を崩さない。
- 一時的な検索結果や毎回変わる時刻を stable prefix へ入れない。
- モデル固有の cache behavior・料金・lifetime は利用時点の公式仕様を確認する。

ChatGPT アプリ内部の hidden system prompt や cache hit はユーザー側から直接制御できない。この方針はユーザー管理の Prompt、Skill、Automation、API / Agent 実装へ適用する。

## Tool / Skill loading

- connected source はタスクに必要なものだけ検索する。
- 既知の file / page ID があれば検索し直さず直接 fetch する。
- 大きなファイルは全文取得せず、search → relevant range read を優先する。
- 再利用可能な手順は Skill へ置き、プロジェクト固有の状態は Skill に埋め込まない。
- **Skill = 手順、State = 現在値、Memory = 安定した個人方針** と役割を分離する。

## Long-running session checkpoint

フェーズ終了時に Project State へ以下だけ checkpoint する。

- 完了した変更
- 現在正常に動く version / URL / commit
- 新しい decision
- 未解決 issue
- 次回最初に行う action

次の Session では checkpoint から開始し、過去チャット全文の再読を避ける。

## Quality and cost priority

**Correctness / Security → Reuse → Minimal Context → Minimal Model/Effort → Visual polish**

低コスト化のために検証を省略しない。

節約対象は以下。

- 重複推論
- 不要な全文読み込み
- 不要な high effort
- LLM で行う必要のない処理

## References

- OpenAI Prompt Caching: https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI Model Selection: https://developers.openai.com/api/docs/guides/model-selection
- OpenAI Agents SDK Sessions: https://openai.github.io/openai-agents-python/sessions/
