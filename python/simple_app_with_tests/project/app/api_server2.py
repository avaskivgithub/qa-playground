#!/usr/bin/python

# Based on examples:
# https://wiki.python.org/moin/BaseHttpServer
# https://pymotw.com/2/BaseHTTPServer/

"""
This version of server will work only with python 2
"""

import time
import BaseHTTPServer
import SocketServer
from urlparse import urlparse

from app.db import SqliteClient
import json
import logging

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 12345
logging.basicConfig(level=logging.DEBUG)

content_type = ('Content-type', 'application/json')

# Supported contexts  POST / GET
paths_to_dbmethod_map_post = {'/add': {'dbmethod': 'add_results_record'},
                             }

paths_to_dbmethod_map_get = {'/getall': {'dbmethod': 'get_all_resultrs_records'},
                             '/getrecord': {'dbmethod': 'get_results_record_by_id'},

                              '/setup': {'dbmethod': 'create_table_results'},
                              '/clear': {'dbmethod': 'delete_table_results'},
                             }


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        """Respond to POST requests: /add
        (see paths_to_dbmethod_map_post)

        Post data like:
          {"Res": 1, "Description": null, "Error": null, "Id": 3, "Name": "Test3"}"

        curl -d "{\"Res\": 1, \"Description\": null, \"Error\": null, \"Id\": 3, \"Name\": \"Test3\"}" http://127.0.0.1:12345/add
        """

        self.send_response(200)
        self.send_header(*content_type)
        self.end_headers()

        length = int(self.headers.getheader('content-length'))
        row_data = self.rfile.read(length)
        data = json.loads(row_data)

        logging.info(data)

        with SqliteClient() as dbcl:
            field_names = dbcl.table_results_column_names
            # param_names = ['id', 'name', 'descr', 'res', 'error_desc']
            param_names = SqliteClient._get_params_names_for_add_results_record()

            kwargs = {}
            for db_clmn_name, db_method_param_name in zip(field_names, param_names):
                kwargs[db_method_param_name] = data[db_clmn_name]

            db_method = getattr(dbcl, paths_to_dbmethod_map_post[self.path]['dbmethod'])
            # db_method(id=3, name='Test3', descr=None, res=0, error_desc='Issue-1')
            db_method(**kwargs)

    def do_GET(self):
        """Respond to GET requests: /getall, /getrecord?id=<record_id>, /setup, /clear
        (see paths_to_dbmethod_map_get)

        where,

        - /setup and /clear respectively creates and drops Results table
        - /getrecord?id=<record_id> returns:
        curl http://127.0.0.1:12345/getrecord?id=1 | python -m json.tool
                            {
                                "Description": null,
                                "Error": null,
                                "Id": 1,
                                "Name": "Test1",
                                "Res": 1
                            }
        - /getall returns:
        curl http://127.0.0.1:12345/getall | python -m json.tool
                    {
                        "Results": [
                            {
                                "Description": null,
                                "Error": null,
                                "Id": 1,
                                "Name": "Test1",
                                "Res": 1
                            },
                            {
                                "Description": "Test steps: \\n1. Step1",
                                "Error": "Failed with unexpected result",
                                "Id": 2,
                                "Name": "Test2",
                                "Res": 0
                            }
                        ]
                    }
        """

        self.send_response(200)
        self.send_header(*content_type)
        self.end_headers()

        query_context = urlparse(self.path).path

        query = urlparse(self.path).query
        query_params = {}
        if query:
            query_params = dict(param.split("=") for param in query.split("&"))

        with SqliteClient() as dbcl:

            try:
                db_method = getattr(dbcl, paths_to_dbmethod_map_get[query_context]['dbmethod'])
                data = db_method(**query_params)
            except:
                data = {}

        self.wfile.write(json.dumps(data))

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':

    server_class = BaseHTTPServer.HTTPServer
    # server_class = ThreadedHTTPServer

    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))


    # ab -n 500 -c 500 http://127.0.0.1:5000/:
    # - BaseHTTPServer.HTTPServer
    # - ThreadedHTTPServer apr_pollset_poll:

    #       The timeout specified has expired (70007)
    #       Total of 497 requests completed
    #     ==> /tmp/web_gui.py.log <==
    #     INFO:werkzeug:127.0.0.1 - - [06/Apr/2016 08:47:16] "GET / HTTP/1.0" 200 -
    #     Traceback (most recent call last):
    #       File "/usr/lib64/python2.7/SocketServer.py", line 295, in _handle_request_noblock
    #         self.process_request(request, client_address)
    #       File "/usr/lib64/python2.7/SocketServer.py", line 321, in process_request
    #         self.finish_request(request, client_address)
    #       File "/usr/lib64/python2.7/SocketServer.py", line 334, in finish_request
    #         self.RequestHandlerClass(request, client_address, self)
    #       File "/usr/lib64/python2.7/SocketServer.py", line 657, in __init__
    #         self.finish()
    #       File "/usr/lib64/python2.7/SocketServer.py", line 716, in finish
    #         self.wfile.close()
    #       File "/usr/lib64/python2.7/socket.py", line 279, in close
    #         self.flush()
    #       File "/usr/lib64/python2.7/socket.py", line 303, in flush
    #         self._sock.sendall(view[write_offset:write_offset+buffer_size])
    #     error: [Errno 32] Broken pipe