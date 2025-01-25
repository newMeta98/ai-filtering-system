import pandas as pd
import json

def filter_allowed_products(all_products_file, allowed_products_file, data_json_file):
    """
    Filters allowed products from all_products_file and saves them to allowed_products_file.
    Removes the allowed products from the original all_products_file.
    """
    try:
        # Load allowed_products from data.json
        with open(data_json_file, 'r') as f:
            data = json.load(f)
        allowed_products = data.get("allowed_products", [])
        print(f"Loaded {len(allowed_products)} allowed products from {data_json_file}")

        # Load the Excel file
        df = pd.read_excel(all_products_file)
        print(f"Loaded {len(df)} products from {all_products_file}")

        # Ensure the 'Title' column is correctly identified (column C)
        # If the column is unnamed, rename it to 'Title'
        if df.columns[2] != 'Title':
            df.rename(columns={df.columns[2]: 'Title'}, inplace=True)
            print("Renamed column C to 'Title'")

        # Filter rows where the Title matches any allowed product
        filtered_df = df[df['Title'].isin(allowed_products)]
        print(f"Found {len(filtered_df)} matching allowed products")

        # Save the filtered rows to allowed_products.xlsx
        filtered_df.to_excel(allowed_products_file, index=False)
        print(f"Saved allowed products to {allowed_products_file}")

        # Remove the filtered rows from the original DataFrame
        df = df[~df['Title'].isin(allowed_products)]
        print(f"Removed allowed products from {all_products_file}")

        # Save the updated DataFrame back to the original file
        df.to_excel(all_products_file, index=False)
        print(f"Updated {all_products_file}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
all_products_file = "allproductsdata.xlsx"
allowed_products_file = "allowed_products.xlsx"
data_json_file = "data.json"

filter_allowed_products(all_products_file, allowed_products_file, data_json_file)