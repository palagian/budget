from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('plans', lazy=True))
    month = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)


class KAM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    clients = db.relationship('Client', secondary='kam_client_association', lazy='subquery', backref=db.backref('kams', lazy=True))


class KAMClientAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kam_id = db.Column(db.Integer, db.ForeignKey('kam.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    kam = db.relationship('KAM', backref=db.backref('client_associations', lazy=True))
    client = db.relationship('Client', backref=db.backref('kam_associations', lazy=True))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class FTE_price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)