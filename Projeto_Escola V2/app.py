from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)

app.secret_key = "chave_escola_123"

CAMINHO_BANCO = os.path.join(
    os.path.dirname(__file__),
    "escola.db"
)


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/alunos")
def alunos():

    conexao = conectar_banco()

    lista_alunos = conexao.execute("""
        SELECT *
        FROM alunos
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "alunos.html",
        alunos=lista_alunos
    )


@app.route("/alunos/cadastrar", methods=["POST"])
def cadastrar_aluno():

    nome = request.form["nome"]
    data_nascimento = request.form["data_nascimento"]
    email = request.form["email"]
    telefone = request.form["telefone"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO alunos
            (
                nome,
                data_nascimento,
                email,
                telefone
            )
            VALUES (?, ?, ?, ?)
        """, (
            nome,
            data_nascimento or None,
            email or None,
            telefone or None
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Aluno cadastrado com sucesso!",
            "sucesso"
        )

    except sqlite3.IntegrityError:

        flash(
            "Este e-mail já está cadastrado!",
            "erro"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao cadastrar aluno: {erro}",
            "erro"
        )

    return redirect(url_for("alunos"))

@app.route("/professores")
def professores():

    conexao = conectar_banco()

    lista_professores = conexao.execute("""
        SELECT *
        FROM professores
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "professores.html",
        professores=lista_professores
    )


@app.route("/professores/cadastrar", methods=["POST"])
def cadastrar_professor():

    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    especialidade = request.form["especialidade"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO professores
            (
                nome,
                email,
                telefone,
                especialidade
            )
            VALUES (?, ?, ?, ?)
        """, (
            nome,
            email or None,
            telefone or None,
            especialidade or None
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Professor cadastrado com sucesso!",
            "sucesso"
        )

    except sqlite3.IntegrityError:

        flash(
            "Este e-mail já está cadastrado!",
            "erro"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao cadastrar professor: {erro}",
            "erro"
        )

    return redirect(url_for("professores"))

@app.route("/turmas")
def turmas():

    conexao = conectar_banco()

    lista_turmas = conexao.execute("""
        SELECT *
        FROM turmas
        ORDER BY ano_letivo, nome
    """).fetchall()

    conexao.close()

    return render_template(
        "turmas.html",
        turmas=lista_turmas
    )


@app.route("/turmas/cadastrar", methods=["POST"])
def cadastrar_turma():

    nome = request.form["nome"]
    serie = request.form["serie"]
    turno = request.form["turno"]
    ano_letivo = request.form["ano_letivo"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO turmas
            (
                nome,
                serie,
                turno,
                ano_letivo
            )
            VALUES (?, ?, ?, ?)
        """, (
            nome,
            serie,
            turno,
            ano_letivo
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Turma cadastrada com sucesso!",
            "sucesso"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao cadastrar turma: {erro}",
            "erro"
        )

    return redirect(url_for("turmas"))


@app.route("/disciplinas")
def disciplinas():

    conexao = conectar_banco()

    lista_disciplinas = conexao.execute("""
        SELECT *
        FROM disciplinas
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "disciplinas.html",
        disciplinas=lista_disciplinas
    )


@app.route("/disciplinas/cadastrar", methods=["POST"])
def cadastrar_disciplina():

    nome = request.form["nome"]
    descricao = request.form["descricao"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO disciplinas
            (
                nome,
                descricao
            )
            VALUES (?, ?)
        """, (
            nome,
            descricao or None
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Disciplina cadastrada com sucesso!",
            "sucesso"
        )

    except sqlite3.IntegrityError:

        flash(
            "Esta disciplina já está cadastrada!",
            "erro"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao cadastrar disciplina: {erro}",
            "erro"
        )

    return redirect(url_for("disciplinas"))

@app.route("/matriculas")
def matriculas():

    conexao = conectar_banco()

    lista_matriculas = conexao.execute("""
        SELECT
            matriculas.id,
            alunos.nome AS aluno,
            turmas.nome AS turma,
            turmas.serie,
            turmas.turno,
            matriculas.data_matricula,
            matriculas.status
        FROM matriculas

        INNER JOIN alunos
            ON matriculas.aluno_id = alunos.id

        INNER JOIN turmas
            ON matriculas.turma_id = turmas.id

        ORDER BY alunos.nome
    """).fetchall()

    alunos = conexao.execute("""
        SELECT *
        FROM alunos
        ORDER BY nome
    """).fetchall()

    turmas = conexao.execute("""
        SELECT *
        FROM turmas
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "matriculas.html",
        matriculas=lista_matriculas,
        alunos=alunos,
        turmas=turmas
    )


@app.route("/matriculas/cadastrar", methods=["POST"])
def cadastrar_matricula():

    aluno_id = request.form["aluno_id"]
    turma_id = request.form["turma_id"]
    status = request.form["status"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO matriculas
            (
                aluno_id,
                turma_id,
                status
            )
            VALUES (?, ?, ?)
        """, (
            aluno_id,
            turma_id,
            status
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Matrícula realizada com sucesso!",
            "sucesso"
        )

    except sqlite3.IntegrityError:

        flash(
            "Não foi possível realizar a matrícula.",
            "erro"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao realizar matrícula: {erro}",
            "erro"
        )

    return redirect(url_for("matriculas"))

@app.route("/professor-disciplinas")
def professor_disciplinas():

    conexao = conectar_banco()

    relacionamentos = conexao.execute("""
        SELECT
            professor_disciplinas.id,
            professores.nome AS professor,
            disciplinas.nome AS disciplina
        FROM professor_disciplinas

        INNER JOIN professores
            ON professor_disciplinas.professor_id = professores.id

        INNER JOIN disciplinas
            ON professor_disciplinas.disciplina_id = disciplinas.id

        ORDER BY professores.nome
    """).fetchall()

    professores = conexao.execute("""
        SELECT *
        FROM professores
        ORDER BY nome
    """).fetchall()

    disciplinas = conexao.execute("""
        SELECT *
        FROM disciplinas
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "professor_disciplinas.html",
        relacionamentos=relacionamentos,
        professores=professores,
        disciplinas=disciplinas
    )


@app.route("/professor-disciplinas/cadastrar", methods=["POST"])
def cadastrar_professor_disciplina():

    professor_id = request.form["professor_id"]
    disciplina_id = request.form["disciplina_id"]

    try:

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO professor_disciplinas
            (
                professor_id,
                disciplina_id
            )
            VALUES (?, ?)
        """, (
            professor_id,
            disciplina_id
        ))

        conexao.commit()
        conexao.close()

        flash(
            "Disciplina vinculada ao professor com sucesso!",
            "sucesso"
        )

    except sqlite3.IntegrityError:

        flash(
            "Não foi possível realizar o vínculo.",
            "erro"
        )

    except sqlite3.Error as erro:

        flash(
            f"Erro ao realizar vínculo: {erro}",
            "erro"
        )

    return redirect(url_for("professor_disciplinas"))


@app.route("/teste-banco")
def teste_banco():

    try:

        conexao = conectar_banco()

        conexao.execute("SELECT 1")

        conexao.close()

        return """
            <h2>
                Conexão com o banco realizada com sucesso!
            </h2>
        """

    except sqlite3.Error as erro:

        return f"""
            <h2>
                Erro ao conectar com o banco:
                {erro}
            </h2>
        """

if __name__ == "__main__":
    app.run(debug=True)