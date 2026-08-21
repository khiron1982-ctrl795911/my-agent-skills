---
name: thumbnail-remake
description: >
  長尺動画スタジオの下書きサムネイルを、色や文言を変えて作り直すスキル。作り直したサムネイルは
  そのまま動画生成時に使われる。
  Use when: 「サムネイル作り直して」「サムネの色を変えて」「サムネイル再生成」と言われたとき、
  /thumbnail-remake が呼ばれたとき。
  Do NOT use for: 下書きが無い状態での新規サムネイル単体作成（アプリの「サムネイルだけ作る」ボタン
  か /long-video-draft を先に）、動画本体の再生成。
---

# /thumbnail-remake — サムネイル作り直し

対象: `C:\Users\khiro\projects\long-video-studio\drafts\thumbnail.png`（下書きサムネイル）

## 手順
1. ユーザーの希望（色・タイトル文言・サブタイトル文言）を確認する。指定がなければ現状から色だけ変えるか聞く
2. 実行:
```
cd ~/projects/long-video-studio
python -X utf8 draft_tool.py thumb [--color pink] [--title "新タイトル"] [--subtitle "新サブタイトル"]
```
   - 色の選択肢: blue / cyan / green / purple / pink / coral / red / yellow
   - タイトル・サブタイトルを変えた場合は draft.json にも反映される（フォームの入力値も変わる）
3. 生成された `drafts/thumbnail.png` を Read で開き、ユーザーに見せて確認する
4. 気に入らなければ 1〜3 を繰り返す
5. 確認が取れたら「アプリの画面を再読み込みすると新しいサムネイルが表示されます。
   動画生成時はこのサムネイルがそのまま使われます」と伝える

## 補足
- 完成済み動画のサムネイルだけ差し替えたい場合: 作り直した thumbnail.png を
  `Desktop\VIDEO\該当フォルダ\thumbnail.png` に上書きコピーすれば、YouTubeアップロード時に反映される
- YouTubeにアップ済みの動画のサムネイル変更は YouTube Studio から手動で行う

## フィードバック反映
- 実行前に `~/.claude/projects/C--Users-khiro/memory/feedback_skills.md` を確認し反映する
- 修正指示を受けたら同ファイルに1行追記する
