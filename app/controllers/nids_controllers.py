from flask import jsonify, request
from joblib import load
import pandas as pd
import io
import logging

model = load('./models/random_forest_model.joblib')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def predict():
    try:
        data = request.data.decode('utf-8')  # Get raw data from the request
        
        logger.debug(f"Received data:\n{data}")

        if not data:
            return jsonify({"error": "No data received or invalid format"}), 400

        # Read CSV data into a DataFrame
        df = pd.read_csv(io.StringIO(data))
        
        # Log the DataFrame
        logger.debug(f"DataFrame:\n{df}")

        # Check for NaN values
        if df.isnull().values.any():
            logger.debug(f"NaN values found:\n{df[df.isnull().any(axis=1)]}")
            # Fill NaN values with 0 (or another suitable value)
            df.fillna(0, inplace=True)

            # Alternatively, you can drop NaN values:
            # df.dropna(inplace=True)

        # Make predictions
        predictions = model.predict(df)

        # Return predictions
        return jsonify({"predictions": predictions.tolist()})
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)})