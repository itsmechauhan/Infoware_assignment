import sqlite3
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                                QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, 
                                QTableWidgetItem)
from fpdf import FPDF
from datetime import datetime

class BillingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Billing Form By Himanshu Chauhan')
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.name_label = QLabel('Customer Name:')
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.item_layout = QVBoxLayout()
        self.add_item_section()

        self.layout.addLayout(self.item_layout)

        self.add_item_button = QPushButton('Add Item')
        self.add_item_button.clicked.connect(self.add_item_section)
        self.layout.addWidget(self.add_item_button)

        self.calculate_button = QPushButton('Calculate Total')
        self.calculate_button.clicked.connect(self.calculate_total)
        self.layout.addWidget(self.calculate_button)

        self.total_label = QLabel('Total:')
        self.total_output = QLabel('0.0')
        self.layout.addWidget(self.total_label)
        self.layout.addWidget(self.total_output)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.retrieve_button = QPushButton('Retrieve Data')
        self.retrieve_button.clicked.connect(self.retrieve_data)
        self.layout.addWidget(self.retrieve_button)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

    def add_item_section(self):
        item_layout = QHBoxLayout()
        item_label = QLabel('Item Name:')
        item_input = QLineEdit()
        quantity_label = QLabel('Quantity:')
        quantity_input = QLineEdit()
        price_label = QLabel('Price per Item:')
        price_input = QLineEdit()

        item_layout.addWidget(item_label)
        item_layout.addWidget(item_input)
        item_layout.addWidget(quantity_label)
        item_layout.addWidget(quantity_input)
        item_layout.addWidget(price_label)
        item_layout.addWidget(price_input)

        self.item_layout.addLayout(item_layout)

    def init_db(self):
        self.conn = sqlite3.connect('billing.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BILLS (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            item_name TEXT,
            quantity INTEGER,
            price REAL,
            total REAL
        )''')
        self.conn.commit()

    def calculate_total(self):
        total = 0.0
        try:
            for i in range(self.item_layout.count()):
                item_layout = self.item_layout.itemAt(i).layout()
                quantity = int(item_layout.itemAt(3).widget().text())
                price = float(item_layout.itemAt(5).widget().text())
                total += quantity * price
            self.total_output.setText(f'{total:.2f}')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Please enter valid numbers for Quantity and Price.')

    def submit_data(self):
        customer_name = self.name_input.text().strip()
        if not customer_name:
            QMessageBox.warning(self, 'Warning', 'Please enter the customer name.')
            return

        try:
            items = []
            grand_total = 0.0
            for i in range(self.item_layout.count()):
                item_layout = self.item_layout.itemAt(i).layout()
                item_name = item_layout.itemAt(1).widget().text().strip()
                quantity = int(item_layout.itemAt(3).widget().text())
                price = float(item_layout.itemAt(5).widget().text())
                total = quantity * price
                grand_total += total
                self.cursor.execute('INSERT INTO BILLS (customer_name, item_name, quantity, price, total) VALUES (?, ?, ?, ?, ?)',
                                    (customer_name, item_name, quantity, price, total))
                items.append((item_name, quantity, price, total))
            self.conn.commit()
            self.generate_invoice(customer_name, items, grand_total)
            QMessageBox.information(self, 'Success', 'Bill Submitted Successfully! Invoice generated.')
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', str(e))

    def generate_invoice(self, customer_name, items, grand_total):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, 'XYZ Infoware', ln=True, align='C')
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(200, 10, 'Billing Invoice', ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, f'Customer: {customer_name}', ln=True)
        pdf.cell(200, 10, f'Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.cell(50, 10, 'Item Name', 1)
        pdf.cell(30, 10, 'Quantity', 1)
        pdf.cell(40, 10, 'Price', 1)
        pdf.cell(30, 10, 'Total', 1)
        pdf.ln()

        for item_name, quantity, price, total in items:
            pdf.cell(50, 10, item_name, 1)
            pdf.cell(30, 10, str(quantity), 1)
            pdf.cell(40, 10, f'{price:.2f}', 1)
            pdf.cell(30, 10, f'{total:.2f}', 1)
            pdf.ln()

        pdf.cell(200, 10, f'Grand Total: {grand_total:.2f}', ln=True, align='R')
        pdf.output('invoice.pdf')

    def retrieve_data(self):
        self.cursor.execute('SELECT * FROM BILLS')
        data = self.cursor.fetchall()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Customer Name', 'Item Name', 'Quantity', 'Price', 'Total'])
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    form = BillingForm()
    form.show()
    app.exec()
