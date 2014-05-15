from app import app
from app import db


class IPWhitelist(db.Model):
    __tablename__ = "ip_whitelist"

    id            = db.Column(db.Integer(), primary_key=True)
    cidr_ip       = db.Column(db.String())
    description   = db.Column(db.Text())
 
    def __init__(self, cidr_ip, description):
        self.cidr_ip       = cidr_ip
        self.description   = description


