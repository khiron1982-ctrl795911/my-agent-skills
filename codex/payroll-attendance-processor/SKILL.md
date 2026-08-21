---
name: payroll-attendance-processor
description: Create processed payroll attendance workbooks from Japanese payroll raw attendance Excel exports. Use when the user provides pasted paths to 勤怠ローデータ, 勤怠データ\元データ, 日別データ, 5区分勤怠, フレックス勤務者勤怠, 60時間超過, 一般アルバイト勤怠, or asks to generate 5区分勤怠データ.xlsx, フレックス勤務者勤怠データ.xlsx, 60時間超過対象者(正社員&フレックス).xlsx, 一般アルバイト勤怠データ.xlsx, and optional 振替休日/振替出勤 data for payroll processing.
---

# Payroll Attendance Processor

## Core Rule

Given one or more pasted Windows paths, create the processed attendance files used before payroll finalization:

- `5区分勤怠データ.xlsx`
- `フレックス勤務者勤怠データ.xlsx`
- `60時間超過対象者(正社員&フレックス).xlsx`
- `一般アルバイト勤怠データ.xlsx`
- optional `振替休日データ一覧.xlsx` / `振替出勤データ一覧.xlsx`

Do not invent missing data. If a source file or column is not found, report it as a warning or required input.

## Quick Start

Run the bundled script with the raw-data file or folder paths:

```powershell
& 'C:\Users\kuwata\AppData\Local\Programs\Python\Python314\python.exe' '<skill>/scripts/build_attendance_outputs.py' '<raw-path-1>' '<raw-path-2>' --out '<output-folder>' --payroll-month '2025-10'
```

`--payroll-month` is optional. If omitted, the script infers the payroll month from sheet names like `custom_csv_20250901_20250930` by adding one month.

Default output folder: `加工済み勤怠データ` under the first input path or its parent.

## Workflow

1. Normalize pasted paths by stripping quotes.
2. Discover Excel files recursively when a folder is provided.
3. Identify attendance-like sheets by headers containing `従業員コード` and `名前`.
4. Build four standard outputs when their source sheets exist.
5. Copy optional transfer/holiday files when filenames contain `振替休日`, `振替出勤`, `振休者`, or `振出`.
6. Write `attendance_processing_report.json` with source files, output paths, and warnings.
7. Review warnings before treating the output as payroll-ready.

## Expected Source Shapes

Read `references/attendance_logic.md` when column mapping or exception handling matters.

The script expects these known R07/R08 structures:

- 5区分/一般アルバイト: 26 columns beginning `雇用区分コード`, `従業員コード`, `名前`.
- フレックス: 35 columns with extra adjusted columns such as `休暇取得日数`, `所定内不足時間`, `総残業時間(確定)`.
- 60時間超過: 6 columns: `雇用区分コード`, `従業員コード`, `名前`, `法定外労働時間`, `所定休日勤務時間`, `60時間超`.
- 5区分 `_3加算用`: may have 32 columns. Use `_3加算用` as the preferred source, but reduce it to the first 26 final-output columns. In observed R08 files, the first 26 columns already contain the adjusted G/H values; trailing duplicate columns can contain helper formulas and must not be left as broken references in the 26-column output.

## Validation Checklist

After generation, verify:

- Every required output is present or explicitly warned as missing.
- `従業員コード` is not blank.
- 5区分 and 一般アルバイト outputs have 26 columns.
- フレックス output has 35 columns.
- 60時間超過 output has 6 columns.
- The target payroll month is correct.
- Any optional transfer/holiday files were copied only when present.

## Completion Gate

Do not describe the data as payroll-ready solely because files were generated. Report the
processing report's warnings, the payroll month, and the row count of every output. Escalate
any duplicate employee code, blank required value, ambiguous source candidate, or missing
standard output for a human payroll decision.

## Unclear Cases

Keep these out of confirmed logic unless the source file proves them:

- Employee master, department master, employment-category master locations.
- Retirement/leave exclusion rules.
- Manual filtering, value paste, sorting, or approval history.
- Month-specific corrected files when multiple candidates exist and filenames do not clearly indicate the final version.


