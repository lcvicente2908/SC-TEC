# SalesInsight PY — Análise de Vendas

Projeto didático de análise de vendas usando apenas a biblioteca padrão do Python (`csv`, `json`, `random`, `pathlib` e `datetime`).

## Arquivos

- `main.py`: ponto de entrada e execução do pipeline.
- `modulo_vendas.py`: leitura, inspeção, limpeza, transformação, métricas, segmentação e exportação.
- `Gerador_de_dataset.py`: geração do arquivo sintético `vendas.csv`.
- `vendas.csv`: criado automaticamente na primeira execução.
- `outputs/metricas_resumo.csv`: métricas de faturamento por categoria e região.
- `outputs/estatisticas.json`: métricas, segmentação de todos os clientes e top 5 por segmento.

## Segmentação de clientes

- **Bronze:** gasto acumulado abaixo de R$ 3.000.
- **Prata:** gasto acumulado de R$ 3.000 até R$ 8.000, inclusive.
- **Ouro:** gasto acumulado acima de R$ 8.000.

O dataset sintético é construído para permitir demonstrar os três segmentos, sem mudar esses limites. Se `vendas.csv` já existir, o programa o utilizará em vez de substituí-lo.

## Como executar

No terminal, dentro desta pasta:

```bash
python3 main.py
```

A aplicação criará `vendas.csv` se necessário, processará os dados e criará a pasta `outputs/` com os relatórios.

## Observação

Os dados gerados são fictícios e servem apenas para aprendizado e teste do pipeline.
