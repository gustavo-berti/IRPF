from scrapers.simulador import SimuladorIRPFTester
from core.analyzer import AnalistaTributarioIA
from core.config import VALORES_TESTE_PADRAO

def run_automation():
    tester = SimuladorIRPFTester()
    resultados_coletados = []
    
    try:
        tester.start()
        print("Iniciando bateria de testes no Simulador da Receita...")
        
        for valor in VALORES_TESTE_PADRAO:
            print(f"Simulando R$ {valor:.2f}...")
            resultado = tester.simular_valor(valor)
            if resultado:
                resultados_coletados.append(resultado)
                
    finally:
        tester.fechar()
        print("Navegador fechado. Processando dados...")
        
    if resultados_coletados:
        df_final = AnalistaTributarioIA.analisar_resultados(resultados_coletados)
        print("\n--- DADOS BRUTOS ---")
        print(df_final[['renda_testada', 'imposto_devido', 'aliquota_efetiva_percentual', 'taxa_marginal']])
    else:
        print("Nenhum resultado foi coletado para análise.")

if __name__ == "__main__":
    run_automation()