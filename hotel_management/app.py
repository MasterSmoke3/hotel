from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для клиента
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    check_in_date = db.Column(db.String(10), nullable=False)
    check_out_date = db.Column(db.String(10), nullable=False)

# Главная страница
@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

# Страница добавления клиента
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        
        new_client = Client(name=name, phone=phone, check_in_date=check_in_date, check_out_date=check_out_date)
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_client.html')

# Страница списка клиентов
@app.route('/list_clients')
def list_clients():
    clients = Client.query.all()
    return render_template('list_clients.html', clients=clients)

if __name__ == '__main__':
    # Создание базы данных (если не существует)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
