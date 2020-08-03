#!/usr/bin/env python

import time
import os
import subprocess
import shutil
from tests.clients.loadcl import Load

# Need this method within system_monitoring script because it would be coppied to the box where app was started
def draw_gnuplot_chart(data_files_paths,
                        result_dir,
                        result_x_clmn_no=1,
                        result_y_clmn_no=2,
                        title='Results title',
                        xlable='Request X',
                        ylable='Request Y',
                        output_file='load_results.png',
                        if_rm_data_file=False):

        chart_file_path = os.path.join(result_dir, output_file)
        gnuplot_script_path = os.path.join(result_dir, 'gnuplot_load_result')

        # Create gnuplot_load_result script
        plot_args = []
        for file_path in data_files_paths:
            plot_args.append('"{}" using {}:{} title "{}" with lines'.format(file_path,
                                                                             result_x_clmn_no,
                                                                             result_y_clmn_no,
                                                                             os.path.basename(file_path).split('.')[0]))
        gnuplot_script = """#!/usr/bin/gnuplot -persist
            set grid
            set title "{}"
            set xlabel "{}"
            set ylabel "{}"

            set terminal png size 2000,1500 enhanced font "Helvetica,20"
            set output "{}"

            plot {}
        """.format(title,
                   xlable,
                   ylable,
                   chart_file_path,
                   ','.join(plot_args))

        # Draw chart (2D plots from data in )
        cmds = ["echo '{}' > {}".format(gnuplot_script, gnuplot_script_path),
                "chmod +x {}".format(gnuplot_script_path),
                "{}".format(gnuplot_script_path),

                "rm {}".format(gnuplot_script_path)
                ]

        for cmd in cmds:
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            time.sleep(1)

        # Cleanup data files data_files_paths
        if if_rm_data_file:
            for file_path in data_files_paths:
                subprocess.Popen("rm {}".format(file_path), stdout=subprocess.PIPE, shell=True)
                time.sleep(1)

        # print('Result chart: {}'.format(chart_file_path))

