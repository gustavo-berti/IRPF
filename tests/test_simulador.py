import pytest
from scrapers.simulador import SimuladorIRPFTester

@pytest.fixture(scope="module")
def simulador():
    tester = SimuladorIRPFTester()
    tester.start()
    yield tester
    tester.fechar()

def test_calculo_isencao_1500(simulador):
    valor_para_simular = 1500.00
    imposto_esperado = 0.00
    aliquota_esperada = 0.00

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_limite_inferior_isencao_4999_99(simulador):
    valor_para_simular = 4999.99
    imposto_esperado = 0.00
    aliquota_esperada = 0.00

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_limite_exato_isencao_5000_00(simulador):
    valor_para_simular = 5000.00
    imposto_esperado = 0.00
    aliquota_esperada = 0.00

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_inicio_reducao_linear_5000_01(simulador):
    valor_para_simular = 5000.01
    imposto_esperado = 0.00
    aliquota_esperada = 0.00

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_meio_reducao_linear_6000_00(simulador):
    valor_para_simular = 6000.00
    imposto_esperado = 394.54
    aliquota_esperada = 6.57

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_fim_reducao_linear_7249_99(simulador):
    valor_para_simular = 7249.99
    imposto_esperado = 904.72
    aliquota_esperada = 12.47

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_limite_retorno_tabela_7350_00(simulador):
    valor_para_simular = 7350.00
    imposto_esperado = 945.54
    aliquota_esperada = 12.86

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_primeiro_centavo_retorno_tabela_7350_01(simulador):
    valor_para_simular = 7350.01
    imposto_esperado = 945.55
    aliquota_esperada = 12.86

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada

def test_calculo_teto_tributacao_10000_00(simulador):
    valor_para_simular = 10000.00
    imposto_esperado = 1674.29
    aliquota_esperada = 16.74

    resultado = simulador.simular_valor(valor_para_simular)

    assert resultado is not None
    assert resultado.get("imposto_devido") == imposto_esperado
    assert resultado.get("aliquota_efetiva_percentual") == aliquota_esperada