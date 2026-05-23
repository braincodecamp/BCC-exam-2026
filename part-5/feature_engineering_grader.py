import numpy as np
import pandas as pd

# ----- ข้อมูลตัวอย่าง -----
example_data = {
    "transaction_id": [1, 2, 3, 4, 5, 6],
    "customer_id": [10, 20, 10, 20, 10, 30],
    "timestamp": pd.to_datetime(
        [
            "2024-01-05 09:30:00",
            "2024-01-05 14:15:00",
            "2024-01-10 22:00:00",
            "2024-01-12 08:45:00",
            "2024-02-01 19:30:00",
            "2024-02-03 03:00:00",
        ]
    ),
    "category": [
        "Electronics",
        "Clothing",
        "Electronics",
        "Clothing",
        "Electronics",
        "Clothing",
    ],
    "original_price": [300.0, 100.0, 200.0, 80.0, 400.0, 60.0],
    "amount": [240.0, 80.0, 180.0, 60.0, 360.0, 45.0],
}

example_df = pd.DataFrame(example_data)

# ----- ฟังก์ชั่นสำหรับตรวจสอบคำตอบ --------
answer_key = pd.DataFrame(
    {
        "transaction_id": [1, 2, 3, 4, 5, 6],
        "customer_id": [10, 20, 10, 20, 10, 30],
        "timestamp": pd.to_datetime(
            [
                "2024-01-05 09:30:00",
                "2024-01-05 14:15:00",
                "2024-01-10 22:00:00",
                "2024-01-12 08:45:00",
                "2024-02-01 19:30:00",
                "2024-02-03 03:00:00",
            ]
        ),
        "category": [
            "Electronics",
            "Clothing",
            "Electronics",
            "Clothing",
            "Electronics",
            "Clothing",
        ],
        "original_price": [300.0, 100.0, 200.0, 80.0, 400.0, 60.0],
        "amount": [240.0, 80.0, 180.0, 60.0, 360.0, 45.0],
        "time_of_day": [
            "morning",
            "afternoon",
            "night",
            "morning",
            "evening",
            "night",
        ],
        "days_since_first_purchase": [
            0.0,
            0.0,
            5.520833333,
            6.770833333,
            27.416666667,
            0.0,
        ],
        "customer_avg_spend_prior": [np.nan, np.nan, 240.0, 80.0, 210.0, np.nan],
        "discount_pct": [20.0, 20.0, 10.0, 25.0, 10.0, 25.0],
    }
)

REQUIRED_INPUT_COLS = [
    "transaction_id",
    "customer_id",
    "timestamp",
    "category",
    "original_price",
    "amount",
]
NEW_COLS = [
    "time_of_day",
    "days_since_first_purchase",
    "customer_avg_spend_prior",
    "discount_pct",
]
FLOAT_COLS = [
    "days_since_first_purchase",
    "discount_pct",
]


# Per-column absolute tolerance for float comparisons
FLOAT_TOLERANCES = {
    "days_since_first_purchase": 0.01,
    "customer_avg_spend_prior": 0.01,
    "discount_pct": 1.0,
}


def is_your_answer_correct(your_answer, answer_key: pd.DataFrame) -> bool:
    if not isinstance(your_answer, pd.DataFrame):
        return False
    for col in REQUIRED_INPUT_COLS + NEW_COLS:
        if col not in your_answer.columns:
            return False
    try:
        a = your_answer.sort_values("transaction_id").reset_index(drop=True)
        e = answer_key.sort_values("transaction_id").reset_index(drop=True)

        # time_of_day — string ต้องตรงเป๊ะ
        if not (a["time_of_day"].astype(str) == e["time_of_day"]).all():
            return False

        # ค่าตัวเลขที่ไม่มี NaN — คลาดเคลื่อนได้ตาม tolerance ของแต่ละคอลัมน์
        for col in FLOAT_COLS:
            if not np.allclose(
                a[col].astype(float).values,
                e[col].values,
                atol=FLOAT_TOLERANCES[col],
                equal_nan=False,
            ):
                return False

        # customer_avg_spend_prior — ตำแหน่ง NaN ต้องตรง และค่าที่ไม่ใช่ NaN คลาดเคลื่อนได้ไม่เกิน ±0.01
        a_vals = a["customer_avg_spend_prior"].astype(float).values
        e_vals = e["customer_avg_spend_prior"].values
        if not (pd.isna(a_vals) == pd.isna(e_vals)).all():
            return False
        mask = ~pd.isna(e_vals)
        if not np.allclose(
            a_vals[mask],
            e_vals[mask],
            atol=FLOAT_TOLERANCES["customer_avg_spend_prior"],
        ):
            return False

        return True
    except (AssertionError, KeyError, TypeError, ValueError):
        return False


def check_answer(your_answer) -> str:
    return "ถูก" if is_your_answer_correct(your_answer, answer_key) else "ผิด"
# ------------------------------------
