# 🚗 Dealership CRM - Sistema de Gestão de Concessionária

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

Um sistema robusto e elegante de CRM (Customer Relationship Management) desenvolvido especialmente para concessionárias de veículos. O **Dealership CRM** permite gerenciar o inventário de veículos, acompanhar o funil de vendas de clientes e registrar transações de forma eficiente.

---

## ✨ Funcionalidades Principais

### � Painel de Controle (Dashboard)
- **KPIs em Tempo Real:** Acompanhe métricas vitais como Vendas Totais, Veículos Vendidos, Estoque Disponível e Leads Ativos.
- **Gráficos Interativos:** Visualização clara da Evolução Financeira, Vendas por Marca e Ranking de Vendedores.
- **Últimas Vendas:** Tabela de acesso rápido às transações mais recentes.

### 🚘 Gestão de Veículos (Inventário)
- **Cadastro Completo:** Registro de Marca, Modelo, Ano, Preço, VIN, Quilometragem e Cor.
- **Gestão de Imagens:** Suporte flexível para upload de fotos ou uso de URLs externas.
- **Busca Avançada:** Filtre rapidamente o estoque por qualquer característica do veículo.
- **Proteção de Estoque:** O sistema impede acidentalmente a exclusão de veículos que já constam como vendidos.

### � Gestão de Clientes (CRM)
- **Funil de Vendas:** Acompanhe a jornada do cliente (Lead -> Contatado -> Interessado -> Comprou).
- **Atribuição Inteligente:** Novos clientes são automaticamente vinculados ao vendedor que os cadastrou.
- **Histórico Integrado:** Visualize todas as compras anteriores diretamente no perfil do cliente.

### 💰 Gestão de Vendas & Automação
- **Fluxo Automatizado:** Ao registrar uma venda, o sistema automaticamente:
  1. Marca o veículo como "Vendido".
  2. Atualiza o status do cliente para "Comprou".
  3. Registra a data e valor da transação.
- **Filtros Poderosos:** Encontre vendas passadas por Data, Vendedor, Cliente ou Carro.

### 📊 Relatórios & Exportação
- **Excel Profissional:** Gerador de relatórios em `.xlsx` utilizando `xlsxwriter`.
- **Modos de Exportação:**
  - **Simples:** Lista tabular perfeita para conferência rápida.
  - **Executivo:** Planilha completa com Dashboard, Gráficos nativos do Excel e abas separadas de dados.
  
### 🛡️ Administração e Segurança
- **Controle de Acesso:** Permissões granulares para Gerentes (acesso total) e Vendedores.
- **Proteção de Dados:** Travas de segurança impedem a exclusão de usuários ou clientes que possuem registros financeiros vinculados.

---

## 🚀 Tecnologias Utilizadas

- **Framework:** [Django 5.0+](https://www.djangoproject.com/)
- **Linguagem:** [Python](https://www.python.org/)
- **Banco de Dados:** SQLite (Desenvolvimento)
- **Exportação:** [XlsxWriter](https://xlsxwriter.readthedocs.io/)
- **Frontend:** HTML5, CSS3, JavaScript e Bootstrap.

---

## 🛠️ Como Instalar e Rodar

### Pré-requisitos
- Python 3.10 ou superior instalada.

### Passo a Passo

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/Lusqta/AG.git
   cd dealership-crm
   ```

2. **Criar Ambiente Virtual (Recomendado)**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar Dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o Banco de Dados**
   ```bash
   python manage.py migrate
   ```


6. **(Opcional) Popular com Dados de Exemplo**
   ```bash
   python populate_data.py
   ```

7. **Iniciar o Servidor**
   ```bash
   python manage.py runserver
   ```
   Acesse o sistema em: `http://127.0.0.1:8000`

---

## 📁 Estrutura do Projeto

- `dealership_crm/`: Configurações centrais do Django.
- `sales/`: Aplicativo principal (Modelos de Vendas, Veículos e Clientes).
- `static/`: Arquivos estáticos (CSS, JS, Imagens).
- `templates/`: Arquivos HTML do sistema.
- `scripts/`: Scripts utilitários para manutenção de dados.

