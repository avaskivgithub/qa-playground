import sys, time
import BaseHTTPServer
from urlparse import urlparse

error_log_path = '/tmp/webserver_errors.log'


class TestHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            time.sleep(0.01)
            data = urlparse(self.path).path

            self.send_response(200)

            try:
                self.end_headers()
            except Exception as e:

                with open(error_log_path, 'a') as f:
                    f.write(str(e.message))

            self.wfile.write('Received: {}'.format(data))

        except Exception as e:

            # "broken pipe" exception means that your code tried to write to a socket/pipe which the other end has closed
            # "connection reset by peer" exception means that your code tried to read from a dead socket

            with open(error_log_path, 'a') as f:
                f.write(str(e))

    # # suppress the stderr log output produced every time a client connects to server
    # def log_message(self, format, *args):
    #     return

if __name__ == '__main__':

    port = int(sys.argv[1])

    with open(error_log_path, 'w') as f:
        f.write('')

    try:

        http_server = BaseHTTPServer.HTTPServer(('', port), TestHttpHandler)
        http_server.serve_forever()

    except Exception as e:

        with open(error_log_path, 'a') as f:
            f.write(str(e.message))


# lsof -i :port

# andriana@linux:~$ lsof -p 7911
# lsof: WARNING: can't stat() tracefs file system /sys/kernel/debug/tracing
#       Output information may be incomplete.
# COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
# ....
# python  7911 andriana    0r  FIFO   0,10      0t0   67677 pipe
# python  7911 andriana    1w   REG   0,48        0  460856 /tmp/webserver_11454.log
# python  7911 andriana    2w  FIFO   0,10      0t0   67679 pipe
# python  7911 andriana    3u  IPv4  66930      0t0     TCP *:11454 (LISTEN)
# python  7911 andriana    7r   CHR    1,9      0t0    1034 /dev/urandom
#
#
#
# andriana@linux:~$ lsof -p 7986
# lsof: WARNING: can't stat() tracefs file system /sys/kernel/debug/tracing
#       Output information may be incomplete.
# COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
# ....
# python  7986 andriana    0u   CHR  136,1      0t0       4 /dev/pts/1
# python  7986 andriana    1w   REG   0,48        0  460856 /tmp/webserver_11454.log
# python  7986 andriana    2u   CHR  136,1      0t0       4 /dev/pts/1
# python  7986 andriana    3u  IPv4  67293      0t0     TCP *:11454 (LISTEN)
# python  7986 andriana    7r   CHR    1,9      0t0    1034 /dev/urandom
