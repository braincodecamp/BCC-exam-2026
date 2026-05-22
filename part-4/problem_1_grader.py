import inspect
import pandas as pd

# ── ข้อมูลตัวอย่าง ──────────────────────────────────────────────────────────
_example_data = {
    "customer_id": [1, 1, 2, 2, 3, 3, 4, 1],
    "transaction_date": [
        "2024-01-15", "2024-01-20", "2024-02-05", "2024-02-10",
        "2024-02-15", "2024-03-01", "2024-03-10", "2024-03-25",
    ],
    "amount": [100.0, 50.0, 200.0, 75.0, 150.0, 30.0, 500.0, 80.0],
    "category": [
        "Electronics", "Food", "Electronics", "Clothing",
        "Electronics", "Food", "Electronics", "Clothing",
    ],
}
example_df = pd.DataFrame(_example_data)
example_df["transaction_date"] = pd.to_datetime(example_df["transaction_date"])

# ── คำตอบที่ถูกต้องสำหรับข้อมูลตัวอย่าง ────────────────────────────────────
answer_key = {
    "compute_n_unique_customers":       4,
    "compute_top_3_categories":         ["Electronics", "Clothing", "Food"],
    "compute_pct_outlier_transactions": 12.5,
    "compute_monthly_revenue":          {"2024-01": 150.0, "2024-02": 425.0, "2024-03": 610.0},
}

# ── ฟังก์ชันตรวจคำตอบ ────────────────────────────────────────────────────────
_EXPECTED_NAMES = [
    "compute_n_unique_customers",
    "compute_top_3_categories",
    "compute_pct_outlier_transactions",
    "compute_monthly_revenue",
]


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

    # ── ตรวจคำตอบแต่ละฟังก์ชัน ──────────────────────────────────────────────
    print("ผลการตรวจคำตอบ:")
    for name in _EXPECTED_NAMES:
        if name in bad_names:
            print(f"  {name}: ⚠️  ไม่พบฟังก์ชัน")
            continue

        func = caller_globals[name]
        expected = answer_key[name]

        try:
            result = func(example_df.copy())

            if name == "compute_n_unique_customers":
                ok = result == expected
            elif name == "compute_top_3_categories":
                ok = isinstance(result, (list, tuple)) and list(result) == expected
            elif name == "compute_pct_outlier_transactions":
                ok = (result is not None
                      and not isinstance(result, bool)
                      and abs(float(result) - expected) < 0.5)
            elif name == "compute_monthly_revenue":
                ok = (isinstance(result, dict)
                      and set(result.keys()) == set(expected.keys())
                      and all(abs(float(result[k]) - expected[k]) < 1.0
                              for k in expected))

            status = "ถูก ✓" if ok else f"ผิด ✗  (คำตอบคุณ: {result!r}, คำตอบที่ถูกต้อง: {expected!r})"

        except Exception as e:
            status = f"ERROR: {e}"

        print(f"  {name}: {status}")
