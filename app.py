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
        return "Lenda"
    elif lvl >= 100:
        return "Mestre"
    elif lvl >= 70:
        return "Diamante"
    elif lvl >= 45:
        return "Platina"
    elif lvl >= 30:
        return "Ouro"
    elif lvl >= 20:
        return "Prata"
    elif lvl >= 12:
        return "Bronze"
    elif lvl >= 6:
        return "Ferro"
    elif lvl >= 2:
        return "Madeira"
    else:
        return "Unranked"


def get_level_from_xp(xp_accumulated):
    level = xp_accumulated // 1024  # Cada nível exige 1024 XP
    return level

def get_progress_to_next_rank(xp_accumulated):
    level = get_level_from_xp(xp_accumulated)
    xp_for_next_rank = (level + 1) * 1024
    xp_for_current_rank = level * 1024
    
    # Cálculo do progresso
    progress = (xp_accumulated - xp_for_current_rank) / (xp_for_next_rank - xp_for_current_rank) * 100
    return max(0, min(progress, 100))

# Rota principal
@app.route('/')
def index():
    # Consulta todos os usuários da tabela e ordena pelo campo 'xp_accumulated'
    users = User.query.order_by(User.xp_accumulated.desc()).all()
    
    # Atribui o rank e o progresso para o próximo rank para cada usuário
    for user in users:
        user.rank = get_rank(user.lvl)
        user.progress = get_progress_to_next_rank(user.xp_accumulated)
    
    return render_template('table.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)
