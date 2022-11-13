from flask import Flask,redirect,url_for,render_template,request, flash

from flask_login import LoginManager, login_required,current_user,UserMixin,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager() # Login manager for flask-login # New
login_manager.init_app(app) # New
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required # New
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    remember = True if request.form.get('remember') else False
    if user:
        if(password == user.password):
            login_user(user,remember=remember)
            return redirect(url_for('profile'))

    return 'login post'+username+password

@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data = [username, password]

        user = User.query.filter_by(username=username).first()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('This username is exiting')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)