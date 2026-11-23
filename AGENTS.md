# Repository instructions

このリポジトリはエージェント向け共通規約と Skill の正本。共通規約は `rules/`、再利用する手順は `skills/<skill-name>/SKILL.md` に置く。案件の現在値や一時ログは案件側で管理する。

- エージェントの設計・挙動・運用を変える提案、修正、機能追加では、方針を決める前に `skills/agent-design-research/SKILL.md` を読む。
- 共通規約・Skill・読込案内を変更したら、完了報告前に [利用先との整合性確認](docs/consumer-consistency.md) を実施する。
- Git 操作は `rules/git-workflow.md` と `skills/git-workflow/SKILL.md` に従う。

## 関連する参照先

- 共通方針と適用範囲は `rules/core.md`。状態管理、モデルと費用、変更と検証はそれぞれ `rules/context-and-state.md`、`rules/model-and-cost.md`、`rules/change-and-validation.md`。
- 計画・実行・レビュー・対話・判断支援は `rules/interaction.md`。
- 研究の判断は `rules/research.md`、研究対話と文献調査は `research-dialogue` と `research-survey`。数学研究は `rules/mathematical-research.md` と `mathematical-research-to-paper`。
- 差分更新、長時間計算、GUI、HTML 教材、油絵は、それぞれ `incremental-update`、`long-running-compute`、`develop-gui`、`textbook-authoring`、`painting-guide`。Skill 名はこの正本の `skills/<skill-name>/SKILL.md` を指す。
