from view.main.view_itens import show_items

def delete_item(self):
    """Deleta item ao estoque e atualiza a lista de itens"""
    identificacao = self.labels_entries["Identificação"][1].get().strip()
    response = self.stock_controller.delete_item(identificacao)

    self.items_list = self.stock_controller.get_all_items()
    self.update_type_combobox()
    self.update_fabricante_combobox()

    self.message_box_view(response)
    
    self.clear_fields()

    show_items(self, all_items="true")
