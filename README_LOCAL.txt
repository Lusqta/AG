# Instalação e Execução - Dealership CRM (Modo Local)

## 1. Instalação Inicial
Se esta for a primeira vez rodando neste computador:

1. Abra o terminal (CMD) nesta pasta.
2. Crie o ambiente virtual:
   python -m venv venv
3. Ative o ambiente:
   venv\Scripts\activate
4. Instale as dependências:
   pip install -r requirements.txt
5. Prepare o banco de dados:
   python manage.py migrate

## 2. Como Rodar no Dia a Dia
Basta clicar duas vezes no arquivo `start.bat`.

O sistema abrirá um terminal preto (não feche ele) e ficará disponível em:
http://127.0.0.1:8000

## 3. Criar ícone de App
Para criar um ícone na área de trabalho que parece um aplicativo:
1. Abra o sistema no Chrome/Edge.
2. Vá em Menu > Mais Ferramentas > Criar Atalho.
3. Marque "Abrir como janela".
