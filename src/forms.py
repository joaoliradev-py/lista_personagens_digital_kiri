# Nossos formulários ficam aqui

# Importando as bibliotecas necessárias
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


# Criando o modelo de cadastro de personagem
class CadastroPersonagemForm(FlaskForm):
    # Nosso campos
    nome = StringField(
        label='Nome do Personagem',
        validators=[DataRequired()]
    )
    descricao = StringField(
        label='Decrição do Personagem',
        validators=[DataRequired()]
    )
    imagem = StringField(
        label='URL da imagem do personagem?',
        validators=[DataRequired()]
    )
    patente = StringField(
        label='Patente para desbloquear o personagem',
    )
    disponivel = RadioField(
        label='O personagem está disponível?',
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não')
        ]
    )
    cadastrar = SubmitField(label='Cadastrar Personagem')
