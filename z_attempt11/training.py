
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import joblib
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import os
# --- Step 1: Load and Prepare Data ---
# Load the data from the CSV file.
try:
    parent = os.path.dirname(__file__)
    data_path=os.path.join(parent, 'Building_A.csv')
    df = pd.read_csv(data_path)
except FileNotFoundError:
    print("Error: Building_A.csv not found in folder.")
    exit()

# --- Step 2: Feature Selection and Data Splitting ---
# For this example, we'll focus on CHR-01
target = 'Total_Cooling_Load'

# One-hot encode the 'season' column
df = pd.get_dummies(df, columns=['season'])
season_columns = [col for col in df.columns if col.startswith('season_')]

features = ['hour_of_day', 'is_weekend', 'is_business_hour','is_holiday','temperature','humidity','solar']
features = features + season_columns

print( features )

# Check if all required columns are present
required_columns = features + [target]
if not all(col in df.columns for col in required_columns):
    print(f"Error: Not all required columns are in the dataframe.")
    exit()

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_test, label=y_test)

evals = [(dtrain, 'train'), (dval, 'val')]
# --- Step 3: Train the Model ---

params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'max_depth': 4,           # Much shallower trees
    'learning_rate': 0.05,    # Moderate learning rate
    'subsample': 0.8,         # Randomly sample 80% of data for each tree
    'colsample_bytree': 0.8,  # Randomly sample 80% of features for each tree
    'reg_lambda': 1,          # L2 regularization
    'n_estimators': 1000      # Let early stopping find the best number
}

model = xgb.train(
    params,
    dtrain,
    num_boost_round=10000,  # Set a very high number
    evals=evals,
    early_stopping_rounds=50, # Stop after 50 rounds without improvement on VALIDATION set
    verbose_eval=50
)

fig, ax = plt.subplots(figsize=(10, 12))
xgb.plot_importance(model, importance_type='weight', ax=ax) # 'weight' is the number of times a feature is used
plt.show()

model_filename = os.path.join(parent, 'rt_model.joblib')
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")
