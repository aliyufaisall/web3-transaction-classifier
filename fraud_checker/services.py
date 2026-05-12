import os
import pandas as pd
import xgboost as xgb
from django.conf import settings

class FraudModelService:
    _model = None

    @classmethod
    def load_model(cls):
        """Loads the model only once to save memory (Singleton pattern)."""
        if cls._model is None:
            # Path to the model you saved yesterday
            model_path = os.path.join(settings.BASE_DIR, 'models', 'optimized_fraud_model.json')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            cls._model = xgb.XGBClassifier()
            cls._model.load_model(model_path)
            print("🧠 XGBoost Model Loaded into Django successfully!")
        return cls._model

    @classmethod
    def predict(cls, data_dict):
        """Takes a dictionary of transaction data and returns a prediction."""
        model = cls.load_model()
        
        # Ensure the columns match your training features EXACTLY
        # These names must be the same as 'important_cols' from your merge script
        cols = ['Avg min between sent tnx', 'Sent tnx', 'Received Tnx', 'total Ether sent']
        df = pd.DataFrame([data_dict])[cols]
        
        prediction = model.predict(df)[0]
        # Get the probability (e.g., 0.85 chance of fraud)
        probability = model.predict_proba(df)[0][1] 
        
        return "Fraud" if prediction == 1 else "Legit", round(float(probability), 4)
