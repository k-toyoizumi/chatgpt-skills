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
- Gitの権限・履歴・送信方針を変更する場合: `rules/git-workflow.md`
- 差分更新 workflow を変更する場合: `skills/incremental-update/SKILL.md`
- 論文・技術調査 workflow を変更する場合: `skills/research-survey/SKILL.md`
- その他の Workflow を変更する場合: 対応する `skills/*/SKILL.md`

ユーザーの最新指示、およびタスク固有の明示的な仕様を最優先する。

## 共通の対話 routing（当面の標準）

- 全分野の作業で `rules/interaction.md` と `skills/iterative-micro-interview/SKILL.md` を基本とする。専門Skillはその上で使い、質問を二重に実施しない。
- 単純な質問・明確な小修正・即答や一任の依頼では、対話工程を縮小または省略する。

## Git操作の routing

- 作業成果のステージング・コミット・プッシュでは `rules/git-workflow.md` と `skills/git-workflow/SKILL.md` を参照する。合意した作業は検証後の通常プッシュまで自律実行し、個別の制限指示を優先する。

## GUI開発の routing

- アプリ・GUIの新規開発や改善では `skills/develop-gui/SKILL.md` を参照する。小修正では質問・画面2案比較を省略し、重要な曖昧さだけ選択式で確認する。

## 研究開発の routing

- 研究方向・サーベイ設計・アイデア・実験・研究コードの具体化は `skills/research-dialogue/SKILL.md` を参照する。通常3〜5問ずつ検討を重ね、段階移行はユーザーが選ぶ。単純な質問・明確な小修正には適用しない。
- 文献調査の実行は `research-survey`、研究GUIの画面・動作検証は `develop-gui` と併用し、同じ質問を重複させない。

## 数学研究・形式証明・論文化の routing

- 数学的な新規発見、証明の監査、Leanによる検証、研究ノートの蓄積、論文候補への昇格では `rules/mathematical-research.md` と `skills/mathematical-research-to-paper/SKILL.md` を参照する。
- 研究方向の対話は既存の `research-dialogue`、文献調査は `research-survey` を併用し、重複した質問をしない。

## HTML教科書の routing

- 日本語HTML教材・オンライン教科書の新規制作・改訂では `skills/textbook-authoring/SKILL.md` を参照する。Quartoを正本とし、図表を自動採番・相互参照する。共通対話Skillとの質問重複を避ける。
