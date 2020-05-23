from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap

from sqlalchemy import text
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# one person (relationship) can have many pets (ForeignKey)

# Sammlung der Many-to-Many relationships
## This markiert die Table mit dem Backref

animalfood = db.Table('animal_food',
    db.Column('animal_id', db.Integer, db.ForeignKey('animals.id')), # This
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
    )

supplierfood = db.Table('supplier_food',
    db.Column('supplier_id', db.Integer, db.ForeignKey('suppliers.id')), # This
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
    )

suppliershelter = db.Table('supplier_shelter',
    db.Column('supplier_id', db.Integer, db.ForeignKey('suppliers.id')), #This
    db.Column('shelter_id', db.Integer, db.ForeignKey('shelters.id'))
)

class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False) #only m or f [or d if the animal insists :D ]
    brought_in = db.Column(db.DateTime, default=datetime.utcnow) # Tiere sind von dem Zeitpunkt der Erfassung offiziell im Tierheim
    taken_at = db.Column(db.DateTime, nullable=True)
    #Many-to-Many
    meal = db.relationship('Animals', secondary=animalfood, backref=db.backref('eaten_by'), lazy = 'dynamic') # Table, secondary(Many-to-Many), name for backref, loads when asked to
    #forgein keys
    shelter = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    taken_by = db.Column(db.Integer, db.ForeignKey('takers.id'), nullable=True) #relationship looks up python code (Class name), ForeignKey looks up database (table name)
    

    def __repr__(self):
      return '<Animal %r>' % self.id
    
class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(20), nullable = False)
    #One-to-Many
    animal = db.relationship('Animals', backref='species', lazy='dynamic') #backref declares property on class Species (my_species.animal possible now). lazy is when to load the data (True is a in one go as normal select, False is a JOIN statement)
    #forgein keys
    sup_species = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=True)

    def __repr__(self):
      return '<Species %r>' % self.id

class Takers(db.Model): #im Modell vgl. mit Animal_Record
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationship 
    animal = db.relationship('Animals', backref='takers', lazy='dynamic')
    #ForeignKey
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Takers %r>' % self.id
    

class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False) 

    #relationships
    shelter = db.relationship('Shelters', backref='addresses', lazy='dynamic')
    vet = db.relationship('Vets', backref='addresses', lazy='dynamic')
    supplier = db.relationship('Suppliers', backref='addresses', lazy='dynamic')
    taker = db.relationship('Takers', backref='addresses', lazy='dynamic')

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
    founded_at = db.Column(db.DateTime)

    #relationships
    manager = db.relationship('Managers', backref='shelters', lazy='dynamic',  cascade="all, delete-orphan")
    donation = db.relationship('Donations', backref='shelters', lazy='dynamic', )
    volunteer = db.relationship('Volunteers', backref='shelters', lazy='dynamic',   cascade="all, delete-orphan") 
    animal = db.relationship('Animals', backref='shelters', lazy='dynamic',  cascade="all, delete-orphan")
        # cascade = "all" includes save-update, merge, refresh-expire, expunge, delete and delete-orphan deletes the row in the other table if the forgein key is set to Null
    #forgein keys
    vet = db.Column(db.Integer, db.ForeignKey('vets.id'), nullable=True)
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Shelters %r>' % self.id


class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime)
    #forgein keys
    shelter = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=True)

    def __repr__(self):
      return '<Managers %r>' % self.id

class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    #forgein keys
    shelter = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=False)

    def __repr__(self):
      return '<Volunteers %r>' % self.id


##Diese Klasse nochmal überdenken als Weak-Entity mit einer Kombination aus den F-Keys und einem Timestamp als P-Key
class Donations(db.Model):
    amount = db.Column(db.Integer, nullable=False)
    shelter = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=False, primary_key=True)
    donor = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    # UniqueConstraint('shelter', 'donor','timestamp', name='prim_key') für den Fall, dass die Verbindung des primary key so nicht klappt, Docs unklar

    def __repr__(self):
      return '<Donations %r>' % self.id

