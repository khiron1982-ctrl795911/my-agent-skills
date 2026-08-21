---
name: hr-dashboard
description: |
  サイマル・インターナショナルの人事データ（全社員リスト・残業有給Excel）から
  HR月次ダッシュボード・PowerPoint資料・部門別KPI分析を自動生成するスキル。

  以下のキーワードが出たら必ずこのスキルを使うこと：
  「HR」「人事」「ダッシュボード」「人員構成」「離職率」「管理職」「女性比率」
  「残業」「有休」「退職者」「役割別」「部門別」「昨対」「人的資本」
  「全社員リスト」「HR月次レポート」「人事データのpptx/パワポ/スライド」
  Excelファイル（全社員リスト*.xlsx / *残業*有給*.xlsx）がアップロードされた場合も必ず使用。

  ※人事データと無関係な一般テキストのスライド整理は powerpoint-corrections スキルを使うこと。
---

# HR ダッシュボード スキル — サイマル・インターナショナル

## このスキルでできること

| アウトプット | 説明 |
|---|---|
| インタラクティブダッシュボード | Chart.js製。部門×指標ヒートマップ・昨対比・グラフ全種 |
| PowerPoint（.pptx） | 9スライド構成。pptxgenjsで生成、ネイティブチャート |
| KPI集計レポート | 全指標を部門別×全社別×昨対比で整理 |
| 役割別構成分析 | GM/MGR/TL/SNR-EX/EX/一般/非正規のデュアルトラック構造 |

---

## 入力ファイルの仕様

### ① 全社員リスト（月次）
- ファイル名パターン: `全社員リスト*.xlsx`
- 主要シート:
  - `YYYY年M月`（月次個人データ）— header行=17行目（0-indexed: 16）
  - `サマリ2`（月次サマリー集計）
  - `退職者一覧`（全年度退職者）— header行=2行目（0-indexed: 1）

### ② 残業・有給ファイル（月次）
- ファイル名パターン: `*残業*有給*.xlsx` or `*更新*残業*有給*.xlsx`
- 主要シート:
  - `基準越え`（100h/89h/45h超 人数）
  - `有休`（部門別有休取得日数）
  - `平均_法定外残業`（個人別残業時間）

---

## データ抽出ロジック

### 全社員リストから個人データを読み込む

```python
import pandas as pd

xl = pd.ExcelFile('全社員リスト*.xlsx')
df = pd.read_excel(xl, sheet_name='YYYY年M月', header=16)
emp = df[pd.to_numeric(df['社員番号'], errors='coerce').notna()].copy()

# 主要列
# 社員番号, (氏名), 雇用形態, 勤続年数, 役職, 役割, 2026G等級
# (所属名1)=部署, (所属名2)=課, (性別), (年齢), (入社日), (退職日), 勤務状態

# 経理課を独立部署として扱う
emp['部署'] = emp['(所属名1)'].fillna('')
emp.loc[emp['(所属名2)'] == '経理課', '部署'] = '経理課'

# 役割クリーニング（整数0は「役割なし」）
emp['役割_c'] = emp['役割'].apply(lambda x: '役割なし' if x == 0 else str(x))

# フラグ
emp['is_female'] = emp['(性別)'] == '女'
emp['is_seishain'] = emp['雇用形態'] == '正社員'
emp['is_kyushoku'] = emp['勤務状態'] == '休職中'
emp['is_mgmt'] = emp['役割_c'].isin(['GM', 'マネージャー'])  # 管理職定義: GM+MGR
emp['is_leader'] = emp['役割_c'].isin(['GM', 'マネージャー', 'チームリーダー'])
emp['age'] = pd.to_numeric(emp['(年齢)'], errors='coerce')
emp['tenure'] = pd.to_numeric(emp['勤続年数'], errors='coerce')
```

### 退職者データの読み込み

```python
dq = pd.read_excel(xl, sheet_name='退職者一覧', header=None)
rows = dq.iloc[2:, :].reset_index(drop=True)
quits = pd.DataFrame({
    '氏名':     rows.iloc[:, 2],
    '雇用形態': rows.iloc[:, 8],
    '勤続年数': pd.to_numeric(rows.iloc[:, 9], errors='coerce'),
    '部署':     rows.iloc[:, 25],
    '課':       rows.iloc[:, 26],
    '退職日':   pd.to_datetime(rows.iloc[:, 33]),
})
quits.loc[quits['課'] == '経理課', '部署'] = '経理課'
quits['is_seishain'] = quits['雇用形態'] == '正社員'
quits['年度'] = quits['退職日'].apply(
    lambda x: '2025年度' if (x.year < 2026 or (x.year == 2026 and x.month <= 3)) else '2026年度'
)
```

