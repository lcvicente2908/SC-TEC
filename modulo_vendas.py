import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def obter_caminho_abs(caminho_relativo):
    """Resolve um caminho relativo à pasta do projeto."""
    caminho = Path(caminho_relativo)
    if caminho.is_absolute():
        return str(caminho)
    return str(BASE_DIR / caminho)


def carregar_csv(caminho_arquivo="vendas.csv"):
    """Carrega o arquivo CSV e devolve uma lista de dicionários."""
    caminho = obter_caminho_abs(caminho_arquivo)
    with open(caminho, "r", newline="", encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def inspecionar_dados(dados):
    """Mostra quantidade de registros e campos vazios."""
    print("\n=== INSPEÇÃO DOS DADOS ===")
    print(f"Registros carregados: {len(dados)}")

    if not dados:
        print("A base não possui registros.")
        return

    campos = list(dados[0].keys())
    total_nulos = 0
    for campo in campos:
        nulos_campo = sum(
            1 for registro in dados
            if registro.get(campo) is None or str(registro.get(campo, "")).strip() == ""
        )
        total_nulos += nulos_campo
        if nulos_campo:
            print(f"Campo '{campo}': {nulos_campo} valor(es) vazio(s)")

    linhas_incompletas = sum(
        1 for registro in dados
        if any(str(registro.get(campo, "")).strip() == "" for campo in campos)
    )
    print(f"Linhas com pelo menos um campo vazio: {linhas_incompletas}")
    print(f"Total de células vazias: {total_nulos}")


def limpar_dados(dados_brutos):
    """Remove registros sem quantidade/preço e converte os tipos numéricos."""
    dados_limpos = []
    descartados = 0

    for linha in dados_brutos:
        try:
            quantidade_texto = str(linha.get("quantidade", "")).strip()
            preco_texto = str(linha.get("preco_unitario", "")).strip()

            if not quantidade_texto or not preco_texto:
                descartados += 1
                continue

            quantidade = int(quantidade_texto)
            preco_unitario = float(preco_texto.replace(",", "."))

            if quantidade <= 0 or preco_unitario < 0:
                descartados += 1
                continue

            registro = {
                chave: (valor.strip() if isinstance(valor, str) else valor)
                for chave, valor in linha.items()
            }
            registro["id_venda"] = int(registro["id_venda"])
            registro["quantidade"] = quantidade
            registro["preco_unitario"] = preco_unitario
            dados_limpos.append(registro)

        except (ValueError, TypeError, KeyError):
            descartados += 1

    print("\n=== LIMPEZA DOS DADOS ===")
    print(f"Registros válidos: {len(dados_limpos)}")
    print(f"Registros descartados: {descartados}")
    return dados_limpos


def criar_campos_derivados(dados):
    """Cria receita_total e faixa_preco para cada venda."""
    dados_transformados = []

    for registro in dados:
        novo = registro.copy()
        novo["receita_total"] = round(
            novo["quantidade"] * novo["preco_unitario"], 2
        )
        receita = novo["receita_total"]

        if receita < 500:
            faixa = "Baixo"
        elif receita <= 2000:
            faixa = "Médio"
        else:
            faixa = "Alto"

        novo["faixa_preco"] = faixa
        dados_transformados.append(novo)

    return dados_transformados


def processar_transformacao(dados, funcao_transformacao):
    """Aplica uma função de transformação a cada registro."""
    return [funcao_transformacao(registro) for registro in dados]


def calcular_metricas(dados):
    """Calcula faturamento geral, por categoria e por região."""
    total_geral = 0.0
    por_categoria = {}
    por_regiao = {}

    for registro in dados:
        receita = float(registro["receita_total"])
        categoria = registro["categoria"]
        regiao = registro["regiao"]

        total_geral += receita
        por_categoria[categoria] = por_categoria.get(categoria, 0.0) + receita
        por_regiao[regiao] = por_regiao.get(regiao, 0.0) + receita

    return {
        "faturamento_global": round(total_geral, 2),
        "receita_por_categoria": {
            chave: round(valor, 2) for chave, valor in sorted(por_categoria.items())
        },
        "receita_por_regiao": {
            chave: round(valor, 2) for chave, valor in sorted(por_regiao.items())
        },
        "quantidade_vendas_validas": len(dados),
    }


def segmentar_clientes(dados):
    """Soma o gasto de cada cliente e classifica em Bronze, Prata ou Ouro."""
    gastos = {}

    for registro in dados:
        cliente = registro["cliente"]
        gastos[cliente] = gastos.get(cliente, 0.0) + float(registro["receita_total"])

    segmentos = {}
    for cliente, total in gastos.items():
        if total < 3000:
            segmento = "Bronze"
        elif total <= 8000:
            segmento = "Prata"
        else:
            segmento = "Ouro"

        segmentos[cliente] = {
            "total_gasto": round(total, 2),
            "segmento": segmento,
        }

    return segmentos


def obter_top_clientes(segmentos, top_n=5):
    """Retorna um dicionário com até top_n clientes de cada segmento."""
    clientes_por_segmento = {
        "Ouro": [],
        "Prata": [],
        "Bronze": [],
    }

    for cliente, info in segmentos.items():
        nome_segmento = info["segmento"]
        if nome_segmento in clientes_por_segmento:
            clientes_por_segmento[nome_segmento].append((cliente, info))

    for nome_segmento, lista in clientes_por_segmento.items():
        lista.sort(key=lambda item: item[1]["total_gasto"], reverse=True)
        clientes_por_segmento[nome_segmento] = lista[:top_n]

    return clientes_por_segmento


def exportar_resultados(metricas, clientes, top_clientes, pasta_saida="outputs"):
    """Exporta resumo em CSV e estatísticas/clientes em JSON."""
    pasta = Path(obter_caminho_abs(pasta_saida))
    pasta.mkdir(parents=True, exist_ok=True)

    caminho_csv = pasta / "metricas_resumo.csv"
    with caminho_csv.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Tipo", "Nome", "Receita Total (R$)"])
        escritor.writerow(["Geral", "Faturamento Global", metricas["faturamento_global"]])

        for categoria, receita in metricas["receita_por_categoria"].items():
            escritor.writerow(["Categoria", categoria, receita])

        for regiao, receita in metricas["receita_por_regiao"].items():
            escritor.writerow(["Região", regiao, receita])

    caminho_json = pasta / "estatisticas.json"
    top_serializavel = {
        segmento: [
            {"cliente": cliente, **info}
            for cliente, info in lista
        ]
        for segmento, lista in top_clientes.items()
    }

    resultado = {
        "metricas_gerais": metricas,
        "clientes": clientes,
        "top_clientes_por_segmento": top_serializavel,
    }

    with caminho_json.open("w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, indent=4, ensure_ascii=False)

    print("\n=== ARQUIVOS EXPORTADOS ===")
    print(f"CSV:  {caminho_csv}")
    print(f"JSON: {caminho_json}")
    return str(caminho_csv), str(caminho_json)
