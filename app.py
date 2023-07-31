from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

from views import *
from models import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5001, debug=True, template_folder='budget_table')