---
name: short-video
description: |
  YouTube Shorts・TikTok用の縦型ショート動画（1080×1920、約60〜75秒）を完全自動生成するスキル。
  VOICEVOX + MoviePy + Pillowを使って、テーマだけで動画・サムネイル・説明文・ハッシュタグをすべて自動生成する。
  イラストは今時のモダンフラットデザイン（グラデーション・グラスモーフィズム・シャドウ）で自動生成。
  出力先は C:\Users\khiro\OneDrive\Desktop\VIDEO に固定。

  「ショート動画」「TikTok」「YouTube Shorts」「縦型動画」「1分動画」「リール」などのキーワードが出たら必ずこのスキルを使うこと。
  イラスト付き・タイトル・ハッシュタグの自動生成も含めてワンストップで対応する。
---

# Short Video Pipeline スキル

## このスキルでできること

テーマを伝えるだけで以下をすべて自動生成：

| 成果物 | 説明 |
|--------|------|
| `動画タイトル_YYYYMMDD.mp4` | 縦型 1080×1920 / 60〜75秒 |
| `動画タイトル_thumb.png` | サムネイル 1080×1920 |
| `動画タイトル_meta.txt` | タイトル・説明文・ハッシュタグ |

**出力先（固定）：** `C:\Users\khiro\OneDrive\Desktop\VIDEO\`

---

## ワークフロー

### STEP 1 — ユーザーからテーマを受け取る

以下を会話から読み取る：

| 項目 | 説明 | デフォルト |
|------|------|------|
| `theme` | 動画テーマ（例：「副業の始め方3選」） | 必須 |
| `target` | ターゲット層（例：「20代会社員」） | 任意 |
| `tone` | トーン（明るい/落ち着き/驚き） | `明るい` |
| `color_scheme` | カラースキーム | テーマから自動選択 |
| `speaker` | VOICEVOX話者ID | `2`（ずんだもん） |

### STEP 2 — スクリプト・メタ情報を自動設計する

#### 2-1. 動画タイトルを生成（3案）
- 数字を使う（「3つの〇〇」「5秒でわかる」）
- インパクトのある問いかけ形式
- トレンドに乗った表現

#### 2-2. シーン構成を設計する（5〜7シーン、合計60〜75秒）

```
[構成テンプレート]
Scene 1: フック（5〜8秒）  → 「見た人が止まる」インパクト冒頭
Scene 2: 問題提起（8〜10秒） → 共感を呼ぶ悩み・課題
Scene 3〜5: コンテンツ本体（各10〜12秒）→ 3ポイント解説
Scene 6: まとめ（8〜10秒） → 要点の再確認
Scene 7: CTA（5〜7秒） → フォロー・保存・コメントを促す
```

#### 2-3. ハッシュタグを30個生成

| カテゴリ | 数 | 例 |
|----------|----|----|
| テーマ直結 | 10個 | #副業 #在宅ワーク |
| 拡散向け | 10個 | #知らなきゃ損 #保存推奨 |
| ターゲット層 | 5個 | #20代 #会社員 |
| プラットフォーム | 5個 | #YouTubeShorts #TikTok |

#### 2-4. 説明文を生成（YouTube用・TikTok用それぞれ）

---

### STEP 3 — make_short.py を生成する

以下のテンプレートに従い `~/projects/short_video/make_short.py` を生成する。

#### ファイル構造

```
~/projects/short_video/
├── make_short.py         ← 生成するメインスクリプト
├── output/
│   ├── frames/           ← 各シーンの画像フレーム
│   ├── audio/            ← 各シーンの音声
│   └── final/            ← 完成ファイル（←ここからDESKTOPにコピー）
```

#### make_short.py テンプレート

```python
# ══════════════════════════════════════
#   Short Video Generator
#   出力先: C:\Users\khiro\OneDrive\Desktop\VIDEO
# ══════════════════════════════════════

import os, requests, json, datetime, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# ── 設定 ────────────────────────────────
OUTPUT_DIR = Path(r"C:\Users\khiro\OneDrive\Desktop\VIDEO")
WORK_DIR   = Path(r"C:\Users\kuwata\projects\short_video\output")
VOICEVOX   = "http://localhost:50021"
W, H       = 1080, 1920   # 縦型 9:16

# ── テーマ設定（ここだけ編集） ─────────────
THEME = {
    "title":      "{title}",
    "filename":   "{filename}",   # 半角英数・アンダーバーのみ
    "speaker":    {speaker_id},
    "color":      "{color_key}",  # modern_blue / neon_purple / warm_coral / fresh_green / dark_premium
    "hashtags":   {hashtags_list},
    "youtube_desc": """{youtube_description}""",
    "tiktok_desc":  """{tiktok_description}""",
}

