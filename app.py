from flask import Flask, render_template, request, redirect, url_for, jsonify
import yaml
from app.ssh_utils import ssh_connect

app = Flask(__name__)

YAML_FILE = 'carparks_data.yaml'

def read_config():
    """Read configuration from the YAML file"""
    with open(YAML_FILE, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('carparks', [])

def write_config(carparks):
    """Write configuration to the YAML file"""
    with open(YAML_FILE, 'w') as file:
        yaml.dump({'carparks': carparks}, file)

@app.route('/')
def index():
    carparks = read_config()
    return render_template('index.html', carparks=carparks)

@app.route('/edit/<int:carpark_id>/<pos_name>', methods=['GET', 'POST'])
def edit_config(carpark_id, pos_name):
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        username = request.form['username'] or None
        password = request.form['password'] or None
        site = request.form['site']

        carparks = read_config()
        for carpark in carparks:
            if carpark['id'] == carpark_id:
                for pos in carpark['pos']:
                    if pos['name'] == pos_name:
                        pos.update({
                            'name': name,
                            'ip': ip,
                            'username': username,
                            'password': password,
                            'site': site
                        })
                        break
                break
        write_config(carparks)
        return redirect(url_for('index'))

    carparks = read_config()
    carpark = next((c for c in carparks if c['id'] == carpark_id), None)
    pos = next((p for p in carpark['pos'] if p['name'] == pos_name), None)
    return render_template('edit.html', carpark=carpark, pos=pos)

@app.route('/delete/<int:carpark_id>/<pos_name>')
def delete_config(carpark_id, pos_name):
    carparks = read_config()
    for carpark in carparks:
        if carpark['id'] == carpark_id:
            carpark['pos'] = [pos for pos in carpark['pos'] if pos['name'] != pos_name]
            break
    write_config(carparks)
    return redirect(url_for('index'))

@app.route('/add/<int:carpark_id>', methods=['POST'])
def add_config(carpark_id):
    name = request.form['name']
    ip = request.form['ip']
    username = request.form['username'] or None
    password = request.form['password'] or None
    site = request.form['site']

    carparks = read_config()
    for carpark in carparks:
        if carpark['id'] == carpark_id:
            carpark['pos'].append({
                'name': name,
                'ip': ip,
                'username': username,
                'password': password,
                'site': site
            })
            break
    write_config(carparks)
    return redirect(url_for('index'))

@app.route('/load_data/<int:carpark_id>/<pos_name>')
def load_data(carpark_id, pos_name):
    carparks = read_config()
    carpark = next((c for c in carparks if c['id'] == carpark_id), None)
    pos = next((p for p in carpark['pos'] if p['name'] == pos_name), None)

    if not pos:
        return jsonify({'success': False, 'message': 'POS not found'})

    success, message, docker_compose_data = ssh_connect(pos['ip'], pos['username'], pos['password'])
    if not success:
        return jsonify({'success': False, 'message': message})

    services = []
    for service_name, service_data in docker_compose_data.get('services', {}).items():
        services.append({
            'name': service_name,
            'image': service_data.get('image', 'N/A')
        })

    return jsonify({
        'success': True,
        'message': message,
        'services': services,
        'docker_compose': docker_compose_data
    })


@app.route('/add_carpark', methods=['POST'])
def add_carpark():
    carpark_id = int(request.form['carpark_id'])
    carpark_name = request.form['carpark_name']

    carparks = read_config()
    new_carpark = {
        'id': carpark_id,
        'name': carpark_name,
        'pos': []
    }
    carparks.append(new_carpark)
    write_config(carparks)
    return redirect(url_for('index'))

@app.route('/delete_carpark/<int:carpark_id>')
def delete_carpark(carpark_id):
    carparks = read_config()
    carparks = [carpark for carpark in carparks if carpark['id'] != carpark_id]
    write_config(carparks)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)