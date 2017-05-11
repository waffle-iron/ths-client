from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, g, redirect, url_for, \
     render_template, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_assets import Environment, Bundle

# Flask Init
app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file, app.py
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SECRET_KEY'] = 'SECRETKEY'
db = SQLAlchemy(app)

# Flask-Assets Bundle Registration
assets = Environment(app)

vendor_bundle = Bundle(
    'bower_components/jquery/dist/jquery.js',
    'bower_components/angular/index.js',
    'bower_components/angular-ui-router/release/angular-ui-router.js',
    'bower_components/bootstrap/dist/js/bootstrap.js',
    'bower_components/moment/moment.js',
    filters='jsmin',
    output='build/vendor.min.js'
)

app_bundle = Bundle(
    'app.js',
    filters='jsmin',
    output='build/app.min.js'
)

style_bundle = Bundle(
    'bower_components/bootstrap/dist/css/bootstrap.css',
    'bower_components/bootstrap/dist/css/bootstrap-theme.css',
    'bower_components/font-awesome/css/font-awesome.css',
    filters='cssmin',
    output='build/style.min.css'
)

assets.register('vendor', vendor_bundle)
assets.register('app', app_bundle)
assets.register('style', style_bundle)


# Load default config and override config from an environment variable
if __name__ == "__main__":
    app.run(debug=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(50), unique=True, index=True)
    password = db.Column('password', db.String(15))
    registered_on = db.Column('registered_on', db.DateTime)
    first_name = db.Column('first_name', db.String(15))
    last_name = db.Column('last_name', db.String(15))

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()
        self.first_name = first_name
        self.last_name = last_name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.first_name+self.last_name)


@app.route('/user/edit')
@login_required
def edit_info():
    # show the user profile for that user
    return render_template('edit.html', user=current_user)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<tweetId>')
@login_required
def tweet(tweetId):
    return render_template('tweets.html', tweetId=tweetId)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['email'], request.form['password'], request.form['first_name'],
                request.form['last_name'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

