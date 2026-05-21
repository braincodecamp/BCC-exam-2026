import pandas as pd

# ----- ข้อมูลตัวอย่าง -----
example_data = {
    "customer_id": [1, 1, 2, 2, 3, 3, 4, 1],
    "transaction_date": [
        "2024-01-15",
        "2024-01-20",
        "2024-02-05",
        "2024-02-10",
        "2024-02-15",
        "2024-03-01",
        "2024-03-10",
        "2024-03-25"
    ],
    "amount": [100.0, 50.0, 200.0, 75.0, 150.0, 30.0, 500.0, 80.0],
    "category": [
        "Electronics",
        "Food",
        "Electronics",
        "Clothing",
        "Electronics",
        "Food",
        "Electronics",
        "Clothing"
    ],
}

example_df = pd.DataFrame(example_data)
example_df["transaction_date"] = pd.to_datetime(example_df["transaction_date"])

# ----- ฟังก์ชั่นสำหรับตรวจสอบคำตอบ --------
answer_key = {
    'n_unique_customers': 4,
    'top_3_categories': ['Electronics', 'Clothing', 'Food'],
    'pct_outlier_transactions': 12.5,
    'monthly_revenue': {'2024-01': 150.0, '2024-02': 425.0, '2024-03': 610.0},
}

def is_your_answer_correct(your_answer: dict, answer_key: dict) -> bool:
    if not isinstance(your_answer, dict):
        return False

    for k in ("n_unique_customers", "top_3_categories"):
        if your_answer.get(k) != answer_key.get(k):
            return False

    try:
        if abs(float(your_answer.get("pct_outlier_transactions"))
               - answer_key["pct_outlier_transactions"]) >= 0.5:
            return False
    except (TypeError, ValueError):
        return False

    your_answer_mr = your_answer.get("monthly_revenue")
    answer_key_mr = answer_key.get("monthly_revenue", {})
    if not isinstance(your_answer_mr, dict) or set(your_answer_mr.keys()) != set(answer_key_mr.keys()):
        return False
    try:
        for m, v in answer_key_mr.items():
            if abs(float(your_answer_mr[m]) - v) >= 1.0:
                return False
    except (TypeError, ValueError):
        return False

    return True

def check_answer(your_answer: dict) -> str:
    return "ถูก" if is_your_answer_correct(your_answer, answer_key) else "ผิด"
# ------------------------------------