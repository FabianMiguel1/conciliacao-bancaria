import mysql.connector
import pandas as pd

# 1. CONEXÃO COM O BANCO DE DADOS
conexao = mysql.connector.connect(
    host="Localhost",
    user="root",
    password="Fabian003$"
)
cursor = conexao.cursor()

# 2. CRIAÇÃO E SELEÇÃO DO BANCO
cursor.execute("CREATE DATABASE IF NOT EXISTS conciliacao_bancaria")
cursor.execute("USE conciliacao_bancaria")

# 3. CRIAÇÃO DAS TABELAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    status_conciliacao VARCHAR(50) DEFAULT 'Pendente'
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS extrato_bancario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_movimentacao DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL
);
""")

# 4. LIMPADOR DE TABELAS
cursor.execute("TRUNCATE TABLE vendas_sistema")
cursor.execute("TRUNCATE TABLE extrato_bancario")
conexao.commit()

df_vendas = pd.read_excel("planilha_vendas_sistema.xlsx")

print("\nSalvando as 20 vendas da planilha no banco de dados...")
for index, linha in df_vendas.iterrows():
    comando_sql = "INSERT INTO vendas_sistema (data_venda, descricao, valor) VALUES (%s, %s, %s)"
    valores = (linha['data_venda'], linha['descricao'], float(linha['valor']))
    cursor.execute(comando_sql, valores)
conexao.commit()

# 6. GERANDO O EXTRATO COPIANDO OS VALORES REAIS 
print("Gerando extrato baseado nos valores reais da sua planilha...")
dados_banco = []

for index, linha in df_vendas.head(3).iterrows():
    dados_banco.append({
        "data_movimentacao": str(linha['data_venda']),
        "descricao": f"PIX RECEBIDO - REF {linha['descricao']}",
        "valor": float(linha['valor'])
    })

df_extrato = pd.DataFrame(dados_banco)

for index, linha in df_extrato.iterrows():
    comando_sql_extrato = "INSERT INTO extrato_bancario (data_movimentacao, descricao, valor) VALUES (%s, %s, %s)"
    valores_extrato = (linha['data_movimentacao'], linha['descricao'], float(linha['valor'])) 
    cursor.execute(comando_sql_extrato, valores_extrato) 
conexao.commit() 

# 7. --- INÍCIO DA CONCILIAÇÃO BANCÁRIA ---
print("\n--- INICIANDO CRUZAMENTO DE DADOS (CONCILIAÇÃO) ---")

query_conciliacao = """
SELECT v.id, v.data_venda, v.descricao, v.valor, e.descricao 
FROM vendas_sistema v
INNER JOIN extrato_bancario e ON CAST(v.valor AS DECIMAL(10,2)) = CAST(e.valor AS DECIMAL(10,2))
"""
cursor.execute(query_conciliacao)
resultados = cursor.fetchall()

print(f"Encontrados {len(resultados)} matches perfeitos de valores!")

print("\nExibindo e atualizando os dados conciliados no banco...")
for item in resultados:
    id_venda = item[0]
    valor = item[3]
    desc_sistema = item[2]
    desc_banco = item[4]
    
    print(f"Conciliando ID {id_venda} (R$ {valor}) -> {desc_sistema} com {desc_banco}")
    
    comando_update = "UPDATE vendas_sistema SET status_conciliacao = 'Conciliado' WHERE id = %s"
    cursor.execute(comando_update, (id_venda,))

conexao.commit()
print("\n[SUCESSO ABSOLUTO] O banco de dados foi atualizado!")