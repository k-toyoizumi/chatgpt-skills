# ChatGPT Skills / Rules

ChatGPT・Codex などの AI Agent で再利用する、個人用の **Rules（規則）** と **Skills（実行手順）** を管理するリポジトリです。

> リポジトリ名は現在 `chatgpt-skills` ですが、Skills だけでなく Rules も管理します。名称変更は必要になった時点で行います。

## 計画・実行・レビュー

計画は `work-planning`、合意済み計画の実行は `work-execution`、明示依頼された独立レビューは `background-critical-review` を使う。計画時に重要な選択が残る場合は `iterative-micro-interview` を併用する。

- [work-planning](skills/work-planning/SKILL.md) は各工程の依存関係、並列に着手できる組み合わせ、担当と合流時の検証を計画に記します。
- [explain-for-decisions](skills/explain-for-decisions/SKILL.md) は計画・実験結果を図表と根拠で説明し、人間の判断を支援します。
- [work-execution](skills/work-execution/SKILL.md) は前提がそろった工程から着手し、担当の成果を回収・統合します。
- [background-critical-review](skills/background-critical-review/SKILL.md)
- [iterative-micro-interview](skills/iterative-micro-interview/SKILL.md)

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
│   ├── change-and-validation.md
│   └── git-workflow.md
└── skills/
    ├── project-session-management/
    │   └── SKILL.md
    ├── incremental-update/
    │   └── SKILL.md
    ├── research-survey/
    │   └── SKILL.md
    └── git-workflow/
        └── SKILL.md
