# Aqui vão ficar nossas configurações referentes ao banco de dados

# Importando as bibliotecas necessárias
from supabase import create_client
from flask import request
import os

# Carregando as variáveis de ambiente

# Nossas credenciais
URL: str = os.environ.get('SUPABASE_URL')
KEY: str = os.environ.get('SUPABASE_KEY')
ROLE_KEY: str = os.environ.get('SUPABASE_ROLE_KEY')

# Criando um cliente geral para fins de autenticação
supabase_admin = create_client(URL, ROLE_KEY)


def get_supabase_client():
    """Retorna uma nova instância do cliente para cada requisição."""

    # Definindo o nosso token
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    # Se não tiver token, visitante sem convite
    if not access_token or not refresh_token:
        return None

    try:
        supabase = create_client(URL, KEY)
        supabase.auth.set_session(
            access_token=access_token,
            refresh_token=refresh_token or ""
        )
    except Exception as e:
        print(f'Erro ao criar usuário: {e}')
    else:
        print('Usuário criado com sucesso')
        return supabase
