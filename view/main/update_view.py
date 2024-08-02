import ttkbootstrap as ttk
from datetime import datetime
from model.entities.stock_model import StockModel

def update_item(self):
    """Atualiza item ao estoque e atualiza a lista de itens"""
    values = {key: entry.get().strip() if not isinstance(entry, ttk.Combobox)
              else entry.get() for key, (_, entry) in self.labels_entries.items()}
    values["Última Edição"] = datetime.now().isoformat()

    item = StockModel.from_dict(values)

    identificacao = values["Identificação"]
    response = self.stock_controller.update_item(identificacao, item)

    self.items_list = self.stock_controller.get_all_items()
    self.update_type_combobox()
    self.update_fabricante_combobox()

    self.message_box_view(response)

    self.clear_fields()
