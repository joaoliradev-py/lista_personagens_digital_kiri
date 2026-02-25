# As nossas rotas ficam aqui

# Importando as bibliotecas necessárias
from flask import (make_response, redirect, url_for,
                   render_template, flash)
# Importando os nossos forms
from ..forms import (CadastraUsuarioForm, LoginUsuarioForm)
# Importando o nosso conector do supabase
from ..config.database import get_supabase_client, supabase_admin
# Importando nosso app
from .. import app


@app.route('/')
def page_splash():
    """page_splash

    Essa função renderiza a página splash
    Essa é a página que antecede a página home
    """
    return render_template('splash.html')


@app.route('/home')
def page_home():
    """page_home

    Essa função renderiza a página home
    É essa página que dá acesso a todas as outras
    """
    # Captruando o nosso usuário logado
    client = get_supabase_client()

    # Os dados do usuário
    user_data = None

    if client:
        try:
            auth_res = client.auth.get_user()
            user_data = auth_res.user
        except Exception as e:
            print(f'Erro ao buscar: {e}')

    # Lógica para pegar o personagem do usuário
    personagem = None

    if user_data is not None:
        # Coletando os dados do usuário
        metadados = user_data.user_metadata or {}
        # Coletando apenas o id do usuário
        id_personagem = metadados.get('personagem')

        personagem = (
            supabase_admin.table('personagens')
            .select('*')
            .eq('id', id_personagem)
            .maybe_single()
            .execute()
        )
    return render_template(
        'home.html',
        personagem=personagem,
        usuario=user_data
    )


@app.route('/login', methods=['GET', 'POST'])
def page_login():
    """page_login

    Essa função renderiza a página de login
    Aqui fica o formulário necessário para logar
    """
    # Criando um objeto do tipo formulário
    form = LoginUsuarioForm()
    if form.validate_on_submit():
        try:
            # Tentando autenticar
            auth_response = supabase_admin.auth.sign_in_with_password({
                'email': f'{form.usuario.data}@kirigakure.com',
                'password': form.senha.data
            })
            # Coletando o token
            access_token = auth_response.session.access_token
            refresh_token = auth_response.session.refresh_token

        except Exception as e:
            print(f'Erro ao logar: {e}')
            flash('Usuário ou senha inválidos :(', category='error')
        else:
            flash('Você entrou com sucesso :)', category='success')
            # Mandando esse token no cookie do site
            response = make_response(redirect(url_for('page_home')))
            # Definindo o access e o refresh
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response

    return render_template('login.html', form=form)


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def page_cadastro_usuario():
    """

    Essa função cadastra um novo usuário
    """
    # Criando um objeto do tipo formulário
    form = CadastraUsuarioForm()

    # Se o formulário for validado, vamos cadastra o usuário
    if form.validate_on_submit():
        try:
            supabase_admin.auth.sign_up({
                'email': f'{form.usuario.data}@kirigakure.com',
                'password': form.senha.data,
                'options': {
                    'data': {
                        'personagem': 0,
                        'admin': False,
                        'patente': form.patente.data
                    }
                }
            })
        except Exception as e:
            print(f'Erro ao cadastrar usuário: {e}')
        else:
            print('Usuário cadastrado com sucesso')
            flash('Você se cadastrou com sucesso', 'success')
        # A gente aproveita e cadastra ele no banco de dados
        try:
            (
                supabase_admin.table('usuario')
                .insert({
                    'usuario': form.usuario.data,
                    'senha': form.senha.data,
                    'patente': form.patente.data,
                    'personagem': 0,
                    'admin': False
                })
                .execute()
            )
        except Exception as e:
            print(f'Erro ao cadastrar usuário no banco?: {e}')
            flash('Usuário cadastrado com sucesso :)', 'sucess')
        else:
            print('Usuário cadatrado no banco com sucesso')
            return redirect(url_for('page_home'))

    return render_template('cadastro_usuario.html', form=form)


@app.route('/logout')
def page_logout():
    # Capturando o usuário atual
    usuario = get_supabase_client()

    if usuario:
        try:
            usuario.auth.sign_out()
        except Exception as e:
            print(f'Erro ao fazer logout: {e}')

    # Informando o navegador para voltar para o home após o logout
    response = make_response(redirect(url_for('page_home')))

    # Apagando os cookies
    try:
        response.set_cookie('access_token', '', expires=0)
    except Exception as e:
        print(f'Erro ao apagar os cookies: {e}')
    else:
        print('Usuário desconectado com sucesso')
        flash('Você saiu som sucesso :)', 'success')
    return response
