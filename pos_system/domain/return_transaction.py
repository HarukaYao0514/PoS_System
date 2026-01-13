import uuid
from datetime import datetime


class ReturnTransaction:
    def __init__(self, sale):
        self.return_id = str(uuid.uuid4())[:8]  # Return order ID
        self.sale = sale  # Associated original sale order
        self.return_items = []  # Items to return
        self.return_amount = 0.0  # Total refund amount
        self.processed = False  # Whether processing is complete
        self.return_time = datetime.now()  # Return timestamp

    def add_return_item(self, sale_item, return_quantity):
        """Add an item for return with specified quantity, validating the returnable amount"""
        # Validation 1: Return quantity must not be zero or negative
        if return_quantity <= 0:
            raise ValueError("Return quantity must be greater than 0.")
        # Validation 2: Return quantity cannot exceed the available return quantity for this item
        if return_quantity > sale_item.available_return_quantity:
            raise ValueError(f"This item can be returned at most {sale_item.available_return_quantity} units.")

        # Calculate refund amount for this item
        item_return_amount = sale_item.product.price * return_quantity
        # Record the return item (SaleItem + return quantity)
        self.return_items.append({
            "sale_item": sale_item,
            "return_quantity": return_quantity
        })
        # Update total refund amount
        self.return_amount += item_return_amount
        # Update the returned quantity of the sale item
        sale_item.returned_quantity += return_quantity
        # Restore inventory
        sale_item.product.update_stock(return_quantity)