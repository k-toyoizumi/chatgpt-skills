# Change and Validation Rules

## 差分更新

既存成果物を更新する場合、可能な限り LLM の前に決定論的な差分抽出を行う。

```text
current metadata / ids / timestamps / hashes
        ↓
deterministic diff
        ↓
changed records + directly dependent records
        ↓
LLM processing (必要な場合のみ)
        ↓
validation
        ↓
publish
```

変更判定は原則として次の順で行う。

1. stable ID
2. updated_at / mtime
3. content hash
4. semantic comparison（上記で判定できない場合のみ LLM）

変更のないデータは既存成果物を再利用する。

## LLM より通常コードを優先する処理

- `canonicalize(data)` — 順序・空白などを正規化する
- `content_hash(data)` — SHA-256 等で変更検知する
- `diff_by_id(old, new)` — added / changed / removed を抽出する
- `dedupe(records, key)` — ID / URL / 複合キーで重複排除する
- `select_changed(records, state)` — 更新日時 / hash から処理対象を絞る
- `validate_schema(data, schema)` — 必須 field・型を検査する
- `validate_refs(data)` — 参照 ID・リンク切れ・孤立 record を検査する
- `bounded_read(source, range)` — 必要範囲だけ読む
- `healthcheck(output)` — 件数、schema、リンク、主要導線を検査する

永続プロジェクトでは、これらの実コードは各プロジェクト repo の `scripts/` または `tools/` に置く。

## Validation / Publish

- 更新後は、変更内容に応じた最小限の検証を必ず行う。
- schema、参照、件数、主要導線、主要機能を可能な範囲で機械的に検証する。
- 検証失敗時は失敗箇所を特定し、その部分だけ修正・再検証する。
- 正常性を確認できない場合、壊れた最新版を「正常版」として公開しない。
- 長期プロジェクトでは last-known-good の version / commit / URL を Project State に保持する。
