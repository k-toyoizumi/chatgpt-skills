# Textbook Authoring Skill v0.4

**用途:** Agentによる日本語HTML教科書の構成、静的図解、比較表、数式・実装、検証。

Quarto Bookをソースの正本とし、図・表は**自動番号とクリック可能な相互参照**を付けます。図の装飾アニメーションは原則使いません。略称は各章の初出で**正式名称（略称）**を示し、数式記号は最初に意味・次元・単位を説明します。見出し・図表・演習にも適用します。

## 含まれるサンプル

`assets/quarto-book/` には研究者向けSelf-Attention教材（**導入ページ＋独立した3章**）を収録しています。SVG図5枚、比較表1件、数式とPyTorch検証例、確認問題4問を維持しています。

## 使い方

1. `SKILL.md` と `references/` を参照し、教材の学習目標・構成を作る。
2. `assets/quarto-book` を教材リポジトリへ複製し、**章ごとに `.qmd` を分けて** `_quarto.yml` の `book.chapters` に登録する。左サイドバー、折りたたみ、右ページ目次、スマホ用章メニューは `references/navigation.md` に従う。図は `{#fig-name}`、表は `{#tbl-name}` を付け、本文から `@fig-name` / `@tbl-name` で参照する。
3. Quartoが使える環境では `cd assets/quarto-book && quarto render` を実行する。
4. このSkill内での検証コマンド：

```sh
python scripts/validate.py
python scripts/test_numeric.py
python scripts/render_preview.py /tmp/attention-book-preview
python scripts/test_browser.py /tmp/attention-book-preview
```

Pandocによる複数ページHTMLプレビューは **Quarto本体のレンダリングの代替ではありません**。図と表の番号をQuarto Book風に表示しますが、Quartoのネイティブサイドバーやレスポンシブ動作を再現した保証はありません。正式なQuartoビルドで章移動・各章の図表番号が確認できるまで公開しないでください。

## ChatGPT と Codex

- 共通Skill正本：`skills/textbook-authoring/SKILL.md`。
- Codex：対象リポジトリの `.agents/skills/textbook-authoring/` にSkillディレクトリをコピーするか、Skillsの検索対象に配置する。
- ChatGPT：専用Skill機能が使用できる環境では登録し、それ以外では `SKILL.md` と必要な `references/` を資料として指定する。リポジトリからの自動同期を前提にしない。
- 外部 `frontend-design`・`visual-explainer` Skills は任意。利用可能な時だけ補助的に使用する。

## 検証状況（初回試作）

- 静的・数値・Pandocの4ページ試作に対するChromium表示検証（320 / 390 / 768 / 1440px）: PASS
- Quarto CLIビルド: NOT RUN（検証環境に未導入）
- 内容の専門家査読: 未実施
