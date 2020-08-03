from tests.clients.wuicl import WUI
from tests.clients.data.wui_descriptors import PageIndex, PageAdd
from tests.tests.base import Base


class BaseWUI(Base):

    @classmethod
    def setUpClass(cls):

        super(BaseWUI, cls).setUpClass()

        cls.browser = WUI()
        cls.base_url = 'http://127.0.0.1:5000'
        cls.browser.open_page(cls.base_url + '/')

        cls.pg_index = PageIndex()
        cls.pg_add = PageAdd()

    @classmethod
    def tearDownClass(cls):

        cls.browser.close()
        super(BaseWUI, cls).tearDownClass()

    def setUp(self):

        super(BaseWUI, self).setUp()
        self.refresh_page_all_results()

    def refresh_page_all_results(self):

        self.browser.open_page(self.base_url + self.pg_index.uri)

    def wait_for_index_page(self):

        # Wait while Delete All Tests button appears
        self.browser.wait_element_present('name', self.pg_index.Buttons.delete['name'], wait_timeout=1)


# EOF

