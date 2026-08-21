---
name: excalidraw-diagram-generator
description: >
  分岐のない自由配置の概念図・構成図（組織図、関係図、システム構成図など）をExcalidrawに貼れる形式で作るスキル。
  Use when: 「組織図を描いて」「構成図にして」「Excalidrawで図解して」「手描き風の図にして」と言われたとき、/excalidraw-diagram-generator が呼ばれたとき。
  Do NOT use for: 判断・分岐があるプロセス図（/flowchart-decision-builder）、数字を見せる1枚もの資料（/infographic-builder）、既存レイアウトの改善助言（/ui-ux-layout-advisor）。
---

# /excalidraw-diagram-generator — 概念図・構成図ジェネレーター

## 使い方
```
/excalidraw-diagram-generator 人事部の組織図を作って（部長→3課長→各メンバー）
/excalidraw-diagram-generator 評価制度の関係図（等級・評価・報酬のつながり）
/excalidraw-diagram-generator 社内システムの構成図（勤怠・給与・採用管理の連携）
/excalidraw-diagram-generator この箇条書きを手描き風の図解にして：（箇条書きを貼り付け）
```

## このスキルがやること
1. 元の文章・箇条書きから「登場する要素（箱にするもの）」と「要素同士のつながり」を洗い出す
2. 分岐や判断が主目的の内容であれば、その旨を伝えて `/flowchart-decision-builder` を勧める
3. 要素を階層・グループごとに整理し、レイアウト（上下関係、横並び、囲みグループなど）を決める
4. Excalidrawにそのまま読み込める `.excalidraw` 形式のJSONを作成する。重要な決まりごと：
   - 箱の文字は四角形の中に書けないため、**四角形とは別に text 要素を作り、箱の中央に重ねて配置する**
   - 矢印は startBinding などの紐付けは使わず、**x・y・points の座標指定だけで描く**（この方が確実に読み込める）
5. JSONが読み込めない環境向けに、同じ内容を「手描き再現用の構造メモ」（箱の一覧・矢印の向き・配置イメージ）としても併記する
6. 検証チェックリストを確認し、要素の抜けや矢印の重なりがあれば調整する

## 出力フォーマット
````markdown
# 概念図：{タイトル（例：人事部 組織図）}

## Excalidrawファイル（そのまま保存して読み込み可）
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    { "type": "rectangle", "id": "box1", "x": 220, "y": 40,  "width": 200, "height": 60 },
    { "type": "text", "id": "label1", "x": 280, "y": 58,  "width": 80, "height": 25, "text": "人事部長", "fontSize": 20 },
    { "type": "rectangle", "id": "box2", "x": 40,  "y": 180, "width": 160, "height": 60 },
    { "type": "text", "id": "label2", "x": 90,  "y": 198, "width": 60, "height": 25, "text": "採用課", "fontSize": 20 },
    { "type": "rectangle", "id": "box3", "x": 240, "y": 180, "width": 160, "height": 60 },
    { "type": "text", "id": "label3", "x": 290, "y": 198, "width": 60, "height": 25, "text": "労務課", "fontSize": 20 },
    { "type": "rectangle", "id": "box4", "x": 440, "y": 180, "width": 160, "height": 60 },
    { "type": "text", "id": "label4", "x": 490, "y": 198, "width": 60, "height": 25, "text": "教育課", "fontSize": 20 },
    { "type": "arrow", "id": "a1", "x": 320, "y": 100, "width": 200, "height": 80, "points": [[0, 0], [-200, 80]] },
    { "type": "arrow", "id": "a2", "x": 320, "y": 100, "width": 0,   "height": 80, "points": [[0, 0], [0, 80]] },
    { "type": "arrow", "id": "a3", "x": 320, "y": 100, "width": 200, "height": 80, "points": [[0, 0], [200, 80]] }
  ],
  "appState": { "gridSize": 20 }
}
```
上記のコードを `組織図.excalidraw` として保存し、excalidraw.com の「開く」からインポートしてください。

## 手描き再現用の構造メモ（JSONが使えない場合）
- 最上段：人事部長（1つの箱）
- 2段目：採用課／労務課／教育課（横並びの3つの箱）
- 矢印：人事部長 → 採用課・労務課・教育課（それぞれ下向き矢印）

[図 - 要確認：excalidraw.com にインポートするか、手描きメモを参照して再現してください]
````

## 検証チェックリスト
- □ 登場する要素（人・部署・システムなど）に抜け漏れがないか
- □ 矢印やつながりの向きが実態と合っているか
- □ 箱同士が座標上で重なっていないか
- □ 箱のラベルを四角形の "text" 属性に書いていないか（別の text 要素として箱の中央に置いたか。四角形に直接 text を書いても表示されない）
- □ 矢印を startBinding／endBinding で書いていないか（x・y・points の座標指定になっているか）
- □ 分岐・判断が主役の内容になっていないか（その場合は /flowchart-decision-builder を案内したか）
- □ JSONとして構文が正しいか（かっこ・カンマの閉じ忘れがないか）
- □ 手描き再現メモだけ見ても配置がイメージできるか

## 終了条件
JSONコードと手描き再現メモを1セット提示したら完成として提示し、「要素の追加・配置変更はないか」を確認して止まる。

## フィードバック反映（自動ブラッシュアップ用）
- 実行前に `~/.claude/projects/C--Users-khiro/memory/feedback_skills.md` があれば読み、このスキルへの過去の修正指示を反映する
- ユーザーから出力への修正指示を受けたら、同ファイルに「日付／スキル名／指示内容／今後どうするか」を1行で追記し、同じ指摘を二度受けないようにする
