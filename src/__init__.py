# Importando as bibliotecas necessárias
from flask import Flask


# Criando nosso app flask
app = Flask(__name__)


# Configurando nossa chave secreta
app.config['SECRET_KEY'] = 'kirigakure'

# Importando nossas rotas
from .routes import users, personagens, administração
