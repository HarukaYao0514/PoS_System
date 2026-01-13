from service.inventory_service import InventoryService
from service.sale_service import SaleService
from service.return_service import ReturnService
from ui.pos_ui import POSUI

if __name__ == "__main__":
    inventory_service = InventoryService()
    sale_service = SaleService(inventory_service)
    return_service = ReturnService(sale_service)

    pos_ui = POSUI(sale_service, return_service, inventory_service)
    pos_ui.show_menu()