import uuid
from datetime import datetime
from .sale_item import SaleItem


class Sale:
    def __init__(self):
        self.sale_id = str(uuid.uuid4())[:8]  # Generate short order ID
        self.sale_items = []  # List of sale items
        self.total_amount = 0.0  # Total order amount
        self.payment_amount = 0.0  # Payment amount
        self.paid = False  # Whether payment is completed
        self.create_time = datetime.now()  # Order creation timestamp

    def add_item(self, product, quantity):
        """Add a product to the order (automatically updates inventory)"""
        if product.stock < quantity:
            raise ValueError(f"Insufficient stock: {product.name}. Current stock {product.stock}.")

        sale_item = SaleItem(product, quantity)
        self.sale_items.append(sale_item)
        self.total_amount += sale_item.total_price
        product.update_stock(-quantity)  # Reduce inventory

    def process_payment(self, amount):
        """Process payment (validate amount and mark payment as completed)"""
        if amount < self.total_amount:
            raise ValueError(f"Insufficient payment amount, required {self.total_amount}.")
        self.payment_amount = amount
        self.paid = True
        return amount - self.total_amount  # Return change