from flask import request, render_template, jsonify
from app import app, db
from models import Plan, Client, KAM, KAMClientAssociation, Project, FTE_price, ClientProjectAssociation

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        kam_id = request.form['kam']
        client_id = request.form['client']
        project_id = request.form['project']
        group_id = request.form['group']
        month = request.form['month']
        value = request.form['value']


        plan = Plan(kam_id=kam_id, client_id=client_id, project_id=project_id, group_id=group_id, month=month, value=value)
        db.session.add(plan)
        db.session.commit()

    clients = Client.query.all()
    kams = KAM.query.all()
    projects = Project.query.all()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    groups = FTE_price.query.all()  # Query all groups from the FTE_price table

    return render_template('budget_table/budget.html', clients=clients, kams=kams, projects=projects, months=months, groups=groups)


@app.route('/get_clients_for_kam/<int:kam_id>')
def get_clients_for_kam(kam_id):
    kam = KAM.query.get(kam_id)
    clients = kam.clients if kam else []
    client_options = [{'id': client.id, 'name': client.name} for client in clients]

    return jsonify(client_options)


@app.route('/get_projects_for_client/<int:client_id>')
def get_projects_for_client(client_id):
    client = Client.query.get(client_id)
    projects = client.projects if client else []
    project_options = [{'id': project.id, 'name': project.name} for project in projects]

    print("Client ID:", client_id)
    print("Client:", client)
    print("Projects:", project_options)

    return jsonify(project_options)
