import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

from core.config import BASE_URL, SELECTORS

class SimuladorIRPFTester:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        self.driver.maximize_window() 
        self.wait = WebDriverWait(self.driver, 10)
    
    def _limpar_moeda_br(self, valor_str: str) -> float:
        """Converte string de moeda BR para float."""
        if not valor_str:
            return 0.0
        valor_limpo = valor_str.replace('R$', '').replace('%', '').replace('.', '').replace(',', '.').strip()
        try:
            return float(valor_limpo)
        except ValueError:
            return 0.0

    def start(self):
        self.driver.get(BASE_URL)
        time.sleep(3) 

    def simular_valor(self, valor_renda: float) -> dict:
        try:
            input_element = self.wait.until(EC.element_to_be_clickable(SELECTORS["renda_input"]))
            
            input_element.send_keys(Keys.CONTROL + "a")
            input_element.send_keys(Keys.DELETE)
            time.sleep(0.5)
            
            valor_str = f"{valor_renda:.2f}".replace('.', ',')
            input_element.send_keys(valor_str)
            input_element.send_keys(Keys.TAB) 
            
            time.sleep(1) 
            
            txt_imposto = self.driver.find_element(*SELECTORS["imposto_devido"]).text
            txt_aliquota = self.driver.find_element(*SELECTORS["aliquota_efetiva"]).text
            
            return {
                "renda_testada": valor_renda,
                "imposto_devido": self._limpar_moeda_br(txt_imposto),
                "aliquota_efetiva_percentual": self._limpar_moeda_br(txt_aliquota)
            }
            
        except TimeoutException:
            print(f"Erro ao simular valor: R$ {valor_renda}. Elementos não encontrados.")
            return None

    def fechar(self):
        self.driver.quit()