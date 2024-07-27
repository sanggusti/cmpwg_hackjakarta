import pandas as pd
import numpy as np
from faker import Faker
import argparse

class FoodProvider:
    def __init__(self, faker_instance):
        self.faker = faker_instance
        self.food_items = [
            "Nasi Goreng", "Bakso", "Sate", "Rendang", "Ayam Goreng", "Martabak", "Pempek", "Gado-Gado",
            "Lontong", "Soto", "Bubur Ayam", "Siomay", "Tahu Gejrot", "Kue Cubit", "Es Cendol", "Kwetiau",
            "Ayam Penyet", "Nasi Uduk", "Tahu Tempe", "Karedok", "Kerupuk", "Nasi Kuning", "Ikan Bakar",
            "Cah Kangkung", "Mie Rebus", "Mie Kuah", "Sop Buntut", "Rujak", "Cendol", "Kue Lapis", "Kue Talam",
            "Dadar Gulung", "Serabi", "Kolak", "Es Teler", "Pecel", "Sop Iga", "Cumi Goreng", "Kerang Hijau",
            "Kepiting Saus Padang", "Nasi Campur", "Tongseng", "Sambal", "Nasi Liwet", "Bubur Ketan Hitam",
            "Es Buah", "Bubur Sumsum", "Dendeng Balado", "Rendang Padang", "Nasi Bakar", "Kwetiau Siram", "Ayam Bumbu Rujak",
            "Tahu Sumedang", "Karedok", "Tahu Tempe", "Klepon", "Roti Bakar", "Martabak Manis", "Martabak Telur",
            "Mie Aceh", "Mie Goreng Jawa", "Nasi Goreng Kampung", "Sate Padang", "Mie Kocok", "Sop Kaki Sapi",
            "Nasi Gudeg", "Cemilan", "Sambel Terasi", "Sop Tahu", "Sate Lilit", "Mie Kriting", "Sop Buntut",
            "Nasi Pecel", "Nasi Bogana", "Ayam Penyet", "Ayam Bakar Taliwang", "Bubur Ketan Hitam", "Pecel Lele",
            "Mie Tahu", "Nasi Goreng Kampung", "Sate Babi", "Nasi Goreng Seafood", "Sop Kambing", "Gulai Kambing",
            "Sate Kambing", "Kue Cubir", "Kue Teflon", "Es Puter", "Keripik Singkong", "Keripik Tempe", "Bubur Ayam Kampung"
        ]

    def food_word(self):
        return np.random.choice(self.food_items)

def generate_synthetic_data(num_merchants, num_categories, num_days, total_rows, output_file):
    fake = Faker('id_ID')
    fake.add_provider(FoodProvider(fake))

    merchants = [f'M{str(i).zfill(3)}' for i in range(1, num_merchants + 1)]
    prefixes = ["Rumah Makan", "Resto", "Cafe"]
    merchant_names = [f"{np.random.choice(prefixes)} {fake.company()}" for _ in range(num_merchants)]
    categories = [
        "Makanan Indonesia", "Makanan Jepang", "Makanan Italia", "Makanan Korea", "Makanan Cina", 
        "Makanan Barat", "Makanan Timur Tengah", "Makanan Thailand", "Makanan Vietnam", "Makanan Meksiko",
        "Pizza", "Burger", "Sushi", "Steak", "Pasta", "Nasi Goreng", "Bakso", "Sate", "Rendang", "Ayam Goreng",
        "Martabak", "Pempek", "Gado-Gado", "Lontong", "Soto", "Bubur Ayam", "Siomay", "Tahu Gejrot", "Kue Cubit", "Es Cendol",
        "Dessert", "Minuman", "Salad", "Roti", "Kue", "Kopi", "Teh", "Jus", "Smoothie", "Es Krim",
        "Seafood", "Dimsum", "Ayam Bakar", "Mie Ayam", "Mie Goreng", "Kari", "Sup", "Sandwich", "Kebab", "Hotdog"
    ]

    columns = ["Merchant_ID", "Merchant_Name", "Date", "Food_Category", "Total_Orders", "Total_Revenue", "Item", "Item_Orders", "Average_Rating", "New_Customers", "Returning_Customers"]
    data = []

    # generate data for each day, merchant, and category
    for day in pd.date_range(start="2024-07-01", periods=num_days):
        for _ in range(total_rows // (num_days * num_merchants)):
            for merchant_id, merchant_name in zip(merchants, merchant_names):
                food_category = np.random.choice(categories)
                total_orders = np.random.randint(1, 101)
                total_revenue = total_orders * np.random.randint(10000, 500000) 
                most_popular_item = fake.food_word()
                most_popular_item_orders = np.random.randint(1, total_orders + 1)
                average_rating = round(np.random.uniform(1.0, 5.0), 1)
                new_customers = np.random.randint(0, total_orders // 2) if total_orders // 2 > 0 else 0
                returning_customers = total_orders - new_customers

                data.append([merchant_id, merchant_name, day, food_category, total_orders, total_revenue, most_popular_item, most_popular_item_orders, average_rating, new_customers, returning_customers])

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)
    print(f"Data generation complete. File saved as {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate synthetic Grab merchant report data.')
    parser.add_argument('--num_merchants', type=int, default=200, help='Number of merchants')
    parser.add_argument('--num_categories', type=int, default=50, help='Number of food categories')
    parser.add_argument('--num_days', type=int, default=7, help='Number of days for the report')
    parser.add_argument('--total_rows', type=int, default=100000, help='Total number of rows of data to generate')
    parser.add_argument('--output_file', type=str, default='../data/grab_merchant_report_synthetic_data.csv', help='Output CSV file name')

    args = parser.parse_args()
    generate_synthetic_data(args.num_merchants, args.num_categories, args.num_days, args.total_rows, args.output_file)
