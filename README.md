# 🚗 Dealership CRM - Sistema de Gestão de Concessionária

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

O **Dealership CRM** é uma solução completa para gestão de concessionárias, focada em simplicidade e controle.

---

## ✨ Funcionalidades Comprovadas

- **KPIs em Tempo Real:** Faturamento, Veículos Vendidos, Veículos Disponíveis e Leads.
- **Gráficos Interativos:** Evolução de Vendas (Diária/Mensal), Vendas por Marca e Top Vendedores.
- **Tabela Recente:** Visualização rápida das últimas 5 vendas.
- **Backup Rápido:** Widget flutuante para exportação e restauração do banco de dados (Json).

### 🚘 Gestão de Veículos (Inventário)
- **Cadastro Completo:** Marca, modelo, ano, preço, VIN, cor, quilometragem e descrição.
- **Imagens:** Upload de arquivo ou URL externa.
- **Busca:** Pesquisa por Marca, Modelo ou VIN.
- **Status Automático:** *Disponível, Vendido, Em Manutenção*.
- **Controle de Exclusão:** Apenas **Gerentes** podem excluir veículos (e apenas se não estiverem vendidos).

### 👥 Gestão de Clientes
- **Cadastro:** Registro rápido de novos clientes com atribuição automática ao vendedor.
- **Listagem e Busca:** Filtre por nome, e-mail ou telefone.
- **Detalhes:** Visualize informações de contato e histórico completo de compras do cliente.
- **Exclusão:** Apenas **Gerentes** podem excluir clientes (protegido se houver vendas vinculadas).
- **Nota:** Edição de clientes disponível via painel Admin.

### 💰 Gestão de Vendas
- **Fluxo Automatizado:** Registrar uma venda automaticamente marca o veículo como "Vendido" e o cliente como "Comprou".
- **Pagamentos Flexíveis:** Suporte para Crédito, Débito e PIX, com cálculo de parcelas.
- **Histórico:** Lista completa com filtros por Data, Vendedor e Pesquisa textual.
- **Edição Inteligente:** Se você alterar o veículo de uma venda, o sistema reverte o status do veículo anterior para "Disponível" automaticamente.
- **Cancelamento:** Apenas **Gerentes** podem excluir vendas (o veículo volta automaticamente para o estoque).

### 📈 Relatórios (Excel)
- **Exportação Flexível:** Gere planilhas Excel `.xlsx`.
- **Modos:**
    - *Relatório Simples:* Lista de dados.
    - *Relatório Executivo:* Inclui Dashboard, KPIs e Gráficos dentro do Excel.

### 🛡️ Gestão de Usuários e Permissões
O sistema possui 3 níveis de acesso bem definidos:

1.  **Vendedor (Padrão):**
    - Pode cadastrar Clientes e Veículos.
    - Pode registrar Vendas.
    - **NÃO PODE** excluir registros.
    - **NÃO PODE** acessar gestão de usuários.

2.  **Gerente (Grupo "Gerentes"):**
    - Tudo o que o Vendedor faz.
    - **Pode EXCLUIR** Veículos, Clientes e Vendas.
    - **Pode CRIAR e EDITAR** outros usuários (Vendedores/Gerentes).
    - *Nota: Gerentes não podem excluir usuários (apenas Admin).*

3.  **Administrador (Superuser):**
    - Acesso total ao sistema e ao painel `/admin` do Django.
    - Único capaz de **Excluir Usuários**.

---

## 🚀 Como Executar

### Pré-requisitos
- Python instalado.
- Dependências instaladas (`pip install -r requirements.txt`).

### Iniciando o Servidor
1. Execute o script **`start.bat`** (Windows).
2. Ou use o comando:
   ```bash
   python manage.py runserver
   ```
3. Acesse: `http://127.0.0.1:8000`

### Credenciais Iniciais
- **Admin:** `admin` / `admin1234`

---

## 🛠️ Tecnologias
- **Backend:** Django 5
- **Banco:** SQLite3
- **Frontend:** Bootstrap 5 + FontAwesome
- **Gráficos:** Chart.js
- **Exportação:** XlsxWriter
