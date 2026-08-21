---
name: ask-codex
description: >
  Codex（OpenAIのAIエージェント）に質問・レビュー・作業依頼を投げて、結果を受け取って統合するスキル。
  Use when: 「Codexに聞いて」「GPTに聞いて」「セカンドオピニオンが欲しい」「別のAIにもレビューさせて」「Codexのスキルで◯◯して」と言われたとき、/ask-codex が呼ばれたとき。
  Do NOT use for: Geminiへの依頼（~/ai-collaboration/scripts/ask-gemini.ps1 を使う）、Claude自身で完結できる通常作業（わざわざCodexを挟まない）。
---

# /ask-codex — Codex連携スキル

## 呼び出し方法（この順で使う）

### 方法1: Codex CLI（推奨・ChatGPTログイン認証で動く）
Bashツールで実行する。**末尾の `< /dev/null` は必須**（付けないと入力待ちで固まる）。

```bash
codex exec --skip-git-repo-check --sandbox read-only "依頼文" < /dev/null
```

- 出力の最後の `codex` 行以降が回答本文
- ファイルを読ませたい場合は依頼文にフルパスを書けば、read-onlyサンドボックス内でCodexが自分で読む
- Codexにファイルを書かせたい場合のみ `--sandbox workspace-write` に変え、作業フォルダを `--cd <フォルダ>` で明示する（安易に使わない。原則はread-onlyで回答だけもらい、ファイル反映はClaude側で行う）

### 方法2: APIスクリプト（予備。現在はOpenAI APIの利用枠が0のため課金設定まで使用不可）
```powershell
& "$HOME\ai-collaboration\scripts\ask-codex.ps1" -Prompt "依頼文" -InputFiles "ファイル" -OutputFile "保存先"
```
「insufficient_quota」エラーが出たら方法1に切り替える。

## Codex側に入っているスキル（依頼文に名前を書くと確実に使われる）
| Codexスキル | 得意なこと | Claude側との使い分け |
|---|---|---|
| pptx-meiryo | 日本語フォント（メイリオ）検証付きのPowerPoint作成 | Claude側 /pptx で作った資料の日本語フォント検証を頼むと相互チェックになる |
| transcribe | 文字起こし＋話者分離 | Claude側にも文字起こしはあるので、話者分離が要るときの第二候補 |
| speech | テキスト読み上げ音声の生成 | VOICEVOX（動画パイプライン）と別の声が欲しいとき |
| playwright | ブラウザの自動操作・Webテスト | Claude側のChrome連携が使えない自動テストのとき |
| screenshot / pdf / ppt | 画面撮影・PDF・PowerPoint処理 | 基本はClaude側スキルを使い、検算役として |
| cli-creator / openai-docs | CLIツール作成・OpenAI公式ドキュメント参照 | OpenAI API関連の質問はここに聞くのが正確 |

このほかプラグイン由来のスキル（teams＝Microsoft Teams連携、spreadsheets、presentations、remotion＝コードで動画生成、openai-developers 系など）もCodex側にある。最新一覧は次で確認できる:
```bash
codex exec --skip-git-repo-check --sandbox read-only "使えるスキル名だけを箇条書きで" < /dev/null
```

## このスキルがやること
1. 依頼内容を1つの自己完結した依頼文にまとめる（Codexはこの会話を見られないため、前提・ファイルパス・出力形式をすべて依頼文に含める）
2. 方法1で実行する（レビュー依頼なら「JSONで」「箇条書きで」と形式指定する）
3. レビュー・セカンドオピニオン結果は `~/ai-collaboration/reviews/codex/日付_内容.md` に保存する
4. **Codexの回答を鵜呑みにせず、重要な主張・数値・コードはClaude側で検証してから採用する**（ai-collaboration/CLAUDE.md のルール）
5. 採用・不採用の判断と理由を添えてユーザーに報告する

## 検証チェックリスト
□ 依頼文が自己完結しているか（会話の文脈に依存していないか）
□ `< /dev/null` を付けたか（入力待ちハング防止）
□ 原則 read-only サンドボックスで実行したか
□ Codexの回答を検証してから採用したか（矛盾があれば両論併記で報告）
□ レビュー結果を reviews/codex/ に保存したか

## 終了条件
Codexの回答と、それに対するClaudeの検証結果・判断を報告したら終了。Codexの提案の実装・ファイル反映は、ユーザーの了解を得てからClaude側で行う。

## フィードバック反映（自動ブラッシュアップ用）
- 実行前に `~/.claude/projects/C--Users-khiro/memory/feedback_skills.md` があれば読み、このスキルへの過去の修正指示を反映する
- ユーザーから出力への修正指示を受けたら、同ファイルに「日付／スキル名／指示内容／今後どうするか」を1行で追記し、同じ指摘を二度受けないようにする
