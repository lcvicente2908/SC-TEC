import csv
import json
import os
import random

# Direciona para a pasta onde este arquivo .py está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def obter_caminho_abs(caminho_relativo):
    """Garante a resolução do caminho absoluto baseado na pasta do projeto."""
    return os.path.join(BASE_DIR, caminho_relativo)


# RF01 - Criar o Dataset de Vendas Sintético
def gerar_dataset_sintetico(
    caminho_arquivo="vendas.csv", n_registros=150, seed=42
):
    random.seed(seed)
    produtos = [
        "Notebook",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse",
    ]
    categorias = {
        "Notebook": "Eletrônicos",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos",
        "Teclado": "Acessórios",
        "Mouse": "Acessórios",
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    cabecalho = [
        "id_venda",
        "data_venda",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario",
    ]
    dados = []

    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        qtd = (
            str(random.randint(1, 8)) if random.random() > 0.05 else ""
        )  # Inserindo nulos sintéticos
        preco = (
            str(round(random.uniform(100, 3500), 2))
            if random.random() > 0.05
            else ""
        )
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod

        dados.append([
            i,
            f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"Cliente_{random.randint(1, 30):03d}",
            prod_nome,
            categorias.get(prod, "Outros"),
            random.choice(regioes),
            qtd,
            preco,
        ])

    caminho_completo = obter_caminho_abs(caminho_arquivo)
    with open(caminho_completo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerows(dados)

    print(f"[OK] Dataset gerado em: {caminho_completo}")


# RF07 - Carregar CSV
def carregar_csv(caminho_arquivo="vendas.csv"):
    caminho_completo = obter_caminho_abs(caminho_arquivo)
    dados = []
    with open(caminho_completo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    return dados


# RF02 - Inspecionar os Dados
def inspecionar_dados(dados):
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if dados:
        print(f"Campos disponíveis: {list(dados[0].keys())}")
        print(f"Exemplo do primeiro registro: {dados[0]}")


# RF03 - Limpar e Tratar os Dados
def limpar_dados(dados_brutos):
    dados_limpos = []
    removidos = 0
    for lin in dados_brutos:
        prod = lin["produto"].strip()
        cat = lin["categoria"].strip()
        reg = lin["regiao"].strip()
        cli = lin["cliente"].strip()

        if not lin["quantidade"] or not lin["preco_unitario"]:
            removidos += 1
            continue

        try:
            qtd = int(lin["quantidade"])
            preco = float(lin["preco_unitario"])
            dados_limpos.append({
                "id_venda": int(lin["id_venda"]),
                "data_venda": lin["data_venda"].strip(),
                "cliente": cli,
                "produto": prod,
                "categoria": cat,
                "regiao": reg,
                "quantidade": qtd,
                "preco_unitario": preco,
            })
        except ValueError:
            removidos += 1

    print(f"\n=== RELATÓRIO DE LIMPEZA ===")
    print(
        f"Registros Válidos: {len(dados_limpos)} | Registros Removidos:"
        f" {removidos}"
    )
    return dados_limpos


# RF04 - Criar Campos Derivados
def criar_campos_derivados(dados):
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita

        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"
    return dados


def processar_transformacao(dados, funcao_transformacao):
    return [funcao_transformacao(item) for item in dados]


# RF05 - Calcular Métricas Agregadas
def calcular_metricas(dados):
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        cat = item["categoria"]
        reg = item["regiao"]
        rec = item["receita_total"]

        receita_categoria[cat] = round(
            receita_categoria.get(cat, 0.0) + rec, 2
        )
        receita_regiao[reg] = round(receita_regiao.get(reg, 0.0) + rec, 2)
        total_geral += rec

    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao,
    }


# RF06 - Segmentar Clientes por Nível de Gasto
def segmentar_clientes(dados):
    gastos_cliente = {}
    for item in dados:
        cli = item["cliente"]
        gastos_cliente[cli] = (
            gastos_cliente.get(cli, 0.0) + item["receita_total"]
        )

    segmentos = {}
    for cli, total in gastos_cliente.items():
        if total > 8000:
            cat = "Ouro"
        elif total >= 3000:
            cat = "Prata"
        else:
            cat = "Bronze"
        segmentos[cli] = {"total_gasto": round(total, 2), "segmento": cat}
    return segmentos


def obter_top_clientes(segmentos, top_n=5):
    clientes_ordenados = sorted(
        segmentos.items(), key=lambda item: item[1]["total_gasto"], reverse=True
    )
    return clientes_ordenados[:top_n]


# RF07 - Exportar Resultados
def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    caminho_pasta = obter_caminho_abs(pasta_saida)
    os.makedirs(caminho_pasta, exist_ok=True)

    caminho_json = os.path.join(caminho_pasta, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(
            {"metricas_gerais": metricas, "clientes": clientes},
            f,
            indent=4,
            ensure_ascii=False,
        )
    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")

    caminho_csv = os.path.join(caminho_pasta, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Categoria", "Receita Total"])
        for cat, rec in metricas["por_categoria"].items():
            escritor.writerow([cat, rec])
    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")
    print(f"[OK] validando CSV exportado em: {caminho_csv}")