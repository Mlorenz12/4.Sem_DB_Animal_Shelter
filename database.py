from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# one person (relationship) can have many pets (forgeinkey)

# Sammlung der Many-to-Many relationships
## This markiert die Table mit dem Backref

animalfood = db.Table('animal_food',
    db.Column('animal_id', db.Integer, db.ForgeinKey('animals.id')), # This
    db.Column('food_id', db.Integer, db.ForgeinKey('food.id'))
    )

supplierfood = db.Table('supplier_food',
    db.Column('supplier_id', db.Integer, db.ForgeinKey('suppliers.id')), # This
    db.Column('food_id', db.Integer, db.ForgeinKey('food.id'))
    )

suppliershelter = db.Table('supplier_shelter',
    db.Column('supplier_id', db.Integer, db.ForgeinKey('suppliers.id')), #This
    db.Column('shelter_id', db.Integer, db.ForgeinKey('shelter.id'))
)

#function which returns a string when you add a new row to the table
###     def __repr__(self):
###          return '<THING %r>' % self.id
#here I return the id of the object created, so u can work with it after creation

class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False) #only m or f [or d if the animal insists :D ]
    brought_in = db.Column(db.DateTime, default=datetime.utcnow) # Tiere sind von dem Zeitpunkt der Erfassung offiziell im Tierheim
    #Many-to-Many
    meal = db.relationship('Animals', secondary=animalfood, backref=db.backref('eaten_by'), lazy = 'dynamic') # Table, secondary(Many-to-Many), name for backref, loads when asked to
    #forgein keys
    ###Shelter
    species_id = db.Column(db.Integer, db.ForgeinKey('species.id'), nullable=False)
    taken_by = db.Column(db.Integer, db.ForgeinKey('takers.id') nullable=True) #relationship looks up python code (Class name), forgeinkey looks up database (table name)
    taken_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
      return '<Animal %r>' % self.id
    
class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(20), nullable = False)
    #One-to-Many
    animal = db.relationship('Animal', backref='species', lazy='dynamic', nullable=True) #backref declares property on class Species (my_species.animal possible now). lazy is when to load the data (True is a in one go as normal select, False is a JOIN statement)
    #forgein keys
    sup_species = db.Column(db.Integer, db.ForgeinKey('species.id'), nullable=True)

    def __repr__(self):
      return '<Species %r>' % self.id

class Takers(db.Model): #im Modell vgl. mit Animal_Record
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationship 
    animal = db.relationship('Animal', backref='takers', lazy='dynamic', nullable=True)
    #forgeinkey
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Takers %r>' % self.id
    

class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)

###SPALTEN EINTRAGEN 

    #relationships
        shelter = db.relationship('Shelters', backref='addresses', lazy='dynamic', nullable=True)
        vet = db.relationship('Vets', backref='addresses', lazy='dynamic', nullable=True)
        supplier = db.relationship('Suppliers', backref='addresses', lazy='dynamic', nullable=True)
        taker = db.relationship('Takers', backref='addresses', lazy='dynamic', nullable=True)

    def __repr__(self):
      return '<Addresses %r>' % self.id

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
      return '<Food %r>' % self.id

class Shelters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelter_name = db.Column(db.String(20), nullable=False)
    founded_at = = db.Column(db.DateTime)

    #relationships
        manager = db.relationship('Managers', backref='shelters', lazy='dynamic', nullable=True, ,  cascade="all, delete-orphan")
        donation = db.relationship('Donations', backref='shelters', lazy='dynamic', nullable=True)
        volunteer = db.relationship('Volunteers', backref='shelters', lazy='dynamic', nullable=True,  cascade="all, delete-orphan") 
        # cascade = "all" includes save-update, merge, refresh-expire, expunge, delete and delete-orphan deletes the row in the other table if the forgein key is set to Null
        # Animal
    #forgein keys
        vet = db.Column(db.Integer, db.ForgeinKey('vets.id'), nullable=True)
        address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Shelters %r>' % self.id


class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime) # zeiteintrag noch ändern
    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=True)

    def __repr__(self):
      return '<Managers %r>' % self.id

class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime)

    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=False)

    def __repr__(self):
      return '<Volunteers %r>' % self.id

class Donations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)

    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=True)
        donor = db.Column(db.Integer, db.ForgeinKey('donors.id'), nullable=True)
    
    def __repr__(self):
      return '<Donations %r>' % self.id

class Donors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationships
    donation = db.relationship('Donations', backref='donors', lazy='dynamic', nullable=True)

    def __repr__(self):
      return '<Donors %r>' % self.id

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    # Many-to-Many
    meal = db.relationship('Suppliers', secondary=supplierfood, backref=db.backref('meal'), lazy = 'dynamic')
    delivery = db.relationship('Suppliers', secondary=suppliershelter, backref=db.backref('delivery'), lazy = 'dynamic')

    #forgein keys
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Suppliers %r>' % self.id
    

class Vets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime)
    shelter = db.relationship('Shelter', backref='vets', lazy='dynamic', nullable=True)
    #forgein keys
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Vets %r>' % self.id


# Start der eigentlichen Funktionen der Applikation
## Überlegen ob die DB nicht komplett in ein anderes File umgelagert wird
## Variablen der Funktionen und Querys müssen noch angepasst werden

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_thing_content = request.form['content']
        new_task = <Table>(<column1>=new_thing_content) # more columns possible

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = <Table>.query.order_by(<Table>.<column2>).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = <Table>.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = <Table>.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
