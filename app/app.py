from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializace Flask-Migrate

# Definice modelu
class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)

# Jednoduchá routa s formulářem
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        person = Person(name=name, email=email)
        db.session.add(person)
        db.session.commit()
        return redirect("/")
    people = Person.query.all()
    return render_template("index.html", people=people)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
