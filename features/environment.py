import logging
import os
from datetime import datetime

def before_all(context):

    context.logger = logging.getLogger('behave')
    context.logger.setLevel(logging.INFO)


    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)


    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    log_file = os.path.join(log_dir, f'testlog{timestamp}.log')


    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    context.logger.addHandler(file_handler)


    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    context.logger.addHandler(console_handler)

    context.logger.info("Logger configurado com sucesso")

def after_scenario(context, scenario):
    if hasattr(context, 'ssh'):
        try:
            context.ssh.close()
            context.logger.info("Conexao SSH fechada")
        except:
            context.logger.error("Erro ao fechar conexão SSH") 