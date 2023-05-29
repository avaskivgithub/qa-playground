#import nose.tools as nose_tools
#from nose.plugins.attrib import attr

from tests.tests.base import Base


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
