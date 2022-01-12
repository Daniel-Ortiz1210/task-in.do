import os
from flask import Flask, render_template
from werkzeug.serving import run_simple


def create_app(test_config=None):
    app = Flask(__name__,
    instance_relative_config=True,
    template_folder='templates',
    static_folder='static'
    )

    app.config.update(
        ENV='development'
        )
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app = create_app(test_config=None)

from flask_bootstrap import Bootstrap
from flask import render_template, request, redirect, flash, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from flaskkr.models import User, Todo
from flaskkr.forms import SignUpForm, LoginForm, UpdateDataForm, UpdatePassword, AddTodo, UpdateTodo


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html', error=error)


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    user = User.query.filter_by(username=username).first_or_404('Este usuario no existe')
    todos = user.todos.all()
    len_todos = len(todos)
    return render_template('dashboard.html', todos=todos)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm()
    message_category = 'message'
    if signup_form.validate_on_submit():
        try:
            new_user = User(
            name=signup_form.name.data,
            username=signup_form.username.data,
            email=signup_form.email.data
            )
            new_user.set_hashed_password(signup_form.password.data)
            db.session.add(new_user)
            db.session.commit()
            message_category = 'success'
            flash('Usuario registrado con éxito', message_category)
            return redirect(url_for('login'))
        except IntegrityError:
            message_category = 'error'
            flash('Intenta cambiar el nombre de usuario o el email, alguien ya se registró con ellos', message_category)
            return redirect(url_for('signup'))
    return render_template('signup.html', signup_form=signup_form, bootstrap=bootstrap)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(csrf_enabled=False)
    message_category = 'message'
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        password = str(login_form.password.data)
        if user is not None and user.check_password(password): # Si el usuario havce login correctamente
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            message_category = 'success'
            flash('Inicio de sesión exitoso!', message_category)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard', username=user.username)
            return redirect(next_page)
        else:
            if user is None:
                message_category = 'error'
                flash('Email incorrecto', message_category)
                return redirect(url_for('login'))
            elif user.check_password(password) is False:
                message_category = 'error'
                flash('Contraseña incorrecta', message_category)
                return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form, bootstrap=bootstrap)


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users')
@login_required
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/update/<username>',  methods=['GET', 'POST'])
@login_required
def update(username):
    form = UpdateDataForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if form.new_name.data == '':
                if user.check_password(form.password.data):
                    user.name = user.name
                    db.session.add(user)
                    db.session.commit()
            else:
                if user.check_password(form.password.data):
                    user.name = form.new_name.data
                    db.session.add(user)
                    db.session.commit()
                    flash('Información actualizada con éxito', 'success')
                    return redirect(url_for('update', username=username))
            if form.new_username.data == '':
                if user.check_password(form.password.data):
                    user.username = user.username
                    db.session.add(user)
                    db.session.commit()
            else:
                if user.check_password(form.password.data):
                    user.username = form.new_username.data
                    db.session.add(user)
                    db.session.commit()
                    flash('Información actualizada con éxito', 'success')
                    return redirect(url_for('update', username=username))
            if form.new_email.data == '':
                if user.check_password(form.password.data):
                    user.email = user.email
                    db.session.add(user)
                    db.session.commit()
            else:
                if user.check_password(form.password.data):
                    user.email = form.new_email.data
                    db.session.add(user)
                    db.session.commit()
                    flash('Información actualizada con éxito', 'success')
                    return redirect(url_for('update', username=username))            
        else:
            pass
    return render_template('update.html', update_form=form)


@app.route('/update/password/<username>', methods=['GET', 'POST'])
@login_required
def update_password(username):
    form = UpdatePassword()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(form.current_password.data):
            user.set_hashed_password(form.new_password2.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('update_password.html', update_password_form=form)


@app.route('/add-todo/<username>', methods=['GET', 'POST'])
@login_required
def add_todo(username):
    form = AddTodo()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        todo = Todo(
        description=form.description.data,
        user_id=user.id
        )
        try:
            db.session.add(todo)
            db.session.commit()
            flash('Tarea agregada exitosamente!', 'success')
            return redirect(url_for('dashboard', username=username))
        except:
            db.session.rollback()
            flash('No pudimos agregar tu tarea con éxito, intenta más tarde', 'error')
            return redirect(url_for('dashboard', username=username))
    return render_template('add_todo.html', form=form)


@app.route('/delete-todo/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    user = todo.user
    if todo_id is not None:
        try:
            db.session.delete(todo)
            db.session.commit()
            flash('Tarea eliminada correctamente', 'success')
            return redirect(url_for('dashboard', username=user.username))
        except:
            db.session.rollback()
            flash('Error al eliminar la tarea', 'error')
            return redirect(url_for('dashboard', username=user.username))


@app.route('/update-todo/description/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
    form = UpdateTodo()
    if form.validate_on_submit():
        todo = Todo.query.get(todo_id)
        user = todo.user # obtener el username del usuario que realizó este todo
        if todo and user:
            todo.description = form.description.data
            try:
                db.session.add(todo)
                db.session.commit()
                flash('Tarea actualizada con éxito', 'success')
                return redirect(url_for('dashboard', username=user.username))
            except:
                db.session.rollback()
                flash('Error al actualizar la tarea', 'error')
                return redirect(url_for('dashboard', username=user.username))
    return render_template('update_todo.html', form=form)


@app.route('/check-todo/<int:todo_id>')
@login_required
def check_todo(todo_id):
    todo = Todo.query.get(todo_id)
    user = todo.user
    if todo and user:
        try:
            todo.status = 'terminado'
            db.session.add(todo)
            db.session.commit()
            flash('Felicidades, has terminado una tarea', 'success')
            return redirect(url_for('dashboard', username=user.username))
        except:
            db.session.rollback()
            flash('No pudimos marcar tu tarea como terminada', 'error')
            return redirect(url_for('dashboard', username=user.username))

@app.route('/pending-todo/<int:todo_id>')
@login_required
def pending_todo(todo_id):
    todo = Todo.query.get(todo_id)
    user = todo.user
    if todo and user:
        try:
            todo.status = 'pendiente'
            db.session.add(todo)
            db.session.commit()
            flash('Marcaste una tarea como pendiente', 'success')
            return redirect(url_for('dashboard', username=user.username))
        except:
            db.session.rollback()
            flash('No pudimos marcar tu tarea como terminada', 'error')
            return redirect(url_for('dashboard', username=user.username))


@app.route('/my_profile/<username>')
@login_required
def my_profile(username):
    return render_template('my_profile.html')



if __name__ == '__main__':
    app.run(debug=True)


# IDEAS----------
# INFORMACION PERSONAL DE CADA USUARIO (PASATIEMPOS, CUMPLEAÑOS, GUSTOS Y PREFERENCIAS, FOTOGRAFIA)


# PENDIENTES TOdo APP
# AGREGAR DISEÑO CON BOOTSTRAP A LAS TAREAS YA CREADAS
# RECUPERAR CONTRASEÑA (PREGUNTAS DE SEGURIDAD, EMAIL)
# LISTA CON DISEÑO DE USUARIOS REGISTRADOS
# ELIMINACION DE CUENTAS
# Eliminacion de tareas
# Editar tarea (status, descripción)
# https://getbootstrap.com/docs/3.4/components/#panels-alternatives




