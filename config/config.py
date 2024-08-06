import configparser

config_file_path = 'config/config.ini'

config = configparser.ConfigParser()
config.read(config_file_path)

class Config:
    LEVEL= config.get('DEBUG', 'LEVEL', fallback='DEBUG')
    LOG_ON_FILE= config.get('DEBUG', 'LOG_ON_FILE', fallback='True')
    FILENAME= config.get('DEBUG', 'FILENAME', fallback='PIC.log')
    FILE_SIZE=config.getint('DEBUG', 'FILE_SIZE', fallback=50)

    APP_IP = config.get('APP', 'APP_IP', fallback='127.0.0.1')
    APP_PORT = config.getint('APP', 'APP_PORT', fallback=8100)










