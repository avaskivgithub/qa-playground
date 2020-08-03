#!/usr/bin/env python

import time
from pprint import pprint
from collections import Counter
from gevent import spawn, joinall
from multiprocessing import Pool
from threading import Thread
import requests
import subprocess
import os
from draw_gnuplot import draw_gnuplot_chart

def timed_it(func):

    def wrapper(self, *args, **kwrgs):
        start = time.time()
        result = func(self, *args, **kwrgs)
        return result, (time.time() - start)

    return wrapper

#=========================== threading =====================================

class LoadThreadCl(Thread):

    def __init__(self, call_func=requests.get, call_func_args_dict=None, res_func=None):

        Thread.__init__(self)
        self.daemon = True

        self.call_func = call_func
        self.call_func_args = call_func_args_dict
        self.res_func = res_func

        self.elapsed_time = 0
        self.result = 0

    def run(self):

        time_sent = time.time()
        #self.elapsed_time = time_sent % 3600

        try:

            call_res = self.call_func(**self.call_func_args)
            time_received = time.time()

            self.elapsed_time = time_received - time_sent
            self.result = self.res_func(call_res)

        except Exception as e:
            self.elapsed_time = time.time() - time_sent
            self.result = str(e)

#=========================== multiprocessing ===============================
# http://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma

def worker_multiprocessing(input_data):
    """Routine for multiprocessing"""
    call_func, kwargs, res_func = input_data
    time_sent = time.time()

    try:
        call_res = call_func(**kwargs)
        result = res_func(call_res)

    except Exception as e:
        result = str(e)

    # RETURN RESULT: [(elapsed_time, result from res_func)]
    return (time.time() - time_sent), result

def load_with_multiprocessing(concurrency, call_func, call_func_args_list, res_func):

    pool = Pool(concurrency)
    pool_args = []
    for args in call_func_args_list:
        pool_args.append((call_func, args, res_func))

    print(pool_args)
    results_all = pool.map(worker_multiprocessing, pool_args)
    pool.close()
    pool.join()

    returned_codes = [el[1] for el in results_all]
    results_distribution = Counter(returned_codes)

    return results_distribution, results_all

#======================================= gevent ====================================

class Load(object):

    def __init__(self, call_func=None,
                       call_func_args_list=None,
                       res_func=None,
                       concurrency=10,
                       result_dir=None):

        self.call_func = requests.get if call_func is None else call_func
        self.call_func_args_list = call_func_args_list
        self.res_func = self._procces_response if res_func is None else res_func

        self.concurrency = concurrency
        self.result_dir = os.path.dirname(__file__) if result_dir is None else result_dir

        # list of: [(elapsed_time, result from res_func)]
        self.results_all = []
        self.all_requests_time = 0

    @classmethod
    def _procces_response(cls, result):

        try:
            res = getattr(result, 'status_code')
            #res = '({}, {})'.format(getattr(result, 'status_code'), getattr(result, 'text'))
        except Exception as e:
            res = str(e)

        return res

    @timed_it
    def _one_call_timed(self, args):
        return self.call_func(**args)

    def _one_call_worker(self, args):
        """Routine for gevent"""
        time_sent = time.time()

        try:
            call_res, elapsed_time = self._one_call_timed(args)
            result = self.res_func(call_res)

            # SAVE RESULTS: [(elapsed_time, result from res_func)]
            self.results_all.append((elapsed_time, result))
            # self.results_all.append((time_sent % 3600, result))
        except Exception as e:
            self.results_all.append((time.time() - time_sent, str(e)))

    def load_with_gevent(self):

        i = 0
        while i <= len(self.call_func_args_list) - self.concurrency:
            my_threads = []
            for args in self.call_func_args_list[i: i + self.concurrency]:
                my_threads.append(spawn(self._one_call_worker, args))
            joinall(my_threads)
            i += self.concurrency

    def load_with_threading(self):

        i = 0
        while i <= len(self.call_func_args_list) - self.concurrency:
            my_threads = []
            for args in self.call_func_args_list[i: i + self.concurrency]:
                cl = LoadThreadCl(call_func=self.call_func,
                                  call_func_args_dict=args,
                                  res_func=self.res_func)
                my_threads.append(cl)

            for t in my_threads:
                t.start()
            for t in my_threads:
                t.join()
            for t in my_threads:
                self.results_all.append((t.elapsed_time, t.result))

            i += self.concurrency

    @timed_it
    def _load_app(self, load_lib=0):

        if load_lib == 0:
            self.load_with_gevent()
        elif load_lib == 1:
            self.load_with_threading()
        elif load_lib == 2:
            _, self.results_all = load_with_multiprocessing(self.concurrency,
                                                            self.call_func,
                                                            self.call_func_args_list,
                                                            self.res_func)

        return self.results_all

    def load_app(self):

        self.results_all = []
        self.all_requests_time = 0

        all_results, all_requests_time = self._load_app()

        self.all_requests_time = all_requests_time
        return all_results, all_requests_time

    def get_results_distribution(self):
        returned_codes = [el[1] for el in self.results_all]
        return Counter(returned_codes)

    def get_all_requests_elapsed_time(self):
        return self.all_requests_time

    def get_elapsed_time_per_request(self):
        return [elapse_time for elapse_time, response_result in self.results_all]

    def get_response_per_request(self):
        return [response_result for elapse_time, response_result in self.results_all]

    def _save_requests_elapse_time_into_file(self, data_file_path):

        with open(data_file_path, 'w') as f:
            for result_no, result in enumerate(self.results_all):
                elapse_time, response_result = result
                line = '{} {}'.format(result_no, elapse_time)
                f.write(line + '\n')

    def _run_cli_cmd(self, cmd):
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(0.5)

    def draw_elapsed_time_distribution(self, output_file='load_results.png'):

        if not self.results_all:
            raise Exception('You have to call load_app before drawing  the chart')

        else:

            title = 'Load with requests={} and rate={}. Max(y)={}, Min(y)={}'.format(len(self.call_func_args_list),
                                                                               self.concurrency,
                                                                               max(self.get_elapsed_time_per_request()),
                                                                               min(self.get_elapsed_time_per_request()))
            xlable = 'Request No'
            ylable = 'Request Elapse Time (secs)'
            # ylable = 'Request Time Send (secs in current hour)'

            data_file_path = '/tmp/{}.dat'.format(os.path.basename(__file__).split('.')[0])
            self._save_requests_elapse_time_into_file(data_file_path)

            chart_file_path = os.path.join(self.result_dir, output_file)

            draw_gnuplot_chart(data_files_paths=[data_file_path],
                               result_dir=self.result_dir,
                               result_x_clmn_no=1,
                               result_y_clmn_no=2,
                               title=title,
                               xlable=xlable,
                               ylable=ylable,
                               output_file=chart_file_path,
                               if_rm_data_file=False)


if __name__ == '__main__':

    # 1. Test Data
    requests_number = 1000
    concurrency = 100
    TEST_URL = 'http://127.0.0.1:12345/edit/{}'

    call_func_args_list = []
    for i in range(requests_number):
        call_func_args_list.append({'url': TEST_URL.format(i)})

    # 2. Load test api
    load_cl = Load(call_func_args_list=call_func_args_list, concurrency=concurrency)
    results, all_test_time = load_cl.load_app()

    pprint(load_cl.get_results_distribution())
    print(load_cl.get_all_requests_elapsed_time())

    load_cl.draw_elapsed_time_distribution(output_file='data/load_results.png')

# EOF
