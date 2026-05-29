# 🚀 Sistema de Conciliação Bancária Automatizado

Este é um projeto prático de automação financeira desenvolvido em **Python** e integrado com o banco de dados **MySQL**. O objetivo principal é facilitar o dia a dia do setor financeiro, automatizando o processo de cruzamento de dados entre as faturas/vendas registradas e o extrato bancário real.

O sistema elimina o trabalho manual de conferência "linha por linha", reduzindo o erro humano e realizando o processamento e a atualização de milhares de registros em poucos segundos.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Python 3**: Linguagem base para a construção da lógica do script.
* **Pandas**: Biblioteca utilizada para manipulação de dados e leitura de arquivos externos (`.xlsx`).
* **MySQL**: Banco de dados relacional onde as tabelas de controle são criadas e os status são atualizados.
* **mysql-connector-python**: Driver de conexão para fazer a ponte de comunicação entre o Python e o banco de dados.

---

## ⚙️ Como o Sistema Funciona na Prática

1. **Modelagem de Dados Automatizada**: O script garante a criação do banco de dados `conciliacao_bancaria` e das tabelas estruturadas (`vendas_sistema` e `extrato_bancario`). A cada execução, ele limpa resquícios anteriores (`TRUNCATE`) para evitar duplicidade de registros.
2. **Ingestão de Dados (Pandas)**: O Python lê a planilha de vendas reais em Excel e injeta as informações dinamicamente no banco MySQL.
3. **Cruzamento Inteligente (SQL via Python)**: Utilizando uma query estruturada com `INNER JOIN` e tratamento de tipos (`CAST AS DECIMAL`), o sistema varre o banco comparando os valores exatos das faturas contra as movimentações do extrato, centavo por centavo.
4. **Atualização Automática de Status**: Ao identificar o "match perfeito", o Python dispara comandos de `UPDATE` diretamente no banco de dados, alterando o status da venda de **'Pendente'** para **'Conciliado'**. O que não for localizado no extrato continua marcado como **'Pendente'** para fácil auditoria.

---

## 📂 Estrutura do Projeto

* `bancario.py`: Código-fonte principal com todo o fluxo de automação, ingestão e conciliação.
* `planilha_vendas_sistema.xlsx`: Arquivo de dados simulando o relatório de faturamento da empresa.
* `README.md`: Documentação explicativa do projeto.

---

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o MySQL Server instalado e rodando em sua máquina local.
2. Instale as dependências necessárias via terminal:
   ```bash
   pip install mysql-connector-python pandas openpyxl