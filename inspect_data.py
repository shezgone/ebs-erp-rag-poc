import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.mock_erp import load_mock_erp_data

def inspect_tables():
    data = load_mock_erp_data()
    print("--- Mock EBS ERP Database Tables ---\n")
    
    for table_name, df in data.items():
        print(f"=== Table: {table_name.upper()} ===")
        print(df.to_markdown(index=False, tablefmt="grid"))
        print("\n")

if __name__ == "__main__":
    try:
        inspect_tables()
    except ImportError:
        # Fallback if tabulate/markdown not installed, though pandas usually handles simple string repr
        data = load_mock_erp_data()
        for table_name, df in data.items():
            print(f"=== Table: {table_name.upper()} ===")
            print(df)
            print("\n")
