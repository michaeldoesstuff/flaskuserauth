from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.secret_key = "key"
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=False, nullable=False)
  def __repr__(self):
    return '<User %r>' % self.username


@app.route('/')
def index():
  if "username" in session:
    return render_template("index.html", user=session["username"])
  else:
    return render_template("login.html")

@app.route('/login', methods=["get", "post"])
def login():
  if request.method == "get":
    return render_template("login.html")
  else:
    un = request.form.get('username')
    pw = request.form.get('password')
    user = User.query.filter_by(username=un).first()
    if user and pw == user.password:
      session["username"] = un
      return redirect("/")
    else:
      return render_template("login.html", message="Username or password did not match.")

@app.route('/register', methods=["GET", "POST"])
def signup():
  if request.method == "GET":
    return render_template("register.html")
  else:
    un = request.form.get('username')
    pw = request.form.get('password')
    pw2 = request.form.get("confirm-password")
    if pw == pw2:
      user = User.query.filter_by(username=un).first()
      if user:
        return render_template("register.html", message="Username is already taken.")
      else:
        new_user = User(username=un, password=pw)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = un
        return redirect("/")
    else:
      return render_template("register.html", message="Passwords did not match.")

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  return render_template("login.html")

with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run()