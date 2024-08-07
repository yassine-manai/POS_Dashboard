from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import yaml
from app.ssh_utils import ssh_connect

bp = Blueprint('routes', __name__)

POS_YAML_FILE = 'pos_data.yaml'
CARPARK_YAML_FILE = 'carparks_data.yaml'

def read_config(file_path, key):
    """ Read configuration from the YAML file """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get(key, [])

def write_config(file_path, key, data):
    """ Write configuration to the YAML file """
    with open(file_path, 'w') as file:
        yaml.dump({key: data}, file)

@bp.route('/')
def index():
    hosts = read_config(POS_YAML_FILE, 'pos')
    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    return render_template('index.html', hosts=hosts, carparks=carparks)

@bp.route('/edit/pos/<host_name>', methods=['GET', 'POST'])
def edit_pos_config(host_name):
    if request.method == 'POST':
        hostname = request.form['hostname']
        ip = request.form['ip']
        password = request.form['password']
        
        hosts = read_config(POS_YAML_FILE, 'pos')
        for host in hosts:
            if host['name'] == host_name:
                host['hostname'] = hostname
                host['ip'] = ip
                host['password'] = password
                break
        
        write_config(POS_YAML_FILE, 'pos', hosts)
        return redirect(url_for('routes.index'))
    
    hosts = read_config(POS_YAML_FILE, 'pos')
    host = next((item for item in hosts if item['name'] == host_name), None)
    return render_template('edit_pos.html', hosts=hosts, host=host)

@bp.route('/delete/pos/<host_name>')
def delete_pos_config(host_name):
    hosts = read_config(POS_YAML_FILE, 'pos')
    hosts = [host for host in hosts if host['name'] != host_name]
    write_config(POS_YAML_FILE, 'pos', hosts)
    return redirect(url_for('routes.index'))

@bp.route('/add/pos', methods=['POST'])
def add_pos_config():
    host_name = request.form['host_name']
    hostname = request.form['hostname']
    ip = request.form['ip']
    password = request.form['password']
    
    hosts = read_config(POS_YAML_FILE, 'pos')
    hosts.append({
        'name': host_name,
        'hostname': hostname,
        'ip': ip,
        'password': password
    })
    write_config(POS_YAML_FILE, 'pos', hosts)
    return redirect(url_for('routes.index'))

@bp.route('/edit/carpark/<int:carpark_id>/<pos_name>', methods=['GET', 'POST'])
def edit_carpark_config(carpark_id, pos_name):
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        username = request.form['username'] or None
        password = request.form['password'] or None

        carparks = read_config(CARPARK_YAML_FILE, 'carparks')
        for carpark in carparks:
            if carpark['id'] == carpark_id:
                for pos in carpark['pos']:
                    if pos['name'] == pos_name:
                        pos.update({
                            'name': name,
                            'ip': ip,
                            'username': username,
                            'password': password
                        })
                        break
                break
        write_config(CARPARK_YAML_FILE, 'carparks', carparks)
        return redirect(url_for('routes.index'))

    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    carpark = next((c for c in carparks if c['id'] == carpark_id), None)
    pos = next((p for p in carpark['pos'] if p['name'] == pos_name), None)
    return render_template('edit_carpark.html', carpark=carpark, pos=pos)

@bp.route('/delete/carpark/<int:carpark_id>/<pos_name>')
def delete_carpark_config(carpark_id, pos_name):
    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    for carpark in carparks:
        if carpark['id'] == carpark_id:
            carpark['pos'] = [pos for pos in carpark['pos'] if pos['name'] != pos_name]
            break
    write_config(CARPARK_YAML_FILE, 'carparks', carparks)
    return redirect(url_for('routes.index'))

@bp.route('/add/carpark/<int:carpark_id>', methods=['POST'])
def add_carpark_config(carpark_id):
    name = request.form['name']
    ip = request.form['ip']
    username = request.form['username'] or None
    password = request.form['password'] or None

    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    for carpark in carparks:
        if carpark['id'] == carpark_id:
            carpark['pos'].append({
                'name': name,
                'ip': ip,
                'username': username,
                'password': password
            })
            break
    write_config(CARPARK_YAML_FILE, 'carparks', carparks)
    return redirect(url_for('routes.index'))

@bp.route('/load_data/<int:carpark_id>/<pos_name>')
def load_data(carpark_id, pos_name):
    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
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

@bp.route('/add_carpark', methods=['POST'])
def add_carpark():
    carpark_id = int(request.form['carpark_id'])
    carpark_name = request.form['carpark_name']

    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    new_carpark = {
        'id': carpark_id,
        'name': carpark_name,
        'pos': []
    }
    carparks.append(new_carpark)
    write_config(CARPARK_YAML_FILE, 'carparks', carparks)
    return redirect(url_for('routes.index'))

@bp.route('/delete_carpark/<int:carpark_id>')
def delete_carpark(carpark_id):
    carparks = read_config(CARPARK_YAML_FILE, 'carparks')
    carparks = [carpark for carpark in carparks if carpark['id'] != carpark_id]
    write_config(CARPARK_YAML_FILE, 'carparks', carparks)
    return redirect(url_for('routes.index'))



if __name__ == '__main__':
    app.run(debug=True)
