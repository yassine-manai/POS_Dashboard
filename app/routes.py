from flask import Flask, render_template, request, redirect, url_for
import yaml

app = Flask(__name__)

YAML_FILE = 'pos_data.yaml'

def read_config():
    """ Read configuration from the YAML file """
    with open(YAML_FILE, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('pos', [])

def write_config(hosts):
    """ Write configuration to the YAML file """
    with open(YAML_FILE, 'w') as file:
        yaml.dump({'pos': hosts}, file)

@app.route('/')
def index():
    hosts = read_config()
    return render_template('index.html', hosts=hosts)

@app.route('/edit/<host_name>', methods=['GET', 'POST'])
def edit_config(host_name):
    if request.method == 'POST':
        hostname = request.form['hostname']
        ip = request.form['ip']
        password = request.form['password']
        
        hosts = read_config()
        for host in hosts:
            if host['name'] == host_name:
                host['hostname'] = hostname
                host['ip'] = ip
                host['password'] = password
                break
        
        write_config(hosts)
        return redirect(url_for('index'))
    
    hosts = read_config()
    host = next((item for item in hosts if item['name'] == host_name), None)
    return render_template('index.html', hosts=hosts)

@app.route('/delete/<host_name>')
def delete_config(host_name):
    hosts = read_config()
    hosts = [host for host in hosts if host['name'] != host_name]
    write_config(hosts)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_config():
    host_name = request.form['host_name']
    hostname = request.form['hostname']
    ip = request.form['ip']
    password = request.form['password']
    
    hosts = read_config()
    hosts.append({
        'name': host_name,
        'hostname': hostname,
        'ip': ip,
        'password': password
    })
    write_config(hosts)
    return redirect(url_for('index'))

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