import inspect
import numpy as np
import pandas as pd

# ── ข้อมูลตัวอย่าง ──────────────────────────────────────────────────────────
example_df = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 1],
    "salary":      ["$70000", "$55000", None, "N/A", "$90000", "$70000"],
    "country":     ["USA", "usa", "United Kingdom", "U.K.", "Germany", "USA"],
})

# ── คำตอบที่ถูกต้องสำหรับข้อมูลตัวอย่าง ────────────────────────────────────
# answer_key แสดงสถานะสุดท้ายหลังทำ deduplicate + ทำความสะอาดทุกคอลัมน์
# (ใช้สำหรับให้ผู้เข้าสอบดูเป็นแนวทาง — grader จะเทียบรายค่าตาม employee_id)
answer_key = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "salary":      [70000.0, 55000.0, 70000.0, 70000.0, 90000.0],
    "country":     ["United States", "United States", "United Kingdom",
                    "United Kingdom", "Germany"],
})

# ── ฟังก์ชันตรวจคำตอบ ────────────────────────────────────────────────────────
_EXPECTED_NAMES    = ["deduplicate", "standardize_countries", "clean_salary"]
_ALLOWED_COUNTRIES = {"United States", "United Kingdom", "Germany"}


def check_all_answers() -> None:
    frame = inspect.currentframe().f_back
    caller_globals = frame.f_globals
    del frame  # avoid reference cycle

    # ── ตรวจชื่อฟังก์ชัน ────────────────────────────────────────────────────
    bad_names = [
        name for name in _EXPECTED_NAMES
        if name not in caller_globals or not callable(caller_globals[name])
    ]
    if bad_names:
        print("⚠️  ชื่อฟังก์ชันต่อไปนี้ไม่ตรงกับที่โจทย์กำหนด — กรุณาตรวจสอบ:")
        for name in bad_names:
            print(f"   ✗ {name}")
        print()

    df_full = example_df.copy()

    def run(name):
        """Call the student's function with the FULL df (with duplicates); return (result, error_str)."""
        if name in bad_names:
            return None, "missing"
        func = caller_globals[name]
        try:
            return func(df_full.copy()), None
        except Exception as e:
            return None, str(e)

    # Build per-id expected maps from answer_key (employee_id is unique in answer_key).
    # Duplicate rows in example_df are exact copies, so each employee_id has one canonical
    # expected value — we can look it up regardless of duplicate position.
    expected_country = dict(zip(answer_key["employee_id"], answer_key["country"]))
    expected_salary  = dict(zip(answer_key["employee_id"], answer_key["salary"]))

    print("ผลการตรวจคำตอบ:")

    # ── 1. deduplicate ───────────────────────────────────────────────────────
    result, err = run("deduplicate")
    if err == "missing":
        print("  1. deduplicate: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  1. deduplicate: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame):
        print(f"  1. deduplicate: ผิด ✗  (ฟังก์ชั่นคำตอบจะคืนค่าที่มีชนิดเป็น DataFrame, ฟังก์ชั่นปัจจุบันคืนค่าที่มีชนิดเป็น: {type(result).__name__})")
    else:
        n_dups  = int(result.duplicated().sum())
        rows_ok = len(result) == len(answer_key)
        if n_dups == 0 and rows_ok:
            print("  1. deduplicate: ถูก ✓")
        else:
            if n_dups > 0:   print(f"  1. deduplicate: ผิด ✗  (ยังมีแถวซ้ำ {n_dups} แถว)")

    # ── 2. standardize_countries ─────────────────────────────────────────────
    # ต้องรับ df ดิบ (มีแถวซ้ำ) เป็น input และคงจำนวนแถวเดิม
    result, err = run("standardize_countries")
    if err == "missing":
        print("  2. standardize_countries: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  2. standardize_countries: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame):
        print(f"  2. standardize_countries: ผิด ✗  (ฟังก์ชั่นคำตอบจะคืนค่าที่มีชนิดเป็น DataFrame, ฟังก์ชั่นปัจจุบันคืนค่าที่มีชนิดเป็น: {type(result).__name__})")
    elif "country" not in result.columns or "employee_id" not in result.columns:
        missing = [c for c in ("employee_id", "country") if c not in result.columns]
        print(f"  2. standardize_countries: ผิด ✗  (ไม่พบคอลัมน์: {', '.join(missing)})")
    else:
        n_null     = int(result["country"].isna().sum())
        unexpected = set(result["country"].dropna().unique()) - _ALLOWED_COUNTRIES
        if n_null > 0 or unexpected:
            parts = []
            if n_null:     parts.append(f"มี null เหลืออยู่ {n_null} ค่า")
            if unexpected: parts.append(f"ค่าที่ไม่ถูกต้อง: {unexpected}")
            print(f"  2. standardize_countries: ผิด ✗  ({', '.join(parts)})")
        elif len(result) != len(df_full):
            print(f"  2. standardize_countries: ผิด ✗  "
                  f"(จำนวนแถวปัจจุบัน: {len(result)}, คาดว่าจะมี {len(df_full)} แถว — "
                  f"ฟังก์ชันนี้ไม่ควรเปลี่ยนจำนวนแถว)")
        else:
            mismatches = 0
            for _, row in result.iterrows():
                emp_id = row["employee_id"]
                if emp_id not in expected_country or row["country"] != expected_country[emp_id]:
                    mismatches += 1
            if mismatches == 0:
                print("  2. standardize_countries: ถูก ✓")
            else:
                print(f"  2. standardize_countries: ผิด ✗  ({mismatches} แถวมีค่าไม่ตรงกับเฉลย)")

    # ── 3. clean_salary ──────────────────────────────────────────────────────
    # ต้องรับ df ดิบ (มีแถวซ้ำ) เป็น input และคงจำนวนแถวเดิม
    result, err = run("clean_salary")
    if err == "missing":
        print("  3. clean_salary: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  3. clean_salary: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame):
        print(f"  3. clean_salary: ผิด ✗  (ฟังก์ชั่นคำตอบจะคืนค่าที่มีชนิดเป็น DataFrame, ฟังก์ชั่นปัจจุบันคืนค่าที่มีชนิดเป็น: {type(result).__name__})")
    elif "salary" not in result.columns or "employee_id" not in result.columns:
        missing = [c for c in ("employee_id", "salary") if c not in result.columns]
        print(f"  3. clean_salary: ผิด ✗  (ไม่พบคอลัมน์: {', '.join(missing)})")
    else:
        is_numeric = pd.api.types.is_numeric_dtype(result["salary"])
        n_null     = int(result["salary"].isna().sum())
        if not is_numeric:
            print("  3. clean_salary: ผิด ✗  (ยังมีค่าที่ไม่ใช่ตัวเลข)")
        elif n_null > 0:
            print(f"  3. clean_salary: ผิด ✗  (มี None/NA/NaN เหลืออยู่ {n_null} ค่า)")
        elif len(result) != len(df_full):
            print(f"  3. clean_salary: ผิด ✗  "
                  f"(จำนวนแถวปัจจุบัน: {len(result)}, คาดว่าจะมี {len(df_full)} แถว — "
                  f"ฟังก์ชันนี้ไม่ควรเปลี่ยนจำนวนแถว)")
        else:
            mismatches = 0
            for _, row in result.iterrows():
                emp_id = row["employee_id"]
                if emp_id not in expected_salary or not np.isclose(
                    float(row["salary"]), float(expected_salary[emp_id])
                ):
                    mismatches += 1
            if mismatches == 0:
                print("  3. clean_salary: ถูก ✓")
            else:
                print(f"  3. clean_salary: ผิด ✗  ({mismatches} แถวมีค่าไม่ตรงกับเฉลย)")
