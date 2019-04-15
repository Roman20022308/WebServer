import sqlite3
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from wtforms import  IntegerField
from flask_wtf import FlaskForm
from wtforms import  PasswordField, BooleanField
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField
from flask import session
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
print()


class AddGoodsForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    picture = StringField('URL изображения товара', validators=[DataRequired()])
    count = IntegerField('колличество товара на складе', validators=[DataRequired()])
    information = TextAreaField('Информация о товаре', validators=[DataRequired()])
    price = IntegerField('цена', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Delete_Good(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    submit = SubmitField('Удалить товар')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class Login_inForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class DB:
    def __init__(self):
        conn = sqlite3.connect('shop13.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


db = DB()


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


number_of_order = 0


class OrdersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        global number_of_order
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             id_user INTEGER,
                             id_good INTEGER,
                             count INTEGER,
                             number_of_order INTEGER,
                             podtverd VARCHAR(128)
                             
                             )''')
        cursor.close()
        number_of_order += 1
        self.connection.commit()

    def insert(self, id_user, id_good, count, number_of_order):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO orders 
                          (id_user,id_good,count,number_of_order,podtverd) 
                          VALUES (?,?,?,?,?)''', (id_user, id_good, count, number_of_order, False))
        cursor.close()
        self.connection.commit()

    def get(self, number_of_order):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE number_of_order = ?", (int(number_of_order),))
        row = cursor.fetchall()
        return row

    def get_on_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE id_user = ?", (str(user_id),))
        row = cursor.fetchall()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete(self, number_of_oreder):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM orders WHERE number_of_order = ?''', (number_of_oreder,))
        cursor.close()
        self.connection.commit()
        return a

    def get_number_of_order(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sqlite_sequence WHERE name = ?", ('orders',))
        row = cursor.fetchone()
        return row[1]

    def podtverd(self, number_of_order):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE orders SET podtverd=True
                              WHERE number_of_order = ? ''', (number_of_order))
        cursor.close()
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM news WHERE number_of_order = ?''', (number_of_order))
        row = cursor.fetchone()
        return row


a = OrdersModel(db.get_connection()).init_table()


class PodtverdModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        global number_of_order
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS podtverd_table 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id VARCHAR(128),
                            number_of_order INTEGER,
                            podtverd VARCHAR(128),
                            Total INTEGER
                             )''')
        cursor.close()
        number_of_order += 1
        self.connection.commit()

    def insert(self, user_id, number_of_order, Total):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO podtverd_table 
                          (user_id,number_of_order,podtverd,Total) 
                          VALUES (?,?,?,?)''', (user_id, number_of_order, 0, Total))
        cursor.close()
        self.connection.commit()

    def get_orders_of_users(self, user_id):
        a = self.get_on_id(user_id)
        list_of_orders = []
        for i in a:
            list_of_orders.append(i[2])
        return list_of_orders

    def get(self, number_of_order):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM podtverd_table WHERE number_of_order = ?", (number_of_order,))
        row = cursor.fetchall()
        return row

    def get_on_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM podtverd_table WHERE user_id = ?", (int(user_id),))
        row = cursor.fetchall()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM podtverd_table WHERE podtverd=1")
        rows = cursor.fetchall()
        return rows

    def get_for_admin(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM podtverd_table  WHERE podtverd=0")
        rows = cursor.fetchall()
        return rows

    def delete(self, number_of_order):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM podtverd_table WHERE number_of_order = ?''', (number_of_order,))
        cursor.close()
        self.connection.commit()

    def podtverd(self, number_of_order):

        cursor = self.connection.cursor()
        cursor.execute('''UPDATE orders SET podtverd=1
                              WHERE number_of_order = ? ''', (number_of_order,))
        cursor.close()
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE podtverd_table SET podtverd=1
                              WHERE number_of_order = ? ''', (number_of_order,))
        cursor.close()
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM orders WHERE number_of_order = ?''', (number_of_order,))
        row = cursor.fetchall()
        Good = GoodsModel(db.get_connection())
        for i in row:
            Good.buy(i[2], i[3])

        return row


