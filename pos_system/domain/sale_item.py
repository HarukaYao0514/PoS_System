class SaleItem:
    def __init__(self, product, quantity):
        self.product = product    # Associated Product object
        self.quantity = quantity  # Purchased quantity
        self.returned_quantity = 0  # Quantity already returned

    @property
    def total_price(self):
        """Calculate the total price for this item"""
        return self.product.price * self.quantity

    @property
    def available_return_quantity(self):
        """Remaining quantity that can be returned for this item"""
        return self.quantity - self.returned_quantity