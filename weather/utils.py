import pandas as pd
import matplotlib.pyplot as plt

def extract_weather( station_name='Hong Kong Park', timestamp_col='datetime'):
    df = pd.read_csv('./weather/data/daily_weather.csv')

    df = df.copy()
    df = df.drop('source_zip', axis=1)
    df = df.drop('source_xml', axis=1)
    df = df[ ( df['station_name'] == station_name  ) ]
    
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

def extract_holiday():
    df = pd.read_csv('./weather/data/hkholidays.csv')

    df = df.copy()
    df = df.drop('uid', axis=1)
    df = df.drop('summary', axis=1)
    df['start_date'] = pd.to_datetime(df['start_date'], format='%Y%m%d')
    df['month'] = df['start_date'].dt.month
    df['day_of_month'] = df['start_date'].dt.day
    df['year'] = df['start_date'].dt.year

    df['end_date'] = pd.to_datetime(df['end_date'], format='%Y%m%d')
    df['days'] = df['end_date'] - df['start_date'] #to confirm no holiday more than 1 day
    df['is_holiday'] = 1
    #df.to_csv('resources/hol.csv', index=False)
    return df


def plot_temp(df):
    df['datetime'] = pd.to_datetime(df['datetime'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df['temperature'])
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title('Temperature vs Date')
    plt.grid(True)
    plt.savefig('temperature_vs_date.png')
    plt.show()

def merge_df(df1, df2, columns):
    merged_df = pd.merge( df1, df2 , on=columns, how='left')
    print(merged_df.head())

    return merged_df

def generate_weather_feature(df):
    weather_df = extract_weather()
    return merge_df(df, weather_df, ['hour_of_day', 'month', 'year', 'day_of_month'])


def generate_holiday_feature(df):
    holiday_df = extract_holiday()
    return merge_df(df, holiday_df, ['month', 'year', 'day_of_month'])
