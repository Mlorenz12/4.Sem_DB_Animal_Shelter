from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# one person (relationship) can have many pets (forgeinkey)

# Sammlung der Many-to-Many relationships

animalfood = db.Table('animal_food',
    db.Column('animal_id', db.Integer, db.ForgeinKey('animals.id')),
    db.Column('food_id', db.Integer, db.ForgeinKey('food.id'))
    )

# in den Models ergänzen
supplierfood = db.Table('supplier_food',
    db.Column('supplier_id', db.Integer, db.ForgeinKey('suppliers.id')),
    db.Column('food_id', db.Integer, db.ForgeinKey('food.id'))
    )

class Supplier_Shelter(db.Model):
    pass

#function which returns a string when you add a new row to the table
###     def __repr__(self):
###          return '<THING %r>' % self.id
#here I return the id of the object created, so u can work with it after creation

class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False) #only m or f [or d if the animal insists :D ]
    brought_in = db.Column(db.DateTime, default=datetime.utcnow) # zeiteintrag noch ändern
    #relationships
    #One-to-Many

    #Many-to-Many
    meal = db.relationship('Animals', secondary=animalfood, backref=db.backref('eaten_by'), lazy = 'dynamic') # Table, secondary(Many-to-Many), name for backref, loads when asked to
    #forgein keys
    species_id = db.Column(db.Integer, db.ForgeinKey('species.id'), nullable=False)
    taken_by = db.Column(db.Integer, db.ForgeinKey('takers.id') nullable=True) #relationship looks up python code (Class name), forgeinkey looks up database (table name)

    
class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(20), nullable = False)
    #relationships
    #One-to-Many
    animal = db.relationship('Animal', backref='species', lazy='dynamic', nullable=True) #backref declares property on class Species (my_species.animal possible now). lazy is when to load the data (True is a in one go as normal select, False is a JOIN statement)
    #forgein keys
    sup_species = db.Column(db.Integer, db.ForgeinKey('species.id'), nullable=True)

class Takers(db.Model): #im Modell vgl. mit Animal_Record
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationship 
        # animal
    #forgeinkey
        # adress
    

class Adresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #relationships
        #shelters
        #vets
        #suppliers
        #takers
    #forgein keys

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    #Many-to-Many to build
    # Supplier_Food
    # Animal_Food

    #relationships

    #forgein keys

class Shelters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelter_name = db.Column(db.String(20), nullable=False)
    founded_at = = db.Column(db.DateTime, default=datetime.utcnow) # zeiteintrag noch ändern
    #relationships
        #(Managers, Donations, Volunteers)
    #forgein keys
        #vets forgein key
        #adress forgein key
    #many-to-many supplier_shelter

class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow) # zeiteintrag noch ändern
    #relationships

    #forgein keys
        #shelter_id

class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    #relationships

    #forgein keys
        #shelter_id forgein key

class Donations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    #relationships

    #forgein keys
        #shelter_id forgein key
        #donor_id forgein key

class Donors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationships
        #donations
    #forgein keys

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    #relationships

    #forgein keys
        # supplier_address
    # Many-to-Many (mit Food und Shelter)
    

class Vets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    #relationships
        #shelter
    #forgein keys
        #clinic_adress
