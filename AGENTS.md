# Repository instructions

このリポジトリは、AI Agent 用の Rules と Skills の正本として扱う。

## 基本方針

- 詳細な共通規則は `rules/` に置く。
- 特定タスクの再利用可能な実行手順は `skills/<skill-name>/SKILL.md` に置く。
- プロジェクト固有の現在状態・ID・URL・一時ログを、このリポジトリの共通 Rules / Skills に埋め込まない。
- Rules / Skills は小さく保ち、同じ内容を複数ファイルへ重複させない。
- 機械的に検証できる内容は、文章ルールよりテスト・schema・通常コードを優先する。

## 編集時の参照

- 構成・分類を変更する場合: `README.md` と `rules/core.md`
- Context / State を変更する場合: `rules/context-and-state.md`
- model / effort / cost を変更する場合: `rules/model-and-cost.md`
- diff / validation を変更する場合: `rules/change-and-validation.md`
- Workflow を変更する場合: 対応する `skills/*/SKILL.md`

ユーザーの最新指示、およびタスク固有の明示的な仕様を最優先する。
