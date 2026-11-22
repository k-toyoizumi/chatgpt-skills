---
name: background-critical-review
description: ユーザーがサブエージェントによる独立レビューを明示依頼したとき、計画・研究・資料・変更差分をバックグラウンドで批判的に検討する。
---

# バックグラウンド批判的レビュー

1. 対象の版を固定する。未コミット差分なら基点と差分の写し、文書なら版または該当箇所を渡す。目的、判断基準、根拠資料、確認範囲を添える。
2. 作成担当から独立した読み取り専用の担当へ依頼する。モデルと effort は正本の `rules/model-and-cost.md` に従う。同じ対象の再確認は独立性を保てるレビュー担当に差分を渡す。委譲できなければ独立レビューが未実施である旨を伝える。
3. 担当は要件漏れ、前提を崩す反例、根拠の不足、検証の抜けを探す。各指摘に対象箇所、根拠、影響、確かめ方を付ける。根拠が得られない疑問と確認済みの不備を区別する。
4. 親は結果に依存しない作業を続ける。対象に依存する判断や完了報告の前に結果を回収し、その間の変更と照合する。指摘の採否と理由を示し、依頼範囲で修正した箇所を再検証する。時間切れ・未回収をレビュー完了と数えない。

参考：[OpenAI の Subagents](https://developers.openai.com/codex/subagents/)、[Superpowers の requesting-code-review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md)
