import pytest
import os
from tests.clients.loadcl import Load, load_with_multiprocessing
from tests.clients.system_monitoring.monitor_deploy import SystemMonitoringServerDeploy
from tests.tests.wui.base import BaseWUI
from tests.tests.base import Base


def _procces_response(result):

    try:
        res = getattr(result, 'status_code')
    except Exception as e:
        res = str(e.message)

    return res

@pytest.mark.load
class TestLoadWUI(Base):

    @classmethod
    def setUpClass(cls):

        super(TestLoadWUI, cls).setUpClass()

        cls.result_dir = os.path.join(os.path.dirname(__file__), 'plots')
        cls.component_version = 'demo_0_0_0'

        cls.monitor = SystemMonitoringServerDeploy()
        cls.monitor.start_top_monitor_server(cls.result_dir, cls.component_version)

    @classmethod
    def tearDownClass(cls):

        cls.monitor.stop_top_monitor_server(cls.result_dir, cls.component_version)
        super(TestLoadWUI, cls).tearDownClass()

    def test_root_500_requests_500_concurrency(self):
        """Load http://127.0.0.1:5000/ by 500 requests sent simultaneously"""

        requests_number = 500
        rate = 500
        output_file = '{}_load_wui_test_1.png'.format(self.component_version)

        self.db.add_results_record(id='T1', name='T1 summary')

        load_cl = Load(call_func=self.wui._get,
                       call_func_args_list=requests_number * [{'url': '/'}],
                       concurrency=rate,
                       result_dir=self.result_dir)
        load_cl.load_app()
        load_cl.draw_elapsed_time_distribution(output_file=output_file)

        print(load_cl.get_results_distribution())
        assert {200: requests_number} == load_cl.get_results_distribution()
                        #'Instead of 200 for all requests were returned {}'.format(load_cl.get_results_distribution()))

    def _test_root_500_requests_500_concurrency_multiprocessing(self):
        """Load http://127.0.0.1:5000/ by 500 requests sent simultaneously"""

        requests_number = 5
        rate = 5

        self.db.add_results_record(id='T1', name='T1 summary')

        #   File "/home/avaskiv/Dropbox/test_python_sh/python/simple_app_with_tests/project/tests/clients/loadcl.py", line 45, in load_with_multiprocessing
        #     results_all = pool.map(worker_multiprocessing, pool_args)
        #   File "/usr/lib64/python2.7/multiprocessing/pool.py", line 251, in map
        #     return self.map_async(func, iterable, chunksize).get()
        #   File "/usr/lib64/python2.7/multiprocessing/pool.py", line 558, in get
        #     raise self._value
        # PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
        # http://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
        # The problem is that multiprocessing must pickle things to sling them among processes, and bound methods are not picklable
        results_distribution, all_results = load_with_multiprocessing(concurrency=rate,
                                                                      call_func=self.wui._get,
                                                                      call_func_args_list=requests_number * [{'url': '/'}],
                                                                      res_func=_procces_response)

        print(results_distribution)
        assert {200: requests_number} == results_distribution
                        #'Instead of 200 for all requests were returned {}'.format(results_distribution))

# EOF

