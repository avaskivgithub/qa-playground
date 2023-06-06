import pytest
from parameterized import parameterized
from tests.tests.base import Base

@pytest.mark.basic
class TestAPI(Base):

    def test_get_all_with_data(self):
        """Check /getall when there are tests in the Results table
        """
        self.db.add_results_record(id='T1', name='T1 summary')

        response = self.api.get_all()
        assert response.status_code == 200
                                 #'Instead of 200 was returned {}'.format(response.status_code))
        # nose_tools.assert_true(response.json()['Results'])

    def test_get_all_no_data(self):
        """Check /getall when Results table is empty
        """
        response = self.api.get_all()
        assert response.status_code == 200
        assert response.json()['Results'] == []

    def test_add_with_all_fields(self):
        """Check /add with all fields filled in
        """
        id, name, descr, res, error_desc = ('1', 'name', 'desc', 0, 'error')
        response = self.api.add(id, name, descr, res, error_desc)
        assert response.status_code == 200
        assert response.text == ''
        
        exp_record = {'Id': id,
                  'Name': name,
                  'Description': descr,
                  'Res': res,
                  'Error': error_desc}
        act_response = self.api.get_all()
        assert act_response.status_code == 200
        assert act_response.json()['Results'] == [exp_record]

    # https://stackoverflow.com/questions/18182251/does-pytest-parametrized-test-work-with-unittest-class-based-tests
    @parameterized.expand([
        ['StatusNotStarted', -1],
        ['StatusFailed', 0],
        ['StatusPassed', 1],
    ])
    def test_add_with_diff_Res(self, test_name, res_loop):
        """Check /add with different Res field values
        """
        id, name = ('1', 'name')
        response = self.api.add(id, name, res=res_loop)
        assert response.status_code == 200
        assert response.text == ''
        
        act_response = self.api.get_all()
        assert act_response.status_code == 200
        assert act_response.json()['Results'][0]['Res'] == res_loop