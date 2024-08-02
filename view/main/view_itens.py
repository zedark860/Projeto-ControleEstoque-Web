import ttkbootstrap as ttk
from tkinter import messagebox

def show_items(self, all_items=False):
    """Exibe itens baseados no identificador e tipo selecionado."""
    identificador = self.view_id_entry.get().strip()
    tipo_selecionado = self.view_type_combobox.get()

    if all_items:
        filtered_items = self.items_list
    else:
        identificador = self.view_id_entry.get().strip()
        tipo_selecionado = self.view_type_combobox.get()

        self.view_text.config(state=ttk.NORMAL)

        filtered_items = [
            item for item in self.items_list
            if (not identificador or str(item.identification) == str(identificador)) and
               (not tipo_selecionado or str(item.type) == str(tipo_selecionado))
        ]

    self.view_text.delete(1.0, "end")
    for item in filtered_items:
        self.view_text.insert("end", f"Identificação: {item.identification}\n"
                              f"Responsável: {item.accountable}\n"
                              f"Fabricante: {item.maker}\n"
                              f"Tipo: {item.type}\n"
                              f"Quantidade: {item.quantity}\n"
                              f"Localização: {item.location}\n"
                              f"Observações: {item.note}\n\n")

    self.view_text.config(state=ttk.DISABLED)
