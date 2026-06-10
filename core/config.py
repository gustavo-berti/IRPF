from selenium.webdriver.common.by import By

BASE_URL = "https://www27.receita.fazenda.gov.br/simulador-irpf/"

SELECTORS = {
    "renda_input": (By.ID, "mat-input-0"),
    "imposto_devido": (By.XPATH, "(//*[contains(@class, 'card-result-input') and contains(@class, 'bold')])[1]"),
    "aliquota_efetiva": (By.XPATH, "(//*[contains(@class, 'card-result-input') and contains(@class, 'bold')])[2]")
}

VALORES_TESTE_PADRAO = [
    1500.00, 
    4999.99, 
    5000.00, 
    5000.01, 
    6000.00,  
    7249.99,
    7350.00, 
    7350.01, 
    10000.00  
]