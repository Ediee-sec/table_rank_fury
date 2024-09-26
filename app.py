from flask import Flask, render_template, request, jsonify
from models import db, User, Log
import os

app = Flask(__name__)

# Configurando a conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USR')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Função para calcular o rank com base no XP acumulado
def get_rank(lvl):
    if lvl >= 100:
        return ["Dragão Preto dos Olhos Vermelhos", "static/img/dragao_preto.png"]
    elif lvl >= 96:
        return ["Medalha de Ouro", "static/img/medalha_ouro.png"]
    elif lvl >= 93:
        return ["Medalha de Prata", "static/img/medalha_prata.png"]
    elif lvl >= 90:
        return ["Medalha de Bronze", "static/img/medalha_bronze.png"]
    elif lvl >= 85:
        return ["Cetro de Diamante Puro", "static/img/cetro_diamante_puro.png"]
    elif lvl >= 80:
        return ["Cetro de Diamante Negro", "static/img/cetro_diamante_negro.png"]
    elif lvl >= 75:
        return ["Cetro de Ruby", "static/img/cetro_ruby.png"]
    elif lvl >= 70:
        return ["Cetro de Safira", "static/img/cetro_safira.png"]
    elif lvl >= 65:
        return ["Cetro de Violeta", "static/img/cetro_violeta.png"]
    elif lvl >= 60:
        return ["Três Estrelas de Ouro", "static/img/tres_estrelas_ouro.png"]
    elif lvl >= 56:
        return ["Duas Estrelas de Ouro", "static/img/duas_estrelas_ouro.png"]
    elif lvl >= 51:
        return ["Estrela de Ouro", "static/img/estrela_ouro.png"]
    elif lvl >= 46:
        return ["Estrela de Prata", "static/img/estrela_prata.png"]
    elif lvl >= 41:
        return ["Estrela de Bronze", "static/img/estrela_bronze.png"]
    elif lvl >= 50:
        return ["Machado de Ouro com Duas Lâminas", "static/img/machado_de_ouro_com_duas_laminas.png"]
    elif lvl >= 45:
        return ["Machado de Prata com Duas Lâminas", "static/img/machado_de_prata_com_duas_laminas.png"]
    elif lvl >= 40:
        return ["Machado de Metal com Duas Lâminas", "static/img/machado_de_metal_com_duas_laminas.png"]
    elif lvl >= 35:
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
        return ["Martelo de Madeira", "static/img/martelo_de_madeira.png"]
    else:
        return ["Iniciante", "static/img/iniciante.png"]



def get_progress_to_next_rank(current_xp, level):
    xp_for_next_rank = (level + 1) * 1024
    progress = (current_xp / xp_for_next_rank) * 100
    return max(0, min(progress, 100))

# Rota principal
@app.route('/rank')
def index():
    # Consulta todos os usuários da tabela e ordena pelo campo 'xp_accumulated'
    users = User.query.order_by(User.xp_accumulated.desc()).all()
    
    # Atribui o rank e o progresso para o próximo rank para cada usuário
    for user in users:
        user.rank = get_rank(user.lvl)[0]
        user.image = get_rank(user.lvl)[1]
        user.progress = get_progress_to_next_rank(user.xp, user.lvl)
    
    return render_template('table.html', users=users)

@app.route('/log')
def log_table():
    # Consulta todos os registros da tabela 'user_activity_log'
    logs = Log.query.order_by(Log.datetime.desc()).all()
    return render_template('log.html', logs=logs)

@app.route('/get_user_logs')
def get_user_logs():
    user_name = request.args.get('user', '').lower()
    date = request.args.get('date', '')  # Captura a data, se fornecida

    # Inicializa a consulta de logs
    query = Log.query

    if user_name:
        # Busca logs onde o nome do usuário contém a substring fornecida
        query = query.filter(Log.user.ilike(f'%{user_name}%'))

    if date:
        # Filtra os logs pela data, se a data foi fornecida
        query = query.filter(Log.datetime.cast(db.Date) == date)

    # Executa a consulta e obtém todos os logs filtrados
    logs = query.order_by(Log.datetime.desc()).all()

    # Formata os logs para envio
    filtered_logs = [
        {
            'datetime': log.datetime,
            'user': log.user,
            'type': log.type,
            'xp': log.xp,
            'multiplier': float(log.multiplier),
            'xp_multiplied': log.xp_multiplied,
            'level': log.level,
            'channel': log.channel,
        }
        for log in logs
    ]
    
    return jsonify(filtered_logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)
