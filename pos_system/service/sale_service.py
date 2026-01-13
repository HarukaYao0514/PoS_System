class SaleService:
    def __init__(self, inventory_service):
        self.inventory_service = inventory_service
        self.sales = []  # List of created orders

    def create_sale(self):
        """Create a new order"""
        from domain.sale import Sale
        new_sale = Sale()
        self.sales.append(new_sale)
        return new_sale

    def get_sale_by_id(self, sale_id):
        """Query an order by its ID"""
        for sale in self.sales:
            if sale.sale_id == sale_id:
                return sale
        raise ValueError(f"Sale not found: {sale_id}.")

    def add_product_to_sale(self, sale_id, product_id, quantity):
        """Add a product to an order"""
        sale = self.get_sale_by_id(sale_id)
        product = self.inventory_service.get_product_by_id(product_id)
        sale.add_item(product, quantity)
        return sale  # Return the updated order