
from datetime import datetime


class StockModel:
    def __init__(self, accountable: str, identification: str, maker: str, type: str, quantity: int, location: str, last_edition: datetime, note: str) -> None:
        self.accountable = accountable
        self.identification = identification
        self.maker = maker
        self.type = type
        self.quantity = quantity
        self.location = location
        self.last_edition = last_edition
        self.note = note

    def to_dict(self) -> dict:
        return {
            "Responsável": self.accountable,
            "Identificação": self.identification,
            "Fabricante": self.maker,
            "Tipo": self.type,
            "Quantidade": self.quantity,
            "Localização": self.location,
            "ÚltimaEdição": self.last_edition.isoformat(),
            "Observação": self.note
        }

    @staticmethod
    def from_dict(dict_stock: dict) -> 'StockModel':
        quantity = dict_stock.get("Quantidade", 0)
        if isinstance(quantity, str):
            quantity = int(quantity) if quantity.isdigit() else 0

        last_edition_str = dict_stock.get(
            "ÚltimaEdição", datetime.now().isoformat())
        try:
            last_edition = datetime.fromisoformat(last_edition_str)
        except ValueError:
            last_edition = datetime.strptime(
                last_edition_str, "%Y-%m-%d %H:%M:%S")

        return StockModel(
            accountable=dict_stock.get("Responsável", ""),
            identification=dict_stock.get("Identificação", ""),
            maker=dict_stock.get("Fabricante", ""),
            type=dict_stock.get("Tipo", ""),
            quantity=quantity,
            location=dict_stock.get("Localização", ""),
            last_edition=last_edition,
            note=dict_stock.get("Observação", "")
        )

    def __repr__(self) -> str:
        return (f"StockModel(accountable={self.accountable}, identification={self.identification}, maker={self.maker}, "
                f"type={self.type}, quantity={self.quantity}, location={self.location}, last_edition={self.last_edition}, note={self.note})")