p = PodtverdModel(db.get_connection()).init_table()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             login VARCHAR(50),
                             password VARCHAR(128),
                             mail VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, mail, password):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (login, password,mail) 
                          VALUES (?,?,?)''', (login, password, mail))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, login, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?",
                       (login, password))
        row = cursor.fetchone()

        return (True, row[0]) if row else (False,)

    def exists_login(self, login):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        row = cursor.fetchone()

        return (True, row[0]) if row else (False,)


UsersModel(db.get_connection()).init_table()


class GoodsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Goods 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(100),
                             picture VARCHAR(100),
                             count INTEGER,
                             information VARCHAR(1000),
                             price INTEGER,
                             is_in_shop INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, picture, count, information, price):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO Goods 
                          (name, picture, count,information,price,is_in_shop) 
                          VALUES (?,?,?,?,?,?)''', (name, picture, count, information, price, 1))
        cursor.close()
        self.connection.commit()

    def get(self, good_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Goods WHERE id = ?", (good_id,))
        row = cursor.fetchone()
        return row

    def come_back(self, name, picture, count, information, price):
        cursor = self.connection.cursor()

        cursor.execute("UPDATE Goods SET picture = ? WHERE name = ?", (picture, name,))
        cursor.execute("UPDATE Goods SET count = ? WHERE name = ?", (count, name,))
        cursor.execute("UPDATE Goods SET information = ? WHERE name = ?", (information, name,))
        cursor.execute("UPDATE Goods SET price = ? WHERE name = ?", (price, name,))
        cursor.execute("UPDATE Goods SET is_in_shop = ? WHERE name = ?", (1, name,))
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Goods WHERE is_in_shop = 1")
        rows = cursor.fetchall()
        return rows

    def get_all_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Goods")
        rows = cursor.fetchall()
        return rows

    def buy(self, good_id, count):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Goods SET count = count - ? WHERE id = ?", (count, good_id))
        cursor.close()
        self.connection.commit()

    def delete(self, name):
        print(name)
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Goods SET count = 0 WHERE name = ?", (name,))
        cursor.execute("UPDATE Goods SET is_in_shop = 0 WHERE name = ?", (name,))
        cursor.close()
        self.connection.commit()

    def get_more(self, good_id, number):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Goods SET count = count + ? WHERE id = ?", (number, good_id))
        cursor.close()
        self.connection.commit()


GoodsModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/registr')

    return redirect('/login_in')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' not in session:
        return redirect('/login_in')
    if 'username' not in session:
        return redirect('/login_in')
    if request.method == 'GET':
        Goods = GoodsModel(db.get_connection()).get_all()
        return render_template('index1.html', Goods=Goods,
                               orders=PodtverdModel(db.get_connection()).get_orders_of_users(session['user_id']))
    elif request.method == 'POST':
        global number_of_order
        Goods = GoodsModel(db.get_connection()).get_all()
        Order = OrdersModel(db.get_connection())
        try:
            number = Order.get_number_of_order()
        except Exception:
            number = 0

        order = OrdersModel(db.get_connection()).get(number)
        Total = 0
        for i in Goods:
            Total += int(request.form[str(i[0])]) * int(i[5])
            Order.insert(session['user_id'], i[0], request.form[str(i[0])], number)
        PodtverdModel(db.get_connection()).insert(session['user_id'], number, Total)
        number_of_order += 1

        return redirect('/shop')


@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect('/login_in')
    users = UsersModel(db.get_connection()).get_all()
    print(PodtverdModel(db.get_connection()).get_all())
    return render_template('admin.html', username=session['username'],
                           Orders_of_all_users=PodtverdModel(db.get_connection()).get_all(),
                           orders_for_podtverd=PodtverdModel(db.get_connection()).get_for_admin(),
                           users=users)


@app.route('/user_order/<int:number_of_order>')
def user_order(number_of_order):
    if 'username' not in session:
        return redirect('/login_in')
    order = OrdersModel(db.get_connection()).get(number_of_order)
    print(PodtverdModel(db.get_connection()).get(number_of_order))
    Total = PodtverdModel(db.get_connection()).get(number_of_order)[0][4]
    podtverd = PodtverdModel(db.get_connection()).get(number_of_order)
    podtverd = podtverd[0][3]
    a = []
    for i in order:
        a.append((GoodsModel(db.get_connection()).get(i[2]), i[3]))

    return render_template('order.html', Goods=a,
                           orders=PodtverdModel(db.get_connection()).get_orders_of_users(session['user_id']),
                           podtverd=podtverd, Total=Total, number_of_order=number_of_order)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login_in')


@app.route('/delete_order/<int:number_of_order>', methods=['GET'])
def delete_news(number_of_order):
    if 'username' not in session:
        return redirect('/login_in')
    OrdersModel(db.get_connection()).delete(number_of_order)
    PodtverdModel(db.get_connection()).delete(number_of_order)
    return render_template('delete_order.html', orders_for_podtverd=PodtverdModel(db.get_connection()).get_for_admin(),
                           number_of_order=number_of_order)


@app.route('/add_Goods', methods=['GET', 'POST'])
def add_Goods():
    if 'username' not in session:
        return redirect('/login_in')
    login = session['username']

    if (login == 'admin_Yusuf'):

        form = AddGoodsForm()
        if form.validate_on_submit():
            name = form.name.data
            picture = form.picture.data
            price = form.price.data
            count = form.count.data
            information = form.information.data
            exist = False
            print(GoodsModel(db.get_connection()).get_all())

            for i in GoodsModel(db.get_connection()).get_all_all():
                if i[1] == name:
                    print(i[1], name)
                    exist = True

            if (not exist):
                GoodsModel(db.get_connection()).insert(name, picture, count, information, price)
            else:
                GoodsModel(db.get_connection()).come_back(name, picture, count, information, price)

            return redirect('/add_Goods')

        return render_template('add_Goods.html', orders_for_podtverd=PodtverdModel(db.get_connection()).get_for_admin(),
                               form=form)
    else:
        return redirect('/shop')


@app.route('/registr', methods=['GET', 'POST'])
def registr():
    if request.method == 'GET':
        return render_template('registr.html', title='Авторизация')
    elif request.method == 'POST':
        login = request.form['login']
        mail = request.form['email']
        password = request.form['password']
        exists = UsersModel(db.get_connection()).exists_login(login)

        if (exists[0]):
            return redirect('/registr')
        else:
            UsersModel(db.get_connection()).insert(login, mail, password)

        return redirect('/login_in')


@app.route('/login_in', methods=['GET', 'POST'])
def login_in():
    if request.method == 'GET':
        return render_template('login_in.html', title='Авторизация')
    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if (login == 'admin_Yusuf' and password == 'admin_Migel'):
            session['username'] = login
            return redirect('/admin')
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(login, password)

        if (exists[0]):
            session['username'] = login
            session['user_id'] = exists[1]

        else:
            return redirect('/login_in')
        return redirect("/shop")


@app.route('/get_more', methods=['GET', 'POST'])
def get_more():
    if 'username' not in session:
        return redirect('/login_in')
    if request.method == 'GET':
        login = session['username']
        if (login == 'admin_Yusuf'):
            Goods = GoodsModel(db.get_connection()).get_all()
            return render_template('get_more.html', Goods=Goods,
                                   orders_for_podtverd=PodtverdModel(db.get_connection()).get_for_admin())
        else:
            return redirect('/shop')
    elif request.method == 'POST':
        global number_of_order
        Goods = GoodsModel(db.get_connection())
        Order = OrdersModel(db.get_connection())
        for i in Goods.get_all():
            Goods.get_more(i[0], request.form[str(i[0])])
        number_of_order += 1
        return redirect('/get_more')


@app.route('/delete_Good', methods=['GET', 'POST'])
def delete_Good():
    if 'username' not in session:
        return redirect('/login_in')
    login = session['username']
    if (login == 'admin_Yusuf'):
        form = Delete_Good()
        if form.validate_on_submit():
            name = form.name.data
            print(1)
            exist = False
            for i in GoodsModel(db.get_connection()).get_all():
                if i[1] == name:
                    exist = True
            if (exist):
                GoodsModel(db.get_connection()).delete(name)
            return redirect('/get_more')
        return render_template('delete_Goods.html',
                               orders_for_podtverd=PodtverdModel(db.get_connection()).get_for_admin(),
                               form=form)
    else:
        return redirect('/shop')


@app.route('/user_order_for_admin/<int:number_of_order>', methods=['GET', 'POST'])
def user_order_for_admin(number_of_order):
    if 'username' not in session:
        return redirect('/login_in')
    if (request.method == 'GET'):
        order = OrdersModel(db.get_connection()).get(number_of_order)
        print(order)
        a = []
        active = True
        for i in order:
            a.append((GoodsModel(db.get_connection()).get(i[2]), i[3]))
            if (GoodsModel(db.get_connection()).get(i[2])[3] < i[3]):
                active = False
        return render_template('order_for_admin.html', Goods=a, orders_for_podtverd=order,
                               orders=PodtverdModel(db.get_connection()).get_for_admin(), active=active)
    elif (request.method == 'POST'):
        PodtverdModel(db.get_connection()).podtverd(number_of_order)
        return redirect('/get_more')


if __name__ == '__main__':
    app.run(port=8451, host='127.0.0.1')
