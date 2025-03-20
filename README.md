# Infoware_assignment
here I have uploaded my assignment

# Billing Form Application

This is a simple billing form application built using Python with PySide6 for the GUI, SQLite for the database, and FPDF for generating PDF invoices. It allows users to create bills, store them in a database, retrieve stored data, and calculate the grand total for a specific customer.

## Features
- **Add Multiple Items:** Add multiple items with quantity and price.
- **Calculate Total:** Calculate the total amount of the bill.
- **Submit Bill:** Save the bill to the SQLite database.
- **Generate Invoice:** Automatically generate a PDF invoice.
- **Retrieve Data:** Display all stored bills using a table.
- **Find Grand Total:** Calculate the grand total for a single customer.

## Requirements
Make sure you have the following installed:
- Python 3.x
- PySide6
- SQLite3
- FPDF

You can install the dependencies using the following command:
```bash
pip install PySide6 fpdf
```

## Usage
1. Run the Python script:
```bash
python billing_form.py
```
2. Enter the customer name and add item details (item name, quantity, and price).
3. Click **Calculate Total** to view the total.
4. Click **Submit** to save the data and generate a PDF invoice.
5. Use the **Retrieve Data** button to view all records stored in the database.
6. Enter the customer name and click **Find Grand Total of Customer** to view their total expenditure.

## Database
The application uses an SQLite database named `billing.db`. A table named `item_bills` is created if it doesn't exist.

Table structure:
```sql
CREATE TABLE IF NOT EXISTS item_bills (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    item_name TEXT,
    quantity INTEGER,
    price REAL,
    total REAL
);
```

## Invoice Generation
Invoices are generated in PDF format using the FPDF library. Each invoice contains the following details:
- Customer Name
- Date & Time
- Item Details (Name, Quantity, Price, and Total)
- Grand Total

## Author
Developed by **Himanshu Chauhan**.

