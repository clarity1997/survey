import json
import os
import subprocess
import sys
import socket
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_requirements(directory):
    try:
        subprocess.check_call(['pipreqs', directory, '--force'])
        logging.info("requirements.txt has been generated successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate requirements.txt: {e}")
        sys.exit(1)

    requirements_file_path = os.path.join(directory, 'requirements.txt')
    with open(requirements_file_path, 'r') as f:
        lines = f.readlines()

    dependencies = {
        "Werkzeug": "Werkzeug==3.1.0\n",
        "PyMuPDF": "PyMuPDF==1.25.1\n",
        "python-docx": "python-docx==1.1.2\n"
    }

    dep_dict = {}
    for line in lines:
        package_name, version = line.strip().split('==')
        if package_name.lower() != "fitz":
            dep_dict[package_name] = line.strip()

    for dep, dep_line in dependencies.items():
        dep_dict[dep] = dep_line.strip()

    with open(requirements_file_path, 'w') as f:
        for dep_line in dep_dict.values():
            f.write(dep_line + '\n')

    logging.info("Updated requirements.txt with specified dependencies and removed 'fitz' if present.")

def create_dockerfile(directory):
    dockerfile_content = '''
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt
    COPY . .

    CMD ["python", "app.py"]
    '''

    dockerfile_path = os.path.join(directory, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)
    logging.info("Dockerfile has been created successfully.")

def find_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def build_docker_image(directory, image_name):
    try:
        subprocess.check_call(['docker', 'build', '-t', image_name, directory])
        logging.info(f"Docker image '{image_name}' has been built successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to build Docker image: {e}")
        sys.exit(1)

def get_container_address(container_name):
    try:
        result = subprocess.run(['docker', 'inspect', container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Failed to inspect container '{container_name}': {result.stderr}")
            return

        container_info = json.loads(result.stdout)
        if not container_info:
            logging.error(f"No information found for container '{container_name}'.")
            return

        network_settings = container_info[0].get('NetworkSettings', {})
        ports = network_settings.get('Ports', {})

        addresses = [f"http://127.0.0.1:{binding['HostPort']}" for port, bindings in ports.items() if bindings for binding in bindings]

        if addresses:
            logging.info(f"Container '{container_name}' is accessible at the following addresses:")
            for address in addresses:
                return address
        else:
            logging.error(f"No accessible addresses found for container '{container_name}'.")
            return ""
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logging.error(f"An error occurred while retrieving the container address: {e}")
        return ""

def ensure_network_exists(network_name):
    try:
        result = subprocess.run(['docker', 'network', 'ls', '--format', '{{json .}}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Failed to list Docker networks: {result.stderr}")
            return

        networks = result.stdout.splitlines()
        network_exists = any(json.loads(network)['Name'] == network_name for network in networks)

        if network_exists:
            logging.info(f"Network '{network_name}' already exists.")
        else:
            subprocess.check_call(['docker', 'network', 'create', '--driver', 'bridge', network_name])
            logging.info(f"Network '{network_name}' created successfully.")
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logging.error(f"An error occurred while checking or creating the network: {e}")

def run_docker_container(directory, image_name, container_name, unused_port, network_name):
    unused_port = 9987
    swap_data_dir = os.path.join(os.path.abspath(directory), '..', 'swap_data')
    try:
        subprocess.check_call([
            'docker', 'run', '-d', '--name', container_name,
            '-p', f'{unused_port}:5000',
            '-v', f'{os.path.abspath(directory)}:/app',
            '-v', f'{swap_data_dir}:/app/swap_data',
            '--network', f'{network_name}',
            image_name
        ])
        logging.info(f"Docker container '{container_name}' has been started successfully on port {unused_port}.")
        return f'http://127.0.0.1:{unused_port}'
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start Docker container: {e}")
        sys.exit(1)

def calculate_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except IOError as e:
        logging.error(f"Failed to read file '{file_path}': {e}")
        sys.exit(1)

def image_exists(image_name):
    try:
        result = subprocess.run(['docker', 'images', '-q', image_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0 and bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check if Docker image exists: {e}")
        return False

def container_exists(container_name):
    try:
        result = subprocess.run(['docker', 'ps', '-a', '-q', '-f', f'name={container_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0 and bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check if Docker container exists: {e}")
        return False

def package_flask_app(directory, network_name, image_name='flask_app_image_survey', container_name='flask_app_container_survey'):
    if not os.path.isdir(directory):
        logging.error(f"The specified directory '{directory}' does not exist.")
        sys.exit(1)
    ensure_network_exists(network_name)
    app_file_path = os.path.join(directory, 'app.py')
    requirements_file_path = os.path.join(directory, 'requirements.txt')

    if not os.path.exists(app_file_path):
        logging.error(f"The specified Flask app file '{app_file_path}' does not exist.")
        sys.exit(1)

    requirements_hash = calculate_file_hash(requirements_file_path) if os.path.exists(requirements_file_path) else None

    generate_requirements(directory)
    new_requirements_hash = calculate_file_hash(requirements_file_path)

    if requirements_hash != new_requirements_hash or not image_exists(image_name) or not container_exists(container_name):
        try:
            subprocess.check_call(['docker', 'rm', '-f', container_name])
            logging.info("Dependencies have changed or image/container does not exist. Rebuilding Docker image.")
        except subprocess.CalledProcessError:
            logging.warning(f"No existing Docker container '{container_name}' to remove.")
        create_dockerfile(directory)
        build_docker_image(directory, image_name)
        unused_port = find_unused_port()
        logging.info(f"Using unused port: {unused_port}")
        return run_docker_container(directory, image_name, container_name, unused_port, network_name)
    else:
        logging.info("Dependencies have not changed and image/container exist. Restarting Docker container.")
        try:
            subprocess.check_call(['docker', 'restart', container_name])
            address = get_container_address(container_name)
            logging.info(f"Docker container '{container_name}' has been restarted successfully.")
            return address
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to restart Docker container: {e}")
            sys.exit(1)