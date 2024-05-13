from models import *
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, login_manager, LoginManager

key = 'hjvdskafjbsdlfe'
app.secret_key = key

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.init_app(app)


@app.route('/')
def home():
    posts = db.session.execute(db.select(Post).order_by(Post.text)).scalars()
    return render_template('home.html', post=posts)

@app.route('/add', methods=['GET', 'POST'])
# @login_required
def add_blog():
    if request.method == 'POST':
        text=request.form['text']
        post = Post(post=text, user_id=current_user.id)
        db.session.add(post)
        db.commit()
    return render_template('create_post.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if post and post.user_id == current_user.id:
        if request.method == 'POST':
            post.data = request.form['text']
            db.session.commit()
            return redirect(url_for('/'))
    return render_template('create_post.html',  user=current_user, post=post)


@app.route('/delete<int:id>', methods=['GET', 'POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    if post and post.user_id == current_user.id:
        if request.method == 'POST':
            db.session.delete(post)
            db.session.commit()
        return redirect(url_for('/'))
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        username=request.form['username']
        password1=request.form['password1']
        password2=request.form['password2']
        if password1 == password2:
            user = User(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('/'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("Incorrect password", category='error')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('login'))