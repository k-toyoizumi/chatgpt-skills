# 作品ごとの保存用 State テンプレート

この情報は**作品プロジェクト側**に置く。公開の共通Skillへ写真、氏名、予定、個人の進捗を記載しない。

```yaml
project_title: ''
medium: oil
canvas: {shape: '', size_mm: ''}
target_reference:
  file_or_link: ''
  approved_at: ''
  essential_elements: []       # 作品らしさを保つ最重要要素
  flexible_elements: []        # 自由に変更・簡略化してよい要素
  notes: ''
color_registry:
  path: 'color-registry.yaml'  # 作品ごとに固有の色見本正本
  updated_at: ''
materials:
  pigments: []                 # メーカーを含む実際の色名
  brushes: []
  medium: ''                    # 正式な製品名、なければunknown
  other: []
constraints:
  deadline: ''
  available_hours: null
  experience: beginner
  priorities: [enjoyment, recognizability, manageability]
plan:
  approval_status: draft
  steps: []                    # step_id / goal / estimate / dependencies
progress:
  latest_photo: ''
  date: ''
  completed_steps: []
  current_step: ''
  wet_areas: []                # 写真だけでは確定しない
  dry_areas: []
  observations: []
  next_actions: []
  decisions: []
```

## 更新規則

- 新しい写真・本人の報告で状態を**差分更新**。最新写真を過去写真と取り違えない。
- 「乾いている／濡れている」は本人の報告や確認結果から記録。写真だけで断定しない。
- STEP開始前には残工程・終了条件・時間的余裕を短く示し、計画変更は理由を添える。
- 新作では、このテンプレートと `templates/color-registry.yaml` を複製する。色見本を初めて提案した時点で台帳を更新する。
- 新作では、このテンプレートを複製して空欄から始める。過去の絵具・サイズ・期限を無断で転用しない。