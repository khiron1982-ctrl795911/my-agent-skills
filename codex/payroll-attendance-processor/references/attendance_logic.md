# Attendance Processing Logic

Use this reference when generating processed payroll attendance files from raw attendance exports.

## Standard Outputs

### 5区分勤怠データ / 一般アルバイト勤怠データ

Final 26 columns:

1. 雇用区分コード
2. 従業員コード
3. 名前
4. 休憩時間
5. 総労働時間(独自)
6. 所定時間(独自)
7. 総残業時間(SI)
8. 所定外労働時間
9. 法定外労働時間
10. 所定休日勤務時間
11. 法定休日勤務時間
12. 深夜時間
13. 総出勤日数
14. 所定休出日数
15. 法定休日出勤日数
16. 有休取得日数
17. 有休時間休取得時間
18. 特別休暇(有給)
19. 特別休暇(無給)
20. 欠勤取得日数
21. 早退回数
22. 早退時間
23. 遅刻回数
24. 遅刻時間
25. 代休取得日数
26. 代休付与日数

If a 5区分 source has `_3加算用` or 32 columns, it may include adjusted duplicate columns:

- 追加所定時間
- 総残業時間(SI)
- 所定外労働時間
- 総残業時間(SI)
- 所定外労働時間

For final 26-column output, prefer the `_3加算用` workbook, then keep the first 26 final-output columns. In observed R08 files, the adjusted G/H values are already materialized in those first 26 columns; trailing duplicate columns may be helper formulas and should not be copied into the reduced output.

## Flex Logic

Final 35 columns include the 26 base attendance columns plus adjustment columns:

- 休暇取得日数
- 休暇取得時間
- 所定時間(休暇取得時間合算)
- 所定内不足時間
- 所定外労働時間(不足分調整)
- 休業日数
- 総残業時間(確定)
- 所定外労働時間(調整)
- 法定外労働時間(調整)

Observed formulas:

- `休暇取得日数 = 有休取得日数 + 特別休暇(有給) + 特別休暇(無給) + 欠勤取得日数 + 代休取得日数`
- `休暇取得時間 = 休暇取得日数 * 7時間 + 有休取得時間`
- `所定時間(休暇取得時間合算) = 所定時間(独自) + 休暇取得時間`
- `所定内不足時間 = 月所定時間 - 所定時間(休暇取得時間合算)`
- `所定外労働時間(不足分調整) = 所定外労働時間 - 所定内不足時間`
- `総残業時間(確定) = 総残業時間(SI) - 所定内不足時間`
- `所定外労働時間(調整) = 総残業時間(確定) - 所定休日勤務時間 - 法定休日勤務時間`
- `法定外労働時間(調整) = 総残業時間(確定) - 所定外労働時間(調整) - 所定休日勤務時間 - 法定休日勤務時間`

Prefer copying an existing 35-column flex workbook over reconstructing one from 26 columns.

## 60時間超過

Final 6 columns:

1. 雇用区分コード
2. 従業員コード
3. 名前
4. 法定外労働時間
5. 所定休日勤務時間
6. 60時間超

Observed formula:

`60時間超 = 法定外労働時間 + 所定休日勤務時間 - 60:00`

Use an existing 60時間 workbook when available. If not available, ask for the intended対象者条件 before deriving it, because the file name says `正社員&フレックス` but the employment-category mapping is not proven by the raw files alone.

## Half-Day / Hourly Leave Overtime Adjustment

Observed source workbook: `超過残業算出シート_YYYYMM.xlsx`.

Important sheets:

- `データ貼付`: paste daily detail data.
- `集計`: sum adjustment by employee.

Observed `データ貼付` logic:

- `O + P`: KOT-counted overtime components.
- `IF(G < H, 1, 0)`: morning-leave or late-count flag.
- `IF(AND(TEXT(G,"hh:mm")>=TEXT(H,"hh:mm"),TEXT(I,"hh:mm")>=TEXT(J,"hh:mm"),R<>""),"中抜け","")`: mid-shift break flag.
- `IF(OR(T=1,U="中抜け"),I,I+R)`: deemed end time.
- `V - J`: overflow time.
- `IF(OR(COUNTIF(Q,"*AM*"),COUNTIF(Q,"*PM*")), W - L - S, "")`: half-day leave additional overtime.
- `IF(COUNTIF(E,"*シフトF*"),1,"")`: shift F flag.
- `IF(AC<>"", AC, IF(X="", Y, X))`: final additional time.
- `IF(K="","","早出")`: early-start comment.

Observed `集計` logic:

- `VLOOKUP` employee code to name.
- `SUMIFS` final additional time by employee code.

Do not claim manual paste, filter, or approval steps as confirmed unless a file explicitly documents them.

