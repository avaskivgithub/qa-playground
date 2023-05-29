
import time
from collections import OrderedDict
from tests.tests.wui.base import BaseWUI


class TestWUI(BaseWUI):

    def test_get_all_empty_table(self):
        """Chack that headers of the empty results table are
        ['Test Id', 'Test Name', 'Test Res', 'Test Description', 'Fail / Error Desc']"""

        expected_list = [['Test Id', 'Test Name', 'Test Res', 'Test Description', 'Fail / Error Desc']]
        actual_list = self.browser.get_table_content_by_name(name='allTestsTable')
        assert actual_list == expected_list

    def test_get_with_record(self):
        """Check that record from Results db table is shown"""

        id, name, descr, res, error_desc = ('T1',
                                            'Test Name {}'.format(int(time.time())),
                                            'Test Description {}'.format(int(time.time())),
                                            0,
                                            'Failed {}'.format(int(time.time())))

        self.add_record(id, name, descr, res, error_desc)
        self.refresh_page_all_results()

        expected_record = [id, name, 'Failed', descr, error_desc]
        actual_list = self.browser.get_table_content_by_name(name=self.pg_index.Tables.allresults['name'])
        assert expected_record in actual_list

    def test_add_show(self):
        """Check /addShow page is opened after clicking 'Add Test' button"""

        self.browser.click_button(self.pg_index.Buttons.add['name'])

        opened_url = self.browser.url()
        assert (self.base_url + self.pg_add.uri) == opened_url

    def test_add_record(self):
        """Check add new test"""

        test_text = 'test{}'.format(int(time.time()))
        test_res = 'Failed'

        # OrderDict just to out of the curiosity to make fields populated in the order defined by dict
        test_data = OrderedDict()
        test_data[self.pg_add.Inputs.test_id['name']] = test_text,
        test_data[self.pg_add.Inputs.test_name['name']] = test_text,
        test_data[self.pg_add.Inputs.test_res['name']] = test_res

        # Open addShow page
        self.browser.click_button(self.pg_index.Buttons.add['name'])

        # Fill in fields
        for field_name, value in test_data.items():
            self.browser.fill_in_text_field(field_name, value)

        # Click Add to add record
        self.browser.click_button(self.pg_add.Buttons.add['name'])

        # Check that it is returned index page
        self.wait_for_index_page()
        opened_url = self.browser.url()
        assert (self.base_url + self.pg_index.uri) == opened_url

        # Check that record was added
        record = self.db.get_record_by_id(test_text)
        assert test_text == record['Name']

# EOF

