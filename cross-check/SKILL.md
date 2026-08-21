---
name: cross-check
description: >
  外部AI CLI（Codex / Gemini / Genspark）との連携・クロスチェック手順。
  トリガー:「Codexと相談」「Codexにも見てもらって」「Codexにレビューさせて」
  「Codexにファクトチェック」「セカンドオピニオン」「Geminiにも聞いて」
  「Gensparkで調べて」「ディープリサーチ」「3モデル合議」「意見をdiffして」など、
  外部AIへのレビュー・検証・調査依頼が出たとき。
---

# 外部AI連携（Codex / Gemini / Genspark）

Claude Code は**司会・統合担当**。Codex/Gemini/Genspark はゲスト・検証担当。
外部AIの回答をそのまま貼らず、最後に Claude Code 側で統合して最終判断を出す。

## CLIの所在（2026-07-03 確認済み）

| CLI | 実体 | 備考 |
|---|---|---|
| codex | `C:\Users\kuwata\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe` | exe なので bash/PowerShell 両方から呼べる |
| gemini | `C:\Users\kuwata\node\node-v24.15.0-win-x64\gemini.ps1` | PowerShell スクリプト |
| gsk | `C:\Users\kuwata\node\node-v24.15.0-win-x64\gsk.ps1` | PowerShell スクリプト |

呼び出しに失敗したら、まず `Get-Command codex,gemini,gsk` で所在を確認し、
見つからない場合はユーザーに報告する（勝手に再インストールしない）。

## トリガー → CLI 対応表

| トリガー | 使うCLI | 主な用途 |
| --- | --- | --- |
| `Codexと相談しながら` | `codex exec` | 実務ロジック、数字、コード、精密レビュー |
| `Codexにも見てもらって` | `codex exec` | 誤字、論理破綻、抜け漏れ確認 |
| `Codexにセカンドオピニオン` | `codex exec` | 判断材料の比較、別観点の抽出 |
| `Codexにファクトチェック` | `codex --search exec` | 数字、固有名詞、価格、年代、出典確認 |
| `Codexに裏で調査回しといて` | `codex exec`（バックグラウンド実行） | 重い調査、大量要約・変換 |
| `Geminiにも聞いて` | `gemini` | 3モデル合議、広めの発想、追加観点 |
| `Gensparkで調べて` | `gsk search` | Web最新情報・一次情報検索 |
| `Gensparkにファクトチェック` | `gsk task cross_check` | クレーム・数字の一次情報検証 |
| `Gensparkにディープリサーチ` | `gsk task deep_research` | 深い調査・包括的レポート |

使い分け: コードロジック・計算式・誤字の精密レビュー＝Codex、
Web最新情報・法律・価格・統計の一次情報＝Genspark、発想の広がり・第3の視点＝Gemini。

## 共通手順

1. **プロンプトをファイルに書く**（インライン渡しはパースエラーの原因）。
   置き場はセッションの scratchpad か `C:\Users\kuwata\work\`
   配下（例: `work\cross-check\prompt.txt`）。日本語はUTF-8で保存する。
2. プロンプトの型: 対象＋観点＋「結論、重要な指摘、根拠、修正案の順で短く返してください」。
3. CLI を実行し、回答を受け取る。
4. Claude 側の見解と突き合わせて統合（下記「統合時の出力ルール」）。

## Codex 呼び出し

**優先: MCP経由**（2026-07-13 に user スコープで登録済み）。`mcp__codex__*` ツールが
使える場合はそれで直接呼ぶ（プロンプトファイル作成・パースエラー対策・文字化け
フォールバックが全部不要になる）。ツールが見えない場合のみ下のCLI経由にフォールバック。

**定型プロンプトのテンプレ**: `C:\Users\kuwata\work\cross-check\templates\` に
code-review.txt / fact-check.txt / second-opinion.txt がある。ゼロから書かずに
テンプレの穴埋めで投げる（前提の渡し漏れ防止）。

### CLI経由（フォールバック。bash が確実）

PowerShell の ExecutionPolicy で codex.ps1 がブロックされることがあるため **bash 経由**で呼ぶ。

```bash
# プロンプトをファイルに書いてから:
codex -a never -s read-only exec --skip-git-repo-check "$(cat prompt.txt)"

