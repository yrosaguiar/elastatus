from flask import current_app

def get_reports(c):
    known_ips = current_app.config['CONFIG']['sgaudit']['known_ips']
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
                    if not grant.cidr_ip in known_ips and not grant.cidr_ip in excluded_ips:
                        if rule.from_port is None:
                            rule.from_port = 'ALL'
                        if rule.to_port is None:
                            rule.to_port = 'ALL'
                        report[group.name].append(
                            [grant.cidr_ip, rule.from_port, rule.to_port])
        if not report[group.name]:
            del report[group.name]
    return report, empty_groups





        
