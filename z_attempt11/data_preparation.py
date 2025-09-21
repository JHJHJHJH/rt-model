import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import time

import pandas as pd
import weather.utils as utils
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
    df['month'] = df[timestamp_col].dt.month
    df['is_weekend'] = (df[timestamp_col].dt.dayofweek >= 5).astype(int)
    #Attempt 3 features
    df['season'] = df['month'].map(season_map)
    df['day_of_month'] = df[timestamp_col].dt.day
    df['year'] = df[timestamp_col].dt.year
    df['minute'] = df[timestamp_col].dt.minute
    start_time = time(7, 30, 0)  # 18:00:00
    end_time = time(18, 0, 0)    # 07:30:00
    #chiller off from 6pm-730am. 18:00 ~ 07:30
    df['is_business_hour'] = df[timestamp_col].apply(
        lambda x: x.time() >= start_time and x.time() <= end_time
    ).astype(int)
    return df

def calculate_cooling_load(df):
    df = df.copy()
    
    print("Adding 7 columns -\nCHR-01-Q, CHR-02-Q, CHR-03-Q, CHR-04-Q, Total_Cooling_Load, Total_Power_Consumption, Total_COP")
    # 1 watt = 1 joule/second
    # Cp = 4.19 kJ/kg.C
    # Calculate cooling capacity Q (kW) = m (l/s) * Cp (kJ/kg.C) * ΔT (C)
    df['CHR-01-Q'] = df['CHR-01-CHWFWR'] * (df['CHR-01-CHWRWT'] - df['CHR-01-CHWSWT']) * 4.19
    df['CHR-02-Q'] = df['CHR-02-CHWFWR'] * (df['CHR-02-CHWRWT'] - df['CHR-02-CHWSWT']) * 4.19
    df['CHR-03-Q'] = df['CHR-03-CHWFWR'] * (df['CHR-03-CHWRWT'] - df['CHR-03-CHWSWT']) * 4.19
    df['CHR-04-Q'] = df['CHR-04-CHWFWR'] * (df['CHR-04-CHWRWT'] - df['CHR-04-CHWSWT']) * 4.19

    # Total cooling load
    df['Total_Cooling_Load'] = df['CHR-01-Q'] + df['CHR-02-Q'] + df['CHR-03-Q'] + df['CHR-04-Q']
    # Total power consumption  
    df['Total_Power_Consumption'] = df['CHR-01-KW'] + df['CHR-02-KW'] + df['CHR-03-KW'] + df['CHR-04-KW']
    # COP
    df['Total_COP'] = df['Total_Cooling_Load'] / df['Total_Power_Consumption']

    return df

def create_weather_features(df):
    df = df.copy()
    
    df = utils.generate_weather_feature(df)

    df = utils.generate_solar_feature(df)
    return df

def create_holiday_feature(df):
    df = df.copy()
    
    df = utils.generate_holiday_feature(df)
    return df

df = pd.read_csv('resources/Building_A_summary_table.csv')
#Data preparation
print( "Initial shape : " + str(df.shape) )

df = calculate_cooling_load(df)

#clean NaN
print("Dropping NaN values...")
df.dropna(inplace=True)
print( f'{len(df)} rows after dropna().' )
 
df = create_time_features( df, 'record_timestamp')

df = create_weather_features(df)

df = create_holiday_feature(df)

print( "Final shape : " + str(df.shape) )
df.to_csv('resources/11_Building_A.csv', index=False)
