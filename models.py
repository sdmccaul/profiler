from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    profile = db.relationship('Profile', backref='person', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    education = db.relationship('Education',
                                backref='profile', lazy='dynamic')
    affiliation = db.relationship('Affiliation',
                                backref='profile', lazy='dynamic')
    award = db.relationship('Award',
                                backref='profile', lazy='dynamic')
    service = db.relationship('Service',
                                backref='profile', lazy='dynamic')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __repr__(self):
        return '<Profile %r>' % self.name

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return '<Education %r>' % self.name

class Affiliation(db.Model):
    __tablename__ = 'affiliation'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return '<Affiliation %r>' % self.name

class Award(db.Model):
    __tablename__ = 'award'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return '<Award %r>' % self.name

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return '<Service %r>' % self.name