import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from pathlib import Path

def load_data(file_path):
    # Load dataset
    return pd.read_csv(file_path)

def train_and_save_model(train_file_path, target_column):
    # Load data
    data = load_data(train_file_path)

    # Drop unwanted columns
    unwanted_columns = ['id', 'label']  # Add any other columns you want to drop
    data = data.drop(columns=[col for col in unwanted_columns if col in data.columns])

    # Split features (X) and target (y)
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Identify categorical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=['object']).columns.tolist()

    # Preprocessor with Imputer for numeric features and OneHotEncoder for categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), numeric_cols),  # Imputer for numeric features
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)  # OneHotEncoder for categorical features
        ]
    )

    # Create a pipeline with preprocessor and classifier
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the model
    models_dir = Path(__file__).parent.parent / 'models'
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(pipeline, os.path.join(models_dir, 'random_forest_model.joblib'))
    print(f"Model saved to {models_dir / 'random_forest_model.joblib'}")

if __name__ == "__main__":
    train_file_path = 'data/UNSW_NB15_training-set.csv'  # Update to your actual path
    target_column = 'attack_cat'
    train_and_save_model(train_file_path, target_column)
