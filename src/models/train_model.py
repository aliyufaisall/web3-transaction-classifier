import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# Paths
DATA_PATH = os.path.join("data", "processed", "hybrid_training_data.csv")
MODEL_DIR = "models"

def train_optimized_model():
    if not os.path.exists(DATA_PATH):
        print(" Error: Hybrid data not found.")
        return

    # 1. Load and Split
    df = pd.read_csv(DATA_PATH)
    X = df.drop('FLAG', axis=1)
    y = df['FLAG']

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in sss.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # 2. Calculate Scale_Pos_Weight (MLOps Best Practice)
    # This mathematically forces XGBoost to pay more attention to the minority (fraud) class
    num_legit = sum(y_train == 0)
    num_fraud = sum(y_train == 1)
    spw = num_legit / num_fraud
    print(f" Calculated scale_pos_weight: {spw:.2f}")

    # 3. Define the Grid (The "Search Space")
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200],
        'scale_pos_weight': [spw] # Fixed to our calculated weight
    }

    # 4. Initialize GridSearchCV
    # We use 'f1' as the scoring metric because it balances precision and recall
    print(" Searching for the best hyperparameters (this may take a minute)...")
    grid_search = GridSearchCV(
        estimator=xgb.XGBClassifier(eval_metric='logloss', random_state=42),
        param_grid=param_grid,
        scoring='f1',
        cv=3, 
        verbose=1
    )

    # 5. Fit and Find the Best Model
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    print(f"\n Best Parameters Found: {grid_search.best_params_}")

    # 6. Final Evaluation
    y_pred = best_model.predict(X_test)
    
    print("\n---  DETAILED PERFORMANCE (TEST SET) ---")
    print(classification_report(y_test, y_pred, target_names=['Legit', 'Fraud']))
    
    print("---  CONFUSION MATRIX ---")
    print(confusion_matrix(y_test, y_pred))

    # 7. Save the Winning Model
    os.makedirs(MODEL_DIR, exist_ok=True)
    best_model.save_model(os.path.join(MODEL_DIR, "optimized_fraud_model.json"))
    print(f"\n Optimized model saved to {MODEL_DIR}/")

if __name__ == "__main__":
    train_optimized_model()
