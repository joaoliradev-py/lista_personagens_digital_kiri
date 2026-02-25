# Importando as bibliotecas necessárias
from flask import (redirect, url_for, render_template, flash)
# Importando o nosso conector do supabase
from ..config.database import get_supabase_client
# Importando o nosso app
from .. import app


@app.route('/lista_personagens', methods=['GET', 'POST'])
def page_lista_personagens():
    """page_lista_personagens

    Esta função renderiza a lista de personagens
    aqui, os jogadores logados poderão escolher seus personagens
    """

    # Criando o nosso cliente supabase
    client = get_supabase_client()
    dados_usuario = client.auth.get_user().user.user_metadata

    # --- SEGURANÇA ---
    if not client:
        flash('Você deve fazer login primeiro!')
        return redirect(url_for('page_home'))

    # Se tudo der certo, vamos estar fazendo a consulta dos personagens

    try:
        response = (
                client.table('personagens')
                .select('*')
                .order('nome', desc=False)
                .neq('id', 0)
                .execute()
        )
    except Exception as e:
        print(f'Erro ao listar os personagens: {e}')
    else:
        print('Listando personagens...')

    personagens = response.data

    return render_template('lista_personagens.html', personagens=personagens,
                           usuario=dados_usuario)


@app.route('/escolher_personagem/<int:id>', methods=['GET', 'POST'])
def page_escolher_personagem(id: int):
    print(f'id do personagem: {id}')
    # Criando o nosso cliente supabase
    client = get_supabase_client()

    # --- SEGURANÇA ---

    # Se o usuário não estiver logado:
    if not client:
        flash('Você deve logar primeiro!')
        return redirect(url_for('page_home'))

    # Dados do usuário
    metadados = client.auth.get_user().user.user_metadata

    # Verificando se o cliente é adm
    if metadados.get('admin'):
        flash("Administradores não trocam de personagem. Use sua conta casual",
              'error')
        return redirect(url_for('page_home'))

    # Capturando o id do personagem atual
    personagem_atual = metadados.get('personagem')

    # Atualizando os dados do personagem atual para disponível
    try:
        (
            client.table('personagens')
            .update({
                'disponível': True
            })
            .eq('id', personagem_atual)
            .execute()
        )
    except Exception as e:
        print(f'Erro ao trocar de personagem: {e}')
    else:
        print(f'personagem {personagem_atual}: DISPONÍVEL')

    # Atualizando os dados do personagem novo para oucupado
    try:
        (
            client.table('personagens')
            .update({
                'disponível': False
            })
            .eq('id', id)
            .execute()
        )
    except Exception as e:
        print(f'Erro ao trocar de personagem: {e}')
    else:
        print(f'Personagem {id} OUCUPADO')

    # Atualizando os metadados do usuário atual
    try:
        (
            client.auth.update_user({
                'data': {
                    'personagem': id
                }
            })
        )
    except Exception as e:
        print(f'Erro ao ataulizar os dados do usuario: {e}')
    else:
        print('Personagem do usuário trocado com sucesso')

    flash('parabéns! você trocou de personagem', 'success')
    return redirect(url_for('page_home'))
