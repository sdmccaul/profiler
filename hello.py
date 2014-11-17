
import os
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    shortid = db.Column(db.String(64), unique=True)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    education = db.relationship('Education',
                                backref='profile', lazy='dynamic')

    def __repr__(self):
        return '<Profile %r>' % self.shortid

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(80))
    organization = db.Column(db.String(80))
    date = db.Column(db.Date)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return '<Education %r>' % self.degree

class EducationForm(Form):
    degree = StringField('degree')
    organization = StringField('organization')
    date = DateField('date')
    submit = SubmitField('submit')

@app.route('/')
def index():
    profileList = Profile.query.all()
    educationList = Education.query.all()
    return render_template('admin.html', profileList=profileList, \
        educationList=educationList)

@app.route('/profile/<shortid>', methods=['GET'])
def profile(shortid):
    profile = Profile.query.filter_by(shortid=shortid).first_or_404()
    eduList = Education.query.filter_by(profile_id=profile.id).all()
    session['profile_id'] = profile.id
    session['shortid'] = profile.shortid
    session['firstName'] = profile.firstName
    session['lastName'] = profile.lastName
    return render_template('profile.html', profile=profile, eduList=eduList)

# @app.route('/edit-education/new', methods=['GET', 'POST'])
# def create_education():
#     form = EducationForm()
#     if form.validate_on_submit():
#         education = Education()
#         education.degree = form.degree.data
#         education.organization = form.organization.data
#         education.date = form.date.data
#         education.profile_id = session.get('profile_id')
#         db.session.add(education)
#         shortid = session.get('shortid')
#         return redirect(url_for('profile', shortid=shortid))
#     return render_template('edit_education.html', form=form)

@app.route('/edit-education/<int:eduid>', methods=['GET', 'POST'])
def edit_education(eduid):
    if eduid:
        education = Education.query.get_or_404(eduid)
    else:
        education = Education()
    form = EducationForm()
    if form.validate_on_submit():
        education.degree = form.degree.data
        education.organization = form.organization.data
        education.date = form.date.data
        education.profile_id = session.get('profile_id')
        db.session.add(education)
        return redirect(url_for('profile', shortid=session.get('shortid')))
    form.degree.data = education.degree
    form.organization.data = education.organization
    form.date.data = education.date
    return render_template('edit_education.html', form=form)

if __name__ == '__main__':
    manager.run()