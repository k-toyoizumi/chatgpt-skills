# WSLでの実行権限・通信障害の切り分け

要点：WSL全体の通信障害、Codexのsandbox境界、承認設定、アプリ側の障害を区別する。通常実行の失敗だけで「PCがオフライン」「設定変更が必須」と断定しない。

## 最小検査

1. 作業ディレクトリ、実行中のpermission profile、書込可能ルート、ツールの昇格可否を確認する。ユーザーの作業承認と実行環境の許可は別に扱う。設定不明を確認済みとしない。
2. 対象ディレクトリ内で一時ファイルを作成・削除できるか確認する。`os.access`だけで実際の書込成功を判断しない。親ディレクトリの作成や既存ファイルの上書きを検査に含めない。
3. 作業に必要な公開URLへの小さい読取と、127.0.0.1の一時サーバーへの要求を別々に検査する。URLは対象サービスに合わせ、timeout・取得量を限定し、検査直後にサーバーを閉じる。認証情報や環境変数全件を出力しない。

以下はPython標準ライブラリだけで行う小さい通信検査の例。作業上必要なURLに置き換える。外部取得とlocalhostを一方の失敗で省略しない。

```python
import http.server
import json
import threading
import urllib.request

result = {}
try:
    with urllib.request.urlopen("https://example.com/", timeout=10) as response:
        result["external"] = {"status": response.status, "bytes": len(response.read(256))}
except Exception as exc:
    result["external"] = {"error": type(exc).__name__, "detail": str(exc)}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"probe-ok")
    def log_message(self, *args):
        pass

try:
    with http.server.HTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/"
            with urllib.request.urlopen(url, timeout=3) as response:
                result["loopback"] = {"status": response.status, "body_ok": response.read(32) == b"probe-ok"}
        finally:
            server.shutdown()
            thread.join(timeout=2)
except Exception as exc:
    result["loopback"] = {"error": type(exc).__name__, "detail": str(exc)}
print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 診断と対処

| 結果 | 判断・次の操作 |
| --- | --- |
| DNS失敗・host解決失敗 | sandboxによる制限も候補。これだけでWSLのDNS設定を変更しない |
| socket作成/bindがEPERM・EACCES | サーバー起動前の権限制限を疑う。接続拒否やアプリ不具合と区別する |
| ConnectionRefused | socket作成は可能。対象portの起動状態・listen先を調べる |
| 通常実行は失敗、許可された昇格実行は成功 | 調べた処理の実行境界に差がある。PC全体のネットワーク断と扱わず、以降の必要コマンドを許可された経路で実行する |
| 両方失敗 | 各エラーに応じて対象host・proxy・証明書・WSL/Windows間の接続先などを調べる。loopback成功だけでWindows側localhostへの到達も確認済みとしない |
| browser/connectorは成功、shellは失敗 | 実行経路が異なる。connectorの成功をshellでのbinary取得成功に読み替えない |

重要な作業がsandbox由来と考えられるエラーで止まったら、ツールと上位policyが許可する場合に限り、**同じ最小検査**を `sandbox_permissions="require_escalated"` と具体的な `justification` で再実行する。先にユーザーへ設定変更やFull accessを求めることを既定にしない。これは通常の権限承認経路であり、ユーザーの作業範囲・課金・実験上限を拡大しない。

昇格が禁止・不提供、または自動承認レビューで拒否された場合はその境界を守る。同じ処理を別ツール・proxy・トンネル等で制限回避しない。拒否された操作と理由をユーザーへ簡潔に報告し、影響しない作業を進める。環境側の対応が必要なら、書込対象・公開host・localhostのどの能力が不足するかを具体化する。スマホや既存会話で設定変更できるとは未確認のまま案内しない。

## 復旧後と引継ぎ

- 取得物は期待するrevision・サイズ・hashで照合する。通信成功は依存・モデル・観測・アプリの互換性成功ではない。
- import後に結果が出てもプロセスが終了しない場合は、deadlineと所有process groupの終了処理を付け、結果生成と正常自然終了を分けて記録する。既存サーバーや無関係プロセスを停止しない。
- 案件のStateへ通常/昇格の結果、未解決事項、必要な実行経路、所有プロセスの終了状態と次の一手を残す。共通Rulesへ案件固有ID・実行ログを埋め込まない。
- 成功した1コマンドを、セッション全体の設定変更、別会話の権限、恒久的な復旧、WSL再起動後の継続保証と扱わない。

## 根拠

[公式Sandbox説明](https://learn.chatgpt.com/docs/sandboxing)では承認とsandboxを別の制御として説明している。画面上の承認モードだけで通信権限が変わったと推測せず、実際の最小検査で判断する。具体的な昇格API名は利用ツールによって異なるため、そのセッションのschemaと上位policyを優先する。
