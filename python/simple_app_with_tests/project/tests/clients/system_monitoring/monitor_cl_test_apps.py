#!/usr/bin/env python

from optparse import OptionParser
from tests.clients.system_monitoring.monitor_core import SystemMonitoring

if __name__ == '__main__':

    # monitor_deploy.py will copy monitor_cl_test_apps.py script to the box where app was started
    #  and then start / stop this client:
    # > python monitor_cl_test_apps.py -s start -r /home/avaskiv/Downloads
    # > python monitor_cl_test_apps.py -s stop -r /home/avaskiv/Downloads

    parser = OptionParser()
    parser.add_option("-s", "--start_monit", dest="start_monitoring",
                      help="start / stop monitoring")
    parser.add_option("-r", "--result_dir", dest="result_dir",
                      help="absolute path to result dir")
    parser.add_option("-c", "--component_version", dest="component_version",
                      help="component version for naming subfolder in result dir")

    (options, args) = parser.parse_args()

    monitor_cl = SystemMonitoring(process_names_top_grep=['api_server.py', 'web_gui.py'],
                                  results_dir=options.result_dir,
                                  component_version=options.component_version)

    if options.start_monitoring in ['start', 'Start', 'True', 'true', '1']:
        # ('===> START monitoring (collecting data)')
        monitor_cl.start_monitorings_top()

    else:
        # ('===> STOP monitoring and draw chart')
        monitor_cl.stop_monitorings_top()

        # we've already stopped monitoring so there is no reason to stop one more time
        monitor_cl.draw_top_monitoring_history(if_stop_monit=False)

# EOF
