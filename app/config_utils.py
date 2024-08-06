import configparser
import os

config_file = 'config/config.ini'

def read_config():
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    return config

def save_config(hostname, username, password):
    # Read the existing config
    config = read_config()
    
    # Ensure the 'POS' section exists
    if 'POS' not in config:
        config['POS'] = {}
    
    # Update or add the new configuration
    config['POS']['hostname'] = hostname
    config['POS']['username'] = username
    config['POS']['password'] = password
    
    # Write the updated config to file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    
    return True
