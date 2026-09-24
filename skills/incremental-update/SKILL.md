---
name: incremental-update
description: 既存の Web アプリ、レポート、設定、データ、ドキュメントなどを更新するときに、全件再処理を避け、差分を決定論的に抽出して変更部分と直接依存部分だけを処理・検証・公開する。
metadata:
  short-description: 差分抽出から検証・公開までを安全に実行
---

# Incremental Update

既存成果物の更新を、最小限の再処理で安全に行う。

## Applicable rules

- `rules/core.md`
- `rules/change-and-validation.md`
- 長期プロジェクトの場合は `rules/context-and-state.md`

## Trigger

次のような依頼で使う。

- 新しいデータだけ同期する
- 既存 Web アプリへ変更を反映する
- 日報・レポートへ新規項目を追加する
- 設定や manifest の変更を既存成果物へ反映する
- 大量データの一部だけ更新する

## Workflow

### 1. Source of Truth を特定

更新対象と、変更判定に使える情報を確認する。

候補:

- stable ID
- updated_at / mtime
- content hash
- version / commit

### 2. Deterministic diff

LLM を使う前に、通常コード・通常ツールで added / changed / removed を抽出する。

変更なしの場合は既存成果物を再利用して終了する。

### 3. Impact selection

処理対象を次に限定する。

- changed records
- directly dependent records

全件を LLM へ再投入しない。

### 4. Apply changes

機械的処理はコードで行い、意味判断・生成・統合が必要な箇所だけ LLM を使う。

### 5. Validate

変更内容に応じて確認する。

- schema
- links / refs
- counts
-主要導線
- 主要機能
- acceptance criteria

### 6. Publish

検証成功後に公開・同期する。

検証失敗時は last-known-good を維持し、失敗箇所だけ修正して再検証する。

### 7. Checkpoint

長期プロジェクトの場合は Project State に次を反映する。

- changed scope
- validation result
- successful version / commit / URL
- unresolved issue

## Completion

変更のない範囲を不必要に再処理せず、必要な差分だけが反映され、検証結果を確認できれば完了。
