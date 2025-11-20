from request_handler import RequestHandler, RequestError


class RequestLibrary(object):
    """Test library for testing *RequestHandler* logic.

    Interacts with the http api caller directly using its ``call`` method.
    """

    def __init__(self):
        self._api_request_handler = RequestHandler()
        self._result_code = -1
        self._result_body = ''

    def call_get(self, uri):
        """Calls http GET``uri``.

        The given value is passed to the request handler directly.

        Examples:
        | Call GET| /api/users |

        """
        self._result_code, self._result_body = self._api_request_handler.call(http_method='get', uri=uri, params={'page': 1})

    def result_code_should_be(self, status_code):
        """Verifies that the current result is ``expected``.

        Example:
        | Call GET              | /api/users |
        | Result Code Should Be | 200        |
        """
        if  str(self._result_code) != str(status_code):
            raise AssertionError('%s != %s' % (self._result_code, status_code))