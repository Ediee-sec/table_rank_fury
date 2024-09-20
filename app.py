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
        return ["Dragão Preto dos olhos Vermelhos", "static/img/dragao_preto.png"]
    elif lvl >= 135:
        return ["Dragão Ambar", "static/img/dragao_ambar.png"]
    elif lvl >= 105:
        return ["Cetro de Diamante Negro", "static/img/cetro_diamante.png"]
    elif lvl >= 80:
        return ["Cetro de Ruby","static/img/cetro_ruby.png"]
    elif lvl >= 60:
        return ["Cetro de Safira", "static/img/cetro_safira.png"]
    elif lvl >= 45:
        return ["Cetro de Violeta", "static/img/cetro_violeta.png"]
    elif lvl >= 37:
        return ["Machado de Ouro Duplo", "static/img/machado_de_ouro_duplo.png"]
    elif lvl >= 32:
        return ["Machado de Ouro", "static/img/machado_de_ouro.png"]
    elif lvl >= 24:
        return ["Machado de Prata Duplo", "static/img/machado_de_prata_duplo.png"]
    elif lvl >= 20:
        return ["Machado de Prata", "static/img/machado_de_prata.png"]
    elif lvl >= 14:
        return ["Machado de Metal Duplo", "static/img/machado_de_metal_duplo.png"]
    elif lvl >= 12:
        return ["Machado de Metal", "static/img/machado_de_metal.png"]
    elif lvl >= 9:
        return ["Martelo de Pedra Duplo", "static/img/martelo_de_pedra_duplo.png"]
    elif lvl >= 7:
        return ["Martelo de Pedra", "static/img/martelo_de_pedra.png"]
    elif lvl >= 4:
        return ["Martelo de Madeira Duplo", "static/img/martelo_de_madeira_duplo.png"]
    elif lvl >= 2:
        return ["Martelo de Madeira","static/img/martelo_de_madeira.png"]
    else:
        return ["Iniciante", "static/img/iniciante.png"]
    

    



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
        user.rank = get_rank(user.lvl)[0]
        user.image = get_rank(user.lvl)[1]
        user.progress = get_progress_to_next_rank(user.xp, user.lvl)
    
    return render_template('table.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)
