import numpy as np
import pandas as pd

# ----- ข้อมูลตัวอย่าง -----
example_data = {
    "employee_id": [1, 2, 3, 4, 5, 1],
    "salary": [
        "$70,000",
        "$55,000",
        np.nan,
        "N/A",
        "$90,000",
        "$70,000",
    ],
    "age": [34.0, 28.0, 200.0, 45.0, -5.0, 34.0],
    "country": [
        "USA",
        "usa",
        "United Kingdom",
        "U.K.",
        "Germany",
        "USA",
    ],
}

example_df = pd.DataFrame(example_data)

# ----- ฟังก์ชั่นสำหรับตรวจสอบคำตอบ --------
answer_key = {
    "employee_id": [1, 2, 3, 4, 5],
    "salary": [70000.0, 55000.0, 70000.0, 70000.0, 90000.0],
    "age": [34.0, 28.0, 34.0, 45.0, 34.0],
    "country": [
        "United States",
        "United States",
        "United Kingdom",
        "United Kingdom",
        "Germany",
    ],
}
answer_key = pd.DataFrame(answer_key)

def is_your_answer_correct(your_answer, answer_key: pd.DataFrame) -> bool:
    if not isinstance(your_answer, pd.DataFrame):
        return False
    if set(your_answer.columns) != set(answer_key.columns):
        return False
    try:
        a = (
            your_answer[answer_key.columns]
            .sort_values("employee_id")
            .reset_index(drop=True)
        )
        e = answer_key.sort_values("employee_id").reset_index(drop=True)
        pd.testing.assert_frame_equal(a, e, check_dtype=False)
        return True
    except (AssertionError, KeyError, TypeError):
        return False


def check_answer(your_answer) -> str:
    return "ถูก" if is_your_answer_correct(your_answer, answer_key) else "ผิด"
# ------------------------------------