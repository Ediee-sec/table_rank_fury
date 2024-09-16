from flask import Flask, render_template
from models import db, User
import os

app = Flask(__name__)

# Configurando a conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USR')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Rota principal
@app.route('/')
def index():
    # Consulta todos os usuários da tabela e ordena pelo campo 'level' (lvl)
    users = User.query.order_by(User.xp_accumulated.desc()).all()  # Ordena por nível em ordem decrescente
    return render_template('table.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
