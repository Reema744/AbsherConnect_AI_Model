# ai_model.py

from pathlib import Path
from typing import List, Dict

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Path to the synthetic dataset
DATA_PATH = Path("data/absher_documents_synthetic.csv")

# Feature names
CATEGORICAL_FEATURES = ["document_type", "document_importance", "has_late_renewal_before"]
NUMERIC_FEATURES = ["days_to_expiry"]

_model = None  # cached model instance


def train_model():
    """
    Train the RandomForest notification model on the synthetic dataset.
    """
    global _model

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            f"Make sure you run generate_dataset.py first."
        )

    df = pd.read_csv(DATA_PATH)

    # Features (X) and target (y)
    X = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = df["notify_now"]

    # Preprocess: One-hot encode categorical features, keep numeric as is
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    # RandomForest model
    rf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    # Full pipeline: preprocessing + model
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", rf),
        ]
    )

    # Split data for a quick validation
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Train the model
    model.fit(X_train, y_train)

    # Optional: print test accuracy to the console
    accuracy = model.score(X_test, y_test)
    print(f"[AI MODEL] Notification model trained. Test accuracy: {accuracy:.3f}")

    _model = model
    return _model


def get_model():
    """
    Return a trained model instance.
    If the model is not trained yet, train it first.
    """
    global _model

    if _model is None:
        _model = train_model()

    return _model


def predict_notify(documents: List[Dict]) -> List[int]:
    """
    Predict whether we should send a notification for each document.

    Each document dict MUST contain:
      - document_type (str)
      - days_to_expiry (int)
      - document_importance (str)
      - has_late_renewal_before (str)
    """
    model = get_model()

    df = pd.DataFrame(documents)

    # Just in case: keep only the expected columns
    df = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]

    preds = model.predict(df)
    return preds.tolist()
