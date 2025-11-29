# generate_dataset.py

from pathlib import Path
import random

import pandas as pd


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "absher_documents_synthetic.csv"


DOCUMENT_TYPES = ["ID", "PASSPORT", "DRIVER_LICENSE", "VEHICLE_REGISTRATION"]
IMPORTANCE_LEVELS = ["HIGH", "MEDIUM", "LOW"]
LATE_RENEWAL_FLAGS = ["YES", "NO"]


def label_rule(document_type: str, days_to_expiry: int, importance: str, has_late: str) -> int:
    """
    Simple heuristic to generate the target label (notify_now).
    Higher score => more likely we send a notification.
    """
    score = 0

    # Very close to expiry
    if days_to_expiry <= 7:
        score += 3
    elif days_to_expiry <= 30:
        score += 2
    elif days_to_expiry <= 60:
        score += 1

    # More important documents get higher weight
    if importance == "HIGH":
        score += 2
    elif importance == "MEDIUM":
        score += 1

    # If user has late renewals, be a bit more aggressive
    if has_late == "YES":
        score += 1

    # Threshold for notification
    return 1 if score >= 3 else 0


def generate_rows(n_samples: int = 1000):
    rows = []

    for _ in range(n_samples):
        document_type = random.choice(DOCUMENT_TYPES)
        days_to_expiry = random.randint(0, 365)
        importance = random.choices(
            IMPORTANCE_LEVELS,
            weights=[0.4, 0.4, 0.2],  # HIGH & MEDIUM more common
            k=1
        )[0]
        has_late = random.choice(LATE_RENEWAL_FLAGS)

        notify_now = label_rule(
            document_type=document_type,
            days_to_expiry=days_to_expiry,
            importance=importance,
            has_late=has_late,
        )

        rows.append(
            {
                "document_type": document_type,
                "days_to_expiry": days_to_expiry,
                "document_importance": importance,
                "has_late_renewal_before": has_late,
                "notify_now": notify_now,
            }
        )

    return rows


def main():
    rows = generate_rows(n_samples=1000)
    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)
    print(f"[DATA] Synthetic dataset saved to {CSV_PATH.resolve()}")
    print(df.head())


if __name__ == "__main__":
    main()