# ファクトチェック（Web検索付き）:
codex --search -a never -s read-only exec --skip-git-repo-check "$(cat prompt.txt)"
```

- ファイルを読ませたいときは、プロンプト内に対象ファイルの絶対パスを書く
  （`-s read-only` なので読み取りは可能、書き込みはさせない）。
- **バックグラウンド実行**（「裏で回しといて」）: Bash ツールの `run_in_background: true` で起動し、
  出力をファイルにリダイレクトしておく（例: `... > /c/Users/kuwata/work/cross-check/result.txt 2>&1`）。
  完了通知が来たら結果ファイルを読む。メイン作業は継続してよい。
- 日本語パスを含む場合は bash のパスは `/c/Users/kuwata/...` 形式にし、文字化けしたら
  PowerShell から `& "C:\...\codex.exe" ...` で直接呼ぶフォールバックを試す。

## Gemini 呼び出し

```bash
gemini --prompt "以下について、Claude/Codexとは違う観点でリスクと代替案を出してください。

対象:
<内容>"
```

## Genspark 呼び出し

```bash
gsk search "キーワード"
gsk task cross_check --task_name "確認" --query "検証したい主張" --instructions "一次情報と根拠を明記してください"
gsk task deep_research --task_name "調査名" --query "テーマ" --instructions "詳細指示"
```

`deep_research` は時間がかかるためバックグラウンド実行を検討する。

## 3モデル合議の手順（「3モデル合議」「意見をdiffして」）

1. 同一のプロンプトファイルを作る（前提・制約・出力形式を揃える）。
2. Codex と Gemini に**並行で**投げる（独立コールは同時実行）。
3. Claude 自身の見解を（外部回答を見る前に）先にまとめておく。
4. 3者の回答を項目ごとに diff し、`一致` / `2対1` / `三者三様` を明記。
5. 相違点は根拠の強さで判定し、Claude が最終判断と理由を出す。

## 統合時の出力ルール

- 重要度は `致命的` / `重要` / `軽微` の3段階で整理する
- 複数モデル一致の指摘は `一致`、片方だけは `片方のみ` と明記する
- ファクトチェックは、確認日・一次情報の有無・出典URLを残す
- 機微データ（給与・評価・個人情報）は外部AIに渡さない。必要ならマスキングしてから渡す

## 裏技7選（用途別の定型運用）

1. **ライティングのクロスチェック**: 外に出す文章は Codex に論理破綻と誤字を指摘させる
2. **ファクトチェック**: 数字・価格・年代・固有名詞は `codex --search` で出典ごと検証
3. **分析のセカンドオピニオン**: データ解釈は Codex にも分析させ、違う観点を抽出
4. **コードレビュー**: HTML・GAS・pptxgenjs 等は Codex にエラー候補を出させる
5. **重要判断の合議**: 価格・採用・戦略は Claude と Codex の意見を分けて出し、最後に diff
6. **構成は Claude、量産は Codex**: 仕様を Claude で固め、確定後の大量生成を Codex へ
7. **重いタスクは裏で実行**: 大量要約・調査・変換は Codex/Gemini に任せ、Claude はメイン作業継続


## 自己改善プロトコル（毎回実行）

このスキルは Sonnet 5 での実行を前提に手順を明示している。
判断に迷ったら本文の規則のみに従い、推測で進めず不明点はユーザーに質問する。

スキル実行の最後に必ず確認する:
1. ユーザーからの訂正・追加指示があったか。手順どおりに進まなかった箇所
   （パス変更・ファイル形式変更・コマンドエラー等）はあるか
2. あれば、このSKILL.mdの該当箇所を直接修正するか、下の改善ログに1行追記する
   （形式: `- YYYY-MM-DD: [事象] → [変更内容]`）
3. 改善ログが10行を超えたら本文に統合してログを整理する

修正はClaude自身が行ってよい（承認不要）。手順の意味を変える大きな変更のみ一言報告する。

## 改善ログ

- 2026-07-13: 自己改善プロトコルを導入（全スキル一斉ブラッシュアップ）
