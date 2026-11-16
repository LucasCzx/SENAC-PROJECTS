# 🎬 Catálogo de Filmes

Sistema web CRUD desenvolvido com **Python (Flask)** e **SQLite**, publicado no **Render**.

**Autor:** Lucas Carlos

## Funcionalidades
- Cadastrar filme (título, gênero, ano e nota de 1 a 10)
- Listar todos os filmes
- Editar um filme existente
- Excluir um filme

## Como rodar localmente
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000

## Deploy no Render
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

> O SQLite no Render é temporário: os dados são apagados quando o serviço reinicia.