SCENES = [
    {
        "id": 1,
        "type": "hook",          # hook / problem / point / summary / cta
        "speaker": {speaker_id},
        "duration": 7,           # 秒（音声長に自動調整）
        "heading": "{見出しテキスト}",
        "body": "{ナレーション文（句読点あり、自然な話し言葉）}",
        "accent": "{アクセント文字列（任意）}",
        "emoji": "{絵文字1文字}",
    },
    # … 以下同様にシーンを追加
]
```

#### カラースキーム定義

```python
COLOR_SCHEMES = {
    "modern_blue": {
        "bg_top":    (15,  23,  42),   # ディープネイビー
        "bg_bottom": (30,  64, 175),   # ロイヤルブルー
        "accent":    (96, 165, 250),   # ライトブルー
        "text":      (255,255,255),
        "card":      (255,255,255, 25),  # グラスモーフィズム
        "shadow":    (0, 0, 0, 120),
    },
    "neon_purple": {
        "bg_top":    (15,  10,  30),
        "bg_bottom": (88,  28, 135),
        "accent":    (196, 100, 255),
        "text":      (255,255,255),
        "card":      (255,255,255, 20),
        "shadow":    (0, 0, 0, 140),
    },
    "warm_coral": {
        "bg_top":    (30,  10,  10),
        "bg_bottom": (185,  28,  28),
        "accent":    (251, 146,  60),
        "text":      (255,255,255),
        "card":      (255,255,255, 20),
        "shadow":    (0, 0, 0, 120),
    },
    "fresh_green": {
        "bg_top":    (5,   46,  22),
        "bg_bottom": (20, 120,  60),
        "accent":    (74, 222, 128),
        "text":      (255,255,255),
        "card":      (255,255,255, 20),
        "shadow":    (0, 0, 0, 120),
    },
    "dark_premium": {
        "bg_top":    (10,  10,  10),
        "bg_bottom": (30,  30,  30),
        "accent":    (212, 175,  55),  # ゴールド
        "text":      (255,255,255),
        "card":      (255,255,255, 15),
        "shadow":    (0, 0, 0, 160),
    },
}
```

#### モダンイラスト生成関数（Pillow）

```python
def draw_modern_bg(draw, img, cs):
    """グラデーション背景（上下2色）"""
    for y in range(H):
        r = int(cs["bg_top"][0] + (cs["bg_bottom"][0]-cs["bg_top"][0]) * y/H)
        g = int(cs["bg_top"][1] + (cs["bg_bottom"][1]-cs["bg_top"][1]) * y/H)
        b = int(cs["bg_top"][2] + (cs["bg_bottom"][2]-cs["bg_top"][2]) * y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def draw_glass_card(img, x, y, w, h, cs, radius=40):
    """グラスモーフィズムカード"""
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([x,y,x+w,y+h], radius=radius,
                         fill=(*cs["card"][:3], cs["card"][3]))
    # カードの上辺にアクセントライン
    d.rounded_rectangle([x, y, x+w, y+4], radius=2, fill=(*cs["accent"],220))
    img.paste(overlay, mask=overlay)

def draw_glow_text(draw, text, xy, font, cs):
    """グロー（発光）エフェクト付きテキスト"""
    for offset in range(8, 0, -2):
        alpha = int(80 * (1 - offset/10))
        draw.text((xy[0]+offset//2, xy[1]+offset//2), text, font=font,
                  fill=(*cs["accent"], alpha))
    draw.text(xy, text, font=font, fill=cs["text"])

def draw_progress_bar(draw, scene_idx, total_scenes, cs):
    """下部プログレスバー"""
    bar_y = H - 60
    bar_h = 8
    total_w = W - 120
    draw.rounded_rectangle([60, bar_y, 60+total_w, bar_y+bar_h],
                            radius=4, fill=(*cs["accent"], 60))
    prog_w = int(total_w * scene_idx / total_scenes)
    if prog_w > 0:
        draw.rounded_rectangle([60, bar_y, 60+prog_w, bar_y+bar_h],
                                radius=4, fill=(*cs["accent"], 220))

def draw_scene_hook(scene, cs):
    """フックシーン: 大きな見出し＋アクセント"""
    ...（実装省略）

def draw_scene_point(scene, cs, point_num):
    """ポイントシーン: 番号バッジ＋カード"""
    ...（実装省略）

def draw_scene_summary(scene, cs):
    """まとめシーン: 箇条書きカード"""
    ...（実装省略）

def draw_scene_cta(scene, cs):
    """CTAシーン: フォロー促進"""
    ...（実装省略）
```

---

### STEP 4 — 完全な make_short.py を出力する

上記テンプレートを **そのまま実行できる完全なコード** として出力する。
省略なしで全関数を実装し、ユーザーが `python make_short.py` を実行するだけで動く状態にする。

必須要件：
- [ ] フォント: `C:\Windows\Fonts\meiryob.ttc`（メイリオBold）を使用
- [ ] VOICEVOX: `http://localhost:50021` で音声合成
- [ ] 出力: `C:\Users\khiro\OneDrive\Desktop\VIDEO\{filename}_{YYYYMMDD}.mp4`
- [ ] サムネイル: `C:\Users\khiro\OneDrive\Desktop\VIDEO\{filename}_thumb.png`
- [ ] メタ: `C:\Users\khiro\OneDrive\Desktop\VIDEO\{filename}_meta.txt`
- [ ] 動画: 縦型1080×1920、fps=30、音声付きMP4

---

### STEP 5 — 実行手順を案内する

```
① VOICEVOXを起動する（タスクバーから）
② Git Bashで以下を実行：
   cd ~/projects/short_video
   pip install moviepy pillow requests --break-system-packages
   python make_short.py
③ 完成したらデスクトップのVIDEOフォルダを確認：
   explorer "C:\Users\khiro\OneDrive\Desktop\VIDEO"
```

---

## シーンタイプ一覧

| type | 用途 | ビジュアル特徴 |
|------|------|------|
| `hook` | 冒頭フック | 大見出し＋グロー効果＋絵文字大きく |
| `problem` | 問題提起 | 警告カード＋赤アクセント |
| `point` | 解説ポイント | 番号バッジ＋グラスカード＋箇条書き |
| `summary` | まとめ | 複数カード縦並び |
| `cta` | 行動促進 | フォロー/保存アイコン＋強調テキスト |

## カラースキーム選び方ガイド

| color_key | 向いているテーマ |
|-----------|---------------|
| `modern_blue` | ビジネス・IT・副業・転職 |
| `neon_purple` | AI・テック・未来系・ゲーム |
| `warm_coral` | 恋愛・感情・モチベーション・生活 |
| `fresh_green` | 健康・食事・節約・エコ |
| `dark_premium` | お金・投資・ラグジュアリー |

## 動画尺ガイド（縦型ショート向け）

| シーン数 | 目標尺 | 各シーン秒数 |
|---------|--------|-----------|
| 5シーン | 45〜55秒 | 8〜11秒 |
| 6シーン | 55〜65秒 | 9〜11秒 |
| 7シーン | 65〜75秒 | 9〜11秒 |

## 重要な制約事項

1. 動画は必ず **1080×1920** （縦型）で生成する
2. 出力先は **`C:\Users\khiro\OneDrive\Desktop\VIDEO`** 固定
3. ナレーション文は **句読点あり・話し言葉** にする（VOICEVOXで自然に読み上げられるよう）
4. フォントパスは `C:\Windows\Fonts\meiryob.ttc` を使う（なければ `msgothic.ttc` にフォールバック）
5. make_short.py は **省略なしの完全なコード** を出力する
6. `pip install moviepy pillow requests` の実行をユーザーに案内する

---

## 【v2.0追加】実行前チェック・法令チェック

### 実行前チェック
- VOICEVOX起動確認（video-pipelineスキルと同じ起動チェックコードを組み込む）
- 出力先 `C:\Users\khiro\OneDrive\Desktop\VIDEO` の存在確認（なければ作成）
- ファイル名は半角英数＋アンダーバーのみを assert（日本語ファイル名はコピー失敗の原因）

### コンテンツ法令チェック（投稿前に必ず確認）
- [ ] アフィリエイト・PR案件の場合、**#PR 表記**が動画内とdescription両方にあるか（景表法ステマ規制、AFFILIATE.mdルール準拠）
- [ ] 「必ず稼げる」等の断定的利益表現がないか
- [ ] 他者の楽曲・映像素材を使っていないか（VOICEVOX話者のクレジット表記ルール確認）

### 出力後セルフチェック
- [ ] 尺が60〜75秒に収まっているか
- [ ] フック（冒頭2秒）にテキストと音声が両方あるか
- [ ] セーフエリア：上下にUIかぶりを想定した余白があるか（TikTokは下部300px危険域）

<!-- CHANGELOG
2026-07-17 v2.0: 起動チェック・ステマ規制チェック・セーフエリア基準を追加
-->
