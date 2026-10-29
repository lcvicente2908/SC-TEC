# SalesInsight PY - Pipeline de Análise de Dados de Vendas

Proposta de pipeline simples e modularizado para tratamento, transformação e agregação de dados de vendas utilizando recursos nativos da linguagem Python.

## 📁 Estrutura do Projeto - Luiz Carlos Vicente

- `main.py`: Ponto de entrada do projeto.
- `modulo_vendas.py`: Módulo contendo as funções de leitura, tratamento e exportação.
- `Gerador_de_dataset.py`: Script auxiliar para geração de dados sintéticos.
- `vendas.csv`: Dataset sintético de vendas.
- `outputs/`: Diretório contendo os relatórios finais em CSV e JSON.

MINI-PROJETO/
│
├── modulo_vendas.py       # Módulo contendo as funções de processamento
├── main.py                # Ponto de entrada (orquestrador do pipeline)
├── Gerador_de_dataset.py  # Utilitário isolado para geração do CSV
├── vendas.csv             # Base de dados de entrada (gerada automaticamente)
├── README.md              # Documentação executiva do projeto
└── outputs/               # Diretório contendo os relatórios finais
    ├── metricas_resumo.csv
    └── estatisticas.json

## 🚀 Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Abra o terminal no diretório do projeto no VS Code.
3. Execute o pipeline com o comando:
   ```bash
   python main.py