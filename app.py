from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from turbo_flask import Turbo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User
from forms import RegisterForm, LoginForm
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cdn import CDN
from flask_session import Session
from flask_babel import Babel
from flask_compress import Compress
from flask import send_from_directory
from os.path import join
from configs.app_configs import AppConfigs
from utils.app_utils import AppUtils


class CyberOlympusApp(AppConfigs, AppUtils):
    def __init__(self, debug:bool=None):
        AppConfigs.__init__(self)
        AppUtils.__init__(self)
        self.debug = debug
        self.__get_configs()
        if debug:
            self.get_scss_compiler()

    def __get_configs(self):
        self.app: Flask = self.get_app()
        self.db: SQLAlchemy = self.get_flask_db()
        self.cache: Cache = self.get_flask_cache()
        self.cdn: CDN = self.get_flask_cdn()
        self.session: Session = self.get_flask_session()
        self.login_manager: LoginManager = self.get_flask_login_manager()
        self.turbo: Turbo = self.get_flask_turbo()
        self.twitter: OAuth = self.get_oauth('twitter')
        self.babel: Babel = self.get_flask_babel()
        self.compress: Compress = self.get_flask_compress()
        self.port = self.get_port()

    def setup_routes(self):        
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))


        @self.app.route('/favicon.ico')
        def favicon():
            return send_from_directory(join(self.app.root_path, 'static'),\
                'favicon.ico', mimetype='image/vnd.microsoft.icon')
        
        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            name = self.page_name()
            form:RegisterForm = RegisterForm()
            if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                self.db.session.add(new_user)
                self.db.session.commit()
                return redirect(url_for('login.html'))
            return render_template(f'{name}{self.HTML}', form=form)



        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            name = self.page_name()
            form:LoginForm = LoginForm()
            if form.validate_on_submit():
                user:User = User.query.filter_by(username=form.username.data).first()
                if user and check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('profile'))
                flash('Invalid username or password')
            return render_template(f'{name}{self.HTML}', form=form)


        @self.app.route('/profile')
        @self.cache.cached(timeout=3600)
        @login_required
        def profile():
            name = self.page_name()
            response = make_response(render_template(f'{name}{self.HTML}', name=current_user.username))
            response.headers['Cache-Control'] = 'private, max-age=3600'
            return response


        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('login'))


        @self.app.route('/login-twitter')
        def login_twitter():
            return self.twitter.authorize(callback=url_for('authorized', _external=True))


        @self.app.route('/logout-twitter')
        def logout_twitter():
            session.pop('twitter_token')
            return redirect(url_for('index.html'))


        @self.app.route('/callback-twitter')
        def authorized_twitter():
            response = self.twitter.authorized_response()
            if response is None or response.get('oauth_token') is None:
                return f"Access denied: reason={request.args['oauth_problem']} error={request.args['error_description']}"
            session['twitter_token'] = (response['oauth_token'],response['oauth_token_secret'])
            user_info = self.twitter.get('account/verify_credentials.json')
            user_id = user_info.data['id_str']
            return jsonify(user_info.data)


        def check_task_completion(username, hashtag):
            # Пример функции проверки выполнения задания
            # Здесь должна быть ваша логика проверки
            return True


        def check_subscriptions(user_id):
            subscriptions = self.twitter.get(f'friends/list.json?user_id={user_id}&count=200')
            return subscriptions.data


        @self.app.route('/check_and_register', methods=['POST'])
        def check_and_register():
            data = request.json
            username = data.get('username')
            hashtag = data.get('hashtag')
            user_info = self.twitter.get('account/verify_credentials.json')
            user_id = user_info.data['id_str']
            if check_task_completion(username, hashtag):
                subscriptions = check_subscriptions(user_id)
                # Логика регистрации события
                # Например, сохранение данных в базу данных
                return jsonify({"status": "success", "message": "Task completed and event registered", "subscriptions": subscriptions})
            else:
                return jsonify({"status": "failure", "message": "Task not completed"})


        @self.cache.cached(timeout=3600)
        @self.app.route('/')
        def index():
            name = self.page_name()
            response = make_response(render_template(f'{name}{self.HTML}'))
            response.headers['Cache-Control'] = 'public, max-age=3600'
            return response


        @self.cache.cached(timeout=3600)
        @self.app.route('/roadmap')
        def roadmap():
            name = self.page_name()
            response = make_response(render_template('roadmap.html'))
            response.headers['Cache-Control'] = 'public, max-age=3600'
            return response

        @self.babel.localeselector
        def get_locale():
            return request.accept_languages.best_match(['en', 'ru', 'es'])

        self.app.route('/update')
        def update():
            dynamic_data = "Updated data"
            return self.turbo.stream(self.turbo.append(dynamic_data, target='dynamic-data'))


    def run(self):
        self.setup_routes()
        self.app.run(debug=self.debug, port=self.port, threaded=True)
