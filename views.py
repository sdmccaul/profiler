
import os
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
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


@app.route('/profile/<name>', methods=['GET'])
def profile(name):
    profile = Profile.query.filter_by(profile_id=profile_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', education=education)

@app.route('/edit-education/<int:id>', methods=['GET', 'POST'])
def edit_education(id):
	education = Education.filter_by(id=id).query.get_or_404(id)
	form = EditEducationForm(education=education)
	if form.validate_on_submit():
		education.name = form.name.data
        education.date = form.date.data
        education.organization = form.organization.data
    	education.degree = form.degree.data
        db.session.add(education)
        flash('The profile has been updated.')
        return redirect(url_for(profile, name=education.name))
	form.name.data = ''
	return render_template('profile.html', form=form, name=name)