from flask import *
import os
from aws import connect
from sgaudit import get_reports
from app import db
from app import auth
from app import cache
from app.models import IPWhitelist


api  = Blueprint('api', __name__)


@auth.get_password
def get_password(username):
    if username == current_app.config['CONFIG']['admin']['username']:
        return current_app.config['CONFIG']['admin']['password']
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)


@api.route('/sgaudit')
@cache.cached()
def sgaudit_monitor():
    monitor = dict()
    for account in current_app.config['CONFIG']['accounts']:
        monitor[account] = dict()
        for region in current_app.config['CONFIG']['regions']:
            c = connect(account, region, 'ec2')
            report, empty_groups = get_reports(c)
            if report:
                monitor[account][region] = True
            else:
                monitor[account][region] = False
    return jsonify(sgaudit=monitor)