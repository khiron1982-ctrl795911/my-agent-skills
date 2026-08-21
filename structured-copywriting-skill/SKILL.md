---
name: structured-copywriting-skill
description: >
  PASONA・AIDMAなど「型」に沿って、伝わる構成の文章（案内文・告知文・説明文など）を組み立てるスキル。
  Use when: 「型に沿って書いて」「PASONAで」「AIDMAで」「構成を整理して文章にして」と言われたとき、/structured-copywriting-skill が呼ばれたとき。
  Do NOT use for: Threads/Instagram投稿そのものの生成（/sns-threads・/sns-instagram）、フック案だけが欲しい場合（/hook-generator）、Situation/Complication/Question/Answerの4段構成が指定された場合（/scqa-writing-framework）。
---

# /structured-copywriting-skill — 型に沿った構成文章スキル

## 使い方
```
/structured-copywriting-skill PASONAで社内向け案内文を書いて（テーマ：新しい勤怠システム）
/structured-copywriting-skill AIDMAで研修告知文を作って
/structured-copywriting-skill この文章をPASONAの型で整理し直して（本文貼り付け）
/structured-copywriting-skill どちらの型が合うか提案して
```

## このスキルがやること
1. テーマ・目的（告知したい／行動してほしい内容）と読み手を確認する
2. 指定がなければ内容に合う型（PASONAかAIDMA）をこちらから提案する
3. 選んだ型の各要素に沿って文章を組み立てる
4. 冗長な言い回しや専門用語を削り、読み手が迷わない流れにする
5. 最後に行動喚起（CTA：申込・返信・確認など）を明確に入れる
6. 完成文と、どの要素がどこに当たるかの対応表を一緒に出力する

## 使える型（どちらも日本の実務でよく使われる）

### PASONA（問題解決・行動喚起向き。案内文・告知文に強い）
- **P（Problem）**：読み手が抱える問題を示す
- **A（Affinity）**：共感し、問題を自分ごととして感じてもらう
- **S（Solution）**：解決策・提案を示す
- **O（Offer）**：具体的な提案内容（日時・条件・やり方）
- **N（Narrowing down）**：対象者や期限を絞る
- **A（Action）**：具体的な行動を促す

### AIDMA（認知〜行動の流れ向き。周知・関心喚起に強い）
- **A（Attention）**：注意を引く一言
- **I（Interest）**：関心を持たせる情報
- **D（Desire）**：欲しい・参加したいと思わせる
- **M（Memory）**：覚えておいてもらう工夫（期限・数字など）
- **A（Action）**：行動を促す

## 出力フォーマット
```markdown
# 構成文章（{PASONA/AIDMA}） — テーマ：{テーマ}

{完成文本文}

---
## 対応表
- {要素1}: {該当箇所の一言要約}
- {要素2}: {該当箇所の一言要約}
...

文字数: {N}文字
[下書き - 要確認]
```

## 検証チェックリスト
```
□ 選んだ型の要素が全て入っているか（抜けがないか）
□ 専門用語を平易な言葉に言い換えたか
□ CTA（行動喚起）が具体的か（いつまでに・何をするか）
□ 冗長な繰り返しがないか
□ 対応表で要素と本文の対応が分かるか
```

## 終了条件
型に沿った完成文と対応表を出力したら止まる。
「{PASONA/AIDMA}の型で作成しました。対応表と合わせて確認してください」と報告する。

## フィードバック反映（自動ブラッシュアップ用）
- 実行前に `~/.claude/projects/C--Users-khiro/memory/feedback_skills.md` があれば読み、このスキルへの過去の修正指示を反映する
- ユーザーから出力への修正指示を受けたら、同ファイルに「日付／スキル名／指示内容／今後どうするか」を1行で追記し、同じ指摘を二度受けないようにする
