# Realizando as importações necessárias
from flask import render_template, redirect, url_for
from . import app
import httpx


# Nossas variáveis
API_URL = 'https://evergreen-lista-personagens-api.onrender.com/personagem/'


# Rotas usadas aqui

# Rota principal
@app.route('/')
def page_home():
    # Retornando a página home
    return render_template('home.html')


# Rota com os peronsagens disponíveis
@app.route('/personagens')
def page_lista_personagens():
    # Realizando a requisição para a API
    response = httpx.get(API_URL)
    # Verificando se a requisição foi bem sucedida
    try:
        response.raise_for_status()
        personagens = response.json()

    except httpx.HTTPStatusError as e:
        print(f'Erro na requisição: {e}')
        personagens = []

    # Retornando a página e os personagens
    return render_template('lista_personagens.html', personagens=personagens)


# Rota para selecionar um personagem
@app.route('/personagem/<id>')
def page_selecionar_personagem(id: str):
    # Coletando o personagem atual pelo id
    get_response = httpx.get(API_URL+id)
    personagem_atual = get_response.json()

    # Pegando o status atual e invertendo
    novo_status = not personagem_atual['disponivel']

    # Criando um dicionário para atualizar o personagem
    novos_dados = {
        'disponivel': novo_status
    }

    # Atualizando o status do personagem
    httpx.put(
        API_URL+id,
        json=novos_dados
    )

    return redirect(url_for('page_lista_personagens'))