---

## KPI 計算式（完全版）

### 全社レベル

```python
total = len(emp)
female_ratio = emp['is_female'].mean()
seishain_ratio = emp['is_seishain'].mean()
mgmt_count = emp['is_mgmt'].sum()            # GM + MGR のみ
mgmt_female_ratio = emp[emp['is_mgmt']]['is_female'].mean()
kyushoku_ratio = emp['is_kyushoku'].mean()
avg_age = emp['age'].mean()
avg_tenure = emp['tenure'].mean()

# 離職率 = 退職数 ÷ (退職数 + 在籍数) × 100
quit_all = quits[quits['年度'] == '2025年度']
turnover_all = len(quit_all) / (len(quit_all) + total) * 100
turnover_sei = len(quit_all[quit_all['is_seishain']]) / \
               (len(quit_all[quit_all['is_seishain']]) + emp['is_seishain'].sum()) * 100

# 退職者平均勤続年数
avg_tenure_quit_all = quit_all['勤続年数'].mean()
avg_tenure_quit_sei = quit_all[quit_all['is_seishain']]['勤続年数'].mean()
```

### 部門別 KPI 一括集計

```python
DEPTS = ['通訳事業部','翻訳事業部','D&IR翻訳事業部','機材事業部',
         'HR事業部','人材サービス部','営業部','経営支援部','経理課']

dept_stats = emp.groupby('部署').agg(
    人数        = ('社員番号', 'count'),
    女性数      = ('is_female', 'sum'),
    管理職数    = ('is_mgmt', 'sum'),
    管理職女性  = ('is_mgmt', lambda x: emp.loc[x.index, 'is_female'].sum()),
    正社員数    = ('is_seishain', 'sum'),
    休職者数    = ('is_kyushoku', 'sum'),
    平均年齢    = ('age', 'mean'),
    平均勤続    = ('tenure', 'mean'),
).reset_index()

# 退職者を結合
dept_quit_all = quit_all.groupby('部署').size().rename('退職数_全')
dept_quit_sei = quit_all[quit_all['is_seishain']].groupby('部署').size().rename('退職数_正')
dept_quit_tenure = quit_all[quit_all['is_seishain']].groupby('部署')['勤続年数'].mean().rename('退職者勤続_正')

dept_stats = dept_stats.set_index('部署')
dept_stats = dept_stats.join([dept_quit_all, dept_quit_sei, dept_quit_tenure]).fillna(0)
dept_stats = dept_stats.reindex(DEPTS)

# 計算指標
dept_stats['女性比率']       = dept_stats['女性数'] / dept_stats['人数'] * 100
dept_stats['管理職比率']     = dept_stats['管理職数'] / dept_stats['人数'] * 100
dept_stats['管理職女性比率'] = dept_stats['管理職女性'] / dept_stats['管理職数'] * 100
dept_stats['正社員比率']     = dept_stats['正社員数'] / dept_stats['人数'] * 100
dept_stats['休職率']         = dept_stats['休職者数'] / dept_stats['人数'] * 100
dept_stats['離職率_全']      = dept_stats['退職数_全'] / (dept_stats['退職数_全'] + dept_stats['人数']) * 100
dept_stats['離職率_正']      = dept_stats['退職数_正'] / (dept_stats['退職数_正'] + dept_stats['正社員数']) * 100
```

### 役割別 KPI（デュアルトラック構造）

```python
ROLE_ORDER = ['GM', 'マネージャー', 'チームリーダー',
              'シニアエキスパート', 'エキスパート', '一般社員', '役割なし']

# ⚠️ 役割=0は整数として格納されているため .apply() でキャッチ必須
role_stats = emp.groupby('役割_c').agg(
    人数   = ('社員番号', 'count'),
    女性   = ('is_female', 'sum'),
).reindex(ROLE_ORDER)
role_stats['男性'] = role_stats['人数'] - role_stats['女性']
role_stats['女性比率'] = role_stats['女性'] / role_stats['人数'] * 100
role_stats['全体比']  = role_stats['人数'] / total * 100
```

---

## 残業・有給データの読み込み

