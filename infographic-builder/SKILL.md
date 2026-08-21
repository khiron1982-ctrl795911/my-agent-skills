---
name: infographic-builder
description: >
  数字・ステップ・要点をHTML1枚もののインフォグラフィックにまとめるスキル。
  Use when: 「インフォグラフィックにして」「1枚にまとめて」「数字を見せる資料にして」「ステップを図解して」と言われたとき、/infographic-builder が呼ばれたとき。
  Do NOT use for: 分岐・判断があるプロセス（/flowchart-decision-builder）、自由配置の概念図・組織図（/excalidraw-diagram-generator）、既存レイアウトの改善助言（/ui-ux-layout-advisor）、PowerPoint化そのもの（/pptx）。
---

# /infographic-builder — 1枚インフォグラフィック作成

## 使い方
```
/infographic-builder 今期の採用実績を1枚のインフォグラフィックにして（応募数・内定数・入社数）
/infographic-builder 新人研修の4ステップをインフォグラフィック風にまとめて
/infographic-builder 離職率の推移データを1枚資料にして
/infographic-builder このExcelの数字をHTMLインフォグラフィックにして：（数字を貼り付け）
```

## このスキルがやること
1. 元データ・文章から「見せたい数字」「ステップ」「要点」を3〜6個に絞り込む（詰め込みすぎない）
2. 内容の性質に応じて構成パターンを選ぶ（数字強調型／ステップ型／比較型など）
3. 見出し・キャッチコピー・出典（データの時点）を整理する
4. HTML1枚（インラインCSS込み、外部ファイル不要）でインフォグラフィックを組み立てる
5. 色は3色以内に抑え、人事資料らしい落ち着いた配色にする
6. 完成後、「PowerPoint（.pptx）の資料に組み込みたい場合は /pptx スキルで対応できる」旨を案内する

## 出力フォーマット
````markdown
# インフォグラフィック：{タイトル（例：2026年度上期 採用実績）}

```html
<div style="font-family: 'Hiragino Sans', sans-serif; max-width: 720px; margin: 0 auto; padding: 32px; background: #ffffff; border: 1px solid #e5e5e5;">
  <h1 style="font-size: 24px; color: #1a2b4c; text-align: center; margin-bottom: 8px;">2026年度上期 採用実績</h1>
  <p style="text-align: center; color: #888; font-size: 12px; margin-bottom: 24px;">集計期間：2026年4月〜9月</p>
  <div style="display: flex; justify-content: space-around; text-align: center;">
    <div>
      <div style="font-size: 36px; font-weight: bold; color: #2f6fed;">128</div>
      <div style="font-size: 13px; color: #444;">応募数</div>
    </div>
    <div>
      <div style="font-size: 36px; font-weight: bold; color: #2f6fed;">24</div>
      <div style="font-size: 13px; color: #444;">内定数</div>
    </div>
    <div>
      <div style="font-size: 36px; font-weight: bold; color: #2f6fed;">18</div>
      <div style="font-size: 13px; color: #444;">入社数</div>
    </div>
  </div>
  <p style="margin-top: 24px; font-size: 12px; color: #999; text-align: center;">出典：人事部採用管理表（2026年10月時点）</p>
</div>
```

このHTMLをファイルに保存してブラウザで開くと画像のように表示されます。

[資料 - 要確認：数字や期間に間違いがないかご確認ください]

※ PowerPointのスライドに組み込みたい場合は `/pptx` スキルをご利用ください（このスキルではpptx化は行いません）。
````

## 検証チェックリスト
- □ 見せる数字・要点が6個以内に絞られているか（詰め込みすぎていないか）
- □ 数字の出典・集計時点が明記されているか
- □ 色数が3色以内で、読みやすいコントラストになっているか
- □ HTMLが1ファイルで完結しており、外部CSS・画像に依存していないか
- □ 分岐や判断フローの説明になっていないか（その場合は /flowchart-decision-builder を案内したか）
- □ pptx化の希望があった場合に /pptx への案内を添えたか

## 終了条件
HTMLコードを1セット提示したら完成として提示し、「数字・デザインの修正はないか」を確認して止まる。

## フィードバック反映（自動ブラッシュアップ用）
- 実行前に `~/.claude/projects/C--Users-khiro/memory/feedback_skills.md` があれば読み、このスキルへの過去の修正指示を反映する
- ユーザーから出力への修正指示を受けたら、同ファイルに「日付／スキル名／指示内容／今後どうするか」を1行で追記し、同じ指摘を二度受けないようにする
