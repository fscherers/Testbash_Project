import paramiko
from behave import given, when, then

@given('I connect via SSH to host "{host}" port {port:d} with username "{username}" and password "{password}"')
def step_connect_ssh(context, host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password, 
    timeout=10)
    context.ssh = ssh

@when('I check disk usage')
def step_check_disk_usage(context):
    stdin, stdout, stderr = context.ssh.exec_command('df -h /')
    context.disk_output = stdout.read().decode().strip()

@when('I check nginx service status')
def step_check_status(context):
    stdin, stdout, stderr = context.ssh.exec_command('systemctl is-active nginx')
    context.nginx_output = stdout.read().decode().strip()

@then('the server should be healthy')
def step_validate_server_health(context):
    disk_output = context.disk_output
    nginx_output = context.nginx_output

    context.logger.info(f"[DISK] Output: {disk_output}")
    context.logger.info(f"[NGINX] Output: {nginx_output}")

    # Validação simples
    if '100%' in disk_output:
        raise AssertionError("Disk usage too high!")

    if 'nginx' not in nginx_output:
        raise AssertionError("Nginx service not running!")

    context.logger.info("Servidor considerado saudável")
