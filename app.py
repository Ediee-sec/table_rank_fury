from flask import Flask, render_template
from models import db, User
import os

app = Flask(__name__)

# Configurando a conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USR')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}"
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:yAXIOkyKLBJOZKtTKOIOXLQsuxXwNuRH@monorail.proxy.rlwy.net:30165/railway"
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


def get_progress_to_next_rank(xp, lvl):
    xp_for_next_rank = (lvl + 1) * 1024  # Cálculo do XP necessário para o próximo rank
    xp_for_current_rank = lvl * 1024  # XP necessário para o rank atual
    
    # Cálculo da porcentagem do progresso
    progress = (xp - xp_for_current_rank) / (xp_for_next_rank - xp_for_current_rank) * 100
    return max(0, min(progress, 100))  # Garante que o progresso esteja entre 0% e 100%

# Rota principal
@app.route('/')
def index():
    # Consulta todos os usuários da tabela e ordena pelo campo 'xp_accumulated'
    users = User.query.order_by(User.xp_accumulated.desc()).all()
    
    # Atribui o rank e o progresso para o próximo rank para cada usuário
    for user in users:
        user.rank = get_rank(user.lvl)
        user.progress = get_progress_to_next_rank(user.xp_accumulated, user.lvl)
    
    return render_template('table.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)
