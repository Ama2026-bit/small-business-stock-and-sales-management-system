"""Small Business Stock and Sales Management System."""

# step 1

"""
Small Business Stock and Sales Management System

Purpose:
To help small business owners manage products, inventory,
sales transactions, and business performance.

Project Language: Python
Project Type: Business Management Application
"""

# Display the application title
print("=" * 60)
print("       SMALL BUSINESS STOCK AND SALES MANAGEMENT SYSTEM")
print("=" * 60)

print("\nWelcome to your Business Management System!")
print("Manage your products, monitor stock, and track sales.")

# ==========================================
# STEP 2: LOAD AND SAVE BUSINESS DATA
# ==========================================

import json
from pathlib import Path

# The data file is created beside the notebook when the system first saves.
DATA_FILE = Path(__file__).resolve().parent / "business_data.json"
LEGACY_SALES_BACKUP = Path(__file__).resolve().parent / "sales_records_backup.json"

def load_business_data():
    """Load saved inventory and sales, or use the older sales backup once."""
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as data_file:
            business_data = json.load(data_file)
        inventory_data = business_data.get("inventory", {})
        saved_sales = business_data.get("sales_records", [])
    else:
        inventory_data = {}
        saved_sales = []
        if LEGACY_SALES_BACKUP.exists():
            with LEGACY_SALES_BACKUP.open("r", encoding="utf-8") as backup_file:
                saved_sales = json.load(backup_file)

    if not isinstance(inventory_data, dict):
        raise ValueError("Saved inventory data must be a dictionary.")
    if not isinstance(saved_sales, list):
        raise ValueError("Saved sales data must be a list.")

    return inventory_data, saved_sales

def save_business_data():
    """Save inventory and sales together to one JSON data file."""
    business_data = {
        "inventory": inventory,
        "sales_records": sales_records
    }
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as data_file:
        json.dump(business_data, data_file, ensure_ascii=False, indent=2)
    temporary_file.replace(DATA_FILE)

# Load saved data when the system starts.
inventory, sales_records = load_business_data()

print("\nINVENTORY MANAGEMENT")
print("-" * 40)
print("Inventory storage loaded successfully.")
print(f"Registered products: {len(inventory)}")


# ==========================================
# STEP 3: MULTIPLE PRODUCT REGISTRATION
# ==========================================

def add_product():
    """Register multiple products in the business inventory."""

    while True:

        print("\n--- ADD NEW PRODUCT ---")

        name = input("Enter product name (or 'done' to finish): ").strip().title()

        if name.lower() == "done":
            print("\nProduct registration completed.")
            break

        if not name:
            print("Error: Product name cannot be empty.")
            continue

        if name in inventory:
            print("Error: This product already exists.")
            continue

        try:
            purchase_price = float(input("Enter purchase price (NGN): "))
            selling_price = float(input("Enter selling price (NGN): "))
            quantity = int(input("Enter available quantity: "))

        except ValueError:
            print("Error: Enter valid numbers for prices and quantity.")
            continue

        if purchase_price <= 0 or selling_price <= 0 or quantity <= 0:
            print("Error: All values must be greater than zero.")
            continue

        if selling_price < purchase_price:
            print("Error: Selling price cannot be lower than purchase price.")
            continue

        inventory[name] = {
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "quantity": quantity
        }

        try:
            save_business_data()
        except OSError as error:
            del inventory[name]
            print(f"Error: Product was not saved. {error}")
            continue

        print(f"Success: {name} has been registered and saved.")


# Start product registration
# add_product()

# ==========================================
# STEP 4: VIEW INVENTORY
# ==========================================

