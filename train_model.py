
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# --- Step 1: Load and Prepare Data ---
# Load the data from the CSV file.
try:
    df = pd.read_csv('resources/Building_A_summary_table.csv')
except FileNotFoundError:
    print("Error: Building_A_summary_table.csv not found in resources folder.")
    exit()

# Convert the 'record_timestamp' column to datetime objects.
df['record_timestamp'] = pd.to_datetime(df['record_timestamp'], format='%d/%m/%Y %H:%M', errors='coerce')

# Remove any rows that have missing values to ensure data quality.
df.dropna(inplace=True)

# --- Step 2: Feature Selection and Data Splitting ---
# For this example, we'll focus on CHR-01
chiller_id = 'CHR-01'
features = [f'{chiller_id}-CHWFWR', f'{chiller_id}-CHWSWT', f'{chiller_id}-CHWRWT']
target = f'{chiller_id}-KW'

# Check if all required columns are present
required_columns = features + [target]
if not all(col in df.columns for col in required_columns):
    print(f"Error: Not all required columns for {chiller_id} are in the dataframe.")
    exit()

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 3: Train the Model ---
# Initialize and train the Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
print("Training the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- Step 4: Evaluate the Model ---
# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Model Mean Squared Error: {mse:.2f}")

# --- Step 5: Save the Model ---
# Save the trained model to a file
model_filename = 'rt_model.joblib'
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")
