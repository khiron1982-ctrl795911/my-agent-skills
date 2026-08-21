# ショート動画（モードB）実装コード集

## カラースキーム定義

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

## モダンイラスト生成関数（Pillow）

```python
W, H = 1080, 1920  # 縦型 9:16

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
```

## シーン描画関数の実装要件

以下の4関数は**必ず完全実装する**（省略禁止）：

| 関数 | 内容 |
|------|------|
| `draw_scene_hook(scene, cs)` | 中央に大見出し（グロー付き）、上部に絵文字（フォントサイズ160相当）、`accent` 文字列があれば下部に帯付きで表示 |
| `draw_scene_point(scene, cs, point_num)` | 上部に円形番号バッジ（accent色）、中央にグラスカード＋見出し、カード内に本文を改行折り返し |
| `draw_scene_summary(scene, cs)` | 見出し＋箇条書き項目を縦並びの小カードで表示（最大5項目） |
| `draw_scene_cta(scene, cs)` | 「フォロー」「保存」を模したボタン風カード2枚＋促進テキスト |

共通処理：
- すべてのシーンで `draw_modern_bg` → シーン固有描画 → `draw_progress_bar` の順
- テキストの折り返しは1行あたり全角14〜16文字を目安に `textwrap` 相当の処理を入れる
- 絵文字はフォントによっては描画できないため、失敗時は無視して続行する
