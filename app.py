import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "catalogo-filmes"  # necessário para mostrar as mensagens na tela

# O banco fica guardado em um arquivo chamado filmes.db, ao lado deste código
PASTA = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(PASTA, "filmes.db")


# ------------------------------------------------------------
# Banco de dados
# ------------------------------------------------------------
def conectar():
    """Abre uma conversa com o banco de dados."""
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row  # deixa pegar os dados pelo nome: filme["titulo"]
    return conexao


def criar_tabela():
    """Cria a tabela de filmes, caso ela ainda não exista."""
    conexao = conectar()
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS filmes (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT    NOT NULL,
            genero TEXT    NOT NULL,
            ano    INTEGER NOT NULL,
            nota   INTEGER NOT NULL
        )
        """
    )
    conexao.commit()
    conexao.close()


def dados_estao_certos(form):
    """Confere se o que a pessoa digitou faz sentido.
    Devolve uma mensagem de erro, ou None se estiver tudo certo."""
    if not form["titulo"].strip() or not form["genero"].strip():
        return "Ei, faltou preencher o título ou o gênero."
    if not form["ano"].isdigit() or not form["nota"].isdigit():
        return "O ano e a nota precisam ser números."
    if not 1 <= int(form["nota"]) <= 10:
        return "A nota precisa ficar entre 1 e 10."
    return None


# ------------------------------------------------------------
# Páginas do sistema (CRUD)
# ------------------------------------------------------------
@app.route("/")
def index():
    """LISTAR: mostra todos os filmes cadastrados."""
    conexao = conectar()
    filmes = conexao.execute("SELECT * FROM filmes ORDER BY titulo").fetchall()
    conexao.close()
    return render_template("index.html", filmes=filmes)


@app.route("/novo", methods=["GET", "POST"])
def novo():
    """CADASTRAR: mostra o formulário (GET) e salva o filme (POST)."""
    if request.method == "POST":
        erro = dados_estao_certos(request.form)
        if erro:
            flash(erro, "erro")
            return render_template("form.html", filme=request.form, editando=False)

        conexao = conectar()
        conexao.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (
                request.form["titulo"].strip(),
                request.form["genero"].strip(),
                int(request.form["ano"]),
                int(request.form["nota"]),
            ),
        )
        conexao.commit()
        conexao.close()
        flash("Pronto! Filme cadastrado. 🎉", "ok")
        return redirect(url_for("index"))

    return render_template("form.html", filme=None, editando=False)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """EDITAR: mostra o formulário já preenchido (GET) e atualiza o filme (POST)."""
    conexao = conectar()
    filme = conexao.execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()

    if filme is None:
        conexao.close()
        flash("Não encontrei esse filme.", "erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        erro = dados_estao_certos(request.form)
        if erro:
            conexao.close()
            flash(erro, "erro")
            return render_template("form.html", filme=request.form, editando=True)

        conexao.execute(
            "UPDATE filmes SET titulo = ?, genero = ?, ano = ?, nota = ? WHERE id = ?",
            (
                request.form["titulo"].strip(),
                request.form["genero"].strip(),
                int(request.form["ano"]),
                int(request.form["nota"]),
                id,
            ),
        )
        conexao.commit()
        conexao.close()
        flash("Tudo certo! Filme atualizado. ✅", "ok")
        return redirect(url_for("index"))

    conexao.close()
    return render_template("form.html", filme=filme, editando=True)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    """EXCLUIR: apaga o filme da lista."""
    conexao = conectar()
    conexao.execute("DELETE FROM filmes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    flash("Filme removido da lista.", "ok")
    return redirect(url_for("index"))


# Cria a tabela assim que o app começa (local e no Render)
criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)
