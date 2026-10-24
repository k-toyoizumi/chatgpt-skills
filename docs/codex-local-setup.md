# ローカルCodex設定と使用量表示

適用日：2026-10-24（日本時間）。WSLのCLI用。デスクトップ・スマホのUIを変更するものではない。
モデル方針の正本は `rules/model-and-cost.md`。

## 起動

対象プロジェクトのディレクトリから起動する。恒久的な追加書込先は設けず、workspace-write/on-requestを基本とし、アプリ・管理ポリシーを優先する。

```bash
codex                               # 通常：6-Luna medium
codex --profile multi-file          # 複数ファイル：6-Luna high
codex --profile review              # 計画・レビュー：6.1-Sol medium
codex --profile orchestrate         # 進行管理・結果統合：6.1-Sol low
codex --profile hard-implementation # 難しい実装：6.1-Sol low
```

設定ファイルはWSLの `$CODEX_HOME`（未指定なら `~/.codex`）内。通常はconfig.toml、用途別は `<profile>.config.toml`。Windowsのアプリ管理設定は保持する。モデル・effortの自動切替やサブエージェント自動起動は行わない。
このデスクトップアプリの子プロセスはWindows側の `CODEX_HOME` を継承する場合がある。WSL専用設定を使うときは `env -u CODEX_HOME codex`、プロファイルは `env -u CODEX_HOME codex --profile review` のように起動する。補助表示もWSLのログを対象とする場合は `env -u CODEX_HOME ~/.codex/bin/codex-status --thread <会話UUID>` とする。環境変数が意図した設定先を指している通常のWSL端末では不要。

起動後 `/status` と `/debug-config` で実効値を確認する。アプリ起動・プロジェクト設定・CLI引数が優先し、既存の会話は設定変更だけで切り替わらない。

## 標準表示

`tui.status_line` にモデル＋effort、コンテキスト残量、累計input/output、週の利用枠を設定。`/statusline` で調整可能。
cache内訳・任意の推奨文は補助ペインに表示する。

## 補助ペイン

以下のコマンドは導入済みWSLでの例。リポジトリ移設時は `~/.codex/bin/codex-status` のリンク先を更新する。

```bash
# tmux内でCLIを起動
 tmux new-session -s codex
 codex
# CLIの/statusで会話IDを確認。tmuxの別ペイン/ウィンドウから：
 ~/.codex/bin/codex-status --thread <会話UUID> --pane
# tmuxを使わない場合は別端末で：
 ~/.codex/bin/codex-status --thread <会話UUID>
# 単発確認、またはログを直接指定：
 ~/.codex/bin/codex-status --log /absolute/path/rollout.jsonl --once
```

`--pane` はコマンドを実行したtmuxウィンドウに高さ12行のペインを追加する。CLIを動かしているウィンドウを指定したい場合は、そのウィンドウでtmuxのコマンドプロンプトから `run-shell 'コマンド'` を実行するか、別ペインから実行する。終了は補助ペインでCtrl-C。Codex本体や学習ジョブは停止しない。

会話UUIDまたはログを明示し、最新の別会話を自動追跡しない。対応ログが一意に見つからない場合は停止する。セッションログの保存形式が変わった場合は対応を見直す。
初回は末尾最大2MiB、その後は追加分を2秒ごとに読む。ログ・設定・会話本文を書き換えず、ネットワーク通信・LLM呼出しも行わない。表示は最後の使用量記録であり、生成中のリアルタイム消費ではない。

## 指標と提案

- input/cache read/cache write/outputは記録がある項目だけ表示。cache readはinputの内数。cache write 0はログの記録値であり、キャッシュ機能の不存在や独立の課金額を意味しない。
- 「直近呼出し」はモデル1呼出し。「今回／直近の応答」はtask_started前後の累計差分を取得できた場合のみ表示。末尾内に基準がなければ非表示。会話累計はログに記録された累計値。
- コンテキスト残量は `last total_tokens / model_context_window` からの概算。予約領域等を考慮したCLI標準値と同一ではない。標準表示を優先する。
- 概算残量30%以下で整理、15%以下で引き継ぎ準備を提案。
- 直近inputが前回の1.5倍超かつ1万tokens以上増加したら読込範囲の確認を提案。
- inputが1万以上でcache read比率50%未満なら共通指示・重複読込を確認。初回や正当な入力変更でも生じるため悪い状態と断定しない。
- outputが8千tokens以上なら詳細のファイル保存を検討。品質を落とす強制削減はしない。
- 閾値は暫定の運用値。提案のみでモデル変更・圧縮・新規会話・課金操作はしない。

## 検証と限界

実ログ3件の読取と、追記・途中行・欠測・応答単位の差分・切詰め・提案境界をテストする。TOMLの構文検査とCLI起動時の設定読込は、モデルへタスクを送信する検証とは区別する。

公式資料：[プロファイル](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles)、[CLIコマンド](https://learn.chatgpt.com/docs/developer-commands)、[設定リファレンス](https://learn.chatgpt.com/docs/config-file/config-reference)。

## 今回の確認結果

- WSL設定・4プロファイルをTOMLとして読込確認。元の設定は `~/.codex/backups/config-status-*` に保存。
- CLIをWSLのCODEX_HOMEで起動し、`GPT-6-Luna medium · Context 100% left · 0 in · 0 out · weekly … left` の表示を確認。モデルへの依頼は未送信。
- このアプリ内のサンドボックスではdaemonソケットが制限されるため、画面検証は `env -u CODEX_HOME codex --no-daemon --no-alt-screen` で実施。通常のWSL端末で恒久的にdaemonを無効化したわけではない。
- 4プロファイルは構文検証済み。各モデルへの実タスク送信による成功確認は行っていない。
- tmuxの補助ペインで実ログの表示とCtrl-Cによる終了を確認。
- 表示処理6テストと既存の利用先同期5テストが成功。
