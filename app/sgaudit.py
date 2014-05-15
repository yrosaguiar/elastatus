from models import IPWhitelist
from flask import current_app


def get_reports(c):
    ip_whitelist = [x.cidr_ip for x in IPWhitelist.query.all()]
    excluded_groups = current_app.config['CONFIG']['sgaudit']['excluded_groups']
    excluded_ips = current_app.config['CONFIG']['sgaudit']['excluded_ips']
    groups = [x for x in c.get_all_security_groups() if not x.name in excluded_groups]
    empty_groups = list()
    report = dict()
    for group in groups:
        report[group.name] = list()
        if not group.rules:
            del report[group.name]
            empty_groups.append(group.name)
            continue
        for rule in group.rules:
            for grant in rule.grants:
                if grant.cidr_ip is None or grant.cidr_ip is False:
                    continue
                else:
                    if not grant.cidr_ip in ip_whitelist and not grant.cidr_ip in excluded_ips:
                        if rule.from_port is None:
                            rule.from_port = 'ALL'
                        if rule.to_port is None:
                            rule.to_port = 'ALL'
                        report[group.name].append(
                            [grant.cidr_ip, rule.from_port, rule.to_port])
        if not report[group.name]:
            del report[group.name]
    return report, empty_groups


def add_description(sg_obj):
    """This feels wrong but I need to add metadata from DB whitelist to
    the boto object so I can access it from the template in a simple way. 
    Sorry"""
    excluded_ips = current_app.config['CONFIG']['sgaudit']['excluded_ips']
    for i in sg_obj:
        for rule in i.rules:
            for grant in rule.grants:
                if grant.cidr_ip:
                    record = IPWhitelist.query.filter_by(cidr_ip=grant.cidr_ip).first()
                    if record:
                        grant.description = record.description
                    else:
                        if grant.cidr_ip in excluded_ips:
                            grant.description = "Explicitly excluded from whitelist in config"
                        else:
                            grant.description = "Not in whitelist. Unknown"
                else:
                    continue
    return sg_obj


