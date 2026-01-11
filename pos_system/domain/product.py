class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id  # Product ID
        self.name = name              # Product name
        self.price = price            # Unit price
        self.stock = stock            # Stock quantity

    def update_stock(self, quantity):
        """Update stock quantity (positive to increase, negative to decrease)"""
        self.stock += quantity