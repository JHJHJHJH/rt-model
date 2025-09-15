import joblib
import pandas as pd

df =  pd.read_csv('resources/Result.csv')

def create_time_features(df, timestamp_col):
    """
    Create basic time-based features from timestamp
    """
    df = df.copy()
    
    # Convert to datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], format='%d/%m/%Y %H:%M')
    
    # Extract features
    df['hour_of_day'] = df[timestamp_col].dt.hour
    df['day_of_week'] = df[timestamp_col].dt.dayofweek  # 0=Monday, 6=Sunday
    df['month'] = df[timestamp_col].dt.month
    df['is_weekend'] = (df[timestamp_col].dt.dayofweek >= 5).astype(int)
    
    return df

df = create_time_features(df, 'prediction_time')
X_test = df[['hour_of_day', 'day_of_week', 'month', 'is_weekend']]
loaded_model = joblib.load('rt_model_2.joblib')
predictions = loaded_model.predict(X_test)

df_res =  pd.read_csv('resources/Result.csv')
df_res['predicted_load'] = predictions
df_res.to_csv('resources/2_predictions.csv',index=False)
