import os, time, subprocess
import paramiko
import logging
# from monitor_core import load_apps_for_test_results

def with_open_connection(func):

    def wrapper(self, *args, **kwrgs):
        self.open_connection()
        result = func(self, *args, **kwrgs)
        self.close_connection()
        return result

    return wrapper

class SystemMonitoringServerDeploy():

    sys_monit_code = 'monitor_cl_test_apps.py'
    sys_monit_source_path = os.path.join(os.path.dirname(__file__), sys_monit_code)

    sys_monit_deployed_root = '/tmp'
    sys_monit_deployed_server_path = os.path.join(sys_monit_deployed_root, sys_monit_code)

    sys_monit_core_source_path = os.path.join(os.path.dirname(__file__), 'monitor_core.py')

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

    def _deploy_monitor_code(self):

        self.copy_file(self.sys_monit_core_source_path, self.sys_monit_deployed_root)
        self.copy_file(self.sys_monit_source_path, self.sys_monit_deployed_server_path)

    @with_open_connection
    def start_top_monitor_server(self, result_dir, component_version):

        self._deploy_monitor_code()

        cmd = 'sh -c "python {} --start_monit start --result_dir {} --component_version {} &"'.format(self.sys_monit_deployed_server_path,
                                                                                                    result_dir,
                                                                                                    component_version)
        self.run_cmd(cmd)
        time.sleep(2)

    @with_open_connection
    def stop_top_monitor_server(self, result_dir, component_version):

        self._deploy_monitor_code()
        cmd = 'sh -c "python {} --start_monit stop --result_dir {} --component_version {} &"'.format(self.sys_monit_deployed_server_path,
                                                                                                   result_dir,
                                                                                                   component_version)
        self.run_cmd(cmd)
        time.sleep(2)


if __name__ == '__main__':

    result_dir = os.path.dirname(__file__)
    component_version = 'results_demo_from_deployment'

    deployer = SystemMonitoringServerDeploy()

    try:
        deployer.start_top_monitor_server(result_dir, component_version)
        #load_apps_for_test_results(time_to_run=10)
    finally:
        deployer.stop_top_monitor_server(result_dir, component_version)

# EOF