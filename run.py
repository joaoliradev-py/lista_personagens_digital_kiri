# Importações necessárias
from src import app


# Garantido que apenas esse arquivo seja executado diretamente
if __name__ == '__main__':
    # Iniciando o servidor Flask
    app.run(debug=True)
