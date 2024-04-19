from usuario import Usuario
from mensagem import Mensagem
from conexao import Conexao
from contato import Contato

class Chat:
    def __init__(self, nome:str, telefone:str):
        self.nome_usuario = nome
        self.telefone_usuario = telefone

    def enviar_mensagem(self, conteudo: str, destinatario:Contato)-> bool:
           # conectando o banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()
            #inserir os dados na tabela 
            dados = f"INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES ('{self.telefone_usuario}' ,'{conteudo}', '{destinatario.telefone}')"
            #executar
            mycursor.execute(dados)
            mydb.commit()
            mydb.close()
            return True
    
    def verificar_mensagem(self, quantidade: int,destinatario:Contato ):
        
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        sql = f"SELECT nome, mensagem FROM tb_mensagem m INNER JOIN tb_usuario u ON m.tel_remetente = u.tel WHERE tel_remetente = '{self.telefone_usuario}' and tel_destinatario = '{destinatario.telefone}' or tel_remetente = '{destinatario.telefone}' and tel_destinatario = '{self.telefone_usuario}'"

        mycursor.execute(sql)

        resultado = mycursor.fetchall()

        mensagens = []

        for linha in resultado:
             mensagem = {"nome":linha[0], "mensagem":linha[1]}
             mensagens.append(mensagem)

        return (mensagens)
    
    #tentativa de fazer
    def retorna_contatos(self):
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome"

        mycursor.execute(sql)

        resultado = mycursor.fetchall()

        contatos = []
        contatos.append({"nome":"TODOS", "telefone":""})

        for linha in resultado:
             contato = {"nome":linha[0], "telefone":linha[1]}
             contatos.append(contato)

        return (contatos)