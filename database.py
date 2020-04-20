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

supplierfood = db.Table('supplier_food',
    db.Column('supplier_id', db.Integer, db.ForgeinKey('suppliers.id')),
    db.Column('food_id', db.Integer, db.ForgeinKey('food.id'))
    )

suppliershelter = db.Table('supplier_shelter',
    db.Column('supplier_id', db.Integer, db.ForgeinKey('suppliers.id')),
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
    animal = db.relationship('Animal', backref='takers', lazy='dynamic', nullable=True)
    #forgeinkey
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)
    

class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #relationships
        shelter = db.relationship('Shelters', backref='addresses', lazy='dynamic', nullable=True)
        vet = db.relationship('Vets', backref='addresses', lazy='dynamic', nullable=True)
        supplier = db.relationship('Suppliers', backref='addresses', lazy='dynamic', nullable=True)
        taker = db.relationship('Takers', backref='addresses', lazy='dynamic', nullable=True)
    #forgein keys

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    #Many-to-Many
    supplie = db.relationship('Food', secondary=supplierfood, backref=db.backref('supplied_by'), lazy='dynamic')
    meal = db.relationship('Food', secondary=animalfood, backref=db.backref('eaten_by'), lazy = 'dynamic')
    #relationships

    #forgein keys

class Shelters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelter_name = db.Column(db.String(20), nullable=False)
    founded_at = = db.Column(db.DateTime, default=datetime.utcnow) # zeiteintrag noch ändern
    #many-to-many
    delivery = db.relationship('Shelters', secondary=suppliershelter, backref=db.backref('delivery'), lazy = 'dynamic')
    #relationships
        #(Managers, Donations, Volunteers)
        manager = db.relationship('Managers', backref='shelters', lazy='dynamic', nullable=True)
        donation = db.relationship('Donations', backref='shelters', lazy='dynamic', nullable=True)
        volunteer = db.relationship('Volunteers', backref='shelters', lazy='dynamic', nullable=True)
    #forgein keys
        vet = db.Column(db.Integer, db.ForgeinKey('vets.id'), nullable=True)
        address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)


class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow) # zeiteintrag noch ändern
    #relationships

    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=True)

class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    #relationships

    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=True)

class Donations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    #relationships

    #forgein keys
        shelter = db.Column(db.Integer, db.ForgeinKey('shelters.id'), nullable=True)
        donor = db.Column(db.Integer, db.ForgeinKey('donors.id'), nullable=True)

class Donors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    #relationships
    donation = db.relationship('Donations', backref='donors', lazy='dynamic', nullable=True)
    #forgein keys

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(40), nullable=False)
    # Many-to-Many
    meal = db.relationship('Suppliers', secondary=supplierfood, backref=db.backref('meal'), lazy = 'dynamic')
    delivery = db.relationship('Suppliers', secondary=suppliershelter, backref=db.backref('delivery'), lazy = 'dynamic')
    #relationships

    #forgein keys
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)
    

class Vets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    #relationships
    shelter = db.relationship('Shelter', backref='vets', lazy='dynamic', nullable=True)
    #forgein keys
    address = db.Column(db.Integer, db.ForgeinKey('addresses.id'), nullable=True)
