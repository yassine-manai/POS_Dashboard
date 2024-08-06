
import yaml
import paramiko


def ssh_connect(hostname, username, password, port=22):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password, timeout=5)
        
        dk_file = './eposDeployment/dockercompose.yaml'
        
        sftp = ssh.open_sftp()
        with sftp.file(dk_file, 'r') as file:
            docker_compose_content = file.read().decode('utf-8')
        
        docker_compose_dict = yaml.safe_load(docker_compose_content)
        
        sftp.close()
        ssh.close()
        
        return True, "Connected successfully", docker_compose_dict
    
    except paramiko.AuthenticationException:
        return False, "Authentication failed", {}
    except paramiko.SSHException as ssh_exception:
        return False, f"Unable to establish SSH connection: {ssh_exception}", {}
    except FileNotFoundError:
        return False, f"File not found: {dk_file}", {}
    except yaml.YAMLError as yaml_exception:
        return False, f"Error parsing YAML file: {yaml_exception}", {}
    except Exception as e:
        return False, f"An error occurred: {str(e)}", {}