class SystemMonitoring(object):

    def __init__(self, process_names_top_grep, results_dir, component_version='demo-0.0.1'):

        self.process_names_top_grep = [process_names_top_grep] if isinstance(process_names_top_grep, str) else process_names_top_grep

        # Dir for saving logged data and drawn charts
        root_dir = results_dir if results_dir else '/tmp'
        self.results_dir = os.path.join(root_dir, component_version)

        self.monitor_top_for_pid_script = 'monitoring_top_for_pid.sh'
        self.monitor_top_for_pid_script_path = os.path.join('/tmp', self.monitor_top_for_pid_script)
        self.monitor_top_for_pid_script_created = False

        self.top_log_template = os.path.join(self.results_dir, 'loadTopForPID{}.dat')

        self.monitoring_pids = []
        self.monitoring_top_data_log_files = []

        self._initialize_monitoring_data()
        self._create_monitoring_top_bash_script()

    def _run_cli_cmd(self, cmd):

        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def _get_monitoring_top_bash_script_content(self):

        script_content = """#!/usr/bin/env bash

            app_pid=$1
            MONITORFILE=$2
            i=0

            if [ -e $MONITORFILE ]
            then
                rm $MONITORFILE
            fi

            while true ; do
                sleep 0.25
                echo $i $(top -p $app_pid -n 1 -b | grep $app_pid) >> $MONITORFILE
                i=$((i + 1))
            done
        """

        return script_content

    def _create_monitoring_top_bash_script(self):
        """Create bash script which would be used for monitoring"""

        if not self.monitor_top_for_pid_script_created:

            cmds = ["echo '{}' > {}".format(self._get_monitoring_top_bash_script_content(),
                                            self.monitor_top_for_pid_script_path),
                    "chmod +x {}".format(self.monitor_top_for_pid_script_path)]
            for cmd in cmds:
                self._run_cli_cmd(cmd)
                time.sleep(1)

            self.monitor_top_for_pid_script_created = True

    def _delete_monitoring_top_bash_script(self):

        self._run_cli_cmd('rm {}'.format(self.monitor_top_for_pid_script_path))
        self.monitor_top_for_pid_script_created = False

    def _init_pids(self):

        pids_list = []

        for proc_name in self.process_names_top_grep:
            cmd = "ps aux | grep '{}' | grep -v grep | awk '{{print $2}}'".format(proc_name)
            result = self._run_cli_cmd(cmd)
            try:
                pids_list.extend(result.stdout.read().split('\n')[:-1])
            except:
                pass

        self.monitoring_pids = [int(pid) for pid in pids_list]

    def _init_monitoring_top_data_log_files(self):

        if not self.monitoring_pids:
            self._init_pids()

        self.monitoring_top_data_log_files = []
        for pid in self.monitoring_pids:
            self.monitoring_top_data_log_files.append(self.top_log_template.format(pid))

    def _start_monitoring_top_by_pid(self, pid):

        cmd = "{} {} '{}'".format(self.monitor_top_for_pid_script_path, pid, self.top_log_template.format(pid))
        self._run_cli_cmd(cmd)

    def _initialize_monitoring_data(self):

        self._init_pids()  # init self.monitoring_pids
        self._init_monitoring_top_data_log_files() # init self.monitoring_top_data_log_files

    def get_monitored_pids(self):
        return self.monitoring_pids

    def get_monitored_top_data_log_files(self):
        return self.monitoring_top_data_log_files

    def _create_result_dir_with_cleanup(self):
        """Create dir for saving logged data and drawn charts
           (rm -rf this folder in case it exists with data from previos run)
        """
        try:
            shutil.rmtree(self.results_dir)
            time.sleep(3)
        except:
            pass
        os.mkdir(self.results_dir)

    def start_monitorings_top(self):

        # Create dir for saving logged data and drawn charts
        self._create_result_dir_with_cleanup()

        # Save ps aux output about monitored processes
        self.log_info_about_pids()

        # Start monitoring each of the pids
        for pid in self.monitoring_pids:
            self._start_monitoring_top_by_pid(pid)

    def stop_monitorings_top(self):

        cmd = "kill $(ps aux | grep {} | grep -v grep | awk '{{print $2}}')".format(self.monitor_top_for_pid_script)
        self._run_cli_cmd(cmd)
        time.sleep(2)

    def log_info_about_pids(self):

        info_file_path = os.path.join(self.results_dir, 'apps_info')
        for pid in self.monitoring_pids:
            self._run_cli_cmd("echo $(ps aux | grep {} | grep -v grep) >> {}".format(pid, info_file_path))

    def draw_top_monitoring_history(self, if_rm_data_file=False, if_stop_monit=True):

        if if_stop_monit:
            self.stop_monitorings_top()

        for chart_lable, y_clmn_no, output_name in [('%CPU', 10, 'cpu'),
                                                    ('%MEM', 11, 'mem'),
                                                    ('RES', 7, 'res')]:

            draw_gnuplot_chart(self.get_monitored_top_data_log_files(), self.results_dir,
                                result_x_clmn_no=1, result_y_clmn_no=y_clmn_no,
                                title='{} Monitoring History'.format(chart_lable),
                                xlable='Snapshot No',
                                ylable=chart_lable,
                                output_file='top_{}_monitoring_history.png'.format(output_name),
                                if_rm_data_file=if_rm_data_file)

def load_apps_for_test_results(time_to_run=2):

    requests_number = 1000
    concurrency = 100

    # 1. Test Data
    test_url_api = 'http://127.0.0.1:12345/edit/{}'
    test_url_gui = 'http://127.0.0.1:5000/'

    call_func_args_list = []
    for i in xrange(requests_number):
        call_func_args_list.append({'url': test_url_api.format(i)})

    # 2. Load Clients
    # with default call_func=requests.get
    load_cl_api = Load(call_func_args_list=call_func_args_list,
                       concurrency=concurrency)
    load_cl_gui = Load(call_func_args_list=requests_number * [{'url': test_url_gui}],
                       concurrency=concurrency)

    # 3. Load for time_to_run time
    start = time.time()
    while time.time() - start < time_to_run:
        for client in [load_cl_api, load_cl_gui]:
            results, _ = client.load_app()
            print(client.get_results_distribution())

if __name__ == '__main__':

    curent_dir = os.path.dirname(__file__)
    monitor_cl = SystemMonitoring(process_names_top_grep=['api_server.py', 'web_gui.py'],
                                  results_dir=curent_dir,
                                  component_version='results_demo_core_0.0.1')

    # ===> START monitoring (collecting data)
    monitor_cl.start_monitorings_top()

    # For demo purpose to load test app to have some spikes on chart
    load_apps_for_test_results(time_to_run=60)
    time.sleep(5)

    # ===> STOP monitoring and draw chart
    monitor_cl.stop_monitorings_top()

    # we've already stopped monitoring so there is no reason to stop one more time
    monitor_cl.draw_top_monitoring_history(if_stop_monit=False)

# EOF
