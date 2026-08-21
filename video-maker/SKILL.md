---
name: video-maker
description: |
  VOICEVOX + MoviePy + Pillow で YouTube動画（横型16:9）と ショート動画（縦型9:16）を
  完全自動生成する統合スキル。テーマを伝えるだけで動画・サムネイル・説明文・ハッシュタグを一括生成する。

  以下のキーワードが出たら必ずこのスキルを使うこと：
  「動画」「ナレーション」「VOICEVOX」「YouTube」「YouTube Shorts」「ショート動画」
  「TikTok」「縦型動画」「1分動画」「リール」「動画スクリプト」「サムネイル」

  ※動画の縦横（ロング/ショート）が不明な場合は、最初に必ずモードを確認すること。
---

# Video Maker スキル（ロング＋ショート統合版）

## STEP 0 — モードを判定する（最重要）

| モード | 判定キーワード | 解像度 | 尺 | 出力スクリプト |
|--------|--------------|--------|-----|--------------|
| **A: ロング動画** | YouTube動画、解説動画、〇分の動画 | 1920×1080（16:9） | 3〜15分 | `~/projects/video_pipeline/make_video.py` |
| **B: ショート動画** | Shorts、TikTok、縦型、1分動画、リール | 1080×1920（9:16） | 45〜75秒 | `~/projects/short_video/make_short.py` |

どちらか判別できない場合は**作業を始める前に1回だけ質問する**。

---

## STEP 1 — 環境を確認する（両モード共通）

生成コードの冒頭に以下の**環境チェック**を必ず含める：

```python
import sys, requests
from pathlib import Path

# --- PC判定（会社PC: kuwata / 個人PC: khiro）---
HOME = Path.home()                      # どちらのPCでも動くようにハードコード禁止
USER = HOME.name                        # 'kuwata' or 'khiro'

# --- VOICEVOX起動チェック ---
VOICEVOX = "http://localhost:50021"
try:
    requests.get(f"{VOICEVOX}/version", timeout=3)
except requests.exceptions.ConnectionError:
    sys.exit("❌ VOICEVOXが起動していません。VOICEVOXを起動してから再実行してください。")

# --- フォント（Bold優先 → フォールバック）---
FONT_CANDIDATES = [r"C:\Windows\Fonts\meiryob.ttc", r"C:\Windows\Fonts\meiryo.ttc",
                   r"C:\Windows\Fonts\msgothic.ttc"]
FONT_PATH = next((f for f in FONT_CANDIDATES if Path(f).exists()), None)
if FONT_PATH is None:
    sys.exit("❌ 日本語フォントが見つかりません。")
```

### moviepy のバージョン互換（重要）

moviepy 2.x では `from moviepy.editor import *` が**廃止**されている。必ず互換インポートを使う：

```python
try:
    from moviepy.editor import *          # moviepy 1.x
except ImportError:
    from moviepy import *                 # moviepy 2.x
```

### 依存パッケージのインストール（初回のみ）

```bash
pip install moviepy pillow requests --break-system-packages
```

---

## STEP 2 — ユーザーから情報を引き出す

| 項目 | 説明 | デフォルト |
|------|------|-----------|
| `theme` / `title` | テーマ・タイトル | **必須** |
| `target` | 対象視聴者（例：20代会社員） | 指定なし |
| `tone` | トーン（明るい/落ち着き/驚き） | 明るい |
| `speaker` | VOICEVOX話者ID | `2`（ずんだもん） |
| `color` | カラー | テーマから自動選択 |
| `duration` | 目標尺 | A: 5分 / B: 60〜75秒 |

### 話者ID一覧（共通）

| ID | 名前 | 特徴 |
|----|------|------|
| 0 | 四国めたん | 女性・落ち着き |
| 1 | 四国めたん（あまあま） | 女性・明るめ |
| 2 | ずんだもん | 元気・親しみやすい（デフォルト） |
| 3 | ずんだもん（あまあま） | 甘め |
| 8 | 春日部つむぎ | 女性・やさしい |
| 10 | 雨晴はう | 女性・ソフト |
| 13 | 青山龍星 | 男性・落ち着き・信頼感 |
| 14 | 冥鳴ひまり | 女性・クール |

複数話者を使う場合は各シーンに `"speaker": ID` を付ける。
ナレーション文は**句読点あり・自然な話し言葉**で書く（VOICEVOXの読み上げが自然になる）。

---

## STEP 3A — ロング動画（モードA）の設計

### シーン構成

| type | 用途 | 追加フィールド | イラストスタイル |
|------|------|--------------|----------------|
| `intro` | オープニング | `sub`, `badge` | 青系グラデ＋幾何学装飾 |
| `mistake` | 悪い例・警告 | `number`, `icon`(✗/⚠), `point` | 左帯赤・✗アイコン |
| `solution` | 解決策 | `number`, `icon`(✓), `point` | 左帯緑・✓アイコン |
| `summary` | まとめ | `items`(箇条書き) | カードリスト（5項目まで） |
| `default` | 汎用 | なし | — |

`mistake`/`solution` はペアで使うとリズムが良い。

### 尺の目安