```python
ot_xl = pd.ExcelFile('*残業*有給*.xlsx')

# 基準越え（45h超人数を部門別に集計）
df_kijun = pd.read_excel(ot_xl, sheet_name='基準越え', header=None)
# 行6以降が実データ。col1=部署, col4=氏名, col8=TTL（基準越え合計回数）
# 45時間超は col7='45時間' の値が>=1 のものをカウント

# 有休（部門別平均取得日数）
df_yukyu = pd.read_excel(ot_xl, sheet_name='有休', header=None)
# row3: ヘッダー（部, 課, 4月, 5月 ...）
# col3=部, col4=課, col4=4月取得日数
```

---

## ダッシュボード生成方針

### グラフ選定ルール（チャートタイプ）

| 指標 | グラフタイプ | 理由 |
|---|---|---|
| 役割別人数 | 横棒（stacked男女） | 6〜7カテゴリ、男女2系列 |
| 部門別離職率（昨対） | 縦棒（grouped） | 7部門×2系列、値が見やすい |
| 月別退職推移 | 棒+折れ線（コンボ） | 棒=退職数、折れ線=社員数 |
| 管理職女性比率 | 横棒（単系列・色分け） | 赤<30%・黄30-50%・緑50%+ |
| 在籍vs退職者勤続比較 | 横棒（grouped） | 差の大きさを視覚化 |
| 年代別構成 | 縦棒（stacked男女） | 5世代、昨対2系列 |
| 雇用形態別 | ドーナツ | 4〜5カテゴリ |
| 部門×指標ヒートマップ | HTMLテーブル | 9部門×10+指標 |
| 退職者勤続分布 | 縦棒（単系列・色階調） | 6バケット、色で深刻度 |

### ヒートマップの色分け閾値

```javascript
function cellColor(col, val) {
  if (col === '女性比率')       return val >= 70 ? 'green' : val >= 50 ? 'amber' : 'red';
  if (col === '管理職比率')     return val >= 10 ? 'green' : val >= 7  ? 'amber' : 'red';
  if (col === '管理職女性比率') return val >= 50 ? 'green' : val >= 30 ? 'amber' : 'red';
  if (col === '正社員比率')     return val >= 80 ? 'green' : val >= 65 ? 'amber' : 'red';
  if (col === '休職率')         return val <  3  ? 'green' : val <  7  ? 'amber' : 'red';
  if (col === '離職率_全')      return val < 10  ? 'green' : val < 15  ? 'amber' : 'red';
  if (col === '離職率_正')      return val <  8  ? 'green' : val < 12  ? 'amber' : 'red';
  if (col === '退職者勤続_正')  return 'blue'; // 参考値、良否判断なし
}
```

---

## PowerPoint 生成仕様

### スライド構成（9枚固定）

```
01 表紙         — ダークネイビー(#0B1D3F)背景、サイマルブルー(#005CFF)左帯
02 サマリー     — 8KPIカード（昨対デルタ付き）+ 総括コメント
03 人員構成     — 年代別昨対棒グラフ + 部門別人員変化横棒
04 ダイバーシティ — 役職別男女stacked + 部門別管理職女性比率昨対
05 離職・定着   — 月別退職推移コンボ + 部門別離職率縦棒（全7部門）
06 退職者分析   — 勤続分布棒グラフ + 在籍vs退職者勤続横棒grouped
07 労務管理     — 残業部門別棒 + 有休×休職コンボ（折れ線+棒）
08 アクション提言 — ダーク背景3列ロードマップ（今すぐ/3ヶ月/半年）
09 付録         — 部門別全指標昨対数値テーブル（色分け）
```

### pptxgenjs 基本設定

```javascript
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10" × 5.625"

// ブランドカラー
const SB   = '005CFF'; // Simul Blue（#なし）
const DARK = '0B1D3F'; // ダークネイビー
const RED  = 'E24B4A';
const AMB  = 'BA7517';
const GRN  = '1D9E75';
const PINK = 'D4537E';
const BLU2 = '85B7EB'; // 昨対用ライトブルー
```

### スライドヘッダー共通関数

```javascript
function addSlideHeader(slide, slideNo, title, sub) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625,
    fill: { color: SB }, line: { color: SB }
  });
  slide.addText(slideNo, {
    x: 0.22, y: 0.22, w: 9.6, h: 0.28,
    fontSize: 9, color: SB, bold: true, charSpacing: 2, fontFace: 'Calibri', margin: 0
  });
  slide.addText(title, {
    x: 0.22, y: 0.48, w: 9.6, h: 0.55,
    fontSize: 22, bold: true, fontFace: 'Calibri', margin: 0
  });
  if (sub) slide.addText(sub, {
    x: 0.22, y: 1.02, w: 9.6, h: 0.3,
    fontSize: 11, color: '5A6577', fontFace: 'Calibri', margin: 0
  });
  slide.background = { color: 'FFFFFF' };
}
```

