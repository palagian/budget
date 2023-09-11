from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projects = db.relationship('Project', secondary='client_project_association', lazy='subquery', backref=db.backref('clients', lazy=True))


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


class ClientProjectAssociation(db.Model):
    __tablename__ = 'client_project_association'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    client = db.relationship('Client', backref=db.backref('project_associations', lazy=True))
    project = db.relationship('Project', backref=db.backref('client_associations', lazy=True))


class FTE_price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)