```

## Rules 一覧

### `rules/core.md`

共通原則、適用範囲、指示の優先順位、品質とコストの優先順位を定義します。

### `rules/context-and-state.md`

Source of Truth、Project State、ChatGPT Memory、Working Set、Scratch の役割と、長期 Session の扱いを定義します。

### `rules/model-and-cost.md`

用途別にLuna medium/highとSol low/mediumを使う方針と、reasoning effort・委譲・Agent再利用の基準を定義します。具体的なモデル識別子は実行時に確認し、論文調査にも同じ役割分担を適用します。

### `rules/change-and-validation.md`

差分更新、LLM と通常コードの役割分担、検証、公開、last-known-good に関する**原則のみ**を定義します。具体的な更新手順は `incremental-update` Skill に置きます。

### `rules/research.md`

研究の探索では問い・問題設定・新しい着想を優先し、方向選択後に厳密な検証と再現可能な蓄積へ進む方針を定義します。探索中の検証は、方向選択を変え得る範囲に絞ります。

### `rules/git-workflow.md`

合意した作業の自律操作範囲、ブランチ選択、既存変更の保全、履歴改変とプッシュの判断基準を定義します。

## Skills 一覧

### `long-running-compute`

長時間の学習・評価・バッチ計算を、少数件での動作確認からWSLでのバックグラウンド起動・起動確認・引き継ぎまで進める[Skill](skills/long-running-compute/SKILL.md)です。他に作業がなければ完了を待たず応答を終了します。

### `project-session-management`

長期プロジェクトを開始・再開・終了するときに、必要な State だけを読み、Working Set を構築し、checkpoint を残すための Skill です。

### `incremental-update`

既存の Web アプリ、レポート、設定、データなどを更新するときに、差分抽出 → 影響範囲選択 → 変更 → 検証 → 公開を行う Skill です。

### `agent-design-research`

エージェントの設計・挙動・運用を変える際に、開発元の公式推奨と公開実例を確認し、利用環境に照らして現行方式と変更案を比較する [Skill](skills/agent-design-research/SKILL.md) です。

### `research-survey`

論文・技術調査を以下の3段階で行います。

1. **pre-survey** — 調査観点・仮説・検索軸を設計
2. **quick-and-wide-survey** — タイトル・abstract 中心に広く候補を収集・一次選別
3. **deep-research** — 重要文献を深く読み、複数文献を統合・比較・分析

調査の明確さや難易度に応じて、段階の省略・effort の調整を許容します。

### `iterative-micro-interview`

計画時に重要な選択を具体化する対話手順。短い選択式質問と回答の検討・追加質問・小さな検証を反復し、重要判断を共有して本格実行へ進みます。

### `research-dialogue`

研究の目的・仮説・サーベイ範囲・実験評価の判断軸を扱います。文献調査・GUIの専門Skillと併用します。

### `develop-gui`

アプリ・GUIの開発・改善を、重要事項の選択式確認 → 大きな変更時の画面2案比較 → 小さな実装 → 実操作・スクリーンショット・既存機能の検証で進めます。小修正では質問や2案比較を省略します。

### `git-workflow`

差分確認・変更の選別・検証・ステージング・コミットを自律実行します。基本的な確認・add・通常のcommitは事前承認済み、pushはユーザーの明示指示時だけ未送信分をまとめて行います。コミットごとのpush承認依頼はしません。小さな個人作業は現在のブランチ、共同作業や大きな変更は作業ブランチ＋PRを基本にします。


### `painting-guide`

初心者の油絵制作を、構想・完成目標画像の選択・工程計画・四角色見本と混色比を使った制作ガイド・写真レビューまで支援するSkill。描く楽しさと本人の表現を尊重し、最低限の重要特徴と簡略化可能な部分を分けて助言します。

- [Skill本体](skills/painting-guide/SKILL.md)
- [表示ルール](skills/painting-guide/references/step-format.md)

### `textbook-authoring`

日本語HTML教科書をQuartoで制作・検証するSkill。静的SVG・Mermaid図解、比較表、数式、演習を扱い、図・表には自動採番と本文からの相互参照を付けます。研究者向けSelf-Attentionのサンプルを導入ページ＋3章の独立したHTMLに分割し、左の折りたたみ可能な章選択、右のページ内目次、スマホの章メニューと前後章移動に対応します。

- [Skill本体](skills/textbook-authoring/SKILL.md)
- [導入・検証ガイド](skills/textbook-authoring/README.md)

## 別のPC・Agentで利用する

```bash
git clone https://github.com/k-toyoizumi/chatgpt-skills.git
```

必要な `skills/<skill-name>/` を対象AgentのSkill配置先へコピーし、ローカル版を用途に合わせて編集してください。GUI開発の入口は [skills/develop-gui/SKILL.md](skills/develop-gui/SKILL.md) です。対象Agentの指示ファイルから明示的に参照する方法も使えます。

このリポジトリは公開された汎用の正本です。会社固有の変更は社内のローカルコピー・非公開リポジトリで管理し、上流更新は差分を確認して取り込んでください。Cloneしただけでは、別プロジェクトやすべての会話に自動適用されるわけではありません。

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

共通設定の更新時は、[利用プロジェクトとの整合性確認](docs/consumer-consistency.md)も実施します。`scripts/sync_consumers.py --check` で読込案内を検査し、`--apply` で専用区画を同期します。`git config core.hooksPath .githooks` でGit操作後の自動同期を有効化できます。既存hookがある場合は先に統合し、意味上の衝突は更新担当Agentが確認します。

## 数学研究から論文化まで

- 判断規則：[rules/mathematical-research.md](rules/mathematical-research.md)
- 実行手順：[skills/mathematical-research-to-paper/SKILL.md](skills/mathematical-research-to-paper/SKILL.md)

数学研究の仮説・計算・Lean形式証明・先行研究との差分を各プロジェクト側に蓄積し、厳密性・新規性・重要性を別々に評価して論文候補へ昇格させます。具体的な研究ノートや証明ログは共通リポジトリに埋め込みません。

## ローカルCodex設定と使用量表示

モデル・プロファイル・補助ペインの使い方は [導入ガイド](docs/codex-local-setup.md) を参照してください。

## WSLの権限・通信トラブル

DNSエラー・localhostのsocket権限エラー・書込拒否は、[診断手順](docs/wsl-execution-troubleshooting.md)で通常実行と許可された昇格実行を比較します。承認設定とsandbox境界を区別し、必要な能力だけを確認して復旧します。
