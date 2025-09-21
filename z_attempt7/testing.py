import joblib
import pandas as pd
import numpy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import weather.utils as utils
parent = os.path.dirname(__file__)
model_path = os.path.join(parent, 'rt_model.joblib')
predictions_path = os.path.join(parent, 'predictions.csv')
df =  pd.read_csv('resources/Result.csv')
season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
}
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
    df['year'] = df[timestamp_col].dt.year  # 0=Monday, 6=Sunday
    df['month'] = df[timestamp_col].dt.month
    df['is_weekend'] = (df[timestamp_col].dt.dayofweek >= 5).astype(int)
    df['season'] = df['month'].map(season_map)
    df = pd.get_dummies(df, columns=['season'])
    season_columns = [col for col in df.columns if col.startswith('season_')]
    if 'season_Winter' not in season_columns:
        df['season_Winter'] = False
    if 'season_Summer' not in season_columns:
        df['season_Summer'] = False
    if 'season_Summer' not in season_columns:
        df['season_Spring'] = False
    if 'season_Summer' not in season_columns:
        df['season_Fall'] = False
        
    df['day_of_month'] = df[timestamp_col].dt.day
    return df

df = create_time_features(df, 'prediction_time')
df = utils.generate_weather_feature(df)
X_test = df[['hour_of_day', 'is_weekend', 'season_Fall', 'season_Spring', 'season_Summer', 'season_Winter']]
loaded_model = joblib.load(model_path)
predictions = numpy.maximum(0., loaded_model.predict(X_test) )
df_res =  pd.read_csv('resources/Result.csv')
df_res['predicted_load'] = predictions
df_res.to_csv(predictions_path, index=False)
