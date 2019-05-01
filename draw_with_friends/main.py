from flask import Flask, render_template, request, redirect, url_for, session
from pictures import button_positions, button_positions_draw, set_pixel
from pictures import left_colors, right_colors, renew_picture
import os
from db_functions import *

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Для сессий

drop_tables()  # Для тестов, её не должно быть, очщает бд
renew_picture()  # Тоже для тестов, делает белой картинку

create_user_password_table()  # Если её нет, создается таблица юзер - пароль
create_user_squares_table()  # Аналогчино: юзер - принадлежащие ему квадратики


# Чтобы картинка сама обновлялась, без нажатия ctrl-f5
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return response


# Сюда отправляются данные из полей входа
@app.route('/login', methods=['POST'])
def check_username():
    username = request.form['login']
    password = request.form['password']
    session['user'] = username
    session['color'] = 'White'

    if check_password(username, password):
        return redirect(url_for('picture'))
    else:
        return '''Неверный логин или пароль.<a href="/logout">Вернуться</a>'''


# Сюда отправляются данные из полей регистрации
@app.route('/sign_in', methods=['POST'])
def add_username():
    username = request.form['login']
    password = request.form['password']
    if not is_name_unique(username):
        return '''Такое имя уже существует.<a href="/logout">Вернуться</a>'''
    if len(password) < 2:
        return '''Пароль получше, пожалуйста.<a href="/logout">Вернуться</a>'''
    add_user(username, password)
    add_square(username, (None, None))
    return redirect(url_for('login'))


# Стартовая страничка, где ты можешь залогиниться/зарегаться
# Если ты уже в системе, то перенаправляешься на картинку
@app.route('/')
def login():
    if 'user' in session:
        return redirect(url_for('picture'))
    return render_template('login_page.html')


# "Разлогинивает" пользователя
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


# Страничка с картинкой, где ты выбрать квадратик для рисования
# Если не зареган, то возвращает на регистрацию
@app.route('/picture')
def picture():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    user_squares = get_squares(username)
    user_squares.remove((None, None))
    return render_template('home_page.html',
                           button_positions=button_positions,
                           user_button_positions=user_squares)


# Твоё поле для рисования, где ты можешь выбрать цвет и покрасить пиксель
@app.route("/drawing<position>")
def draw(position):
    coordinates_of_square = tuple([int(i) for i in position[1:-1:].split(',')])
    username = session['user']

    # Теперь выбранный квадратик не смогут выбрать другие,
    try:
        # Если пользователь первый раз выбирает квадрат, он удаляется из общей
        button_positions.remove(coordinates_of_square)
        add_square(username, coordinates_of_square)
    except ValueError:
        pass

    coordinates_of_square = tuple(map(lambda x: x*(-8), coordinates_of_square))
    return render_template('drawing_page.html',
                           button_positions=button_positions_draw,
                           pos=coordinates_of_square,
                           left_colors=left_colors,
                           right_colors=right_colors)


# Изменяет "цвет курсора". Теперь нажатие будет красить в выбранный цвет
@app.route("/drawing<position>/<color>", methods=['POST'])
def choose_color(position, color):
    position = tuple([int(int(i) * -1/8) for i in position[1:-1:].split(',')])
    session['color'] = color
    return redirect(url_for('draw', position=(str(position))))


# Красит пиксель в выбранный до этого цвет
@app.route("/drawing<position>/<coordinates>", methods=['GET'])
def set_color(position, coordinates):
    # position - позиция квадртарика в общей картине
    # coordinates - позиция пикселя в квадратике

    pos = tuple([int(int(i) * (-1) / 8) for i in position[1:-1:1].split(',')])
    coord = tuple([int(int(i) / 64) for i in coordinates[1:-1:1].split(',')])
    x_coord = int(pos[1]/8) + coord[0]
    y_coord = int(pos[0]/8) + coord[1]
    set_pixel(x_coord, y_coord, session['color'])

    return redirect(url_for('draw', position=pos))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
