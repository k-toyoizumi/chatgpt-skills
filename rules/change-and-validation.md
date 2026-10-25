# Change and Validation Rules

このファイルには、変更・検証に関する安定した原則だけを置く。
具体的な実行手順は `skills/incremental-update/SKILL.md` に置く。
Gitによる記録・送信の判断は `rules/git-workflow.md`、手順は `skills/git-workflow/SKILL.md` を参照する。

## Change principles

- 既存成果物の更新では、可能な限り全件再処理より差分更新を優先する。
- 変更のないデータ・成果物は再利用する。
- 変更対象だけでなく、直接依存する範囲まで影響を確認する。
- stable ID、更新時刻、hash などで決定論的に差分判定できる場合は、LLM に semantic comparison をさせない。
- 機械的に処理できる内容は、LLM より通常コード・通常ツールを優先する。
- 共通 Rules では utility 関数の具体的実装を固定しない。必要な実コードは各プロジェクト側に置く。

## Validation principles

- 更新後は、変更内容に応じた検証を必ず行う。
- 研究では `rules/research.md` に従い、段階と判断への寄与に応じて検証範囲を選ぶ。探索中のアイデアに網羅的なコードテストを完了条件として課さず、コードの動作確認と研究上の価値・仮説の検証を区別する。
- 長時間かかる処理の動作確認は、全件ではなく代表的な数件で行い、学習ステップ数なども小さく制限する。少数件の成功を全件検証・性能評価の完了と扱わない。具体的な手順は `skills/long-running-compute/SKILL.md` を参照する。
- schema、参照、件数、主要導線、主要機能など、機械的に検証できるものは通常コード・テストを優先する。
- LLM の自己評価だけを唯一の validation としない。
- 検証失敗時は、失敗箇所を限定して修正・再検証する。
- 正常性を確認できない成果物を、正常版として公開しない。
- 長期プロジェクトでは、必要に応じて last-known-good の version / commit / URL を Project State に保持する。
- 共通Rules / Skillsの変更では、利用プロジェクトの読込経路と関連する規約との整合性も検証する。機械的な同期成功を意味上の整合性の検証と同一視しない。具体的手順は正本ルートの `docs/consumer-consistency.md` を参照する。

## Publish principles

- 公開・同期は、必要な validation の成功後に行う。
- 公開先が既存の正常版を置き換える場合は、復旧可能性を考慮する。
- validation の不足や未解決 issue が残る場合は、その状態を明示する。