class Donors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationships
    donation = db.relationship('Donations', backref='donors', lazy='dynamic')

    def __repr__(self):
      return '<Donors %r>' % self.id

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    # Many-to-Many
    meal = db.relationship('Suppliers', secondary=supplierfood, backref=db.backref('meal2'), lazy = 'dynamic')
    delivery = db.relationship('Suppliers', secondary=suppliershelter, backref=db.backref('delivery2'), lazy = 'dynamic')

    #forgein keys
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Suppliers %r>' % self.id
    

class Vets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime)
    #relationship
    shelter = db.relationship('Shelters', backref='vets', lazy='dynamic')
    #forgein keys
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    def __repr__(self):
      return '<Vets %r>' % self.id


# Start der eigentlichen Funktionen der Applikation
## Überlegen ob die DB nicht komplett in ein anderes File umgelagert wird
## Variablen der Funktionen und Querys müssen noch angepasst werden

@app.route('/')
def Start():
        return render_template('index.html')

@app.route('/delete/<int:id>') #Funktioniert!
def delete(id):
    task_to_delete = Volunteers.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Volunteers.query.get_or_404(id)

    if request.method == 'POST':
        task.shelter = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/UC1', methods=['POST', 'GET'])
def UC1():
    
    sql = text('select shelters.shelter_name, a.city,a.zip_code,a.street,a.number from shelters, addresses as a \
                where a.id == shelters.address')
    query = db.engine.execute(sql)
    result = [row for row in query]
    
    '''
    The select statement gets all the relevant information from the tabels shelters and addresses
    by querying the needed columens where the ID of addresses is equal
    to the forgein key written in shelters.addresses
    '''

    return render_template('UC1Anfahrt.html', places=result[:])

@app.route('/UC2', methods=['POST', 'GET'])
def UC2():

    if request.method == 'POST':
        
        #method to convert from '2015-01-02T00:00' to 2015, 1, 2, 0, 0
        date_in = request.form['Datum']
        date_out = datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])

        volu_data= [request.form['niederlassung'],
                    request.form['vorname'],
                    request.form['nachname'],
                    request.form['gender'],
                    date_out,
                    request.form['Password'],
                    request.form['Password2']]

        new_volu = Volunteers(firstname=volu_data[1],
                            lastname=volu_data[2],
                            gender=volu_data[3],
                            birthday=volu_data[4],
                            password=volu_data[5],
                            shelter=volu_data[0])

        try:
            db.session.add(new_volu)
            db.session.commit()
            return redirect('/UC2Eintrag')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('UC2Helfer.html')
    
@app.route('/UC2Eintrag', methods=['POST', 'GET'])
def UC2Eintrag():
    volu_data = ["Ihre Vorname","Ihr Nachname","Das Tierheim in dem Sie helfen"]
    if request.method == 'POST':
        volu_data= [request.form['vorname'],
                    request.form['nachname'],
                    request.form['Password']]
        sql = text('select v.id, v.firstname,v.lastname, s.shelter_name from volunteers as v, shelters as s\
                    where v.firstname == :fn \
                    and v.lastname == :ln \
                    and v.password == :pd \
                    and s.id == v.shelter')
        query = db.engine.execute(sql, fn = volu_data[0], ln= volu_data[1], pd= volu_data[2])
        result = [row for row in query]

        return render_template('UC2Eintrag.html', volus=result)

    else:
        sql = text('select v.id, v.firstname,v.lastname, s.shelter_name from volunteers as v, shelters as s\
                    where v.firstname == :fn \
                    and v.lastname == :ln \
                    and v.password == :pd \
                    and s.id == v.shelter')
        query = db.engine.execute(sql, fn = volu_data[0], ln= volu_data[1], pd= volu_data[2])
        result = [row for row in query]

        return render_template('UC2Eintrag.html', volus=result)
        

@app.route('/UC3', methods=['POST', 'GET'])
def UC3():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Animals(animal_name=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        animals = Animals.query.order_by(Animals.taken_at.desc()).all()
        shelters = Shelters.query.order_by(Shelters.id).all()
        species = Species.query.order_by(Species.id).all()
        return render_template('UC3Tiere.html', animals=animals, shelters=shelters, species=species)

if __name__ == "__main__":
    app.run(debug=True)