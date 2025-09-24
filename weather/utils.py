import pandas as pd
import matplotlib.pyplot as plt

def extract_weather( station_name='Hong Kong Park', timestamp_col='datetime'):
    df = pd.read_csv('./weather/data/daily_weather.csv')

    df = df.copy()
    df = df.drop('source_zip', axis=1)
    df = df.drop('source_xml', axis=1)
    df = df[ ( df['station_name'] == station_name  ) ]
    df = df.drop('station_name', axis=1)
    # Convert to datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], format='%Y-%m-%d %H:%M:%S')
    
    # Extract features
    df['hour_of_day'] = df[timestamp_col].dt.hour
    df['month'] = df[timestamp_col].dt.month
    df['day_of_month'] = df[timestamp_col].dt.day
    df['year'] = df[timestamp_col].dt.year
    df = df.drop('datetime', axis=1)
    #df.to_csv('resources/weather1.csv', index=False)
    
    return df

def extract_weather_interpolated( station_name='Hong Kong Park', timestamp_col='datetime'):
    df = pd.read_csv('./weather/data/daily_weather.csv')

    df = df.copy()
    df = df.drop('source_zip', axis=1)
    df = df.drop('source_xml', axis=1)
    df = df[ ( df['station_name'] == station_name  ) ]
    df = df.drop('station_name', axis=1)
    # Convert to datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], format='%Y-%m-%d %H:%M:%S')
    df[timestamp_col] = df[timestamp_col] - pd.Timedelta(minutes=2)
    df = df.drop_duplicates(subset=[timestamp_col])

    df_15min = df.set_index(timestamp_col).resample('15T').asfreq()
    print(df_15min.head())
    df_15min['temperature'] = df_15min['temperature'].interpolate(method='linear')
    df_15min['humidity'] = df_15min['humidity'].interpolate(method='linear')
    print(df_15min.head())
    df_15min = df_15min.reset_index()
 
    # Extract features
    df_15min['hour_of_day'] = df_15min[timestamp_col].dt.hour
    df_15min['minute'] = df_15min[timestamp_col].dt.minute
    df_15min['month'] = df_15min[timestamp_col].dt.month
    df_15min['day_of_month'] = df_15min[timestamp_col].dt.day
    df_15min['year'] = df_15min[timestamp_col].dt.year
    df_15min = df_15min.drop('datetime', axis=1)
    # df_15min.to_csv('resources/weatherzxc.csv', index=False)
    return df_15min

def extract_holiday():
    df = pd.read_csv('./weather/data/hkholidays.csv')

    df = df.copy()
    df = df.drop('uid', axis=1)
    df = df.drop('summary', axis=1)
    df['start_date'] = pd.to_datetime(df['start_date'], format='%Y%m%d')
    df['month'] = df['start_date'].dt.month
    df['day_of_month'] = df['start_date'].dt.day
    df['year'] = df['start_date'].dt.year
    df = df.drop('start_date', axis=1)
    df = df.drop('end_date', axis=1)
    # df['end_date'] = pd.to_datetime(df['end_date'], format='%Y%m%d')
    # df['days'] = df['end_date'] - df['start_date'] #to confirm no holiday more than 1 day
    df['is_holiday'] = 1
    #df.to_csv('resources/hol.csv', index=False)
    return df

def extract_solar():
    df = pd.read_csv('./weather/data/daily_KP_SolarRadiation_ALL.csv')

    df = df.copy()
    df = df.drop('數據完整性/data Completeness', axis=1) #checked all required data are 'C'

    df = df.rename(columns={'年/Year': 'year', '月/Month': 'month', '日/Day' : 'day_of_month' , '數值/Value': 'solar'})

    #df.to_csv('resources/solar.csv', index=False)
    return df

def extract_wind():
    df = pd.read_csv('./weather/data/daily_KP_WindSpeed_ALL.csv')

    df = df.copy()
    df = df.drop('數據完整性/data Completeness', axis=1) #checked all required data are 'C'

    df = df.rename(columns={'年/Year': 'year', '月/Month': 'month', '日/Day' : 'day_of_month' , '數值/Value': 'wind'})
    df['wind'] = pd.to_numeric(df['wind'], errors='coerce').fillna(0)

    #df.to_csv('resources/solar.csv', index=False)
    return df

def extract_rain():
    df = pd.read_csv('./weather/data/daily_KP_Rainfall_ALL.csv')

    df = df.copy()
    df = df.drop('數據完整性/data Completeness', axis=1) #checked all required data are 'C'

    df = df.rename(columns={'年/Year': 'year', '月/Month': 'month', '日/Day' : 'day_of_month' , '數值/Value': 'rain'})
    df['rain'] = pd.to_numeric(df['rain'], errors='coerce').fillna(0)

    #df.to_csv('resources/solar.csv', index=False)
    return df

def merge_df(df1, df2, columns):
    merged_df = pd.merge( df1, df2 , on=columns, how='left').fillna(0)
    print(merged_df.head())

    return merged_df

def generate_weather_feature(df):
    weather_df = extract_weather()
    return merge_df(df, weather_df, ['hour_of_day', 'month', 'year', 'day_of_month'])

def generate_weather_feature_interpolated(df):
    weather_df = extract_weather_interpolated()
    return merge_df(df, weather_df, ['hour_of_day', 'month', 'year', 'day_of_month','minute'])


def generate_holiday_feature(df):
    holiday_df = extract_holiday()
    return merge_df(df, holiday_df, ['month', 'year', 'day_of_month'])

def generate_solar_feature(df):
    solar_df = extract_solar()

    merged = merge_df(df, solar_df, ['month', 'year', 'day_of_month'])
    return merged


def generate_wind_feature(df):
    solar_df = extract_wind()

    merged = merge_df(df, solar_df, ['month', 'year', 'day_of_month'])
    return merged


def generate_rain_feature(df):
    solar_df = extract_rain()

    merged = merge_df(df, solar_df, ['month', 'year', 'day_of_month'])
    return merged

def generate_holiday_feature(df):
    holiday_df = extract_holiday()
    return merge_df(df, holiday_df, ['month', 'year', 'day_of_month'])

def generate_workday_feature(df):
    df['is_workday']= ((df['is_weekend'] == 0) & (df['is_holiday'] == 0)).astype(int)
    return df


def generate_weather_lag_features(df):
    # Define the lag periods you want to test (in hours)
    lags = [1, 2, 3, 4, 6] # e.g., 1 hour ago, 2 hours ago, etc.
    
    # Create lagged features for temperature and solar radiation
    for lag in lags:
        shift_ind = lag * 4 
        df[f'temperature_lag_{lag}'] = df['temperature'].shift(shift_ind)
        df[f'temperature_lag_{lag}'] = df[f'temperature_lag_{lag}'] .where( (df['is_business_hour'] == 1) | (df['is_workday'] == 0)  , 0)
        # df[f'solar_radiation_lag_{lag}'] = df['solar_radiation'].shift(lag)

    df = df.fillna( df['temperature'].iloc[0])
    # df.dropna(inplace=True)

    return df