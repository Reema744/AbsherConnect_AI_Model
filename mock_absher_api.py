# mock_absher_api.py

from datetime import date, timedelta
from typing import List, Dict


def _plus_days(days: int) -> str:
    """Return a date string YYYY-MM-DD after `days` from today."""
    today = date.today()
    target = today + timedelta(days=days)
    return target.strftime("%Y-%m-%d")


def get_user_documents(user_id: int) -> List[Dict[str, str]]:
    """
    Mock Absher API: returns a synthetic list of documents for a given user.

    In a real integration, this would call Absher / government APIs.
    """

    if user_id == 1234567890:
        # Example user with an ID expiring soon
        return [
            {
                "document_type": "ID",
                "expiry_date": _plus_days(10),
                "document_importance": "HIGH",
                "has_late_renewal_before": "NO",
            },
            {
                "document_type": "PASSPORT",
                "expiry_date": _plus_days(180),
                "document_importance": "MEDIUM",
                "has_late_renewal_before": "YES",
            },
        ]

    elif user_id == 9999999999:
        # Another user where nothing is urgent
        return [
            {
                "document_type": "ID",
                "expiry_date": _plus_days(120),
                "document_importance": "HIGH",
                "has_late_renewal_before": "NO",
            },
            {
                "document_type": "DRIVER_LICENSE",
                "expiry_date": _plus_days(200),
                "document_importance": "LOW",
                "has_late_renewal_before": "NO",
            },
        ]

    # Default case
    return [
        {
            "document_type": "ID",
            "expiry_date": _plus_days(45),
            "document_importance": "HIGH",
            "has_late_renewal_before": "NO",
        }
    ]
