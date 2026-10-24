# Context and State Rules

## State の階層

### A. Source of Truth

コード、DB、Sheets、Notion DB、設定ファイルなどの実データ。

事実確認や現在値の確認は、可能な限り Source of Truth を直接参照する。

### B. Project State

長期プロジェクトごとに `PROJECT_STATE.md` または同等の外部 State を用意する。

最低限、以下を保持する。

- Goal / acceptance criteria
- 現在の architecture
- 確定済み decision
- 現在有効な設定・主要 ID
- open issues
- last successful state
- next actions
- source pointers

Project State は作業ログではない。過去の試行錯誤や raw tool output を蓄積しない。

### C. ChatGPT Memory

長期間安定する以下の情報だけを保持する。

- ユーザーの安定した方針・好み
- どの Rule / Skill / Project State を参照するかという routing

コード、長い仕様、raw log、短命な状態、頻繁に変わる ID は原則として保存しない。

### D. Working Set

そのターン / Session で推論に必要な情報だけを保持する。

主な構成要素:

- Goal
- hard constraints
- acceptance criteria
- 関連する確定 decision
- 変更対象
- 依存箇所
- open issue
- 直近の検証結果
- 必要な source pointer

過去チャット全文ではなく、必要な情報を検索・取得して構築する。

### E. Scratch

検索途中の結果、仮説、tool output、思考途中の一時情報。

原則として次 Session へ持ち越さない。将来必要なら構造化された State に昇格させる。

## memo文書の命名

- `memo/` の日付付き文書は `YYYY-MM-DD_N_short-english-title.md` とする。例：`2026-10-24_1_environment-setup.md`。日付・連番だけの `YYYY-MM-DD_N.md` にはしない。
- 日付は日本時間の作成日、Nは同日・そのプロジェクトのmemo全体で共通の作成順連番（1から開始）。新規作成時に全サブディレクトリの同日最大番号を確認して次を採番し、既存番号を再利用・繰上げしない。
- タイトル部分は内容が分かる短い英語とし、小文字の英数字をハイフンで区切る。文書本文・見出しの日本語を英語化する必要はない。
- READMEや継続更新する仕様書・テンプレートの固定名には適用しない。既存文書を改名する場合は日付・番号・内容を保ち、参照リンクも更新する。命名規則の修正だけで過去文書を一括改名しない。

## Context の読み込み

- 既知の file / page ID がある場合は、不要な再検索を避けて直接取得する。
- 大きなファイルは全文取得より、search → relevant range read を優先する。
- 「今回変更する」「直接依存する」「直近で検証した」情報を優先する。
- connected source はタスクに必要なものだけ読む。
- Rules / Skills も、そのタスクに必要なものだけ読む。

## 長期 Session

Context が肥大化した場合は、次を残して compact する。

- 確定 decision
- 現在の結果
- 未解決 issue
- source pointer

次は原則として破棄する。

- raw 検索結果
- 解決済みの試行錯誤
- 重複説明
- 失敗した中間出力

フェーズ終了時には Project State に checkpoint を残す。

- 完了した変更
- 現在正常に動く version / URL / commit
- 新しい decision
- 未解決 issue
- 次回最初に行う action
