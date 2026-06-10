import pandas as pd

class AnalistaTributarioIA:
    @staticmethod
    def analisar_resultados(resultados: list) -> pd.DataFrame:
        df = pd.DataFrame(resultados)
        df = df.sort_values(by='renda_testada').reset_index(drop=True)        
        df['delta_renda'] = df['renda_testada'].diff()
        df['delta_imposto'] = df['imposto_devido'].diff()
        df['taxa_marginal'] = (df['delta_imposto'] / df['delta_renda']) * 100
        
        df.fillna(0, inplace=True)
        
        print("\n--- RELATÓRIO DE ANÁLISE DE FAIXAS TRIBUTÁRIAS ---")
        
        faixa_atual = 0.0
        for index, row in df.iterrows():
            if index == 0:
                continue
            taxa_marginal_arredondada = round(row['taxa_marginal'], 1)
            
            if row['delta_imposto'] < 0 and row['delta_renda'] > 0:
                print(f"[ANOMALIA DETECTADA] Renda subiu para R$ {row['renda_testada']}, mas o imposto caiu!")
            
            if taxa_marginal_arredondada != faixa_atual and row['delta_imposto'] > 0:
                print(f"[MUDANÇA DE FAIXA] Limite ultrapassado próximo a R$ {row['renda_testada']:.2f}")
                print(f"  -> Nova Taxa Marginal calculada: {taxa_marginal_arredondada}% (Alíquota Efetiva: {row['aliquota_efetiva_percentual']}%)")
                faixa_atual = taxa_marginal_arredondada

        return df