import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80))
    body = db.Column(db.Text)

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    def __repr__(self):
        return 'Subject:%s Body:%s' % (self.subject, self.body)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        email = Email(subject=request.form.get("title"), body=request.form.get("Body"))
        #add email to database
        db.session.add(email)
        db.session.commit()
    emails = Email.query.all()
    return render_template("home.html", emails=emails)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    email = Email.query.filter_by(subject=oldtitle).first()
    email.title = newtitle
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    email = Email.query.filter_by(subject=title).first()
    db.session.delete(email)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)