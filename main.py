from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()



# db = sqlite3.connect("books-collection.db", check_same_thread=False)
# cursor = db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute('INSERT INTO books VALUES(1, "Harry Potter", "JK Rowling", "9.5")')
# db.commit()

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        book_to_update = Book.query.get(id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    book_selected = Book.query.get(id)
    return render_template("edit.html", book=book_selected)

if __name__ == "__main__":
    app.run(debug=True)

