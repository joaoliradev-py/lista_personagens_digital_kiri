# Importando as bibliotecas necessárias
from flask import (redirect, url_for, render_template, flash)
# Importando nossos formulários
from ..forms import CadastroPersonagemForm
# importando nosso conector do supabase
from ..config.database import get_supabase_client, supabase_admin
# Importando o nosso app
from .. import app


# Criando uma rota para cadastrar usuários
@app.route('/cadastro_personagem', methods=['GET', 'POST'])
def page_cadastro_personagem():
    """page_cadastro_personagem

    Rota que renderiza o formulário de cadastros
    Essa rota é feita para que os admnistradores
    possam cadastrar usuários no banbco
    """
    # Criando um objeto do tipo formulário
    form = CadastroPersonagemForm()
    # Criando nosso cliente supabase
    client = get_supabase_client()

    # --- SEGURANÇA ---
    # se o cliente não estiver logado:
    if not client:
        flash('Você precisa logar primeiro', 'error')
        return redirect(url_for('page_login'))

    # Capturando os dados do cliente
    metadados = client.auth.get_user().user.user_metadata

    # Se o cliente não for adm
    if client and not metadados.get('admin'):
        flash('Te peguei no pulo! apenas administradores aqui.', 'error')
        return redirect(url_for('page_home'))

    # Se o formulário for validado...
    if form.validate_on_submit():
        # Cadastrando o personagem novo no banco
        try:
            (
                client.table('personagens')
                .insert({
                    'nome': form.nome.data,
                    'descricao': form.descricao.data,
                    'imagem': form.imagem.data,
                    'patente': form.patente.data,
                    'disponível': form.disponivel.data
                })
                .execute()
            )
        except Exception as e:
            print(f'Erro ao cadastrar personagem: {e}')
        else:
            print('Personagem cadastrado com sucesso')
            flash('Personagem cadastrado com sucesso :D', 'success')
            return redirect(url_for('page_home'))

    return render_template('cadastro_personagem.html', form=form)


# Criando a rota para renderizar a tabela de personagens
@app.route('/tabela_personagens', methods=['GET'])
def page_tabela_personagens():
    """page_tabela_personagens

    Esta função renderiza a tabela de personagens
    Somenete administradores podem acessá-la
    Serve para verificar a quantidade de personagens dispoínveis
    """
    # Criando o nosso cliente supabase
    client = get_supabase_client()
    # Coletando os dados do usuários
    dados = client.auth.get_user().user.user_metadata

    # --- SEGURANÇA ---
    if not client:
        flash('Você precisa logar primeiro!', 'error')

    if not dados.get('admin'):
        flash('Te pegeui no pulo! Apenas adiministradores.', 'error')

    # Realizando a consulta no supabase
    response = (
        client.table('personagens')
        .select('*')
        .neq('id', 0)
        .order('id', desc=False)
        .execute()
    )
    # Armazenando os dados em uma variável personagens
    personagens = response.data

    # Renderizando o template
    return render_template('tabela_personagens.html', personagens=personagens)


@app.route('/listar_usuarios', methods=['GET'])
def page_tabela_usuarios():
    """page_tabela_usuarios

    Essa função renderiza a tabela contendo os usuários
    somente os admnistradores podem acessar essa tela
    """
    # Criando nosso cliente de usuários
    client = get_supabase_client()
    dados_usuario = client.auth.get_user().user.user_metadata

    # --- SEGURANÇA ---
    if not client:
        flash('Você precisa logar primeiro!', 'error')
        return redirect(url_for('page_home'))

    if not dados_usuario.get('admin'):
        flash('Pegeui você no pulo! Somente administradores aqui.')
        return redirect(url_for('page_home'))

    # Coletando todos os usuários dispníveis:
    usuarios = supabase_admin.auth.admin.list_users()

    # Renderizando o template
    return render_template('tabela_usuarios.html', usuarios=usuarios)


@app.route('/atualizar_personagens/<int:id>', methods=['GET', 'POST'])
def page_atualizar_personagem(id: int):
    """page_atualizar_personagem

    Essa função renderiza o formulário de edição dos atributos do personagem.
    Somente admnistradores podem acessar essa página
    """
    # coletando o usuário atual
    client = get_supabase_client()
    dados_usuarios = client.auth.get_user().user.user_metadata

    # --- SEGURANÇA ---
    if not client:
        flash('você precisa fazer login primeiro', 'error')
        return redirect(url_for('page_home'))

    if not dados_usuarios.get('admin'):
        flash('Te pegeui no pulo! Apenas administradores aqui.')
        return redirect(url_for('page_home'))

    # Coletando o personagem atual:
    personagem_atual = (
        client.table('personagens')
        .select('*')
        .eq('id', id)
        .maybe_single()
        .execute()
        .data
    )

    # Criando um objeto do tipo formulario
    form = CadastroPersonagemForm(
        nome=personagem_atual.get('nome'),
        descricao=personagem_atual.get('descricao'),
        imagem=personagem_atual.get('imagem'),
        patente=personagem_atual.get('patente'),
        disponivel=personagem_atual.get('disponível')
    )

    # Se o formulário for validado...
    if form.validate_on_submit():
        try:
            (
                client.table('personagens')
                .update({
                    'nome': form.nome.data,
                    'descricao': form.descricao.data,
                    'imagem': form.imagem.data,
                    'patente': form.patente.data,
                    'disponível': form.disponivel.data
                })
                .eq('id', id)
                .execute()
            )
        except Exception as e:
            print(f'Erro ao atualizar usuário: {e}')
            flash('Ocorreu um erro ao atualizar o personagem', 'error')
        else:
            flash('Personagem atualizado com sucesso :)', 'success')
            return redirect(url_for('page_home'))

    # Renderizando o template
    return render_template('atualizar_personagem.html', form=form,
                           personagem=personagem_atual)


@app.route('/deletar_personagens/<int:id>', methods=['GET', 'POST'])
def page_deletar_personagem(id: int):
    # coletando o usuário atual
    client = get_supabase_client()
    dados_usuarios = client.auth.get_user().user.user_metadata

    # --- SEGURANÇA ---
    if not client:
        flash('você precisa fazer login primeiro', 'error')
        return redirect(url_for('page_home'))

    if not dados_usuarios.get('admin'):
        flash('Te peguei no pulo! Apenas administradores aqui.', 'error')
        return redirect(url_for('page_home'))

    # Deletando o personagem
    try:
        (
            client.table('personagens')
            .delete()
            .eq('id', id)
            .execute()
        )
    except Exception as e:
        print(f'Ocorreu um erro ao deletar o personagem: {e}')
        flash('Erro ao deletar o personagem', 'error')
        return redirect(url_for('page_home'))
    else:
        flash('Personagem deletado com sucesso :)', 'success')
        return redirect(url_for('page_home'))
