#!/usr/bin/env python

import time, os

import gevent
import requests

import base as load_utils


@load_utils.timed_it
def load_api(call_func=requests.get, call_func_args_list=None, res_func='status_code',
             concurrency=10):

    if call_func is None:
        raise Exception('Args error: call_func have to be provided')

    results_all = []

    def worker(args):

        try:
            time_sent = time.time()
            call_res = call_func(**args)
            time_received = time.time()

            elapsed_time = time_received - time_sent
            #result = getattr(call_res, res_func)
            result = res_func(call_res)

            results_all.append((elapsed_time, result))
        except Exception as e:
            results_all.append((time.time() - time_sent, str(e.message)))

    # jobs = [gevent.spawn(worker, args) for args in call_func_args_list]
    # gevent.joinall(jobs)

    i = 0
    while i <= len(call_func_args_list) - concurrency:

        my_threads = []
        for args in call_func_args_list[i: i + concurrency]:
            my_threads.append(gevent.spawn(worker, args))
        gevent.joinall(my_threads)

        i += concurrency

    return results_all


if __name__ == '__main__':

    # Check thread count
    # for i in {1..20}; do sleep 0.5; echo $(ps -eLf | grep python | grep multiproces| wc -l); done

    # pprint.pprint(load_api(requests.get, {'url': 'https://translate.google.com/'}, 'status_code',
    #                        concurrency=1))

    load_utils.main(load_func=load_api, test=os.path.basename(__file__).split('.')[0])


# EOF
