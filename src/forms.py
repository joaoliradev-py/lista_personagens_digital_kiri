# Nossos formulários ficam aqui

# Importando as bibliotecas necessárias
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, RadioField,
                     PasswordField, SelectField)
from wtforms.validators import DataRequired, Regexp


# Criando um form para logar com o usuário
class LoginUsuarioForm(FlaskForm):
    usuario = StringField(
        label='informe o seu usuário (use o nome real, mas não completo)',
        validators=[DataRequired(),
                    Regexp(r'^[a-zA-Z0-9]+$',
                           message="O nome não pode conter espaços ou acentos")
                    ]
    )
    senha = PasswordField(
        label='informe sua senha',
        validators=[DataRequired()]
    )
    enviar = SubmitField(
        label='enviar'
    )


# Criando um form para cadastrar um usuario
class CadastraUsuarioForm(FlaskForm):
    usuario = StringField(
        label='informe o seu usuário',
        validators=[DataRequired(),
                    Regexp(r'^[a-zA-Z0-9]+$',
                           message="O nome não pode conter espaços ou acentos")
                    ]
    )
    senha = PasswordField(
        label='Informe a sua senha',
        validators=[DataRequired()]
    )
    patente = SelectField(
        label='Escolha sua patente (todos começamos como gennin)',
        choices=[
            ('Gennin', 'Gennin'),
            ('Chunnin', 'Chunnin'),
            ('Jounnin', 'Jounnin')
        ]
    )
    enviar = SubmitField(
        label='enviar'
    )


# Criando o modelo de cadastro de personagem
class CadastroPersonagemForm(FlaskForm):
    # Nosso campos
    nome = StringField(
        label='Nome do Personagem',
        validators=[DataRequired()]
    )
    descricao = StringField(
        label='Descrição do Personagem',
        validators=[DataRequired()]
    )
    imagem = StringField(
        label='URL da imagem do personagem',
        validators=[DataRequired()]
    )
    patente = SelectField(
        label='Patente para desbloquear o personagem',
        choices=[
            ('Gennin', 'Gennin'),
            ('Chunnin', 'Chunnin'),
            ('Jounnin', 'Jounnin')
        ]
    )
    disponivel = RadioField(
        label='O personagem está disponível?',
        choices=[
            (True, 'Sim'),
            (False, 'Não')
        ]
    )
    enviar = SubmitField(label='enviar')
