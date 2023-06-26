import pytest
import os
from tests.clients.loadcl import Load
from tests.clients.system_monitoring.monitor_deploy import SystemMonitoringServerDeploy
from tests.tests.base import Base

@pytest.mark.load
class TestLoadAPI(Base):

    @classmethod
    def setUpClass(cls):

        super(TestLoadAPI, cls).setUpClass()

        cls.result_dir = os.path.join(os.path.dirname(__file__), 'plots')
        cls.component_version = 'demo_0_0_0'

        cls.monitor = SystemMonitoringServerDeploy()
        cls.monitor.start_top_monitor_server(cls.result_dir, cls.component_version)

    @classmethod
    def tearDownClass(cls):

        cls.monitor.stop_top_monitor_server(cls.result_dir, cls.component_version)
        super(TestLoadAPI, cls).tearDownClass()

    def test_get_all_1000_requests(self):
        """Check /getall with 1000 requests sent with rate=100
        """
        requests_number = 1000
        rate = 100
        output_file = '{}_load_api_test_1.png'.format(self.component_version)

        self.db.add_results_record(id='T1', name='T1 summary')

        load_cl = Load(call_func=self.api.get_all,
                       call_func_args_list=requests_number * [{}],
                       concurrency=rate,
                       result_dir=self.result_dir)
        load_cl.load_app()
        load_cl.draw_elapsed_time_distribution(output_file=output_file)

        assert load_cl.get_results_distribution() == {200: requests_number}
                        # 'Instead of 200 for all requests were returned {}'.format(load_cl.get_results_distribution()))

    def test_edit_1000_requests(self):
        """Check /add with 1000 requests sent with rate=100 when edit the same record
        """
        requests_number = 1000
        rate = 100
        output_file = '{}_load_api_test_2.png'.format(self.component_version)

        record_id = 'T1'
        self.db.add_results_record(id=record_id, name='T1 summary')

        add_args_list = []
        for i in range(requests_number):
            record = {'id': record_id,
                      'name': 'T1 summary {}'.format(i),
                      'descr': 'T1 descr {}'.format(i),
                      'res': 0,
                      'error_desc': 'T1 error {}'.format(i)}
            add_args_list.append(record)

        load_cl = Load(call_func=self.api.add,
                       call_func_args_list=add_args_list,
                       concurrency=rate,
                       result_dir=self.result_dir)
        load_cl.load_app()
        load_cl.draw_elapsed_time_distribution(output_file=output_file)

        assert load_cl.get_results_distribution() == {200: requests_number}
