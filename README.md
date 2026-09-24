# ChatGPT Skills / Rules

ChatGPT・Codex などの AI Agent で再利用する、個人用の **Rules（規則）** と **Skills（実行手順）** を管理するリポジトリです。

> リポジトリ名は現在 `chatgpt-skills` ですが、Skills だけでなく Rules も管理します。名称変更は必要になった時点で行います。

## Rules と Skills の役割

### Rules

「どう判断し、何を守るか」を定義します。

- 長期的に安定した原則・制約
- Context / State の扱い
- model / reasoning effort の選択方針
- 差分処理・検証・公開の原則

原則として、特定タスクの細かい手順は Rules に書きません。

### Skills

「特定の種類のタスクを、どう実行するか」を定義します。

- 明確な利用条件（trigger）
- 再利用可能な workflow
- 必要な Rules / source への参照
- 完了条件・検証方法

Skill は標準的な `SKILL.md` 形式で管理します。

```yaml
---
name: skill-name
description: この Skill をいつ、何のために使うか
metadata:
  short-description: 短い説明
---
```

## ディレクトリ構成

```text
chatgpt-skills/
├── README.md
├── AGENTS.md
├── rules/
│   ├── core.md
│   ├── context-and-state.md
│   ├── model-and-cost.md
│   └── change-and-validation.md
└── skills/
    ├── project-session-management/
    │   └── SKILL.md
    └── incremental-update/
        └── SKILL.md
```

## Rules 一覧

### `rules/core.md`

共通原則、適用範囲、指示の優先順位、品質とコストの優先順位を定義します。

### `rules/context-and-state.md`

Source of Truth、Project State、ChatGPT Memory、Working Set、Scratch の役割と、長期 Session の扱いを定義します。

### `rules/model-and-cost.md`

model / reasoning effort の選択、multi-agent の利用条件、Prompt Cache を意識した Context 設計を定義します。

### `rules/change-and-validation.md`

差分更新、LLM と通常コードの役割分担、検証、公開、last-known-good の維持方針を定義します。

## Skills 一覧

### `project-session-management`

長期プロジェクトを開始・再開・終了するときに、必要な State だけを読み、Working Set を構築し、checkpoint を残すための Skill です。

### `incremental-update`

既存の Web アプリ、レポート、設定、データなどを更新するときに、全件再処理を避け、差分抽出 → 必要部分の処理 → 検証 → 公開までを行う Skill です。

## 運用方針

- **Skill = 実行手順**
- **Rule = 安定した規則・判断基準**
- **State = プロジェクト固有の現在値**
- **Memory = 長期間安定する個人方針と routing**
- コードや長い仕様、raw log、短命な状態は Memory に持たせません。
- プロジェクト固有の State は原則として各プロジェクト側で管理します。
- Rules / Skills は必要なものだけ読み込み、毎回すべてを Context に入れません。

## Codex との関係

Codex がリポジトリ作業時に自動で参照する入口は `AGENTS.md` です。このリポジトリの `AGENTS.md` は短い routing 情報だけを保持し、詳細な規則は `rules/`、具体的な手順は `skills/` に分離します。
