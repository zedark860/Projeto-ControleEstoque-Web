
from model.entities.stock_model import StockModel

class StockController:
    def __init__(self, worksheet) -> None:
        self.wks = worksheet
        

    def add_item(self, item_stock: StockModel) -> str:
        try:
            rows = self.wks.get_all_values(include_tailing_empty_rows=False)
            for row in rows:
                if row[1] == item_stock.identification:
                    return (f"Erro: Ativo #{item_stock.identification} já existe no estoque.")

            new_row_index = len(rows)
            self.wks.insert_rows(new_row_index, values=[list(item_stock.to_dict().values())])
            return (f"Item #{item_stock.identification} adicionado com sucesso!")
        except Exception as error:
            raise Exception(f"Erro ao adicionar item:\n{error}")
        

    def update_item(self, identification: str, item_stock: StockModel) -> str:
        try:
            rows = self.wks.get_all_values(include_tailing_empty_rows=False)
            row_index = None
            for i, row in enumerate(rows):
                if row[1] == identification:
                    row_index = i + 1
                    break
            if row_index is None:
                return (f"Item #{item_stock.identification} não encontrado para atualização.")

            self.wks.update_row(row_index, list(item_stock.to_dict().values()))
            return (f"Item #{item_stock.identification} alterado com sucesso!")
        except Exception as error:
            raise Exception(f"Erro ao alterar item no estoque:\n{error}")
        

    def delete_item(self, identification: str) -> str:
        try:
            rows = self.wks.get_all_values(include_tailing_empty_rows=False)
            row_index = None
            for i, row in enumerate(rows):
                if row[1] == identification:
                    row_index = i + 1
                    break
            if row_index is None:
                return "Item não encontrado."

            self.wks.delete_rows(row_index)
            return "Item excluído com sucesso!"
        except Exception as error:
            raise Exception(f"Erro ao excluir item no estoque:\n{error}")
        

    def get_item_by_identification(self, identification: str) -> StockModel:
        try:
            rows = self.wks.get_all_values(include_tailing_empty_rows=False)
            for row in rows:
                if row[1] == identification:
                    data = {
                        "Responsável": row[0],
                        "Identificação": row[1],
                        "Fabricante": row[2],
                        "Tipo": row[3],
                        "Quantidade": row[4],
                        "Localização": row[5],
                        "ÚltimaEdição": row[6],
                        "Observação": row[7]
                    }
                    return StockModel.from_dict(data)
            return None
        except Exception as error:
            raise Exception(f"Erro ao obter item pela identificação {identification}:\n{error}")
        

    def get_all_items(self) -> list:
        try:
            rows = self.wks.get_all_records()
            return [StockModel.from_dict(row) for row in rows]
        except Exception as error:
            raise Exception(f"Erro ao obter todos os itens do estoque:\n{error}")