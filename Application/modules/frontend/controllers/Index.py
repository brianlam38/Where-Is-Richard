from flask.ext.classy import FlaskView, route
from flask import render_template, url_for, redirect, current_app, flash, request
from flask_menu.classy import classy_menu_item
from models.Sighting import Sighting
from models import Subscription
from Application import app
import threading

def send_email(location):
    import smtplib
    sess = app.db.create_scoped_session()
    from_user = 'admin@whereisrichard.info'
    server = smtplib.SMTP('localhost')
    for sub in sess.query(Subscription).all():
        to = sub.email

        message = """\
From: {from_user}
To: {to}
Subject: {subject}

Richard has been sighted!

>> {location}

See more info at http://whereisrichard.info
Unsubscribe: http://whereisrichard.info/unsub?email={to}""".format(
        from_user=from_user, 
        to=to, 
        location=location, 
        subject='[FindRichard] Richard has been sighted!')

        print(message)

        server.sendmail(from_user, to, message)
    
    server.quit()
    sess.close()



class Index(FlaskView):
    route_base = '/'

    @route('/', methods=['GET','POST'])
    @classy_menu_item('frontend.account', 'Home', order=0)
    def index(self):
        form = SightingForm(prefix='main')
        email_form = EmailForm(prefix='email')

        all_sightings = Sighting.query.order_by(Sighting.id.desc())

        if form.submit.data and form.validate_on_submit():
            # Add a new sighting
            sighting = Sighting(
                    location=form.description.data,
                    username=form.username.data
                )
            current_app.db.session.add(sighting)
            current_app.db.session.commit()

            thr = threading.Thread(target=send_email, args=(form.description.data,), kwargs={})
            thr.start()

            flash('Your sighting has been added!', 'success')
            form = SightingForm(formdata=None)


            # Tell all subscribed users.

        elif email_form.submit.data and email_form.validate_on_submit():
            exists = Subscription.query.filter(Subscription.email==email_form.email.data).first()
            if not exists:
                email_user = Subscription(email=email_form.email.data)
                current_app.db.session.add(email_user)
                current_app.db.session.commit()

            flash('You have been added to the subscribers', 'success')
            email_form = EmailForm(formdata=None)

        return render_template('frontend/index.html', is_form=True, 
            form=form, 
            sightings=all_sightings,
            email_form=email_form)

    @route('/unsub')
    def unsub(self):
        email = request.args.get('email')
        if email:
            sub = Subscription.query.filter(Subscription.email==email).first()
            if sub:
                current_app.db.session.delete(sub)
                current_app.db.session.commit()
                return "You have been unsubscribed"

        return "An error occured. Please contact nick@nickwhyte.com"


from flask_wtf import Form
from wtforms import (
    TextField,
    validators,
    IntegerField,
    PasswordField,
    SubmitField,
    BooleanField
)

from wtforms.ext.sqlalchemy.orm import model_form
from flask_boilerplate_utils.forms import Unique
from Application import app

class SightingForm(Form):
    description = TextField('Where?', [validators.Required()])
    username = TextField('Your Name (Blank for anon)', [validators.Optional()])
    submit = SubmitField('Submit', [validators.Optional()])


class EmailForm(Form):
    email = TextField('Your Email', [validators.Required(), validators.email()])
    submit = SubmitField('Submit', [validators.Optional()])
