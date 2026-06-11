import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            input_element.click()
            input_element.send_keys(Keys.END)
            for _ in range(15): 
                input_element.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)

            valor_str = f"{valor_renda:.2f}".replace('.', ',')
            input_element.send_keys(valor_str)
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1.5)

            cards = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'card-result-input') and contains(@class, 'bold')]")
            valores_reais = []
            for c in cards:
                val = c.get_attribute('value') or c.text
                if val and val.strip():
                    valores_reais.append(val.strip())
        
            if len(valores_reais) >= 2:
                txt_imposto = valores_reais[-2]
                txt_aliquota = valores_reais[-1]
            else:
                txt_imposto = "0,00"
                txt_aliquota = "0,00"
                
            return {
                "renda_testada": valor_renda,
                "imposto_devido": self._limpar_moeda_br(txt_imposto),
                "aliquota_efetiva_percentual": self._limpar_moeda_br(txt_aliquota)
            }
            
        except Exception as e:
            print(f"Erro ao simular R$ {valor_renda}: {e}")
            return None

    def fechar(self):
        self.driver.quit()