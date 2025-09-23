import joblib
import pandas as pd
import numpy
import sys
import os
from datetime import time
import xgboost as xgb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import weather.utils as utils
parent = os.path.dirname(__file__)
model_path_a = os.path.join(parent, 'rt_model_a.joblib')
model_path_b = os.path.join(parent, 'rt_model_b.joblib')
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
    df['minute'] = df[timestamp_col].dt.minute
    start_time = time(7, 30, 0)  # 18:00:00
    end_time = time(18, 0, 0)    # 07:30:00
    #chiller off from 6pm-730am. 18:00 ~ 07:30
    df['is_business_hour'] = df[timestamp_col].apply(
        lambda x: x.time() >= start_time and x.time() <= end_time
    ).astype(int)
    return df

def split_buildings(df):
    df['building'] = df['building_id'].apply(lambda x :  'A' if 'BuildingA' in str(x) else 'B')
    df_a = df[ df['building'] == 'A']
    df_b = df[ df['building'] == 'B']
    
    # print(df_a.tail())
    # print(df_b.head())
    return df_a, df_b

def create_features(df):
    df = create_time_features(df, 'prediction_time')
    df = utils.generate_weather_feature(df)
    df = utils.generate_solar_feature(df)
    df = utils.generate_holiday_feature(df)
    df = utils.generate_rain_feature(df)
    df = utils.generate_workday_feature(df)
    df = utils.generate_wind_feature(df)
    return df

df_a, df_b = split_buildings(df)

#model a
df_a = create_features(df_a)

features =  ['hour_of_day', 'is_business_hour', 'is_workday','season_Fall', 'season_Spring', 'season_Summer', 'season_Winter']
X_test = df_a[features]

loaded_model_a = joblib.load(model_path_a)
dval_a = xgb.DMatrix(X_test, feature_names=features)
predictions_a = numpy.maximum(0., loaded_model_a.predict(dval_a) )
# df_res =  pd.read_csv('resources/Result.csv')
# df_res['predicted_load'] = predictions_a
# df_res.to_csv(predictions_path, index=False)


#model b
df_b = create_features(df_b)

X_test = df_b[features]

loaded_model_b = joblib.load(model_path_b)
dval_b = xgb.DMatrix(X_test, feature_names=features)
predictions_b = numpy.maximum(0., loaded_model_b.predict(dval_b) )

import numpy as np
predictions = np.concatenate( (predictions_a, predictions_b))
df_res =  pd.read_csv('resources/Result.csv')
df_res['predicted_load'] = predictions
df_res.to_csv(predictions_path, index=False)
