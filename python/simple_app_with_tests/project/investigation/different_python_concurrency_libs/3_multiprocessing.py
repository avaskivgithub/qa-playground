#!/usr/bin/env python

import multiprocessing
import time, os

import requests

import base as load_utils


def worker(args):

    try:

        call_func, call_func_args_dict, res_func = args

        time_sent = time.time()
        call_res = call_func(**call_func_args_dict)
        time_received = time.time()
        #time.sleep(2)

        elapsed_time = time_received - time_sent
        #result = getattr(call_res, res_func)
        result = res_func(call_res)

    except Exception as e:
        elapsed_time = time.time() - time_sent
        result = str(e.message)

    return (elapsed_time, result)

@load_utils.timed_it
def load_api(call_func=requests.get, call_func_args_list=None, res_func=None,
             concurrency=10):

    if call_func is None:
        raise Exception('Args error: call_func have to be provided')

    pool = multiprocessing.Pool(concurrency)

    pool_args = []
    for args in call_func_args_list:
        pool_args.append((call_func, args, res_func))

    results_all = pool.map(worker, pool_args)

    pool.close()
    # To wait until a process has completed its work and exited, use the join() method.
    pool.join()

    return results_all


if __name__ == '__main__':

    # Check thread count
    # for i in {1..20}; do sleep 0.5; echo $(ps -eLf | grep python | grep multiproces| wc -l); done

    # pprint.pprint(load_api(requests.get, {'url': 'https://translate.google.com/'}, 'status_code',
    #                        concurrency=1))

    load_utils.main(load_func=load_api, test=os.path.basename(__file__).split('.')[0])


# EOF
