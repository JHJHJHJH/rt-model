import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load and Prepare Data ---
# Load the data from the CSV file.
try:
    df = pd.read_csv('resources/Building_A_summary_table.csv')
except FileNotFoundError:
    print("Error: Building_A_summary_table.csv not found in resources folder.")
    exit()

# Convert the 'record_timestamp' column to datetime objects for time series analysis.
df['record_timestamp'] = pd.to_datetime(df['record_timestamp'], format='%d/%m/%Y %H:%M', errors='coerce')

# Set the timestamp as the index for plotting against time.
df.set_index('record_timestamp', inplace=True)

# Remove any rows that have missing values to ensure data quality.
df.dropna(inplace=True)

# --- Step 2: Loop Through Chillers to Generate Plots ---
chiller_ids = ['CHR-01', 'CHR-02', 'CHR-03', 'CHR-04']

for chiller_id in chiller_ids:
    kw_col = f'{chiller_id}-KW'
    flow_col = f'{chiller_id}-CHWFWR'

    # Check if the required columns exist in the DataFrame.
    if kw_col not in df.columns or flow_col not in df.columns:
        print(f"Warning: Columns for {chiller_id} not found. Skipping this chiller.")
        continue

    # Create a new DataFrame with only the power and flow rate columns for the selected chiller.
    chiller_df = df[[kw_col, flow_col]].copy()

    # Normalize both columns using Min-Max scaling.
    chiller_df[kw_col] = (chiller_df[kw_col] - chiller_df[kw_col].min()) / (chiller_df[kw_col].max() - chiller_df[kw_col].min())
    chiller_df[flow_col] = (chiller_df[flow_col] - chiller_df[flow_col].min()) / (chiller_df[flow_col].max() - chiller_df[flow_col].min())

    # --- Step 3: Plot the Overlayed Time Series for Each Chiller ---
    plt.figure(figsize=(15, 7))

    plt.plot(chiller_df.index, chiller_df[kw_col], label=f'Normalized {kw_col}')
    plt.plot(chiller_df.index, chiller_df[flow_col], label=f'Normalized {flow_col}', linestyle='--')

    # Set the title and labels for clarity.
    plt.title(f'Normalized Power and Flow Rate Over Time for {chiller_id}')
    plt.xlabel('Time')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file.
    output_filename = f'{chiller_id}_power_and_flowrate_over_time.png'
    plt.savefig(output_filename)
    plt.close() # Close the figure to free up memory

    print(f"Plot for {chiller_id} saved as {output_filename}")

print("\nAll analyses complete.")