def view_inventory():
    """
    Display all registered products and their stock information.
    """

    print("\n" + "=" * 75)
    print("                    BUSINESS INVENTORY REPORT")
    print("=" * 75)

    if not inventory:
        print("No products have been registered yet.")
        return

    # Display the inventory table headings
    print(
        f"{'PRODUCT':<20}"
        f"{'PURCHASE PRICE':>18}"
        f"{'SELLING PRICE':>18}"
        f"{'QUANTITY':>12}"
    )

    print("-" * 75)

    # Display each registered product
    for name, details in inventory.items():

        print(
            f"{name:<20}"
            f"₦{details['purchase_price']:>16,.2f}"
            f"₦{details['selling_price']:>16,.2f}"
            f"{details['quantity']:>12}"
        )

    print("-" * 75)
    print(f"Total registered products: {len(inventory)}")


# Display the current inventory
# view_inventory()


# ==========================================
# STEP 5: DELETE PRODUCT
# ==========================================

def delete_product():
    """Safely remove a product from the inventory."""

    print("\n--- DELETE PRODUCT ---")

    if not inventory:
        print("Inventory is empty. No products to delete.")
        return

    product_name = input(
        "Enter the name of the product to delete: "
    ).strip().title()

    if product_name not in inventory:
        print(f"Error: {product_name} was not found.")
        return

    confirmation = input(
        f"Are you sure you want to delete {product_name}? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        deleted_product = inventory.pop(product_name)
        try:
            save_business_data()
        except OSError as error:
            inventory[product_name] = deleted_product
            print(f"Error: Product was not deleted. {error}")
            return
        print(f"Success: {product_name} has been deleted and saved.")
    else:
        print("Deletion cancelled.")


# Run the delete product feature
# delete_product()

# ==========================================
# STEP 6: SALES RECORD INITIALIZATION
# ==========================================

# Sales records were loaded with the inventory in Step 2.
print("Sales management system initialized.")
print(f"Total recorded sales: {len(sales_records)}")


# ==========================================
# STEP 6B: MULTI-PRODUCT SALES MANAGEMENT
# ==========================================

from datetime import datetime


def record_sale():
    """Process a customer transaction containing multiple products."""

    print("\n" + "=" * 50)
    print("             CUSTOMER SALES")
    print("=" * 50)

    if not inventory:
        print("Error: No products available in inventory.")
        return

    # Create a temporary shopping cart
    cart = {}

    while True:
        product_name = input(
            "\nEnter product name (or 'done' to checkout): "
        ).strip().title()

        if product_name.lower() == "done":
            break

        if product_name not in inventory:
            print("Error: Product not found.")
            continue

        try:
            quantity = int(input("Enter quantity purchased: "))
        except ValueError:
            print("Error: Please enter a valid whole number.")
            continue

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            continue

        # Add quantities if the product is entered again
        cart[product_name] = cart.get(product_name, 0) + quantity

        print(f"Added {quantity} unit(s) of {product_name} to cart.")

    # Check whether the customer selected any products
    if not cart:
        print("\nNo products were added. Transaction cancelled.")
        return

    # Validate the entire cart before changing inventory
    for product_name, quantity in cart.items():

        available_stock = inventory[product_name]["quantity"]

        if quantity > available_stock:
            print(
                f"\nTransaction cancelled: Insufficient stock for "
                f"{product_name}."
            )
            print(f"Requested: {quantity}")
            print(f"Available: {available_stock}")
            return

    # Calculate transaction totals
    transaction_items = []
    total_revenue = 0
    total_cost = 0

    for product_name, quantity in cart.items():

        product = inventory[product_name]

        unit_price = product["selling_price"]
        unit_cost = product["purchase_price"]

        line_revenue = unit_price * quantity
        line_cost = unit_cost * quantity

        transaction_items.append({
            "product": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
            "line_revenue": line_revenue,
            "line_cost": line_cost,
            "profit": line_revenue - line_cost
        })

        total_revenue += line_revenue
        total_cost += line_cost

    total_profit = total_revenue - total_cost

    # Update stock only after the entire cart passes validation
    for product_name, quantity in cart.items():
        inventory[product_name]["quantity"] -= quantity

    # Save the complete customer transaction
    sale = {
        "transaction_id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": transaction_items,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit
    }

    sales_records.append(sale)

    try:
        save_business_data()
    except OSError as error:
        sales_records.pop()
        for product_name, quantity in cart.items():
            inventory[product_name]["quantity"] += quantity
        print(f"Transaction cancelled: Business data could not be saved. {error}")
        return

    # Display customer receipt
    print("\n" + "=" * 65)
    print("                  CUSTOMER RECEIPT")
    print("=" * 65)

    for item in transaction_items:
        print(
            f"{item['product']:<18}"
            f"{item['quantity']:>5} units"
            f"{item['line_revenue']:>18,.2f}"
        )

    print("-" * 65)
    print(f"{'TOTAL REVENUE:':<25} NGN {total_revenue:,.2f}")
    print(f"{'TOTAL COST:':<25} NGN {total_cost:,.2f}")
    print(f"{'ESTIMATED GROSS PROFIT:':<25} NGN {total_profit:,.2f}")
    print("=" * 65)

    print("\nTransaction completed successfully.")
    print(f"Transaction ID: {sale['transaction_id']}")


# Start the customer sales process
# record_sale()

# ==========================================
# OPTIONAL: CREATE A TIMESTAMPED SALES BACKUP
# ==========================================

def create_sales_backup():
    """Create a timestamped sales backup without replacing older files."""
    backup_name = "sales_records_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
    backup_path = Path(__file__).resolve().parent / backup_name

    with backup_path.open("x", encoding="utf-8") as backup_file:
        json.dump(sales_records, backup_file, ensure_ascii=False, indent=2)

    print(f"Backup created: {backup_path}")
    print(f"Records saved: {len(sales_records)}")

def view_sales_history():
    """Display legacy sales records and newer multi-item transactions."""

    print("\n" + "=" * 65)
    print("                  BUSINESS SALES HISTORY")
    print("=" * 65)

    if not sales_records:
        print("No sales transactions have been recorded yet.")
        return

    total_revenue = 0
    total_profit = 0

    for sale_number, sale in enumerate(sales_records, start=1):
        print(f"\nTRANSACTION {sale_number}")
        print("-" * 65)

        print(f"Transaction ID: {sale.get('transaction_id', 'Legacy record')}")
        print(f"Date: {sale.get('date', 'Unknown')}")

        # Newer records contain an "items" list.
        # Older records store the product details directly on the sale.
        items = sale.get("items")
        if items is None:
            items = [sale]

        for item in items:
            product = item.get("product", "Unknown product")
            quantity = item.get("quantity", 0)

            line_revenue = item.get("line_revenue")
            if line_revenue is None:
                line_revenue = item.get(
                    "total_revenue",
                    quantity * item.get("unit_price", 0)
                )

            print(
                f"{product:<18}"
                f"Quantity: {quantity:<6}"
                f"Amount: NGN {line_revenue:,.2f}"
            )

        revenue = sale.get("total_revenue", 0)
        profit = sale.get("total_profit", sale.get("profit", 0))

        print("-" * 65)
        print(f"Transaction Revenue: NGN {revenue:,.2f}")
        print(f"Transaction Profit: NGN {profit:,.2f}")

        total_revenue += revenue
        total_profit += profit

    print("\n" + "=" * 65)
    print("OVERALL BUSINESS SALES SUMMARY")
    print("=" * 65)
    print(f"Total Transactions: {len(sales_records)}")
    print(f"Total Revenue: NGN {total_revenue:,.2f}")
    print(f"Total Gross Profit: NGN {total_profit:,.2f}")
    print("=" * 65)


# Display sales history
# view_sales_history()

# ==========================================
# STEP 8: MAIN MENU
# ==========================================

def main_menu():
    """Let the user choose a stock or sales task."""
    while True:
        print("\n" + "=" * 50)
        print("SMALL BUSINESS STOCK AND SALES MANAGEMENT")
        print("=" * 50)
        print("1. Add a product")
        print("2. View inventory")
        print("3. Delete a product")
        print("4. Record a sale")
        print("5. View sales history")
        print("6. Create sales backup")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            record_sale()
        elif choice == "5":
            view_sales_history()
        elif choice == "6":
            create_sales_backup()
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 7.")

main_menu()
