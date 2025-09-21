import pandas as pd

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

df = pd.read_csv('resources/Building_A_summary_table.csv')
#Data preparation
print( "Initial shape : " + str(df.shape) )

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

#clean NaN
print("Dropping NaN values...")
df.dropna(inplace=True)
print( f'{len(df)} rows after dropna().' ) 
 
df = create_time_features( df, 'record_timestamp')
#clean zeros
print("Dropping Zero values...")
df = df[ ( df['Total_Cooling_Load'] != 0 ) ]
print( f'{len(df)} rows where "Total Cooling Load != 0" .' )


import os
parent = os.path.dirname(__file__)
df.to_csv(os.path.join(parent, 'Building_A.csv'), index=False)