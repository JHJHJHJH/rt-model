
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import joblib
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

# Define the parameter grid to search

# --- Step 1: Load and Prepare Data ---
# Load the data from the CSV file.
try:
    df = pd.read_csv('resources/10_Building_A.csv')
except FileNotFoundError:
    print("Error: File not found in resources folder.")
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

# --- Step 3: Train the Model ---

# Initialize and train the Random Forest Regressor model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# print("Training the model...")
# model.fit(X_train, y_train)
model = xgb.XGBRegressor(
    objective = 'reg:squarederror',  # For regression tasks
    n_estimators = 100,             # Number of boosting rounds (trees)
    learning_rate = 0.05,            # How quickly the model learns
    max_depth = 6,                   # Maximum depth of each tree
    subsample = 0.8,                 # Fraction of samples used per tree
    colsample_bytree = 0.8,          # Fraction of features used per tree
    reg_alpha = 1,                   # L1 regularization (optional)
    reg_lambda = 1,                  # L2 regularization (optional)
    random_state = 42
)
# Initialize Grid Search
param_grid = {
    'max_depth': [6, 8],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [ 900, 1000 , 1200],
    'subsample': [ 0.8, 1.0],
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                           scoring='neg_mean_squared_error', cv=5, verbose=1, n_jobs=-1)

grid_search.fit(X_train, y_train)
print("Best parameters found: ", grid_search.best_params_)


best_model = grid_search.best_estimator_
y_pred_tuned = best_model.predict(X_test)

final_model = xgb.XGBRegressor(
    **grid_search.best_params_,           # Unpack the best_params dictionary
    objective='reg:squarederror',
    random_state=42
)

# 4. Train this new model on the ENTIRE training dataset (X_train, y_train)
final_model.fit(X_train, y_train)

# 5. Make predictions and evaluate
y_pred_final = final_model.predict(X_test)
mse_final = root_mean_squared_error(y_test, y_pred_final)
print(f"Final Model RMSE: {mse_final}")
print("Model training complete.")
xgb.plot_importance(final_model, max_num_features=10) # Show top 10 features
plt.show()
# # --- Step 4: Evaluate the Model ---
# # Make predictions on the test set
# y_pred = model.predict(X_test)
# # --- Step 5: Save the Model ---
# # Save the trained model to a file
model_filename = 'rt_model_10.joblib'
joblib.dump(final_model, model_filename)
print(f"Model saved as {model_filename}")
