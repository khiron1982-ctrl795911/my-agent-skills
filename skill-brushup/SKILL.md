---
name: skill-brushup
description: >
  Claude Code、Codex、共通領域の全SKILL.mdを監査し、安全な修正、重複差分の検出、公式スキルの更新確認、結果の保存まで行う。Use when: 「スキルをブラッシュアップ」「スキルを点検」「スキルを同期」と言われたとき、または週次メンテナンス時。Do NOT use for: 目的が未定の新規スキル作成。
---

# Skill Brushup

全スキルを「予測しやすさ」「安全性」「Claude Code／Codex間の一貫性」の3軸で保守する。

## 実行

1. 共通ルールと `feedback_*.md` を読む。
2. 次の監査を実行する。

```powershell
python C:\Users\khiro\.claude\skills\skill-brushup\scripts\audit_skills.py
```

3. `error` は今回直す。`warning` は根拠を確認して直し、見送る理由を報告書へ残す。
4. 削除、改名、大幅な役割変更は提案に留める。上書き前に対象と差分を確認する。
5. Matt Pocock公式スキルは公式配布元と比較し、Claude Code用とCodex用へ同じ版を反映する。
6. 再監査で `error` が0件になれば完了とする。

報告書は `C:\Users\khiro\ai-collaboration\reviews\codex\skill-brushup\` に保存する。

## Codex連携

Claude Codeから内容判断が必要な修正を行う場合は、`ask-codex` を使って読み取り専用レビューを依頼する。Codexが利用できない場合も監査と安全な修正は続け、未実施理由を残す。

## 同期方針

- 独自の共通スキルは `C:\Users\khiro\.agents\skills\` をCodex側の基準にする。
- Claude Codeは `C:\Users\khiro\.claude\skills\` から利用する。
- Matt Pocock公式スキルは両方へ同じ内容で反映する。
- Claude/Codex固有の文言が必要な同名スキルは、無理に上書きせず差分を報告する。

## 完了報告

点検数、修正数、error/warning件数、Matt公式版の反映状況、未解決差分、報告書のパスを日本語で簡潔に伝える。
