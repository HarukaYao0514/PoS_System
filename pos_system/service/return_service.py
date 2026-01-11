class ReturnService:
    def __init__(self, sale_service):
        self.sale_service = sale_service
        self.returns = []  # List of processed return orders

    def create_return(self, sale_id):
        """Create a return order based on the sale ID"""
        sale = self.sale_service.get_sale_by_id(sale_id)
        if not sale.paid:
            raise ValueError("Unpaid order cannot be returned.")

        from domain.return_transaction import ReturnTransaction
        return_trans = ReturnTransaction(sale)
        self.returns.append(return_trans)
        return return_trans

    def add_return_item(self, return_id, sale_item_index, return_quantity):
        """Add a return quantity parameter and pass it to the return order"""
        for ret in self.returns:
            if ret.return_id == return_id:
                sale = ret.sale
                # Validate if the item index is valid
                if sale_item_index < 0 or sale_item_index >= len(sale.sale_items):
                    raise ValueError("Invalid sale item index")
                sale_item = sale.sale_items[sale_item_index]
                # Call the return order's add_return_item method with the return quantity
                ret.add_return_item(sale_item, return_quantity)
                return ret
        raise ValueError(f"Return transaction not found: {return_id}.")