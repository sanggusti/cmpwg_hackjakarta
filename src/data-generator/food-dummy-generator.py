import os
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta

def generate_random_dates(start_date, end_date, num_dates):
    return [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days + 1)) for _ in range(num_dates)]

def process_data(input_file, output_file):
    df = pd.read_csv(input_file)
    unique_merchants = df['merchant_name'].unique()

    print(f"Processing data for {len(unique_merchants)} unique merchants.")
    merchant_id_mapping = {name: f'M{str(i).zfill(3)}' for i, name in enumerate(unique_merchants, start=1)}
    
    start_date = datetime.strptime("2024-07-22", "%Y-%m-%d")
    end_date = datetime.strptime("2024-07-27", "%Y-%m-%d")
    
    print(f"Generating random dates between {start_date} and {end_date}.")
    df['merchant_id'] = df['merchant_name'].map(merchant_id_mapping)
    df['date'] = generate_random_dates(start_date, end_date, len(df))
    
    df.to_csv(output_file, index=False)
    print(f"Data processing complete. File saved as {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process merchant data and assign IDs and random dates.')
    parser.add_argument('--input_file', default= 'food_dataset.csv', type=str, help='Input CSV file with merchant data')
    parser.add_argument('--output_file', type=str, default='food_dataset_v1.csv', help='Output CSV file name')

    args = parser.parse_args()

    # Define paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, '../../data', args.input_file)
    output_file_path = os.path.join(script_dir, '../../data', args.output_file)

    print(f'reading data from {input_file_path}')
    print(f'writing data to {output_file_path}')
    process_data(input_file_path, output_file_path)
