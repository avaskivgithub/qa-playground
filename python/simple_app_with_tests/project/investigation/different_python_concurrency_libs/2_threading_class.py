#!/usr/bin/env python

from threading import Thread
import time
import os
import requests
import base as load_utils


class LoadApiCl(Thread):

    def __init__(self, call_func=requests.get, call_func_args_dict=None, res_func=None):

        Thread.__init__(self)
        self.daemon = True

        self.call_func = call_func
        self.call_func_args = call_func_args_dict
        self.res_func = res_func

        self.elapsed_time = 0
        self.result = 0

    def run(self):

        try:
            time_sent = time.time()
            call_res = self.call_func(**self.call_func_args)
            time_received = time.time()
            #time.sleep(2)

            self.elapsed_time = time_received - time_sent
            # self.result = getattr(call_res, 'status_code')
            self.result = self.res_func(call_res)

        except Exception as e:
            self.elapsed_time = time.time() - time_sent
            self.result = str(e.message)

@load_utils.timed_it
def load_api(call_func=requests.get, call_func_args_list=None, res_func=None,
             concurrency=10):

    if call_func is None:
        raise Exception('Args error: call_func have to be provided')

    results_all = []

    i = 0
    while i <= len(call_func_args_list) - concurrency:

        my_threads = []
        for call_func_args in call_func_args_list[i: i + concurrency]:
            cl = LoadApiCl(requests.get, call_func_args, res_func)
            my_threads.append(cl)

        for t in my_threads:
            t.start()
        for t in my_threads:
            t.join()

        # for t in my_threads:
        #     del t

        for t in my_threads:
            results_all.append((t.elapsed_time, t.result))

        i += concurrency

    return results_all

if __name__ == '__main__':

    # Check thread count
    # for i in {1..20}; do sleep 0.5; echo $(ps -eLf | grep python | grep threading | wc -l); done

    # pprint.pprint(load_api(requests.get, {'url': 'https://translate.google.com/'}, 'status_code',
    #                        concurrency=1))

    load_utils.main(load_func=load_api, test=os.path.basename(__file__).split('.')[0])

# EOF
