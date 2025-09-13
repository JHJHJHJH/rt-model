import pandas as pd

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

print( f'Updated shape : {str(df.shape)}' )

#clean NaN
print("Dropping NaN values...")
df.dropna(inplace=True)
print( f'{len(df)} rows after dropna().' ) 
 
#clean zeros
print("Dropping Zero values...")
df = df[ ( df['Total_Cooling_Load'] != 0 ) ]
print( f'{len(df)} rows where "Total Cooling Load != 0" .' )

# df = df[(df['Total_Cooling_Load'] == 0) | (df['y'] != 0)]
df.to_csv('resources/cleaned_Building_A.csv', index=False)