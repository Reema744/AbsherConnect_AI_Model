# main.py

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ai_model import predict_notify
from mock_absher_api import get_user_documents
import uvicorn


app = FastAPI(
    title="Absher Connect API",
    description="AI-driven proactive notification service",
    version="1.0"
)


class DocumentItem(BaseModel):
    document_type: str                 # e.g. "ID"
    expiry_date: str                   # "YYYY-MM-DD"
    document_importance: str           # HIGH / MEDIUM / LOW
    has_late_renewal_before: str       # YES / NO


class UserRequest(BaseModel):
    user_id: int
    documents: Optional[List[DocumentItem]] = None


def calculate_days_to_expiry(date_str: str) -> int:
    today = datetime.now().date()
    expiry = datetime.strptime(date_str, "%Y-%m-%d").date()
    delta = (expiry - today).days
    return max(delta, 0)


@app.post("/user-notifications")
def get_notifications(payload: UserRequest):

    if not payload.documents:
        raw_docs = get_user_documents(payload.user_id)
        documents = [DocumentItem(**doc) for doc in raw_docs]
    else:
        documents = payload.documents

    converted_docs = []
    for doc in documents:
        days_to_expiry = calculate_days_to_expiry(doc.expiry_date)

        converted_docs.append({
            "document_type": doc.document_type,
            "days_to_expiry": days_to_expiry,
            "document_importance": doc.document_importance,
            "has_late_renewal_before": doc.has_late_renewal_before
        })

    predictions = predict_notify(converted_docs)

    notifications = []
    for doc, pred in zip(documents, predictions):
        if pred == 1:
            notifications.append({
                "document_type": doc.document_type,
                "message": f"Your {doc.document_type} will expire soon. Would you like to renew it now?",
                "action_url": f"/renew/{doc.document_type.lower()}"
            })

    return {
        "user_id": payload.user_id,
        "notifications": notifications
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
