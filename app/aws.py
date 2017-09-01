__author__    = "Phil Hendren aka dizzythinks"
__credits__   = ["Phil Hendren"]
__version__   = "1.0"

from flask import current_app
import boto.ec2
import boto.ec2.autoscale
import boto.ec2.elb
import boto.ec2.cloudwatch
import boto.elasticache
import boto.rds
import boto.dynamodb
import boto.sqs
import boto.sns
import boto.cloudformation
import boto.route53
import boto.redshift


def connect(account, region, service=None):
    aws_access_key_id = current_app.config['CONFIG']['accounts'][account]['aws_access_key_id']
    aws_secret_access_key  = current_app.config['CONFIG']['accounts'][account]['aws_secret_access_key']


    if service == 'ec2' or service == 'ebs' or service is None:
        conn = [x for x in boto.ec2.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn


    elif service == 'autoscale':
        conn = [x for x in boto.ec2.autoscale.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn


    elif service == 'elb':
        conn = [x for x in boto.ec2.elb.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'ami':
        conn = [x for x in boto.ec2.image.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn


    elif service == 'rds':
        conn = [x for x in boto.rds.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'dynamodb':
        conn = [x for x in boto.dynamodb.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'elasticache':
        conn = [x for x in boto.elasticache.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn


    elif service == 'sqs':
        conn = [x for x in boto.sqs.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'sns':
        conn = [x for x in boto.sns.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'cloudformation':
        conn = [x for x in boto.cloudformation.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'cloudwatch':
        conn = [x for x in boto.ec2.cloudwatch.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'redshift':
        conn = [x for x in boto.redshift.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn


def r53():
    account = current_app.config['CONFIG']['route53']['account']
    aws_access_key_id = current_app.config['CONFIG']['accounts'][account]['aws_access_key_id']
    aws_secret_access_key  = current_app.config['CONFIG']['accounts'][account]['aws_secret_access_key']    
    domain = current_app.config['CONFIG']['route53']['domain']
    zone_id = current_app.config['CONFIG']['route53']['zone_id']
    c = boto.connect_route53(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return c, domain, zone_id
