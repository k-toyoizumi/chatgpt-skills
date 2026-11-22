---
name: work-planning
description: 開発・研究・調査・資料制作などの依頼を、検証可能な工程と担当配分を備えた計画にする。
---

# 計画立案

1. 依頼と案件の既存資料から、目的・成果物・完了条件・制約を特定する。ユーザーの選択で方針が変わる場合だけ iterative-micro-interview を使う。
2. 各工程に入力・成果物・依存関係・確認方法を付ける。研究なら仮説を見直す条件、調査なら出典と打ち切り条件、資料制作なら読者と確認すべき内容など、成果物に適した条件を選ぶ。
3. 正本の `rules/model-and-cost.md` に従い、親と各担当について「担当するタスク群／成果物と完了条件／具体的モデル・effort／新規または再利用の理由」を示す。難易度・誤判断の影響・共有する資料を見て割り当てる。例えば同じ文献群の抽出と比較表の作成は、設定が適合する同一担当へ順次渡す。小作業なら親だけで足りる理由を一行で示す。
4. 当日中に完了する短い計画も含め、計画は案件内に Markdown で保存し、会話で保存先を示す。既存の計画・State の置き場を優先し、複数日または引き継ぎを伴う場合は前提と再開地点も添える。
5. 計画だけの依頼は提示して終了する。実行まで依頼されていれば work-execution に引き継ぐ。

参考：[OpenAI Cookbook の ExecPlans](https://developers.openai.com/cookbook/articles/codex_exec_plans)、[Superpowers の writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)
