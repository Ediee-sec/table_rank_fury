from flask import Flask, render_template
from models import db, User
import os

app = Flask(__name__)

# Configurando a conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USR')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Função para calcular o rank com base no XP acumulado
def get_rank(lvl):
    if lvl >= 200:
        return "Dragão Preto de olhos Vermelhos"
    elif lvl >= 100:
        return "Cetro de Diamante"
    elif lvl >= 70:
        return "Cetro de Safira"
    elif lvl >= 45:
        return "Machado de Batalha de Metal"
    elif lvl >= 30:
        return "Machado de Ouro"
    elif lvl >= 20:
        return "Machado de Prata Duplo"
    elif lvl >= 12:
        return "Machado de Prata"
    elif lvl >= 6:
        return "Machado de Metal"
    elif lvl >= 2:
        return "Martelo de Madeira"
    else:
        return "Unranked"


def get_progress_to_next_rank(current_xp, level):
    xp_for_next_rank = (level + 1) * 1024
    progress = (current_xp / xp_for_next_rank) * 100
    
    return max(0, min(progress, 100))



# Rota principal
@app.route('/')
def index():
    # Consulta todos os usuários da tabela e ordena pelo campo 'xp_accumulated'
    users = User.query.order_by(User.xp_accumulated.desc()).all()
    
    # Atribui o rank e o progresso para o próximo rank para cada usuário
    for user in users:
        user.rank = get_rank(user.lvl)
        user.progress = get_progress_to_next_rank(user.xp, user.lvl)
    
    return render_template('table.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)
