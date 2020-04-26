import os
from ML_Stuff.prepData import *
from ML_Stuff.processing import *
from ML_Stuff.classifer import *
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import keras
from keras.models import load_model
import pandas as pd

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

# we need to redefine our metric function in order 
# to use it when loading the model 
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

# load the model, and pass in the custom metric function
global graph
graph = tf.get_default_graph()
model = load_model("C:/Users/John Q-G/Documents/GitHub/FishDaPhish/ML_Stuff/model.h5", custom_objects={'auc': auc})
@app.route('/validate', methods=['POST'])
def validate():
    data = {"success": False}
    #fetch data
    info = request.form.get("input_val")
    #invoke prep functions and label encode
    pos, sentis = get_emailData(info)
    le = preprocessing.LabelEncoder()
    le.fit(pos)
    vals = le.transform(pos)
    model_in = np.array(vals).reshape(-1,1)

    input_scale = scaler(model_in)
    input_context = define_context(input_scale,4)
    finIn = final_prep(input_context, 4, 1)
    print("This: ", finIn.shape)

    #model
    with graph.as_default():
        pred = model.predict(finIn)
        #data["prediction"] = str(model.predict(finIn)[0][0])
        data["success"] = True
        #model = build_model("C:/Users/John Q-G/Documents/GitHub/ae_weights.h5")

    #classification
    #pred = get_prediction(finIn, model)
    #model._make_predict_function()
    #pred = model.predict(finIn)
    # pred = data["prediction"]
    #print("MIRA: ", finIn)
    outliers = find_anomalies(finIn, pred)
    print("outliers", outliers, type(outliers))
    if(outliers.size == 0):
        out = "Ther is something a bit off about this"
    else:
        out = "Looks Good"
    email = Email.query.filter_by(body=info).first()
    email.title = out
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)