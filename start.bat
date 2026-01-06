@echo off
title Dealership CRM
cd /d "%~dp0"

echo ========================================================
echo                 DEALERSHIP CRM - INICIO
echo ========================================================
echo.
echo [INSTRUCOES IMPORTANTES]
echo 1. Se ocorrer erro de dependencia (ModuleNotFoundError), execute:
echo    pip install -r requirements.txt
echo.
echo 2. Para preencher o sistema com dados de teste (carros, vendas):
echo    Execute o comando: py populate_rich.py
echo.
echo 3. Para deixar o banco de dados "novo em folha" (vazio):
echo    Delete o arquivo 'db.sqlite3' nesta pasta e execute:
echo    py manage.py migrate
echo    (Ou use: py scripts/wipe_data.py para limpar mantendo usuarios)
echo.
echo ========================================================
echo.
echo Iniciando servidor...
echo Acesse em: http://127.0.0.1:8000
echo.
py manage.py runserver 127.0.0.1:8000
pause
