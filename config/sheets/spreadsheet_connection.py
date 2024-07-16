
import pygsheets
import os

class SpreadsheetConnection:
    def __init__(self) -> None:
        # Coloque aqui o caminho para as configurações de credenciais do Google Developers
        self.config_path = os.path.join(os.getcwd(), "config", "credentials", "")
        self._initialize_connection()
        
    
    def _initialize_connection(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.config_path}")
            
        try:
            self.gc = pygsheets.authorize(service_file=self.config_path)
            # Coloque no sh o nome da planilha que está no sheets/drive
            self.sh = self.gc.open("")
            self.wks = self.sh.sheet1
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar à planilha: {e}")
        
    
    def get_worksheet(self):
        return self.wks