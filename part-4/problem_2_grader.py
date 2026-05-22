import inspect
import numpy as np
import pandas as pd

# ── ข้อมูลตัวอย่าง ──────────────────────────────────────────────────────────
example_df = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 1],
    "salary":      ["$70,000", "$55,000", None, "N/A", "$90,000", "$70,000"],
    "age":         [34.0, 28.0, 200.0, 45.0, -5.0, 34.0],
    "country":     ["USA", "usa", "United Kingdom", "U.K.", "Germany", "USA"],
})

# ── คำตอบที่ถูกต้องสำหรับข้อมูลตัวอย่าง ────────────────────────────────────
answer_key = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "salary":      [70000.0, 55000.0, 70000.0, 70000.0, 90000.0],
    "age":         [34.0, 28.0, 34.0, 45.0, 34.0],
    "country":     ["United States", "United States", "United Kingdom",
                    "United Kingdom", "Germany"],
})

# ── ฟังก์ชันตรวจคำตอบ ────────────────────────────────────────────────────────
_EXPECTED_NAMES    = ["deduplicate", "standardize_countries", "clean_salary", "clean_age"]
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

    df_full    = example_df.copy()
    df_deduped = example_df.drop_duplicates().reset_index(drop=True)

    def run(name):
        """Call the student's function; return (result, error_str)."""
        if name in bad_names:
            return None, "missing"
        func     = caller_globals[name]
        input_df = df_full if name == "deduplicate" else df_deduped
        try:
            return func(input_df.copy()), None
        except Exception as e:
            return None, str(e)

    def can_align(res):
        return (
            isinstance(res, pd.DataFrame)
            and "employee_id" in res.columns
            and len(res) == len(answer_key)
            and set(res["employee_id"].tolist()) == set(answer_key["employee_id"].tolist())
        )

    def aligned(res):
        """Return (r_sorted, e_sorted) both sorted by employee_id."""
        r = res.sort_values("employee_id").reset_index(drop=True)
        e = answer_key.sort_values("employee_id").reset_index(drop=True)
        return r, e

    print("ผลการตรวจคำตอบ:")
    dedup_ok = False

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
        dedup_ok = n_dups == 0 and rows_ok
        if dedup_ok:
            print("  1. deduplicate: ถูก ✓")
        else:
            parts = []
            if n_dups > 0:   parts.append(f"ยังมีแถวซ้ำ {n_dups} แถว")
            if not rows_ok:  parts.append(f"จำนวนแถวปัจจุบัน: {len(result)} (คำตอบ: {len(answer_key)})")
            print(f"  1. deduplicate: ผิด ✗  ({', '.join(parts)})")

    # ── 2. standardize_countries ─────────────────────────────────────────────
    result, err = run("standardize_countries")
    if err == "missing":
        print("  2. standardize_countries: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  2. standardize_countries: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame) or "country" not in result.columns:
        print("  2. standardize_countries: ผิด ✗  (ไม่พบคอลัมน์ country)")
    else:
        n_null     = int(result["country"].isna().sum())
        unexpected = set(result["country"].dropna().unique()) - _ALLOWED_COUNTRIES
        if n_null > 0 or unexpected:
            parts = []
            if n_null:     parts.append(f"มี null เหลืออยู่ {n_null} ค่า")
            if unexpected: parts.append(f"ค่าที่ไม่ถูกต้อง: {unexpected}")
            print(f"  2. standardize_countries: ผิด ✗  ({', '.join(parts)})")
        elif can_align(result):
            r, e = aligned(result)
            n_diff = int((r["country"] != e["country"]).sum())
            if n_diff == 0:
                print("  2. standardize_countries: ถูก ✓")
            else:
                print(f"  2. standardize_countries: ผิด ✗  ({n_diff} ค่าไม่ตรงกับเฉลย)")
        else:
            print("  2. standardize_countries: ถูก ✓")

    # ── 3. clean_salary ──────────────────────────────────────────────────────
    result, err = run("clean_salary")
    if err == "missing":
        print("  3. clean_salary: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  3. clean_salary: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame) or "salary" not in result.columns:
        print("  3. clean_salary: ผิด ✗  (ไม่พบคอลัมน์ salary)")
    else:
        is_numeric = pd.api.types.is_numeric_dtype(result["salary"])
        n_null     = int(result["salary"].isna().sum())
        if not is_numeric:
            print("  3. clean_salary: ผิด ✗  (ยังมีค่าที่ไม่ใช่ตัวเลข)")
        elif n_null > 0:
            print(f"  3. clean_salary: ผิด ✗  (มี None/NA/NaN เหลืออยู่ {n_null} ค่า)")
        elif can_align(result):
            r, e = aligned(result)
            if np.allclose(r["salary"].astype(float), e["salary"].astype(float)):
                print("  3. clean_salary: ถูก ✓")
            else:
                n_diff = int((~np.isclose(
                    r["salary"].astype(float), e["salary"].astype(float))).sum())
                print(f"  3. clean_salary: ผิด ✗  ({n_diff} ค่าไม่ตรงกับเฉลย)")
        else:
            print("  3. clean_salary: ถูก ✓")

    # ── 4. clean_age ─────────────────────────────────────────────────────────
    result, err = run("clean_age")
    if err == "missing":
        print("  4. clean_age: ⚠️  ไม่พบฟังก์ชัน")
    elif err:
        print(f"  4. clean_age: ERROR: {err}")
    elif not isinstance(result, pd.DataFrame) or "age" not in result.columns:
        print("  4. clean_age: ผิด ✗  (ไม่พบคอลัมน์ age)")
    else:
        out_of_range = result["age"].notna() & ~result["age"].between(18, 100)
        n_bad = int(out_of_range.sum())
        if n_bad > 0:
            bad_vals = result.loc[out_of_range, "age"].tolist()
            print(f"  4. clean_age: ผิด ✗  (มีค่าที่ไม่ถูกต้อง: {bad_vals} ค่า)")
        elif can_align(result):
            r, e = aligned(result)
            if np.allclose(r["age"].astype(float), e["age"].astype(float)):
                print("  4. clean_age: ถูก ✓")
            else:
                n_diff = int((~np.isclose(
                    r["age"].astype(float), e["age"].astype(float))).sum())
                print(f"  4. clean_age: ผิด ✗  ({n_diff} ค่าไม่ตรงกับเฉลย)")
        else:
            print("  4. clean_age: ถูก ✓")

    # ── แจ้งเตือนถ้า dedup ยังไม่ผ่าน ───────────────────────────────────────
    if not dedup_ok:
        print()
        print("  ⚠️  ขั้นตอนที่ 2, 3 และ 4 ต้องทำขั้นตอนที่ 1 (deduplicate) ให้สำเร็จก่อน")
