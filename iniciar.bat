@echo off
cd /d "%~dp0"
echo Instalando o Flask (so precisa na primeira vez)...
python -m pip install -r requirements.txt
echo.
echo Abrindo o sistema! Acesse: http://127.0.0.1:5000
echo (feche esta janela para parar o servidor)
echo.
python app.py
pause
