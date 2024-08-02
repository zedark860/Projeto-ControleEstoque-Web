
import pygsheets
import os
import sys

class SpreadsheetConnection:
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    
        return os.path.join(base_path, relative_path)
    
    def __init__(self) -> None:
        self.config_path = self.resource_path(r"")
        self._initialize_connection()
        
    
    def _initialize_connection(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.config_path}")
            
        try:
            self.gc = pygsheets.authorize(service_file=self.config_path)
            self.sh = self.gc.open("")
            self.wks = self.sh.sheet1
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar à planilha: {e}")
    
    def get_worksheet(self):
        return self.wks