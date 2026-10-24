#!/usr/bin/env python3
"""Synchronize a small routing block; never claim a semantic review."""
import argparse
import hashlib
from pathlib import Path
import sys

START = '<!-- chatgpt-skills:begin -->'
END = '<!-- chatgpt-skills:end -->'


def source_digest(source):
    files = [source / 'AGENTS.md', *sorted((source / 'rules').glob('*.md')),
             *sorted((source / 'skills').rglob('*'))]
    digest = hashlib.sha256()
    for path in files:
        if path.is_file() and '__pycache__' not in path.parts:
            digest.update(str(path.relative_to(source)).encode())
            digest.update(b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


def routing(source):
    return f'''{START}
## 共通Rules・Skillsの読込（自動管理）

- 正本ルート：`{source}`。正本内の `rules/...` と `skills/...` はこのルートから解決する。
- セッション開始時に `{source}/rules/core.md` と `{source}/rules/interaction.md` を実際に読む。参照先が読めない場合は不足を報告する。
- その他のRules・Skillsは作業に関連するものだけ読む。プロジェクト固有の目的・予算・承認条件も併用する。
- 作業後は **実施事項・現状報告・次のアクション** を簡潔に回答する。次のアクションはAgent側・ユーザー側を区別し、不要なら「なし」と記す。
- 正本変更後は、今回の変更に関係する案件側の規約・仕様との整合性も確認する。下記の同期値は読込案内の生成元であり、意味上の整合性や実際の会話での適用を検証済みとする証拠ではない。

正本内容SHA256: `{source_digest(source)}`
{END}'''


def updated(text, block):
    if START not in text and END not in text:
        return text.rstrip() + '\n\n' + block + '\n'
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('管理区画のマーカーが不正（自動修復しません）')
    start, end = text.index(START), text.index(END)
    if end < start:
        raise ValueError('管理区画のマーカー順序が不正')
    return text[:start] + block + text[end + len(END):]


def candidates(source, roots):
    # Immediate siblings only. Unrelated projects are not enrolled automatically.
    for root in roots:
        for project in sorted(root.iterdir()):
            if project.is_symlink() or not project.is_dir() or project.resolve() == source:
                continue
            path = project / 'AGENTS.md'
            if path.is_symlink() or not path.is_file():
                continue
            text = path.read_text()
            if str(source) in text or START in text:
                yield path, text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    parser.add_argument('--projects-root', type=Path, action='append',
                        help='探索する親ディレクトリ（複数指定可、既定は正本の親）')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    for relative in ('rules/core.md', 'rules/interaction.md'):
        if not (source / relative).is_file():
            parser.error(f'共通参照先がありません: {relative}')
    block = routing(source)
    changes = errors = count = 0
    seen = set()
    for root in args.projects_root or [source.parent]:
        try:
            for path, old in candidates(source, [root]):
                if path in seen:
                    continue
                seen.add(path)
                count += 1
                try:
                    new = updated(old, block)
                    if new != old:
                        changes += 1
                        if args.apply:
                            # Preserve concurrent edits rather than overwriting them.
                            if path.read_text() != old:
                                raise ValueError('検査後に変更されたため停止')
                            path.write_text(new)
                        print(f'{"SYNC" if args.apply else "DRIFT"}: {path}')
                    else:
                        print(f'OK: {path}')
                except (OSError, ValueError) as exc:
                    errors += 1
                    print(f'ERROR: {path}: {exc}', file=sys.stderr)
        except OSError as exc:
            errors += 1
            print(f'ERROR: {root}: {exc}', file=sys.stderr)
    print(f'対象={count}, 差分={changes}, エラー={errors}。意味上の整合性はAgentによる確認が必要。')
    if count == 0:
        print('WARNING: 対象なし。探索先と各AGENTS.mdの正本参照を確認してください。', file=sys.stderr)
    return 1 if errors or count == 0 or (args.check and changes) else 0


if __name__ == '__main__':
    sys.exit(main())