### チャートオプション共通設定

```javascript
function chartOpts(extra) {
  return Object.assign({
    chartArea: { fill: { color: 'FFFFFF' } },
    catAxisLabelColor: '5A6577', valAxisLabelColor: '5A6577',
    valGridLine: { color: 'E2E8F0', size: 0.5 },
    catGridLine: { style: 'none' },
    catAxisLabelFontSize: 9, valAxisLabelFontSize: 9,
    showLegend: false, showTitle: false
  }, extra);
}
```

### 重要な実装注意事項

```
⚠️ pptxgenjs カラーコード: '#' は絶対に付けない（ファイル破損）
⚠️ shadow の color: 8文字16進数（透明度込み）は使用不可→ opacity プロパティを使う
⚠️ ROUNDED_RECTANGLE にアクセントバーを重ねない → RECTANGLE を使う
⚠️ combo chart で Y軸2本: 現バージョンでは非対応のため、月別推移は BAR のみで実装
⚠️ 部門別離職率の barDir: 'bar'（横棒）は高さが足りないと部門が切れる
    → barDir: 'col'（縦棒）に変更すると全部門が表示される
⚠️ valAxisMinVal: 0 を明示しないと負値が軸に出る場合がある
```

---

## 業界ベンチマーク（比較用）

| 指標 | 業界平均 | 出典 |
|---|---|---|
| 管理職比率（全業種） | 11.5% | 厚生労働省 令和3年賃金構造基本統計調査 |
| 女性管理職比率（課長相当以上） | 12.7% | 厚生労働省 令和5年度雇用均等基本調査 |
| サービス業 管理職比率 | 約10% | 帝国データバンク2024 |
| サービス業 女性管理職比率 | 15.4% | 帝国データバンク2025 |
| 全規模平均 女性管理職比率 | 11.1% | 帝国データバンク2025 |

---

## 役割別キャリアトラック構造（サイマル固有）

```
管理職トラック:  一般社員 → チームリーダー(TL) → マネージャー(MGR) → GM
                 G1          G1-4/G2              G3                  G4

専門職トラック:  一般社員 → エキスパート(EX) → シニアエキスパート(SNR-EX)
                 G1          G2                  G3

非正規（役割なし）: 一般アルバイト・シニアアルバイト・契約社員(無期)・嘱託
                    等級なし（G等級=-）、役割列が整数0として格納
```

### ⚠️ データ取得の注意点
- 役割列の `0` は **整数**として格納されている（文字列'0'ではない）
- `emp['役割'].apply(lambda x: '役割なし' if x == 0 else str(x))` で必ずキャッチ
- チームリーダーはG1（2名）とG2（29名）に分かれている（G2がメイン）
- シニアエキスパートはG3扱い（マネージャーと同等級）

---

## 現在把握できていない指標（未整備）

以下はデータファイルに存在せず、別途収集が必要：

| 指標 | 重要度 | 備考 |
|---|---|---|
| 役員（取締役・監査役）の人数・男女比 | 高 | ISO 30414 必須。経営陣の多様性 |
| 男性育児休業取得率 | 高 | 女活法・有報開示義務対象 |
| 昇格・昇進率（パイプライン） | 高 | 一般→TL→MGR への昇格実績 |
| 男女賃金格差 | 高 | 有報開示義務（101名以上） |
| 研修時間・研修投資額 | 中 | ISO 30414 推奨指標 |
| 障害者雇用率 | 中 | 法定報告義務（2.5%以上） |
| 外国籍社員数 | 中 | 通訳・翻訳業界の重要多様性指標 |

---

## ワークフロー

### ユーザーがExcelをアップロードした場合

1. ファイル名を確認し、全社員リスト / 残業有給 を識別
2. `references/data-schema.md` を参照してシート構造を確認
3. 上記 Python コードでデータ抽出・KPI 計算
4. ユーザーの要求（ダッシュボード/PPT/集計）に応じてアウトプット選択

### ダッシュボード生成を求められた場合

1. データ抽出・KPI 計算を実行
2. Chart.js + HTML で show_widget を使いインタラクティブ表示
3. 部門×指標ヒートマップは HTMLテーブル で実装（Chart.js 不要）
4. 昨対データがあれば必ず比較グラフを追加

### PPT 生成を求められた場合

