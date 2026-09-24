---
name: project-session-management
description: 長期プロジェクトを開始・再開・終了するときに、外部 State から必要情報だけを取得して Working Set を構築し、Session 終了時に checkpoint を残す。Web 開発、研究支援、自動化、Agent 開発など、複数 Session にまたがる作業で使用する。
metadata:
  short-description: 長期プロジェクトの開始・再開・checkpoint を管理
---

# Project Session Management

長期プロジェクトで過去チャット全文に依存せず、外部 State を使って安全に作業を継続する。

## Applicable rules

- `rules/core.md`
- `rules/context-and-state.md`
- 必要に応じて `rules/model-and-cost.md`

## Trigger

次のような状況で使う。

- 長期プロジェクトを新しく始める
- 別 Session から作業を再開する
- 長い Session の Context を整理する
- 作業フェーズを終了し、次回へ引き継ぐ

短い単発質問には使わない。

## Workflow

### 1. Goal を確定

現在の依頼から以下を抽出する。

- Goal
- hard constraints
- acceptance criteria
- 今回変更する対象

### 2. State を取得

既存 Project State がある場合は最初に読む。

不足情報だけ Source of Truth から取得し、過去ログ全文は読み直さない。

### 3. Working Set を構築

今回の実行に必要なものだけを集める。

- 関連 decision
- 変更対象
- 直接依存する箇所
- open issue
- 直近の検証結果
- source pointer

### 4. 実行

Working Set の範囲で作業する。

更新作業で差分処理が有効な場合は `incremental-update` Skill を併用する。

### 5. 検証

acceptance criteria と変更内容に応じて結果を確認する。

### 6. Checkpoint

フェーズ終了時、Project State に以下だけを反映する。

- 完了した変更
- 正常に動く version / URL / commit
- 新しく確定した decision
- 未解決 issue
- next action
- 必要な source pointer

raw tool output や解決済みの試行錯誤は保存しない。

## Completion

次の Session が過去チャット全文を読まなくても、Project State と Source of Truth から作業を再開できれば完了。
