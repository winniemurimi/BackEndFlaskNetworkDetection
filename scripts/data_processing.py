import pandas as pd

def load_data(train_file_path, test_file_path):
    # Load training data
    train_data = pd.read_csv(train_file_path)
    
    # Load test data (without label)
    test_data = pd.read_csv(test_file_path)
    
    return train_data, test_data

def split_data(data, target_column):
    # Check if the target_column is present in the data
    if target_column not in data.columns:
        raise KeyError(f"{target_column} not found in DataFrame columns: {data.columns.tolist()}")
    
    # Split features (X) and target (y)
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    return X, y

def prepare_test_data(test_data, drop_columns=None):
    # Drop any unwanted columns
    if drop_columns:
        test_data = test_data.drop(columns=drop_columns)
    else:
        unwanted_columns = ['id', 'label']  # List of columns to drop
        test_data = test_data.drop(columns=[col for col in unwanted_columns if col in test_data.columns])
    
    return test_data