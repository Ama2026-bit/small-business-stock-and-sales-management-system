# Small Business Stock and Sales Management System

A practical Python command-line application for managing products, stock, and sales. This submission copy contains a standalone app and a step-by-step Jupyter notebook.

## Features

- Add products with purchase price, selling price, and stock quantity.
- View current inventory.
- Delete a product with confirmation.
- Record a sale with multiple products.
- Validate available stock before checkout and update quantities after a completed sale.
- Review transaction history, revenue, costs, and gross profit.
- Save inventory and sales to JSON between sessions.
- Create timestamped sales backups without replacing earlier backups.
- Read both older single-product records and newer multi-product transactions.

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Run the program

Open a terminal in this folder and run:

```text
python business_system.py
```

Choose an option from the menu. Choose **7. Exit** to close the program.

To load the included demonstration records, copy `sample_business_data.json` and name the copy `business_data.json` in this folder before starting the program. The sample is fictional. The app will save changes to `business_data.json`.

You can also open `business.ipynb` in VS Code or Jupyter and run the cells in order to see the project step by step. The notebook in this submission copy has its saved outputs cleared.

## Project files

- `business_system.py` — standalone command-line application.
- `business.ipynb` — step-by-step notebook, with saved outputs cleared for sharing.
- `sample_business_data.json` — fictional demonstration inventory and sales.
- `.gitignore` — excludes local business data and backup files from Git.

## Data privacy

Keep your own `business_data.json`, `sales_records_backup.json`, and timestamped sales backup files private. They are excluded from Git by `.gitignore`. The included sample file contains fictional records for demonstration.

## Project purpose

This project demonstrates practical Python skills, including functions, dictionaries, loops, input validation, JSON file handling, exception handling, persistence, and multi-item transaction processing for a small business use case.
