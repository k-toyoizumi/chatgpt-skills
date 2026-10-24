# Textbook Authoring Skill v0.3

**用途:** Agentによる日本語HTML教科書の構成、静的図解、比較表、数式・実装、検証。

Quarto Bookをソースの正本とし、図・表は**自動番号とクリック可能な相互参照**を付けます。図の装飾アニメーションは原則使いません。

## 含まれるサンプル

`assets/quarto-book/` に研究者向け Self-Attention 1章を収録しています。SVG図5枚、比較表1件、数式とPyTorch検証例、確認問題4問を含みます。

## 使い方

1. `SKILL.md` と `references/` を参照し、教材の学習目標・構成を作る。
2. `assets/quarto-book` を教材リポジトリへ複製し `.qmd` を編集する。図は `{#fig-name}`、表は `{#tbl-name}` を付け、本文から `@fig-name` / `@tbl-name` で参照する。
3. Quartoが使える環境では `cd assets/quarto-book && quarto render` を実行する。
4. このSkill内での検証コマンド：

```sh
python scripts/validate.py
python scripts/test_numeric.py
python scripts/render_preview.py /tmp/attention-preview.html
python scripts/test_browser.py /tmp/attention-preview.html
```

Pandocによる単体HTMLプレビューは **Quarto本体のレンダリングの代替ではありません**。図と表の番号をQuarto Book風に表示しますが、複数章の場合は正式なQuartoビルドで章ごとの番号が確認できるまで公開しないでください。

## ChatGPT と Codex

- 共通Skill正本：`skills/textbook-authoring/SKILL.md`。
- Codex：対象リポジトリの `.agents/skills/textbook-authoring/` にSkillディレクトリをコピーするか、Skillsの検索対象に配置する。
- ChatGPT：専用Skill機能が使用できる環境では登録し、それ以外では `SKILL.md` と必要な `references/` を資料として指定する。リポジトリからの自動同期を前提にしない。
- 外部 `frontend-design`・`visual-explainer` Skills は任意。利用可能な時だけ補助的に使用する。

## 検証状況（初回試作）

- 静的・数値・Chromium表示検証（320 / 390 / 768 / 1440px）: PASS
- Quarto CLIビルド: NOT RUN（検証環境に未導入）
- 内容の専門家査読: 未実施
