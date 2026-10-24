# Git Workflow Rules

Git操作の判断基準。実行手順は `skills/git-workflow/SKILL.md` を参照する。

## 権限と範囲

- 合意した作業は、必要な検証後のステージング・コミット・通常のプッシュまでAgentが自律実行する。同じ範囲の承認を繰り返し求めない。「編集のみ」「プッシュしない」などの個別指示を優先する。
- この既定値は既存の送信先への作業成果の反映を対象とする。新規リポジトリ作成、公開範囲変更、リリース、デプロイ、PRのマージの承認には広げない。プッシュがデプロイ等を起動する場合は、その処理が合意範囲か確認する。
- 小さな個人作業は現在のブランチを使う。共同作業・大きな変更は作業ブランチ＋PRを基本とし、既存の保護設定・プロジェクト方針を優先する。detached HEADでは送信先を推測せず、対応するブランチを確認する。
- 既存の未コミット・ステージ済み変更を保存し、担当範囲外を取り込まない。分離できない場合だけ相談する。

## 変更と履歴

- ステージングはファイル・変更部分を明示して行い、コミット対象の差分を確認する。無差別な `git add .` / `git add -A` / `git commit -a` を既定にしない。
- 一つのコミットは一つの説明可能な目的にまとめる。メッセージは何を変えたかを具体的にし、必要なら理由を本文に書く。言語・形式は既存の規約を優先し、Conventional Commitsは採用済みの場合に用いる。
- 認証情報・個人情報・不要な生成物を履歴へ入れない。プッシュ時は今回の差分だけでなく送信対象の未送信コミット全体を確認する。秘密情報の漏えい時は値を再掲せず、失効・再発行と履歴対処を相談する。
- 通常の作業依頼から、既存コミットのamend、rebase等の履歴改変、force push、ブランチ削除、変更破棄を承認済みとしない。必要な対象・影響を具体化し、明示的な許可がある場合だけ行う。
- hookや必須チェックを無断で迂回しない。ユーザー名・メール・署名設定・認証情報・保護ルールを都合に合わせて変更しない。

## 完了の判断

- 検証は `rules/change-and-validation.md` に従い、記録される内容と検証対象が一致することを確認する。
- 送信先remote・ブランチ・未送信履歴を確認して通常のプッシュを行う。拒否時は原因を確認し、強制送信や自動のpull/rebaseで押し通さない。
- 編集済み・ステージ済み・コミット済み・プッシュ済みを区別して報告する。ネットワーク・認証等で失敗した場合はローカル成果を保持し、未完了の操作と理由を示す。

## 根拠と位置づけ

以下はGitの仕様・GitHubの公開手順。自律実行の範囲と個人作業のブランチ方針は、このリポジトリの運用上の選択であり、公式の必須要件ではない。

- [git-add](https://git-scm.com/docs/git-add)：indexへ次のコミット対象を選ぶ。
- [git-commit](https://git-scm.com/docs/git-commit)：通常はindexの内容を記録する。
- [git-push](https://git-scm.com/docs/git-push)：ref更新、fast-forward、forceの動作。
- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)：ブランチ・PR・レビューを用いる作業手順。
- [機密情報の削除](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)：漏えい後の対処と履歴変更の影響。
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)：任意に採用するメッセージ規約。
