from flask import *
from app import db
from app import auth
from app import mail
from flask.ext.mail import Message
from app.models import IPWhitelist
import ipaddr


admin  = Blueprint('admin', __name__)


def sendmail(subject, content):
    msg = Message(sender=current_app.config['CONFIG']['admin']['email_from'],
                  recipients=current_app.config['CONFIG']['admin']['email_to'],
                  subject=subject,
                  body=content
                  )
    mail.send(msg)


@auth.get_password
def get_password(username):
    if username == current_app.config['CONFIG']['admin']['username']:
        return current_app.config['CONFIG']['admin']['password']
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)


@admin.route('/')
@auth.login_required
def index():
    return redirect(url_for('admin.whitelist'))


@admin.route('/whitelist')
@auth.login_required
def whitelist():
    records = IPWhitelist.query.all()
    return render_template('whitelist.html', records=records)


@admin.route('/whitelist/add', methods=['POST'])
@auth.login_required
def whitelist_add():
    try:
        is_ip = ipaddr.IPv4Network(request.form['cidr_ip'])
    except:
        is_ip = False

    if is_ip:
        check = IPWhitelist.query.filter_by(cidr_ip=request.form['cidr_ip']).first()
        if check:
            flash('IP Address already exists: %s' % request.form['cidr_ip'])
        else:
            new = IPWhitelist(request.form['cidr_ip'], request.form['description'])
            db.session.add(new)
            db.session.commit()
            if current_app.config['CONFIG']['admin']['enable_email']:
                try:
                    sendmail("IP Whitelist Updated", 
                         "New IP added to Whitelist: %s, %s" % (request.form['cidr_ip'], request.form['description'])
                         )
                    recipients = ', '.join(current_app.config['CONFIG']['admin']['email_to'])
                    flash('Email sent to %s' % recipients)
                except Exception, e:
                    flash('Email Error: %s' % e)
    else:
        flash('Invalid IP address: %s' % request.form['cidr_ip'])
    return redirect(url_for('admin.whitelist'))


@admin.route('/whitelist/delete/<record>')
@auth.login_required
def whitelist_delete(record):
    record = IPWhitelist.query.filter_by(id=record).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('admin.whitelist'))

