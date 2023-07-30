#import libs
from netmiko import ConnectHandler
from datetime import datetime, timedelta
import sys, re, logging, logging.handlers, socket, os, numbers, time
from icecream import ic

#global logging setting
logging.basicConfig(filename='logs/app-'+datetime.now().strftime('%Y_%m_%d_%I-%M-%S.log'), filemode='w+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)

#class network
class network:
    def __init__(self, user, password, target, target_type): self.user, self.password, self.target, self.target_type = user, password, target, target_type

    def execute_command(self, command):
        try:
            connection = ConnectHandler(device_type=self.target_type, host=self.target, username=self.user, password=self.password)
            output = connection.send_command(command, read_timeout=360)
            connection.disconnect()
            return output
        except Exception as e: logging.critical(str(e)); return None

    def write_to_file(self, filename, content):
        try:
            with open(filename, 'w+') as file:
                file.write(content)
        except IOError: logging.critical(f'Unable to write to the file {filename}.')

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                contents = file.read()
            return contents
        except FileNotFoundError: logging.critical(f'File {filename} not found.'); return None
        except IOError: logging.critical(f'Unable to read the file {filename}.'); return None

    def send_syslog(self, syslog_server_ip, message, port): 
        try:
            logger = logging.getLogger('my_logger'); 
            logger.setLevel(logging.INFO); 
            logger.addHandler(logging.handlers.SysLogHandler(address=(syslog_server_ip, port))); 
            logger.handlers[0].facility = logging.handlers.SysLogHandler.LOG_USER; 
            logger.handlers[0].setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(self.target)s - %(message)s')); 
            logger.info(message)   
        except Exception as e: logging.critical(str(e)); return None