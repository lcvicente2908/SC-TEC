# SalesInsight PY — Pipeline de Análise de Dados de Vendas

O **SalesInsight PY** é um mini-projeto desenvolvido em Python para demonstrar um pipeline modular de análise de dados de vendas, utilizando recursos nativos da linguagem para leitura, tratamento, transformação, agregação e exportação de dados.

## 📁 Estrutura do Projeto

```text
MINI-PROJETO/
├── modulo_vendas.py       # Funções de processamento e análise de vendas
├── main.py                # Ponto de entrada e orquestrador do pipeline
├── Gerador_de_dataset.py  # Script para geração de dados sintéticos
├── vendas.csv             # Base de dados de entrada
├── README.md              # Documentação do projeto
└── outputs/               # Diretório com os relatórios gerados
    ├── metricas_resumo.csv
    └── estatisticas.json
```

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3 instalado.
- Visual Studio Code ou outro editor de código.
- Terminal com acesso ao diretório do projeto.

### 2. Acessar o diretório

Abra o terminal e navegue até a pasta do projeto:

```bash
cd MINI-PROJETO
```

### 3. Gerar a base de dados

Caso o arquivo `vendas.csv` ainda não exista, execute:

```bash
python Gerador_de_dataset.py
```

### 4. Executar o pipeline

Execute o arquivo principal:

```bash
python main.py
```

O programa realizará o processamento dos dados e gerará os relatórios definidos no pipeline.

## 📊 Arquivos de Saída

Os resultados são armazenados no diretório `outputs/`.

| Arquivo | Descrição |
|---|---|
| `metricas_resumo.csv` | Arquivo com as métricas e os indicadores resumidos de vendas. |
| `estatisticas.json` | Arquivo com as estatísticas consolidadas em formato JSON. |

## 🧩 Componentes do Projeto

- **`main.py`**: coordena a execução das etapas do pipeline.
- **`modulo_vendas.py`**: centraliza as funções de leitura, tratamento, análise e exportação dos dados.
- **`Gerador_de_dataset.py`**: gera uma base de dados sintética para testes e demonstrações.
- **`vendas.csv`**: contém os dados utilizados na análise.
- **`outputs/`**: armazena os arquivos resultantes do processamento.

## 🎯 Objetivos do Projeto

- Praticar programação em Python.
- Aplicar modularização e organização de código.
- Trabalhar com arquivos CSV e JSON.
- Automatizar etapas de processamento de dados.
- Gerar indicadores e estatísticas para apoiar a análise de vendas.
- Desenvolver conhecimentos aplicáveis a projetos de análise de dados e automação.

## 👨‍💻 Autor

**Luiz Carlos Vicente**

Projeto desenvolvido para fins de estudo e demonstração de conhecimentos em Python, análise de dados e automação.
