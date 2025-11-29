# Absher Connect – AI Backend

This repository contains the backend AI engine for **Absher Connect**, an AI-powered proactive notification service.

Given a `user_id`, the backend:
1. Fetches the user's government documents from a **Mock Absher API**.
2. Converts expiry dates into `days_to_expiry`.
3. Runs a **Random Forest Classifier** to decide whether to send a proactive renewal notification.
4. Returns a list of notifications ready to be shown in the frontend.

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- scikit-learn (RandomForest)
- pandas / numpy

---

## Setup & Installation

Install dependencies:

```bash
pip install fastapi "uvicorn[standard]" pandas numpy scikit-learn
