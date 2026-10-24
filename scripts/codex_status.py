#!/usr/bin/env python3
"""Local, read-only Codex usage companion. No API or model calls."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

CAP = 2 * 1024 * 1024
FIELDS = [('input_tokens', 'input'), ('cached_input_tokens', 'cache read'),
          ('cache_write_input_tokens', 'cache write'), ('output_tokens', 'output')]


def safe(value):
    return ''.join(c if c.isprintable() else '?' for c in str(value))


def recommend(remaining, last, previous):
    result = []
    if remaining is not None:
        if remaining <= 15:
            result.append('引き継ぎ準備：目的・決定・未解決点・次の一手を保存')
        elif remaining <= 30:
            result.append('整理を推奨：読込範囲を絞り、決定事項を外部Stateへ保存')
    inp = last.get('input_tokens')
    old = previous.get('input_tokens')
    cache = last.get('cached_input_tokens')
    if isinstance(inp, int) and isinstance(old, int) and old > 0 and inp > old * 1.5 and inp - old >= 10000:
        result.append('入力が増加：全文読込や大きなツール出力が必要だったか確認')
    if isinstance(inp, int) and inp >= 10000 and isinstance(cache, int) and 0 <= cache < inp * .5:
        result.append('cache read比率が低め：共通指示の並び・重複読込を確認（初回は自然）')
    out = last.get('output_tokens')
    if isinstance(out, int) and out >= 8000:
        result.append('出力が多め：詳細をファイルに保存し、会話では要点を共有できるか確認')
    return result or ['現時点で追加の提案なし。作業品質を優先して継続']


class Tracker:
    def __init__(self, path):
        self.path = path
        self.offset = 0
        self.pending = b''
        self.identity = None
        self.info = None
        self.previous = {}
        self.stamp = ''
        self.baseline = None
        self.turn = None
        self.in_turn = False

    def poll(self):
        st = self.path.stat()
        identity = (st.st_dev, st.st_ino)
        if self.identity != identity or st.st_size < self.offset:
            self.__init__(self.path)
            self.identity = identity
        if st.st_size == self.offset:
            return
        with self.path.open('rb') as stream:
            if st.st_size - self.offset > CAP:
                self.offset = st.st_size - CAP
                self.pending = b''
                self.baseline = None
                self.turn = None
                self.in_turn = False
                stream.seek(self.offset)
                stream.readline()  # Drop potentially partial first record.
            else:
                stream.seek(self.offset)
            data = self.pending + stream.read(CAP)
            self.offset = stream.tell()
        lines = data.split(b'\n')
        self.pending = lines.pop()
        for line in lines:
            try:
                record = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if record.get('type') != 'event_msg':
                continue
            p = record.get('payload', {})
            kind = p.get('type')
            if kind == 'task_started':
                self.baseline = dict((self.info or {}).get('total_token_usage') or {}) or None
                self.turn = None
                self.in_turn = True
            elif kind == 'task_complete':
                self.in_turn = False
            elif kind == 'token_count' and isinstance(p.get('info'), dict):
                info = p['info']
                total = info.get('total_token_usage') or {}
                prior = (self.info or {}).get('total_token_usage') or {}
                if total != prior:
                    self.previous = (self.info or {}).get('last_token_usage') or {}
                self.info = info
                self.stamp = record.get('timestamp', '')
                if self.in_turn and self.baseline:
                    delta = {k: total[k] - v for k, v in self.baseline.items()
                             if isinstance(v, int) and isinstance(total.get(k), int)}
                    self.turn = delta if all(v >= 0 for v in delta.values()) else None

    def render(self):
        if not self.info:
            return '使用量記録を待機中（末尾2MiB以内のみ読取）'
        last = self.info.get('last_token_usage') or {}
        total = self.info.get('total_token_usage') or {}
        win, used = self.info.get('model_context_window'), last.get('total_tokens')
        remaining = max(0, min(100, 100 * (1 - used / win))) if isinstance(win, int) and win > 0 and isinstance(used, int) else None
        stamp = self.stamp
        try:
            dt = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
            stamp = dt.astimezone(timezone(timedelta(hours=9))).strftime('%m-%d %H:%M:%S JST')
        except (ValueError, AttributeError):
            pass
        lines = [f'Codex usage | 記録時刻 {safe(stamp)}',
                 '残量（概算） ' + f'{remaining:.1f}%' if remaining is not None else '残量：未取得',
                 '※直近呼出しのtokens/windowから算出。標準CLIの残量表示を優先。']
        rows = [('直近呼出し', last)]
        if self.turn is not None:
            rows.append(('今回の応答（進行中）' if self.in_turn else '直近の応答', self.turn))
        rows.append(('会話累計', total))
        for title, usage in rows:
            vals = [f'{label} {usage[k]:,}' for k, label in FIELDS if isinstance(usage.get(k), int)]
            if vals:
                lines.append(title + ' | ' + ' | '.join(vals))
        lines += ['※cache readはinputの内数。writeはログ記録値（独立課金額ではない）。',
                  '提案のみ（モデル変更・圧縮・新規会話は実行しません）']
        lines += ['・' + s for s in recommend(remaining, last, self.previous)]
        lines.append('更新待ちの間は最後の記録値を表示。Ctrl-Cで表示を終了。')
        return '\n'.join(lines)


def resolve(args):
    if args.log:
        return args.log.expanduser().resolve(strict=True)
    import uuid
    thread = str(uuid.UUID(args.thread))
    home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    matches = list((home / 'sessions').rglob(f'*{thread}*.jsonl'))
    if len(matches) != 1:
        raise ValueError(f'会話IDに対応するログが一意に見つかりません（{len(matches)}件）。--logで指定してください')
    return matches[0].resolve()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--log', type=Path)
    g.add_argument('--thread', help='Codexの/statusで確認した会話UUID')
    p.add_argument('--once', action='store_true')
    p.add_argument('--pane', action='store_true', help='現在のtmuxへ補助ペインを追加')
    p.add_argument('--interval', type=float, default=2)
    a = p.parse_args()
    if a.interval < .5:
        p.error('--interval must be >= 0.5')
    try:
        path = resolve(a)
        if a.pane:
            if not os.environ.get('TMUX') or not shutil.which('tmux'):
                p.error('--paneはtmux内で使います。別端末では--paneなしで実行してください')
            command = shlex.join([sys.executable, str(Path(__file__).resolve()), '--log', str(path), '--interval', str(a.interval)])
            target = ['-t', os.environ['TMUX_PANE']] if os.environ.get('TMUX_PANE') else []
            subprocess.run(['tmux', 'split-window', *target, '-v', '-l', '12', command], check=True)
            return
        t = Tracker(path)
        while True:
            t.poll()
            if sys.stdout.isatty() and not a.once:
                print('\033[2J\033[H', end='')
            print(t.render(), flush=True)
            if a.once:
                return
            time.sleep(a.interval)
    except KeyboardInterrupt:
        return
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        p.exit(1, safe(e) + '\n')


if __name__ == '__main__':
    main()
