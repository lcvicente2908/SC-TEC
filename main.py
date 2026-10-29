<<<<<<< HEAD
import pathlib
import sys

# 1. Obtém o caminho absoluto resolvido da pasta onde está este script
DIRETORIO_ATUAL = pathlib.Path(__file__).resolve().parent

# 2. Converte para string e adiciona no início do sys.path
if str(DIRETORIO_ATUAL) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_ATUAL))

# 3. Agora a importação do modulo_vendas é 100% garantida
import modulo_vendas as mv


def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    arquivo_dados = "vendas.csv"
    caminho_abs_dados = mv.obter_caminho_abs(arquivo_dados)

    # 1. Gerar dataset sintético se não existir
    if not pathlib.Path(caminho_abs_dados).exists():
        print(
            f"[INFO] Arquivo '{arquivo_dados}' não encontrado. Gerando dataset"
            " sintético..."
        )
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150)
    else:
        print(f"[OK] Base de dados encontrada em: {caminho_abs_dados}")

    # 2. Leitura
    dados_brutos = mv.carregar_csv(arquivo_dados)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza e Transformação
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # 4. Uso de Função de Ordem Superior com Lambda
    dados_com_tag = mv.processar_transformacao(
        dados_transformados, lambda x: {**x, "processado": True}
    )

    # 5. Métricas e Segmentação
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 6. Exibição de Resultados
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")
    print("\nTop 5 Clientes:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # 7. Exportação dos Arquivos
    mv.exportar_resultados(metricas, segmentos)
=======
from pathlib import Path

import Gerador_de_dataset as gerador
import modulo_vendas as mv


BASE_DIR = Path(__file__).resolve().parent


def formatar_moeda(valor):
    """Formata valores no padrão brasileiro: R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    print("=" * 65)
    print(" SALESINSIGHT PY - Pipeline de Análise de Dados de Vendas")
    print("=" * 65)

    caminho_csv = BASE_DIR / "vendas.csv"

    # 1. Cria o dataset somente se ele ainda não existir.
    if not caminho_csv.exists():
        print("\n[INFO] vendas.csv não encontrado. Gerando dataset sintético...")
        gerador.gerar_dataset_sintetico(
            caminho_arquivo=caminho_csv,
            n_registros=150,
            seed=42,
        )
    else:
        print(f"\n[OK] Dataset encontrado: {caminho_csv}")

    # 2. Leitura e inspeção.
    dados_brutos = mv.carregar_csv(caminho_csv)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza, transformação e campo de controle.
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)
    dados_processados = mv.processar_transformacao(
        dados_transformados,
        lambda registro: {**registro, "processado": True},
    )

    # 4. Métricas, segmentação e top 5 por segmento.
    metricas = mv.calcular_metricas(dados_processados)
    clientes = mv.segmentar_clientes(dados_processados)
    top_clientes = mv.obter_top_clientes(clientes, top_n=5)

    print("\n=== MÉTRICAS GERAIS ===")
    print(f"Vendas válidas: {metricas['quantidade_vendas_validas']}")
    print(f"Faturamento global: {formatar_moeda(metricas['faturamento_global'])}")

    print("\nReceita por categoria:")
    for categoria, receita in metricas["receita_por_categoria"].items():
        print(f"  {categoria}: {formatar_moeda(receita)}")

    print("\nReceita por região:")
    for regiao, receita in metricas["receita_por_regiao"].items():
        print(f"  {regiao}: {formatar_moeda(receita)}")

    print("\n=== TOP 5 CLIENTES POR SEGMENTO ===")
    for segmento in ("Ouro", "Prata", "Bronze"):
        lista_clientes = top_clientes[segmento]
        print(f"\n--- TOP {len(lista_clientes)} CLIENTES {segmento.upper()} ---")

        if not lista_clientes:
            print("Nenhum cliente encontrado neste segmento.")
            continue

        for posicao, (cliente, info) in enumerate(lista_clientes, start=1):
            print(
                f"{posicao}. {cliente} | "
                f"Gasto: {formatar_moeda(info['total_gasto'])} | "
                f"Segmento: {info['segmento']}"
            )

    # 5. Exportação em CSV e JSON.
    mv.exportar_resultados(
        metricas,
        clientes,
        top_clientes,
        pasta_saida="outputs",
    )

>>>>>>> 7d835a1 (Projeto atualizado)
    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 7d835a1 (Projeto atualizado)
