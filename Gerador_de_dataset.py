import csv
import random

def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=150, seed=42):
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {
        "Notebook": "Eletrônicos", 
        "Smartphone": "Celulares", 
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos", 
        "Teclado": "Acessórios", 
        "Mouse": "Acessórios"
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    
    cabecalho = ["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]
    dados = []
    
    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        # Inserindo nulos pontuais para testar a limpeza
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else "" 
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod
        
        dados.append([
            i, 
            f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            f"Cliente_{random.randint(1, 30):03d}", 
            prod_nome,
            categorias.get(prod, "Outros"), 
            random.choice(regioes), 
            qtd, 
            preco
        ])
        
    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerows(dados)
        
    print(f"[OK] Dataset gerado com sucesso em: {caminho_arquivo}")

if __name__ == "__main__":
    gerar_dataset_sintetico()