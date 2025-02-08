"""
This module computes sales data and generates reports.

Functions:
- compute_sales: Computes the total sales from the provided data.
- generate_report: Generates a sales report based on the computed sales data.
"""
# pylint: disable=invalid-name
import json
import argparse
import time


def load_json_file(file_path):
    """
    This function loads the json files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON.")
    return None


def compute_total_sales(price_catalog, sales_records):
    """
    This function makes the math to compute sales based on product price.
    """
    total_cost = 0.0
    errors = []

    for sale in sales_records:
        product_name = sale.get('Product')
        quantity = sale.get('Quantity', 0)
        product = next(
            (
                item for item in price_catalog
                if item.get('title') == product_name
            ),
            None
        )
        if product and 'price' in product:
            total_cost += product['price'] * quantity
        else:
            errors.append(
                f"Error: Product '{product_name}' not found in catalog."
            )
    return total_cost, errors


def main():
    """
    Main function that calls the rest of the functions.
    """
    parser = argparse.ArgumentParser(description='Compute total sales cost.')
    parser.add_argument(
        'price_catalog_file', help='Path to the price catalog JSON file.'
    )
    parser.add_argument(
        'sales_record_file', help='Path to the sales record JSON file.'
    )
    args = parser.parse_args()

    start_time = time.time()

    price_catalog = load_json_file(args.price_catalog_file)
    sales_records = load_json_file(args.sales_record_file)

    if price_catalog is None or sales_records is None:
        print("Error: Failed to load input files.")
        return

    total_cost, errors = compute_total_sales(price_catalog, sales_records)

    end_time = time.time()
    elapsed_time = end_time - start_time

    result_lines = [
        f"Total Sales Cost: ${total_cost:.2f}",
        f"Execution Time: {elapsed_time:.2f} seconds"
    ]

    if errors:
        result_lines.append("\nErrors:")
        result_lines.extend(errors)

    result_text = "\n".join(result_lines)

    print(result_text)

    with open('SalesResults.txt', 'w', encoding='utf-8') as result_file:
        result_file.write(result_text)


if __name__ == '__main__':
    main()
