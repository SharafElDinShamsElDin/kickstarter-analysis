"""Utility functions for training and serving the Kickstarter success model.

Author: Mohamed SharafEldin
Academic number: 202201849
Academic email: 12422021653750@pg.cu.edu.eg

Under Supervision of:
    - Dr. Tarek Ali, Faculty of Graduate Studies for Statistical Research
    - Prof. Mervat Gheith, Faculty of Graduate Studies for Statistical Research

The module reorganizes the original notebook-style workflow into reusable
functions that can be called from an Excel plugin or any other client. It
includes helpers to train the TensorFlow model, persist the preprocessing
and run predictions for a single campaign instance.
"""

import argparse
import json
import pickle
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
import tensorflow as tf


UNNEEDED_COLUMNS = ["ID", "name"]
CATEGORICAL_COLUMNS = ["category", "main_category", "currency", "country"]


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw Kickstarter dataframe.

    Args:
        df: Raw dataframe loaded from the CSV file.

    Returns:
        A dataframe with unused columns removed, outcome encoded as 0/1,
        dates expanded into year/month/day components, and categorical
        values ready for one-hot encoding.
    """

    normalized = df.copy()
    normalized = normalized.drop(columns=[col for col in UNNEEDED_COLUMNS if col in normalized.columns], errors="ignore")

    # Replace missing pledged values with the mean to keep the numerical scale stable.
    if "usd pledged" in normalized.columns:
        normalized["usd pledged"] = normalized["usd pledged"].fillna(normalized["usd pledged"].mean())

    # Limit labels to the binary outcomes the model understands.
    if "state" in normalized.columns:
        normalized = normalized[normalized["state"].isin(["failed", "successful"])]
        normalized["state"] = normalized["state"].map({"successful": 1, "failed": 0})

    # Convert dates to structured components for the neural network.
    for column in ["deadline", "launched"]:
        if column in normalized.columns:
            normalized[column] = pd.to_datetime(normalized[column], errors="coerce")
            normalized[f"{column}_year"] = normalized[column].dt.year
            normalized[f"{column}_month"] = normalized[column].dt.month
            normalized[f"{column}_day"] = normalized[column].dt.day
            normalized = normalized.drop(columns=[column])

    return normalized.reset_index(drop=True)


def preprocess_features(
    df: pd.DataFrame, *, feature_columns: Optional[Iterable[str]] = None
) -> Tuple[pd.DataFrame, Optional[pd.Series], List[str]]:
    """Prepare model-ready features.

    Args:
        df: Input dataframe.
        feature_columns: Optional ordered list of feature column names. When
            provided, the returned dataframe will contain exactly this set of
            columns (missing values are filled with zeros) to keep inference
            aligned with training.

    Returns:
        features: Numerical dataframe ready for scaling.
        labels: Binary labels if available, otherwise ``None``.
        used_feature_columns: The ordered list of feature columns used to
            construct the features matrix.
    """

    normalized = _normalize_dataframe(df)
    labels = normalized["state"] if "state" in normalized.columns else None
    if "state" in normalized.columns:
        normalized = normalized.drop(columns=["state"])

    categorical = [col for col in CATEGORICAL_COLUMNS if col in normalized.columns]
    encoded = pd.get_dummies(normalized, columns=categorical, drop_first=False)

    if feature_columns is None:
        used_columns = list(encoded.columns)
        features = encoded
    else:
        used_columns = list(feature_columns)
        missing_columns = [col for col in used_columns if col not in encoded.columns]
        for column in missing_columns:
            encoded[column] = 0
        features = encoded[used_columns]

    return features, labels, used_columns


def build_model(input_dim: int) -> tf.keras.Model:
    """Create a small feedforward neural network for binary classification."""

    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(128, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
    )
    return model


def train_model(
    csv_path: Path,
    *,
    batch_size: int = 64,
    epochs: int = 50,
    validation_split: float = 0.2,
) -> Tuple[tf.keras.Model, StandardScaler, List[str], Dict[str, float]]:
    """Train the Kickstarter classifier and report evaluation metrics."""

    data = pd.read_csv(csv_path)
    features, labels, feature_columns = preprocess_features(data)

    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, train_size=0.7, random_state=34, stratify=labels
    )

    weights = class_weight.compute_class_weight(
        class_weight="balanced", classes=np.unique(y_train), y=y_train
    )
    class_weights = dict(enumerate(weights))

    model = build_model(X_train.shape[1])
    history = model.fit(
        X_train,
        y_train,
        validation_split=validation_split,
        class_weight=class_weights,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=3, restore_best_weights=True, verbose=1
            )
        ],
        verbose=2,
    )

    evaluation = model.evaluate(X_test, y_test, verbose=0)
    metric_names = model.metrics_names
    metrics = {name: float(value) for name, value in zip(metric_names, evaluation)}

    return model, scaler, feature_columns, metrics


def save_artifacts(
    model: tf.keras.Model,
    scaler: StandardScaler,
    feature_columns: Iterable[str],
    output_dir: Path,
) -> None:
    """Persist the trained model and preprocessing assets to disk."""

    output_dir.mkdir(parents=True, exist_ok=True)
    model.save(output_dir / "kickstarter_model.keras")

    with open(output_dir / "scaler.pkl", "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)

    with open(output_dir / "feature_columns.json", "w", encoding="utf-8") as features_file:
        json.dump(list(feature_columns), features_file, indent=2)


def load_artifacts(model_dir: Path) -> Tuple[tf.keras.Model, StandardScaler, List[str]]:
    """Load a previously trained model and preprocessing assets."""

    model = tf.keras.models.load_model(model_dir / "kickstarter_model.keras")
    with open(model_dir / "scaler.pkl", "rb") as scaler_file:
        scaler: StandardScaler = pickle.load(scaler_file)
    with open(model_dir / "feature_columns.json", "r", encoding="utf-8") as features_file:
        feature_columns: List[str] = json.load(features_file)
    return model, scaler, feature_columns


def predict_success_probability(
    campaign_data: Dict[str, object],
    model: tf.keras.Model,
    scaler: StandardScaler,
    feature_columns: Iterable[str],
) -> float:
    """Predict the success probability for a single campaign.

    Args:
        campaign_data: Dictionary representing a single Kickstarter campaign.
        model: Trained TensorFlow model.
        scaler: StandardScaler fitted on the training data.
        feature_columns: Ordered list of training feature columns.

    Returns:
        Probability that the campaign will be successful.
    """

    campaign_df = pd.DataFrame([campaign_data])
    features, _, _ = preprocess_features(campaign_df, feature_columns=feature_columns)
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features, verbose=0)[0][0]
    return float(prediction)


def _cli_train(args: argparse.Namespace) -> None:
    model, scaler, feature_columns, metrics = train_model(
        Path(args.csv), batch_size=args.batch_size, epochs=args.epochs
    )
    save_artifacts(model, scaler, feature_columns, Path(args.output_dir))

    print("Training complete. Metrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")


def _cli_predict(args: argparse.Namespace) -> None:
    model, scaler, feature_columns = load_artifacts(Path(args.model_dir))
    with open(args.json_path, "r", encoding="utf-8") as file:
        campaign_data = json.load(file)

    probability = predict_success_probability(
        campaign_data, model=model, scaler=scaler, feature_columns=feature_columns
    )
    print(f"Predicted success probability: {probability:.4f}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kickstarter success model utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train a new model")
    train_parser.add_argument("--csv", required=True, help="Path to the Kickstarter dataset CSV")
    train_parser.add_argument(
        "--output-dir", default="artifacts", help="Directory to store the trained model and preprocessors"
    )
    train_parser.add_argument("--batch-size", type=int, default=64)
    train_parser.add_argument("--epochs", type=int, default=50)
    train_parser.set_defaults(func=_cli_train)

    predict_parser = subparsers.add_parser("predict", help="Predict for a single campaign")
    predict_parser.add_argument("--model-dir", default="artifacts", help="Directory containing saved artifacts")
    predict_parser.add_argument("--json-path", required=True, help="Path to a JSON file describing the campaign")
    predict_parser.set_defaults(func=_cli_predict)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
