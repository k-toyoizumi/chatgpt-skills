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

特定タスクの具体的な手順は Rules に置かず、Skills に分離します。

### Skills

「特定の種類のタスクを、どう実行するか」を定義します。

- 明確な利用条件（trigger）
- 再利用可能な workflow
- 必要な Rules / source への参照
- 完了条件・検証方法

Skill は `SKILL.md` 形式で管理します。

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
    ├── incremental-update/
    │   └── SKILL.md
    └── research-survey/
        └── SKILL.md
```

## Rules 一覧

### `rules/core.md`

共通原則、適用範囲、指示の優先順位、品質とコストの優先順位を定義します。

### `rules/context-and-state.md`

Source of Truth、Project State、ChatGPT Memory、Working Set、Scratch の役割と、長期 Session の扱いを定義します。

### `rules/model-and-cost.md`

具体的なモデル名を固定せず、高速 / 標準 / 高性能という能力区分で model / reasoning effort を選択する方針を定義します。通常質問・Web調査と、論文調査各段階の routing もここで定義します。

### `rules/change-and-validation.md`

差分更新、LLM と通常コードの役割分担、検証、公開、last-known-good に関する**原則のみ**を定義します。具体的な更新手順は `incremental-update` Skill に置きます。

## Skills 一覧

### `project-session-management`

長期プロジェクトを開始・再開・終了するときに、必要な State だけを読み、Working Set を構築し、checkpoint を残すための Skill です。

### `incremental-update`

既存の Web アプリ、レポート、設定、データなどを更新するときに、差分抽出 → 影響範囲選択 → 変更 → 検証 → 公開を行う Skill です。

### `research-survey`

論文・技術調査を以下の3段階で行います。

1. **pre-survey** — 調査観点・仮説・検索軸を設計
2. **quick-and-wide-survey** — タイトル・abstract 中心に広く候補を収集・一次選別
3. **deep-research** — 重要文献を深く読み、複数文献を統合・比較・分析

調査の明確さや難易度に応じて、段階の省略・effort の調整を許容します。

## 運用方針

- **Skill = 実行手順**
- **Rule = 安定した規則・判断基準**
- **State = プロジェクト固有の現在値**
- **Memory = 長期間安定する個人方針と routing**
- 決定論的に処理できる作業は、利用可能な通常コード・通常ツールを優先します。
- 汎用 utility の具体的実装はこの共通リポジトリで固定せず、必要になった各プロジェクト側で実装します。
- コードや長い仕様、raw log、短命な状態は Memory に持たせません。
- プロジェクト固有の State は原則として各プロジェクト側で管理します。
- Rules / Skills は必要なものだけ読み込み、毎回すべてを Context に入れません。

## Codex との関係

Codex がリポジトリ作業時に参照する入口は `AGENTS.md` とし、このファイルには短い routing 情報だけを保持します。詳細な規則は `rules/`、具体的な手順は `skills/` に分離します。
