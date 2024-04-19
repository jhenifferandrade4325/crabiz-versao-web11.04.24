#cria o servidor
# 

from flask import Flask , render_template, request, redirect, session, jsonify
from usuario import Usuario
from chat import Chat
from mensagem import Mensagem
from contato import Contato 
import sqlite3 #banco de dados

#app é o servidor
#criei o objeto app usando a classe Flask
app = Flask(__name__)
app.secret_key = 'crabiz'

#roteamento da página
@app.route("/", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    if request.method == "POST":
        telefone = request.form["telefone"]
        nome = request.form["nome"]
        senha = request.form["senha"]
        usuario = Usuario()
        if usuario.cadastrar(telefone,nome,senha):
            return render_template("login.html")
        else:
          return("ERRO")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        telefone = request.form['telefone']
        senha = request.form['senha']

        usuario = Usuario()
        usuario.logar(telefone, senha)
        if usuario.logado:
            session['usuario_logado'] = {'nome':usuario.nome,
                                         'telefone':usuario.telefone}
            return redirect('/chat')
        else:
            session.clear()
            return 'Telefone ou senha incorretos.'

@app.route("/chat", methods=["GET", "POST"])
def chat():
        if request.method == "GET":
            return render_template("chat.html")

@app.route("/get/usuarios")
def api_get_usuarios():
    nome_usuario = session['usuario_logado']['nome']
    telefone_usuario = session['usuario_logado']['telefone']
    chat = Chat(nome_usuario,telefone_usuario)
    contatos = chat.retorna_contatos()
    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    quantidade = 0
    nome_usuario = session['usuario_logado']['nome']
    telefone_usuario = session['usuario_logado']['telefone']
    chat = Chat(nome_usuario,telefone_usuario)
    destinatario = Contato("",tel_destinatario)
    verifica = chat.verificar_mensagem(quantidade,destinatario)
    return jsonify(verifica), 200

@app.route("/post/enviamensagem" , methods=["POST"])
def api_post_enviamensagem():
    #pegando dados do html
    dados = request.get_json()
    mensagem = dados['mensagem']
    telefone = dados['usuario']
    nome_usuario = session['usuario_logado']['nome']
    telefone_usuario = session['usuario_logado']['telefone']
    chat = Chat(nome_usuario,telefone_usuario)
    destinatario = Contato("",telefone)
    #chamando a função e enviando os dados coletados
    envia = chat.enviar_mensagem(mensagem,destinatario)
    return jsonify({}), 200

app.run(debug=True)