1. `npm list -g pptxgenjs` で確認（未インストールなら `npm install -g pptxgenjs`）
2. 上記 pptxgenjs 仕様に従い 9スライド .js ファイルを生成
3. `node hr_deck.js` で実行
4. LibreOffice + pdftoppm で PDF 変換・目視確認
5. スライド5の部門別離職率は `barDir: 'col'` で実装（横棒は切れる）
6. 出力先: `C:\Users\kuwata\Desktop\人事フォルダ\` 配下の依頼元フォルダ（作業スクリプトは `C:\Users\kuwata\work\pptx-tools\`）

### 月次更新を求められた場合

1. 新しい月のシート名を確認（例：`2026年6月`）
2. 昨年同月シート（例：`2025年6月`）と比較
3. 退職者一覧に新規退職者が追加されているか確認
4. KPI を再計算し前月比・昨対比を更新
5. ダッシュボードの月別推移データを1ヶ月スライド

---

## 品質レビュー（出力前に毎回実行・デジタル庁ダッシュボードガイドブック観点）

ダッシュボード・PPTを出力する前に、以下を自分でチェックして NG があれば直してから出す:

1. **グラフ選択の妥当性** — 時間変化（月別推移など）を棒グラフ単体で表現していないか
   （推移は折れ線かコンボにする。上の「グラフ選定ルール」表に従う）
2. **比較対象の有無** — 単独の数字（例: 離職率12%）だけを出していないか。
   必ず「昨対比・前月比・業界ベンチマーク」のいずれかを添える
3. **並び順の意味** — 部門・カテゴリを五十音順ではなく「値の大きい順」か
   「組織の固定順（DEPTS順）」で並べているか
4. **表示エラー** — HTML出力なら `NaN` / `undefined` / 空セルが画面に出ていないか。
   全KPI計算後に `isna()` チェックを1回通す
5. **凡例・単位** — %か人数か時間かが各グラフで明記されているか

## 完了判定

対象月、母数、除外条件、計算式、前月比・ベンチマークの比較基準を併記する。集計結果と
元データの件数整合を確認し、欠損・定義変更・比較不能な指標は可視化しても結論に使わない。

## 個人情報保護ルール（必須遵守）

このスキルが扱うのは給与・健康状態に紐づく個人データである。以下を厳守する。

- ダッシュボード・PPTには氏名・社員番号を出力せず、集計値だけを出す。
- 休職者・退職者を個人特定できる粒度（例: 部門×年代×性別で1名）は「-」表示にする。
- CSVなどの中間ファイルは、作業完了後に削除を案内する。
- OneDriveなどクラウド同期フォルダに成果物を保存する場合は、社内共有ポリシーの確認を促す。

## 計算セルフチェック（出力前に必ず実行）

- [ ] 部門別人数の合計と全社人数が一致する（不一致は部署マッピング漏れ）。
- [ ] 役割別人数の合計と全社人数が一致する（役割なしの整数0の取りこぼしを確認）。
- [ ] 昨対比較の対象が同月である（年度・月の取り違えを確認）。
- [ ] 離職率の分母定義をスライド脚注に明記する。
- [ ] 女性比率が100%または0%の部門は元データを目視確認する。

## Codexレビュー連携

PythonコードやpptxgenjsのJSを外部レビューする場合は、`codex-bridge` のHANDOFFテンプレートを使う。特にpandasの暗黙の型変換・SettingWithCopyWarning、パスや年度のハードコード、個人情報の中間出力漏れを確認する。

## 参照ファイル

- `references/data-schema.md` — Excel各シートの列定義詳細
- `references/kpi-formulas.md` — 全KPI計算式と注意点

## 自己改善プロトコル（毎回実行）

スキル実行の最後に必ず確認する:
1. ユーザーからの訂正・追加指示があったか。手順どおりに進まなかった箇所（列位置ズレ・
   シート名変更・pptxgenjsのエラー等）はあるか
2. あれば、このSKILL.mdまたは references/ の該当箇所を直接修正するか、
   下の改善ログに1行追記する（形式: `- YYYY-MM-DD: [事象] → [変更内容]`）
3. 改善ログが10行を超えたら本文に統合してログを整理する

修正はClaude自身が行ってよい（承認不要）。KPI定義の変更など意味が変わる修正のみ一言報告する。

## 改善ログ

- 2026-07-13: デジタル庁ガイドブック観点の品質レビュー節を追加。出力先をWindows実環境に修正
- 2026-07-17: 個人情報保護、集計値検算、Codexレビュー連携を追加
