import ttkbootstrap as ttk
import requests
from ttkbootstrap.constants import *
from controller.stock_controller import StockController
from config.sheets.spreadsheet_connection import SpreadsheetConnection
from tkinter import messagebox

from view.main.add_view import add_item
from view.main.delete_view import delete_item
from view.main.update_view import update_item
from view.main.view_itens import show_items

class MainPage(ttk.Window):
    @staticmethod
    def check_internet_connection():
        try:
            # Tenta fazer uma solicitação HTTP para um site confiável
            requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Controle do Estoque - T.I")
        self.resizable(False, False)
        self.center_window()

        sheets = SpreadsheetConnection()
        self.stock_controller = StockController(sheets.get_worksheet())

        self.letter_validation = self.register(self.only_letters)
        self.number_validation = self.register(self.only_numbers)
        self.alnum_validation = self.register(self.letters_and_numbers)

        self.items_list = self.stock_controller.get_all_items()

        self.create_widgets()

        # Verifica a conexão periodicamente
        self.check_internet_periodically()

    def center_window(self):
        """Centraliza a janela na vertical."""
        window_width = 600
        window_height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
    def check_internet_periodically(self):
        if not self.check_internet_connection():
            messagebox.showerror(
                "Erro de Conexão", "Perdeu a conexão com a internet. Por favor, verifique sua conexão!")
            self.destroy()  # Fechar a aplicação se a conexão cair
        else:
            # Agendar a próxima verificação em 10 segundos (10000 milissegundos)
            self.after(10000, self.check_internet_periodically)

    def create_widgets(self):
        self.create_action_combobox()
        self.create_form()
        self.update_form_visibility()
        
    def create_form(self):
        """Cria todos os campos do formulário e os botões."""
        self.create_form_fields()
        self.create_buttons()
        self.create_view_fields()
        
    def create_form_fields(self):
        """Cria e organiza os campos do formulário e armazena referências."""
        self.labels_entries = {
            "Responsável": self.create_combobox_entry("Responsável:", self.get_responsavel_values() ,self.letter_validation),
            "Identificação": self.create_label_entry("Identificação do Ativo:", self.number_validation),
            "Fabricante": self.create_combobox_entry("Fabricante:", self.get_fabricante_values(), self.letter_validation),
            "Tipo": self.create_combobox_entry("Tipo do Item:", self.get_tipo_values(), self.letter_validation),
            "Quantidade": self.create_label_entry("Quantidade:", self.number_validation),
            "Localização": self.create_combobox_entry("Localização do Item:", self.get_localizacao_values(), self.alnum_validation),
            "Observação": self.create_label_entry("Observações do Item:", self.alnum_validation)
        }

    def create_action_combobox(self):
        """Cria o combobox para selecionar a ação."""
        self.action_var = ttk.StringVar()
        self.action_combobox = ttk.Combobox(
            self, textvariable=self.action_var, state="readonly")
        self.action_combobox['values'] = (
            "Adicionar item", "Modificar item", "Deletar item", "Visualizar item")
        self.action_combobox.current(0)
        self.action_combobox.pack(pady=5)
        self.action_combobox.bind(
            "<<ComboboxSelected>>", self.update_form_visibility)

    def create_label_entry(self, text, validation_command):
        """Cria um rótulo e um campo de entrada e retorna as referências."""
        label = ttk.Label(self, text=text, bootstyle="info")
        entry = ttk.Entry(self, validate="key",
                          validatecommand=(validation_command, '%S'))
        return label, entry

    def create_buttons(self):
        """Cria diferentes botões para cada opção selecionada no ComboBox"""
        self.add_button = ttk.Button(
            self, text="Adicionar", bootstyle="success", command=lambda: add_item(self))
        self.update_button = ttk.Button(
            self, text="Modificar", bootstyle="success", command=lambda: update_item(self))
        self.delete_button = ttk.Button(
            self, text="Deletar", bootstyle="success", command=lambda: delete_item(self))
        self.clear_button = ttk.Button(
            self, text="Limpar", bootstyle="warning", command=self.clear_fields)

    def create_view_fields(self):
        """Cria os campos para visualizar os itens."""
        # Campo para digitar identificador
        self.view_id_label = ttk.Label(
            self, text="Identificação do ativo:", bootstyle="info")
        self.view_id_entry = ttk.Entry(
            self, validate="key", validatecommand=(self.number_validation, "%S"))

        # Campo para selecionar tipo do item
        self.view_type_label = ttk.Label(
            self, text="Tipo do item:", bootstyle="info")
        self.view_type_combobox = ttk.Combobox(self, state="readonly")

        # Campo para mostrar os itens
        self.view_text = ttk.Text(wrap='word', height=20, width=80)

        # Botão para visualizar itens
        self.view_button = ttk.Button(
            self, text="Mostrar Itens", bootstyle="success", command=lambda: show_items(self))
        
        # Organizar a visualização dos campos
        self.view_id_label.pack(pady=5)
        self.view_id_entry.pack(pady=5)
        self.view_type_label.pack(pady=5)
        self.view_type_combobox.pack(pady=5)
        self.view_text.pack(pady=5)
        self.view_button.pack(pady=5)

        # Atualiza opções do combobox de tipos
        self.update_type_combobox()

    def update_form_visibility(self, event=None):
        """Atualiza a visibilidade dos campos com base na ação selecionada."""
        action = self.action_var.get()
        if action == "Deletar item":
            self.show_delete_item_form()
        elif action == "Visualizar item":
            self.show_view_item_form()
        elif action == "Adicionar item":
            self.show_add_item_form()
        elif action == "Modificar item":
            self.show_update_item_form()
        else:
            self.hide_all_fields()

    def show_delete_item_form(self):
        """Mostra somente os campos necessários para deletar um item e oculta os outros campos e botões."""
        self.hide_all_fields()
        self.labels_entries["Identificação"][0].pack(pady=5)
        self.labels_entries["Identificação"][1].pack(pady=5)
        self.delete_button.pack(pady=5)
        self.view_text.pack(pady=5)
        
        show_items(self, all_items=True)

    def show_view_item_form(self):
        """Mostra campos para visualizar itens e oculta outros campos e botões."""
        self.hide_all_fields()
        self.view_id_label.pack(pady=5)
        self.view_id_entry.pack(pady=5)
        self.view_type_label.pack(pady=5)
        self.view_type_combobox.pack(pady=5)
        self.view_text.pack(pady=5)
        self.view_button.pack(pady=5)
        self.clear_button.pack(pady=5)

        show_items(self, all_items=True)

    def show_add_item_form(self):
        """Mostra todos os campos do formulário e oculta o botão Deletar."""
        self.hide_all_fields()
        for label, entry in self.labels_entries.values():
            label.pack(pady=5)
            entry.pack(pady=5)
        self.add_button.pack(pady=5)
        self.clear_button.pack(pady=5)
        
    def autofill_callback(self, delay):
        """Cria uma função de callback que será chamada após um atraso."""
        def callback(event):
            # Remove o evento antigo, se houver
            if hasattr(self, '_autofill_timer'):
                self.after_cancel(self._autofill_timer)

            # Agenda o preenchimento automático
            self._autofill_timer = self.after(delay, self.autofill_fields)

        return callback
    
    def autofill_fields(self):
        """Preenche os campos do formulário com os dados do item correspondente ao identificador fornecido."""
        identificador = self.labels_entries["Identificação"][1].get().strip()

        # Encontra o item com o identificador fornecido
        item = next((item for item in self.items_list if str(
            item.identification) == identificador), None)

        if item:
            self.message_box_view("Item encontrando com sucesso! Aguarde...", "Item encontrado")
            
            self.labels_entries["Responsável"][1].delete(0, "end")
            self.labels_entries["Responsável"][1].insert(0, item.accountable)

            self.labels_entries["Fabricante"][1].set(item.maker)

            self.labels_entries["Tipo"][1].set(item.type)

            self.labels_entries["Quantidade"][1].delete(0, "end")
            self.labels_entries["Quantidade"][1].insert(0, item.quantity)

            self.labels_entries["Localização"][1].delete(0, "end")
            self.labels_entries["Localização"][1].insert(0, item.location)

            self.labels_entries["Observação"][1].delete(0, "end")
            self.labels_entries["Observação"][1].insert(0, item.note)
        else:
            self.message_box_view("Nenhum item encontrado com esse identificador!", "Item não encontrado")
            
            # Se não encontrar o item, limpa os campos
            self.clear_fields()

    def show_update_item_form(self):
        """Mostra todos os campos do formulário e oculta o botão Deletar."""
        self.hide_all_fields()
        for label, entry in self.labels_entries.values():
            label.pack(pady=5)
            entry.pack(pady=5)
        self.update_button.pack(pady=5)
        self.clear_button.pack(pady=5)

        self.labels_entries["Identificação"][1].bind(
            "<KeyRelease>", self.autofill_callback(1000))

    def hide_all_fields(self):
        """Oculta todos os campos do formulário e botões."""
        for label, entry in self.labels_entries.values():
            label.pack_forget()
            entry.pack_forget()
        self.add_button.pack_forget()
        self.update_button.pack_forget()
        self.delete_button.pack_forget()
        self.clear_button.pack_forget()
        self.view_id_label.pack_forget()
        self.view_id_entry.pack_forget()
        self.view_type_label.pack_forget()
        self.view_type_combobox.pack_forget()
        self.view_text.pack_forget()
        self.view_button.pack_forget()
        
        self.labels_entries["Identificação"][1].unbind("<KeyRelease>")

    def create_combobox_entry(self, text, values, validation_command):
        """Cria um rótulo e um combobox editável e retorna as referências."""
        label = ttk.Label(self, text=text, bootstyle="info")
        combobox = ttk.Combobox(self, values=values, state="normal")
        combobox.set('')  # Configura o valor inicial para vazio
        combobox.bind(
            '<FocusOut>', lambda e: self.update_combobox_values(combobox))
        return label, combobox

    def update_combobox_values(self, combobox):
        """Atualiza o combobox com novos valores digitados."""
        new_value = combobox.get().strip()
        if new_value and new_value not in combobox['values']:
            values = list(combobox['values']) + [new_value]
            combobox['values'] = values
            
    def get_responsavel_values(self):
        """Obtém todos os valores únicos de nomes para o combobox."""
        return sorted(set(item.accountable for item in self.items_list))

    def get_fabricante_values(self):
        """Obtém todos os valores únicos de fabricantes para o combobox."""
        return sorted(set(item.maker for item in self.items_list))

    def get_tipo_values(self):
        """Obtém todos os valores únicos de tipos para o combobox."""
        return sorted(set(item.type for item in self.items_list))
    
    def get_localizacao_values(self):
        """Obtém todos os valores únicos de localizações para o combobox."""
        return sorted(set(item.location for item in self.items_list))
    
    def update_responsavel_combobox(self):
        """Atualiza o combobox de responsavel com os nomes responsáveis presentes nos itens."""
        responsavel = self.get_nome_values()
        self.labels_entries["Nome"][1]['values'] = responsavel

    def update_fabricante_combobox(self):
        """Atualiza o combobox de fabricantes com os fabricantes únicos presentes nos itens."""
        fabricantes = self.get_fabricante_values()
        self.labels_entries["Fabricante"][1]['values'] = fabricantes
        
    def update_type_combobox(self):
        """Atualiza o combobox de tipos com os tipos únicos presentes nos itens."""
        types = self.get_tipo_values()
        self.view_type_combobox['values'] = types
        
    def update_localizacao_combobox(self):
        """Atualiza o combobox de localização com os localizacoes únicas presentes nos itens."""
        localizacao = self.get_localizacao_values()
        self.labels_entries["Localização"][1]['values'] = localizacao

    def clear_fields(self):
        """Limpa todos os campos e widgets."""
        for label, entry in self.labels_entries.values():
            entry.delete(0, "end")

        self.view_id_entry.delete(0, "end")
        self.view_type_combobox.set('')
        self.view_text.config(state=ttk.NORMAL)
        self.view_text.delete(1.0, "end")

    def message_box_view(self, message, title="Aviso"):
        try:
            messagebox.showinfo(title, message)
        except:
            messagebox.showerror(title, message)

    @staticmethod
    def only_letters(char):
        return char.isalpha() or char.isspace()

    @staticmethod
    def only_numbers(char):
        return char.isdigit()

    @staticmethod
    def letters_and_numbers(char):
        return char.isascii() or char.isspace()