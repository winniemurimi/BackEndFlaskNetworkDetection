import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from pathlib import Path
from scripts.data_processing import load_data, split_data
from scripts.train_model import train_and_save_model

def main():
    base_path = Path(__file__).parent
    train_file_path = base_path / 'data' / 'UNSW_NB15_training-set.csv'
    
    target_column = 'attack_cat'

    # Call train_and_evaluate_model directly with file paths and target column
    train_and_save_model(train_file_path, target_column)

if __name__ == "__main__":
    main()
