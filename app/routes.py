from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario
from . import db

main = Blueprint("main", __name__)

# Rota para a página inicial
@main.route("/")
def home():
    return render_template("home.html")

# Rota para a aba 1
@main.route("/aba1")
def aba1():
    return render_template("aba1.html")

# Rota para a aba 2
@main.route("/aba2")
def aba2():
    return render_template("aba2.html")

# Rota para o acesso/login
@main.route("/acesso", methods=["GET", "POST"])
def acesso():
    if request.method == "POST":
        # Lógica de login
        if "login" in request.form:
            email = request.form["username"]
            senha = request.form["password"]

            # Verificar se o usuário existe no banco
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                session["usuario_id"] = usuario.id
                session["perfil"] = usuario.perfil

                # Redirecionar baseado no perfil
                if usuario.perfil == "admin":
                    return redirect(url_for("main.home"))
                elif usuario.perfil == "responsavel":
                    return redirect(url_for("main.aba1"))
            else:
                erro = "Credenciais inválidas!"
                return render_template("acesso.html", erro=erro)
    return render_template("acesso.html")

# Rota para criação de novo usuário
@main.route("/novo_usuario", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        nome = request.form["name"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        senha = request.form["password"]
        confirm_senha = request.form["confirmPassword"]
        role = request.form["role"]

        # Validar se as senhas correspondem
        if senha != confirm_senha:
            erro = "As senhas não coincidem!"
            return render_template("novo_usuario.html", erro=erro)

        # Validar critérios da senha
        import re
        senha_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
        if not re.match(senha_regex, senha):
            erro = "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial."
            return render_template("novo_usuario.html", erro=erro)

        # Verificar se o email já existe
        if Usuario.query.filter_by(email=email).first():
            erro = "Email já registrado!"
            return render_template("novo_usuario.html", erro=erro)

        # Criar o novo usuário
        hashed_password = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, data_nascimento=birthdate, email=email, senha=hashed_password, perfil=role)
        db.session.add(novo_usuario)
        db.session.commit()

        # Redirecionar para a página de login
        sucesso = "Usuário criado com sucesso! Faça login para continuar."
        return redirect(url_for("main.acesso", sucesso=sucesso))

    return render_template("novo_usuario.html")
