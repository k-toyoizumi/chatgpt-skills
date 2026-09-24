# Repository instructions

このリポジトリは、AI Agent 用の Rules と Skills の正本として扱う。

## 基本方針

- 詳細な共通規則は `rules/` に置く。
- 特定タスクの再利用可能な実行手順は `skills/<skill-name>/SKILL.md` に置く。
- プロジェクト固有の現在状態・ID・URL・一時ログを、このリポジトリの共通 Rules / Skills に埋め込まない。
- Rules / Skills は小さく保ち、同じ内容を複数ファイルへ重複させない。
- 機械的に検証・処理できる内容は、LLM よりテスト・schema・通常コード・通常ツールを優先する。
- 共通 Rule では具体的なモデル名を原則固定せず、能力区分と reasoning effort で記述する。

## 編集時の参照

- 構成・分類を変更する場合: `README.md` と `rules/core.md`
- Context / State を変更する場合: `rules/context-and-state.md`
- model / effort / cost を変更する場合: `rules/model-and-cost.md`
- diff / validation の原則を変更する場合: `rules/change-and-validation.md`
- 差分更新 workflow を変更する場合: `skills/incremental-update/SKILL.md`
- 論文・技術調査 workflow を変更する場合: `skills/research-survey/SKILL.md`
- その他の Workflow を変更する場合: 対応する `skills/*/SKILL.md`

ユーザーの最新指示、およびタスク固有の明示的な仕様を最優先する。
