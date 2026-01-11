class POSUI:
    def __init__(self, sale_service, return_service, inventory_service):
        self.sale_service = sale_service
        self.return_service = return_service
        self.inventory_service = inventory_service

    def show_menu(self):
        """Display main menu"""
        while True:
            print("\n====== Supermarket POS System ======")
            print("1. Process Sale")
            print("2. Handle Returns")
            print("3. View Products")
            print("4. Exit")
            choice = input("Enter option (1-4): ")

            if choice == "1":
                self.process_sale_flow()
            elif choice == "2":
                self.handle_return_flow()
            elif choice == "3":
                self.view_products()
            elif choice == "4":
                print("System exited.")
                break
            else:
                print("Invalid option, please try again.")

    def process_sale_flow(self):
        """Sales process"""
        print("\n===== Current Product Inventory =====")
        for p_info in self.inventory_service.view_products():
            print(p_info)

        # 1. Create order
        sale = self.sale_service.create_sale()
        print(f"\nNew order created, Order ID: {sale.sale_id}")

        # 2. Continuously add products
        while True:
            product_id = input("Enter product ID (enter 'q' to finish): ")
            if product_id.lower() == "q":
                break
            try:
                quantity = int(input("Enter quantity: "))
                sale = self.sale_service.add_product_to_sale(sale.sale_id, product_id, quantity)
                # Display current order details
                self.show_sale_details(sale)
            except Exception as e:
                print(f"Error: {e}")

        # 3. Process payment - payment loop logic
        if sale.total_amount > 0:
            print(f"\n===== Order Checkout =====")
            print(f"Current order total amount due: ${sale.total_amount}")
            while True:
                try:
                    payment = float(input("Enter payment amount: "))
                    change = sale.process_payment(payment)
                    print(f"Payment successful! Change amount: ${change}")
                    print(f"Order completed, Order ID: {sale.sale_id}.")
                    break
                except ValueError as e:
                    print(f"{e}, please re-enter payment amount!")
        else:
            print("\nNo items in order, order cancelled.")

    def handle_return_flow(self):
        """Return process"""
        # 1. Enter original order ID
        sale_id = input("Enter original order ID: ")
        try:
            return_trans = self.return_service.create_return(sale_id)
            print(f"Return transaction created, Return ID: {return_trans.return_id}.")
            print("Original order items:")
            # Display product + purchased quantity + returned quantity + available quantity
            for idx, item in enumerate(return_trans.sale.sale_items):
                print(
                    f"[{idx}] Product: {item.product.name} | Purchased: {item.quantity} | Returned: {item.returned_quantity} | Available to return: {item.available_return_quantity} | Price: ${item.product.price}")

            # 2. Select return product and enter return quantity, loop to add return items
            while True:
                idx_input = input("Enter product index to return (enter 'q' to finish): ")
                if idx_input.lower() == "q":
                    break
                try:
                    item_idx = int(idx_input)
                    # Get selected product item, validate remaining returnable quantity
                    sale_item = return_trans.sale.sale_items[item_idx]
                    max_return_num = sale_item.available_return_quantity
                    if max_return_num <= 0:
                        print("This item has no remaining quantity available for return.")
                        continue
                    # Enter return quantity
                    return_quantity = int(input(f"Enter return quantity (maximum {max_return_num} units): "))
                    # Call return service, pass return quantity for validation
                    return_trans = self.return_service.add_return_item(return_trans.return_id, item_idx,
                                                                       return_quantity)
                    print(f"Return item added, current total refund amount: ${return_trans.return_amount}")
                except Exception as e:
                    print(f"Error: {e}")

            # 3. Complete return process
            if return_trans.return_amount > 0:
                return_trans.complete_return()
                print(
                    f"Return completed! Refund amount: ${return_trans.return_amount}, Return ID: {return_trans.return_id}.")
            else:
                print("No return items selected, return transaction cancelled.")
        except Exception as e:
            print(f"Return failed: {e}")

    def view_products(self):
        """View product list"""
        print("\n===== Product List =====")
        for p_info in self.inventory_service.view_products():
            print(p_info)

    def show_sale_details(self, sale):
        """Display order details"""
        print("\n===== Current Order Details =====")
        for item in sale.sale_items:
            print(
                f"Product: {item.product.name} | Quantity: {item.quantity} | Price: ${item.product.price} | Subtotal: ${item.total_price}")
        print(f"Current total amount due: ${sale.total_amount}")