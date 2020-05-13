from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#in der Database.py ist dies Volunteers
class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)

        #forgein keys
        #shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=False)
        #Problem Shelter (Integer) entspricht Niederlassung (String)
        #Am besten Datenbank später erstellen die IDs der Niederlassungen nachschauen und dann die Werte hinterlegen statt den Strings

    def __repr__(self):
        return '<Help %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/UC1')
def UC1():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('UC1Anfahrt.html', tasks=tasks)


@app.route('/UC2')
def UC2():
    if request.method == 'POST':
        if request.form['password1'] == request.form['password2']:
            dict = {
                "nl" : request.form['niederlassung'],
                "vn" : request.form['vorname'],
                "nn" : request.form['nachname'],
                "bd" : request.form['date'],
                "gd" : request.form['gender'],
                "pw" : request.form['password1'],
            }
            new_helper = Helper(niederlassung = dict["nl"],
                                firstname = dict["vn"],
                                lastname = dict["nn"],
                                birthday = dict["bd"],
                                gender = dict["gd"],
                                password = dict["pw"])

            try:
                db.session.add(new_helper)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding you to the list'

        else: return 'passwords must be equal'

    else:
        return render_template('UC2Helfer.html')
    
@app.route('/UC2Eintrag')
def UC2Eintrag():
    if request.method == 'POST':
        dict = {
            niederlassung : request.form['niederlassung'],
            vorname : request.form['vorname'],
            nachname : request.form['nachname'],
            vorname : request.form['vorname'],
            gender : request.form['gender']
        }
        
        new_helper = Help(content=task_content)
        #Falsch, muss noch angepasst werden, das hier ist der Eintrag für UC2Helfer
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).first()
        return render_template('UC2Eintrag.html', tasks=tasks)

@app.route('/UC3')
def UC3():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('UC3Tiere.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)