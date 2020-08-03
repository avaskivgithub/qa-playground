import nose.tools as nose_tools
from nose.plugins.attrib import attr

from tests.tests.base import Base


class TestAPI(Base):

    @attr(id='API-1')
    def test_get_all_with_data(self):
        """Check /getall when there are tests in the Results table
        """

        self.db.add_results_record(id='T1', name='T1 summary')

        response = self.api.get_all()
        nose_tools.assert_equals(200, response.status_code,
                                 'Instead of 200 was returned {}'.format(response.status_code))
        nose_tools.assert_true(response.json()['Results'])

    @attr(id='API-2')
    def test_get_all_no_data(self):
        """Check /getall when Results table is empty
        """

        response = self.api.get_all()
        nose_tools.assert_equals(200, response.status_code,
                                 'Instead of 200 was returned {}'.format(response.status_code))
        nose_tools.assert_false(response.json()['Results'])
