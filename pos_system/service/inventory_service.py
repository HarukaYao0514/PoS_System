class InventoryService:
    def __init__(self):
        # Initialize test products
        from domain.product import Product
        self.products = [
            Product("P001", "Coke", 3.5, 100),
            Product("P002", "Potato Chips", 5.0, 50),
            Product("P003", "Bread", 4.0, 30),
            Product("P004", "Mineral Water", 2.0, 200),
            Product("P005", "Chocolate", 8.5, 45),
            Product("P006", "Instant Noodles", 4.5, 80),
            Product("P007", "Ham Sausage", 3.0, 150),
            Product("P008", "Milk", 5.5, 60),
            Product("P009", "Cookies", 6.8, 70),
            Product("P010", "Ice Black Tea", 3.8, 95)
        ]

    def get_product_by_id(self, product_id):
        """Query a product by its ID"""
        for p in self.products:
            if p.product_id == product_id:
                return p
        raise ValueError(f"Product not found: {product_id}.")

    def view_products(self):
        """View information for all products"""
        product_list = []
        for p in self.products:
            product_list.append(f"ID:{p.product_id} | Name:{p.name} | Price:{p.price} | Stock:{p.stock}")
        return product_list