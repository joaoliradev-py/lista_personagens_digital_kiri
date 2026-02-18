# Importando as blbliotecas necessárias
from flask import Flask


# Criando as configurações da nossa aplicação
app = Flask(__name__)  # app
app.config['SECRET_KEY'] = 'kirigakure'  # Chave secreta


# Importando as rotas
from . import routes
