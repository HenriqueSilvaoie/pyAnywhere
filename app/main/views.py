from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        email_digitado = form.email.data
        destinatarios = ['henrique.teodoro@aluno.ifsp.edu.br','flaskaulasweb@zohomail.com', email_digitado]
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            if current_app.config['FLASKY_ADMIN']:
                for destinatario in destinatarios:
                    send_email(destinatario, form.name.data)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    users = User.query.all()
    #current_app.config['FLASKY_MAIL_SENDER'], current_app.config['EMAIL_FABIO']
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           users=users,
                           known=session.get('known', False))
