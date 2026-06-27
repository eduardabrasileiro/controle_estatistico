# MVP - Controle Estatístico da Qualidade aplicado ao consumo de energia elétrica

Este repositório contém um mínimo produto viável em Python/Google Colab para aplicar conceitos de estatística estratégica e Controle Estatístico do Processo (CEP) a uma base de consumo de energia elétrica.

## Estudo de caso

O projeto monitora a variabilidade mensal do consumo de energia elétrica por consumidor em uma Unidade Federativa e em uma classe de consumo. O recorte inicial do MVP é:

- UF: DF
- Tipo de consumo: Residencial
- Janela: últimos 60 meses disponíveis
- Indicador: `consumo_por_consumidor = consumo / numero_consumidores`

A ideia é evitar olhar apenas para consumo bruto, pois o consumo bruto pode crescer simplesmente porque o número de consumidores cresceu. O indicador normalizado permite uma análise mais comparável ao longo do tempo.

## Referencial teórico

O projeto foi construído com base em conceitos de Controle Estatístico da Qualidade, especialmente:

- variabilidade como elemento central da qualidade;
- estatística descritiva aplicada à qualidade;
- gráficos de controle para observações individuais;
- identificação de possíveis causas especiais;
- lógica de melhoria contínua e DMAMC/DMAIC.

Referência principal: Montgomery, Douglas C. *Introdução ao Controle Estatístico da Qualidade*. 7ª ed. Rio de Janeiro: LTC, 2017.

## Estrutura do repositório

```text
.
├── data/
│   └── consumo_energia_eletrica.csv
├── notebooks/
│   └── controle_estatistico_energia_mvp.ipynb
├── src/
│   └── cep_utils.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
jupyter notebook notebooks/controle_estatistico_energia_mvp.ipynb
```

## O que o notebook faz

1. Carrega a base de dados.
2. Valida tipos, datas, valores nulos e duplicatas.
3. Remove duplicatas exatas.
4. Mostra estatística descritiva.
5. Evita dupla contagem entre `Total` e subcategorias.
6. Cria o indicador `consumo_por_consumidor`.
7. Aplica gráfico de controle I-MR.
8. Simula aumento de 20% nos últimos 6 meses.
9. Detecta alertas de possíveis causas especiais.
10. Resume limitações e próximos passos.

## Observações metodológicas

A base contém categorias como `Total`, `Cativo`, `Residencial`, `Comercial`, `Industrial` e `Outros`. Por isso, não se deve somar todas as categorias de forma indiscriminada, pois isso pode gerar dupla contagem. Para consumo agregado, o notebook usa apenas `tipo_consumo == "Total"`. Para análise por consumidor, usa classes com `numero_consumidores` preenchido, como `Residencial`.
