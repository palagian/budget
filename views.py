from flask import request, render_template, jsonify
from app import app, db
from models import Plan, Client, KAM, KAMClientAssociation, Project, FTE_price

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_id = request.form['client']
        project_name = request.form['project']
        group_id = request.form['group']  # Get the selected group ID from the form
        month = request.form['month']
        value = request.form['value']

        # Create a new project entry if the user input is not empty
        if project_name:
            project = Project(name=project_name)
            db.session.add(project)
            db.session.commit()

        # Get the ID of the project (whether it's new or already existing)
        project_id = project.id if project else None

        plan = Plan(client_id=client_id, project_id=project_id, group_id=group_id, month=month, value=value)
        db.session.add(plan)
        db.session.commit()

    clients = Client.query.all()
    kams = KAM.query.all()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    groups = FTE_price.query.all()  # Query all groups from the FTE_price table

    return render_template('budget_table/budget.html', clients=clients, kams=kams, months=months, groups=groups)


@app.route('/get_clients_for_kam/<int:kam_id>')
def get_clients_for_kam(kam_id):
    kam = KAM.query.get(kam_id)
    clients = kam.clients if kam else []
    client_options = [{'id': client.id, 'name': client.name} for client in clients]

    return jsonify(client_options)
