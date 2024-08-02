
from datetime import datetime


class StockModel:
    def __init__(self, accountable: str, identification: str, maker: str, type: str, quantity: int, location: str, last_edition: datetime, note: str) -> None:
        self.accountable = accountable
        self.identification = identification
        self.maker = maker
        self.type = type
        self.quantity = quantity
        self.location = location
        self.note = note
        self.last_edition = last_edition        

    def to_dict(self) -> dict:
        return {
            "Responsável": self.accountable,
            "Identificação": self.identification,
            "Fabricante": self.maker,
            "Tipo": self.type,
            "Quantidade": self.quantity,
            "Localização": self.location,
            "Observação": self.note,
            "Última Edição": self.last_edition.strftime("%d/%m/%Y %H:%M:%S")
        }

    @staticmethod
    def from_dict(dict_stock: dict) -> 'StockModel':
        quantity = dict_stock.get("Quantidade", 0)
        if isinstance(quantity, str):
            quantity = int(quantity) if quantity.isdigit() else 0

        last_edition_str = dict_stock.get("Última Edição", "")
        
        if last_edition_str:
            try:
                last_edition = datetime.strptime(last_edition_str, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                try:
                    last_edition = datetime.strptime(last_edition_str, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    last_edition = datetime.now()
        else:
            last_edition = datetime.now()

        return StockModel(
            accountable=dict_stock.get("Responsável", ""),
            identification=dict_stock.get("Identificação", ""),
            maker=dict_stock.get("Fabricante", ""),
            type=dict_stock.get("Tipo", ""),
            quantity=quantity,
            location=dict_stock.get("Localização", ""),
            note=dict_stock.get("Observação", ""),
            last_edition=last_edition
        )

    def __repr__(self) -> str:
        return (f"StockModel(accountable={self.accountable}, identification={self.identification}, maker={self.maker}, "
                f"type={self.type}, quantity={self.quantity}, location={self.location}, note={self.note}), last_edition={self.last_edition}")
