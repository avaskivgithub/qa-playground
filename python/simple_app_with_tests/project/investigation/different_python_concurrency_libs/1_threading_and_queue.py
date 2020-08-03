#!/usr/bin/env python

from threading import Thread
from Queue import Queue
import time, os

import requests

import base as load_utils


@load_utils.timed_it
def load_api(call_func=requests.get, call_func_args_list=None, res_func=None,
             concurrency=10):

    if call_func is None:
        raise Exception('Args error: call_func have to be provided')

    results_all = []

    def f():
        while True:
            args = q.get()

            if args is None:
                break

            try:
                time_sent = time.time()
                res = call_func(**args)
                time_received = time.time()

                results_all.append((time_received - time_sent, res_func(res)))

            except Exception as e:
                results_all.append((time.time() - time_sent, str(e.message)))

            q.task_done()

    q = Queue(concurrency)
    for i in xrange(concurrency):
        t=Thread(target=f)
        t.daemon=True
        t.start()

    for args in call_func_args_list:
        q.put(args)
    q.join()

    # to stop the threads
    for i in xrange(concurrency):
        q.put(None)

    return results_all


if __name__ == '__main__':

    # Check thread count
    # for i in {1..20}; do sleep 0.5; echo $(ps -eLf | grep python | grep threading | wc -l); done

    # pprint.pprint(load_api(requests.get, {'url': 'https://translate.google.com/'}, 'status_code',
    #                        concurrency=1))

    load_utils.main(load_func=load_api, test=os.path.basename(__file__).split('.')[0])

# EOF
