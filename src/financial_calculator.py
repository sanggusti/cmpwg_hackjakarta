import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import os

def process_data(input_file):
    df = pd.read_csv(input_file)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    weekly_data = df.groupby('merchant_id').resample('W').agg({
        'product': lambda x: ', '.join(x),  # Concatenate products for most and least ordered calculation
        'price': 'sum',
        'discount_price': 'sum',
        'isDiscount': 'sum',
        'merchant_name': 'first',
        'merchant_area': 'first',
        'category': 'first',
        'display': 'first',
        'description': 'first',
    }).reset_index()

    weekly_data['total_orders'] = df.groupby('merchant_id').resample('W').size().values
    
    weekly_data['total_revenue'] = weekly_data['price'] - weekly_data['discount_price']
    weekly_data['average_discount'] = weekly_data['discount_price'] / weekly_data['price'].replace(0, np.nan)

    most_least_ordered = df.groupby('merchant_id').resample('W').apply(lambda x: pd.Series({
        'most_ordered_item': x['product'].value_counts().idxmax() if not x['product'].empty else None,
        'least_ordered_item': x['product'].value_counts().idxmin() if not x['product'].empty else None
    })).reset_index()

    weekly_data = pd.merge(weekly_data, most_least_ordered[['merchant_id', 'date', 'most_ordered_item', 'least_ordered_item']], on=['merchant_id', 'date'])

    weekly_data.rename(columns={
        'price': 'weekly_total_price',
        'discount_price': 'weekly_total_discount_price',
        'isDiscount': 'weekly_total_discounts',
        'merchant_name': 'merchant_name',
        'merchant_area': 'merchant_area',
        'category': 'category',
        'display': 'display',
        'description': 'description'
    }, inplace=True)


    # from df data, aggregate the most ordered item for each category
    most_ordered_item = df.groupby('category').apply(lambda x: x['product'].value_counts().idxmax()).reset_index()

    # merge the most ordered item to the weekly_data based on category
    weekly_data = pd.merge(weekly_data, most_ordered_item, left_on='category', right_on='category', how='left')
    weekly_data.rename(columns={0: 'most_ordered_item_category'}, inplace=True)
    

    # Save the processed data to a new CSV file
    # weekly_data.to_csv(output_file, index=False)
    # print(f"Weekly metrics processing complete. File saved as {output_file}.")
    return weekly_data

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Generate weekly metrics for merchant report including most and least ordered items.')
#     parser.add_argument('--input_file', default= 'food_dataset_v1.csv', type=str, help='Input CSV file with merchant data (default: food_dataset.csv)')
#     parser.add_argument('--output_file', type=str, default='gmr_metrics.csv', help='Output CSV file name (default: weekly_metrics.csv)')

#     args = parser.parse_args()

#     # Define paths relative to the script location
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     input_file_path = os.path.abspath(os.path.join(script_dir, '../data', args.input_file))
#     output_file_path = os.path.abspath(os.path.join(script_dir, '../data', args.output_file))

#     # Print paths for debugging
#     print(f"Input file path: {input_file_path}")
#     print(f"Output file path: {output_file_path}")

#     process_data(input_file_path, output_file_path)
