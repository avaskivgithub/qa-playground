import os, time, subprocess
import paramiko
import logging

def with_open_connection(func):

    def wrapper(self, *args, **kwrgs):
        self.open_connection()
        result = func(self, *args, **kwrgs)
        self.close_connection()
        return result

    return wrapper

class TestServerDeploy():

    webserver_code = 'webserver_mockup.py'
    webserver_source_path = os.path.join(os.path.dirname(__file__), webserver_code)
    webserver_full_path = os.path.join('/tmp', webserver_code)

    log_path_template = '/tmp/webserver_{}.log'

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    def __init__(self, hostname='127.0.0.1', username=None, password=None):


        self.conn = None # None means that we are deploying to the same host no reason to open ssh connection

        if hostname != '127.0.0.1':
            self.hostname = hostname
            self.username = username
            self.password = password

            self.conn = paramiko.SSHClient()

    def open_connection(self):

        self.logger.warn('Open connection')

        if self.conn:
            self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conn.connect(self.hostname, username=self.username, password=self.password, look_for_keys=False)

    def close_connection(self):

        self.logger.warn('Close connection')

        if self.conn:
            self.conn.close()

    def copy_file(self, source, destination):

        if self.conn:
            self.logger.warn('cp {} {}'.format(source, destination))
            scp = self.conn.open_sftp()
            scp.put(source, destination)
            scp.close()
        else:
            self.run_cmd('cp {} {}'.format(source, destination))

    def run_cmd(self, cmd):

        self.logger.warn(cmd)

        if self.conn:
            self.conn.exec_command(cmd)
        else:
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    @with_open_connection
    def deploy_server(self, port):

        log_path = self.log_path_template.format(port)

        self.copy_file(self.webserver_source_path, self.webserver_full_path)

        # cmd = "nohup python {} {} > {} & &> /dev/null".format(self.webserver_full_path, port, log_path)
        cmd = 'sh -c "python {} {} > {} 2>&1 &"'.format(self.webserver_full_path, port, log_path)

        self.run_cmd(cmd)
        time.sleep(2)

        self.port = port
        self.log_path = log_path

    @with_open_connection
    def kill_server(self, port):

        # http://stackoverflow.com/questions/268629/how-to-stop-basehttpserver-serve-forever-in-a-basehttprequesthandler-subclass
        started_service = "{} {}".format(self.webserver_code, port)

        # Stop webserver mockup
        cmd = "kill $(ps aux|grep '{}' |grep -v 'grep'|awk '{{print $2}}') 2> /dev/null".format(started_service)
        self.run_cmd(cmd)

        # Delete code and log file
        log_path = self.log_path_template.format(port)

        for file_path in (self.webserver_full_path, log_path):
            self.run_cmd('rm {}'.format(file_path))


if __name__ == '__main__':

    deployer = TestServerDeploy()
    # deployer.deploy_server(11378)
    deployer.kill_server(11378)

