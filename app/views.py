from flask import *
import os
from decorators import validate_account_and_region
from aws import connect, r53
from sgaudit import get_reports, add_description
from app.models import IPWhitelist

elastatus  = Blueprint('elastatus', __name__)


@elastatus.route('/')
def index():
    default_account = current_app.config['CONFIG']['default_account']
    default_region  = current_app.config['CONFIG']['default_region']
    default_service = current_app.config['CONFIG']['default_service']
    return redirect(url_for('.'+default_service, account=default_account, region=default_region))


@elastatus.route('/<account>/<region>/ec2')
@validate_account_and_region
def ec2(account, region):
    c = connect(account, region, 'ec2')
    instances = c.get_only_instances()
    return render_template('ec2.html', region=region, instances=instances)


@elastatus.route('/<account>/<region>/ebs')
@validate_account_and_region
def ebs(account, region):
    c = connect(account, region, 'ebs')
    volumes = c.get_all_volumes()
    return render_template('ebs.html', volumes=volumes)


@elastatus.route('/<account>/<region>/snapshots')
@validate_account_and_region
def snapshots(account, region):
    c = connect(account, region, 'ec2')
    snapshots = c.get_all_snapshots(owner='self')
    return render_template('snapshots.html', region=region, snapshots=snapshots)


@elastatus.route('/<account>/<region>/autoscale')
@validate_account_and_region
def autoscale(account, region):
    c = connect(account, region, 'autoscale')
    asg = c.get_all_groups()
    return render_template('asg.html', region=region, asg=asg)


@elastatus.route('/<account>/<region>/elb')
@validate_account_and_region
def elb(account, region):
    c = connect(account, region, 'elb')
    elb = c.get_all_load_balancers()
    return render_template('elb.html', region=region, elb=elb)


@elastatus.route('/<account>/<region>/sg/<id>')
@validate_account_and_region
def sg(account, region, id):
    c = connect(account, region,'ec2')
    sg = c.get_all_security_groups(filters={'group-id': id})
    sg = add_description(sg)
    return render_template('sg.html', region=region, sg=sg)


@elastatus.route('/<account>/<region>/elasticache')
@validate_account_and_region
def elasticache(account, region):
    c = connect(account, region, 'elasticache')
    clusters = c.describe_cache_clusters(show_cache_node_info=True)
    clusters = clusters['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']
    return render_template('elasticache.html', region=region, clusters=clusters)


@elastatus.route('/<account>/<region>/route53')
def route53(account, region):
    c, domain, zone_id = r53()
    r = list()
    try:
        records = c.get_all_rrsets(zone_id)
        paginate = True
        while paginate:
            for item in records:
                r.append(item)
            paginate = records.next_token
    except:
        domain = None
    return render_template('r53.html', domain=domain, records=r)


@elastatus.route('/<account>/<region>/rds')
def rds(account, region):
    c = connect(account, region, 'rds')
    db_instances = c.get_all_dbinstances()
    return render_template('rds.html', db_instances=db_instances)


@elastatus.route('/<account>/<region>/dynamodb')
def dynamodb(account, region):
    c = connect(account, region, 'dynamodb')
    tables = c.list_tables()
    if tables:
        tables = [c.describe_table(x) for x in tables]
    else:
        tables = list()
    return render_template('dynamodb.html', tables=tables)


@elastatus.route('/<account>/<region>/cloudformation')
def cloudformation(account, region):
    c = connect(account, region, 'cloudformation')
    stacks = c.describe_stacks()
    return render_template('cloudformation.html', stacks=stacks)


@elastatus.route('/<account>/<region>/cloudformation/<stack_name>.json')
def get_template(account, region, stack_name):
    c = connect(account, region, 'cloudformation')
    template = c.get_template(stack_name)
    template = template["GetTemplateResponse"]["GetTemplateResult"]["TemplateBody"]
    response = make_response(template)
    response.headers["Content-Disposition"] = "attachment; filename=%s.json" % stack_name
    return response


@elastatus.route('/<account>/<region>/cloudwatch')
def cloudwatch(account, region):
    return render_template('cloudwatch.html')


@elastatus.route('/<account>/<region>/sns')
def sns(account, region):
    c = connect(account, region, 'sns')
    subscriptions = c.get_all_subscriptions()
    subscriptions = subscriptions['ListSubscriptionsResponse']['ListSubscriptionsResult']['Subscriptions']
    return render_template('sns.html', subscriptions=subscriptions)


@elastatus.route('/<account>/<region>/redshift')
def redshift(account, region):
    c = connect(account, region, 'redshift')
    clusters = c.describe_clusters()
    clusters = clusters['DescribeClustersResponse']['DescribeClustersResult']['Clusters']
    return render_template('redshift.html', clusters=clusters)


@elastatus.route('/<account>/<region>/sqs')
def sqs(account, region):
    c = connect(account, region, 'sqs')
    queues = list()
    all_queues = c.get_all_queues()
    for q in all_queues:
        url = 'https://sqs.%s.amazonaws.com%s' % (region, q.id)
        attributes = q.get_attributes()
        attributes['url'] = url
        queues.append(attributes)
    return render_template('sqs.html', queues=queues)


@elastatus.route('/<account>/<region>/sgaudit')
def sgaudit(account, region):
    c = connect(account, region, 'ec2')
    report, empty_groups = get_reports(c)
    return render_template('sgaudit.html', report=report)