| 目標尺 | シーン数 | 1シーンの文字数 |
|--------|---------|---------------|
| 3分 | 4〜5 | 100〜150文字 |
| 5分 | 7〜8 | 150〜200文字 |
| 10分 | 12〜15 | 200〜280文字 |
| 15分 | 18〜22 | 250〜300文字 |

### テーマカラー（モードA）

| 値 | 雰囲気 | 推奨用途 |
|----|--------|---------|
| `blue` | 信頼・ビジネス | ビジネス・解説（デフォルト） |
| `cyan` | クール・テック | IT・ツール系 |
| `purple` | 高級・クリエイティブ | デザイン・AI |
| `green` | 自然・安心 | 健康・学習 |
| `yellow` | 明るい・注意 | 注意喚起・初心者向け |
| `pink` | ポップ | エンタメ・ライフスタイル |

### ハッシュタグ（12個）
テーマ直結4 ＋ 関連ジャンル4 ＋ 拡散向け（ビジネス・仕事術・効率化等）4

### 出力

```
~/projects/video_pipeline/output/
├── final_video.mp4      ← 完成動画（1920×1080, fps=30, 音声付き）
├── thumbnail.png        ← サムネイル（1280×720）
├── description.txt      ← 説明文＋ハッシュタグ（1行ずつ・コピペ用）
├── images/              ← 各シーンのイラスト
└── audio/               ← 各シーンの音声
```

---

## STEP 3B — ショート動画（モードB）の設計

### シーン構成テンプレート（5〜7シーン、合計45〜75秒）

```
Scene 1: hook（5〜8秒）    → 見た人が止まるインパクト冒頭
Scene 2: problem（8〜10秒）→ 共感を呼ぶ悩み・課題
Scene 3〜5: point（各10〜12秒）→ 3ポイント解説
Scene 6: summary（8〜10秒）→ 要点の再確認
Scene 7: cta（5〜7秒）     → フォロー・保存・コメント促進
```

| type | ビジュアル特徴 |
|------|--------------|
| `hook` | 大見出し＋グローエフェクト＋絵文字大 |
| `problem` | 警告カード＋赤アクセント |
| `point` | 番号バッジ＋グラスモーフィズムカード |
| `summary` | 複数カード縦並び |
| `cta` | フォロー/保存アイコン＋強調テキスト |

### カラースキーム（モードB）

| color_key | 向いているテーマ |
|-----------|----------------|
| `modern_blue` | ビジネス・IT・副業・転職 |
| `neon_purple` | AI・テック・未来系 |
| `warm_coral` | 恋愛・感情・モチベーション |
| `fresh_green` | 健康・食事・節約 |
| `dark_premium` | お金・投資・ラグジュアリー |

RGB定義・グラデ背景・グラスカード・グローテキスト・プログレスバーの実装は
`references/short-video-code.md` を参照（旧short-videoスキルのコードをそのまま収録）。

### ハッシュタグ（30個）
テーマ直結10 ＋ 拡散向け10 ＋ ターゲット層5 ＋ プラットフォーム（#YouTubeShorts #TikTok等）5

### 動画タイトルは3案提示
数字入り（「3つの〇〇」）／問いかけ形式／トレンド表現 の3パターン。

### 出力（PC別に自動切替）

```python
# ハードコード禁止。ユーザー名で出力先を決定する
OUTPUT_DIR = HOME / "OneDrive" / "Desktop" / "VIDEO"   # khiro / kuwata 両対応
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR = HOME / "projects" / "short_video" / "output"
```

| 成果物 | ファイル名 |
|--------|-----------|
| 動画（1080×1920, fps=30） | `{filename}_{YYYYMMDD}.mp4` |
| サムネイル（1080×1920） | `{filename}_thumb.png` |
| メタ（タイトル・説明文・タグ） | `{filename}_meta.txt` |

`filename` は半角英数＋アンダーバーのみ。

---

## STEP 4 — コードを出力する

- **省略なしの完全なコード**を出力する（`...（実装省略）`は禁止。実行して即動く状態にする）
- 「ここだけ編集する」ブロック（THEME / SCENES）をファイル冒頭に置く
- 各シーンの音声長に画像表示時間を自動調整する
- 例外時は原因が分かる日本語メッセージで `sys.exit()` する

## STEP 5 — 実行手順を案内する

```
① VOICEVOXを起動する（タスクバーから）
② Git Bashで実行：
   cd ~/projects/video_pipeline   （ショートは ~/projects/short_video）
   python make_video.py           （ショートは make_short.py）
③ 完成確認：
   explorer output                （ショートは explorer "$USERPROFILE\OneDrive\Desktop\VIDEO"）
```

## STEP 6 — 失敗時のトラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| ConnectionError | VOICEVOX未起動 | VOICEVOXを起動して再実行 |
| `No module named 'moviepy.editor'` | moviepy 2.x | STEP 1の互換インポートを使う |
| 文字化け・豆腐 | フォント未検出 | FONT_CANDIDATESの順にフォールバック |
| `FileNotFoundError: C:\Users\khiro\...` | PC違い（会社PC） | `Path.home()` ベースのパスに修正 |
| 音声と画像の長さ不一致 | duration固定 | 音声長 `AudioFileClip.duration` に合わせる |


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
