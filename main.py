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
    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()