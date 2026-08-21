---
name: sns-instagram
description: >
  Instagramのリール台本・カルーセル・ストーリー・キャプションを生成して ~/sns/_drafts/instagram/ に保存するスキル。
  Use when: 「Instagram」「インスタ」「リール」「カルーセル」の投稿や台本を作ってと言われたとき、/sns-instagram が呼ばれたとき。
  Do NOT use for: Threads（/sns-threads）、下書きの一覧・承認（/sns-draft）、インサイト分析（/sns-insight）。
---

# /sns-instagram — Instagram台本・キャプション生成スキル

## 使い方
```
/sns-instagram                            # リール台本＋キャプションを1本生成
/sns-instagram テーマ：Claude Codeの使い方  # テーマ指定
/sns-instagram --carousel 5枚             # カルーセル投稿用（5枚分）
/sns-instagram --story                    # ストーリー用テキスト生成
```

## このスキルがやること
1. `~/sns/BRAND_GUIDE.md` と `~/sns/CLAUDE.md` を読み込む
2. `~/.claude/projects/C--Users-khiro/memory/feedback_sns.md` のフィードバックを確認
3. リール台本（または指定フォーマット）を生成する
4. 検証チェックリストを実行する
5. `~/sns/_drafts/instagram/YYYY-MM-DD_N.md` に保存する
6. 報告して止まる

## 生成ルール

### リール台本フォーマット
```
【冒頭3秒フック】視聴者が止まる一言（疑問形・数字・驚き）

【本編】
- ポイント1（10〜15秒）
- ポイント2（10〜15秒）
- ポイント3（10〜15秒）

【CTA】
「詳しくはプロフィールリンクから」
「保存して後で見てください」
```

### カルーセルフォーマット
- スライド1: タイトル（強いフック）
- スライド2〜N-1: 各ポイント（1スライド1メッセージ）
- スライド最終: まとめ＋CTA

### キャプション規定
- 推奨150文字以内（長くても300文字まで）
- ハッシュタグ: 5〜10個、末尾にまとめる
- 改行で読みやすくする

### 検証チェックリスト
```
□ 冒頭3秒にフックが入っているか
□ キャプションが推奨150文字以内か
□ ハッシュタグが5〜10個か
□ BRAND_GUIDE.md の文体と合っているか
□ 禁止表現が含まれていないか
□ CTAが入っているか
□ 「[下書き - 要確認]」が付いているか
```

### 保存フォーマット
```markdown
# Instagram下書き — {YYYY-MM-DD} #{N}

## リール台本
{台本テキスト}

## キャプション
{キャプションテキスト}

#ハッシュタグ1 #ハッシュタグ2 ...

---
形式: {リール/カルーセル/ストーリー}
推定尺: {秒数}
生成日時: {YYYY-MM-DD HH:MM}

[下書き - 要確認]
```

## /loop との組み合わせ方
```
/loop 今週のInstagramリール台本を1本/sns-instagramで生成して_drafts/instagram/に保存されたら止まって
```

## 終了条件
指定本数のファイルが `~/sns/_drafts/instagram/` に保存されたら止まる。
