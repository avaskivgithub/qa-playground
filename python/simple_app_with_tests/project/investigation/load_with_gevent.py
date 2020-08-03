#!/usr/bin/env python

import time, os, subprocess
from pprint import pprint
from collections import Counter
import gevent, requests

curent_dir = os.path.dirname(__file__)
data_file_path = '/tmp/{}.dat'.format(os.path.basename(__file__).split('.')[0])

def timed_it(func):

    def wrapper(*args, **kwrgs):
        start = time.time()
        result = func(*args, **kwrgs)
        return result, (time.time() - start)

    return wrapper

@timed_it
def load_api(call_func=requests.get, call_func_args_list=None, res_func=None,
             concurrency=10):
    """
        Returns list of: [(elapsed_time, result)]
    """

    if call_func is None:
        raise Exception('Args error: call_func have to be provided')

    results_all = []

    def worker(args):

        time_sent = time.time()
        try:
            call_res = call_func(**args)
            time_received = time.time()
            elapsed_time = time_received - time_sent
            result = res_func(call_res)
            # SAVE RESULTS: [(elapsed_time, result)]
            results_all.append((elapsed_time, result))
        except Exception as e:
            results_all.append((time.time() - time_sent, str(e.message)))

    i = 0
    while i <= len(call_func_args_list) - concurrency:
        my_threads = []
        for args in call_func_args_list[i: i + concurrency]:
            my_threads.append(gevent.spawn(worker, args))
        gevent.joinall(my_threads)
        i += concurrency

    # Returns list of: [(elapsed_time, result)]
    return results_all

def result_procces(result):

    try:
        res = getattr(result, 'status_code')
        #res = '({}, {})'.format(getattr(result, 'status_code'), getattr(result, 'text'))
    except Exception as e:
        res = str(e.message)

    return res

def draw_chart(data_file_path, title='', xlable='', ylable='', output_file='load_results.png'):

    gnuplot_script_path = os.path.join(curent_dir, 'gnuplot_load_result')

    gnuplot_script = """#!/usr/bin/gnuplot -persist

set grid
set title "{}"
set xlabel "{}"
set ylabel "{}"

set terminal png size 2000,1500 enhanced font "Helvetica,20"
set output "{}"

plot "{}" using 1:2 title "Test Results" with lines
    """.format(title, xlable, ylable, os.path.join(curent_dir, output_file), data_file_path)

    subprocess.Popen("echo '{}' > {}".format(gnuplot_script, gnuplot_script_path), stdout=subprocess.PIPE, shell=True)
    subprocess.Popen("chmod +x {}".format(gnuplot_script_path), stdout=subprocess.PIPE, shell=True)
    subprocess.Popen("{}".format(gnuplot_script_path), stdout=subprocess.PIPE, shell=True)

def monitor_system_state(port):

    load_data_file = '/tmp/load_top.dat'
    # ~> true > /tmp/load_top.dat
    # ~> app_pid=$(lsof -i :12345 | tail -n 1 | awk '{print $2}')
    # ~> i=0; while true ; do echo $i $(top -p $app_pid -n 1 -b | grep $app_pid) >> /tmp/load_top.dat; sleep 0.05 ; i=$((i + 1)); done
    # gnuplot> plot "/tmp/load_top.dat" using 1:9 title "Load" with lines

    get_pid = "lsof -i :{{}} | tail -n 1 | awk '{print $2}'".format(port)
    get_state = 'echo $(date +"%s") $(top -p {0} -n 1 | grep {0}) >> {1}'.format(port, load_data_file)

if __name__ == '__main__':

    # 1. Test Data
    requests_number = 100
    concurrency = 10
    TEST_URL = 'http://127.0.0.1:12345/edit/{}'

    call_func_args_list = []
    for i in xrange(requests_number):
        call_func_args_list.append({'url': TEST_URL.format(i)})

    # 2. Load test web gui and api
    for i in xrange(10):
        results, all_test_time = load_api(call_func=requests.get,
                                          call_func_args_list=requests_number * ['http://127.0.0.1:5000/'],
                                          res_func=result_procces,
                                          concurrency=concurrency)

        time.sleep(1)
        results, all_test_time = load_api(call_func=requests.get,
                                          call_func_args_list=call_func_args_list,
                                          res_func=result_procces,
                                          concurrency=concurrency)

        returned_codes = [el[1] for el in results]
        pprint(Counter(returned_codes))

    # # 3. Draw chart for requests elapsed time
    # with open(data_file_path, 'w') as f:
    #     for result_no, result in enumerate(results):
    #         elapse_time, result_code = result
    #         line = '{} {}'.format(result_no, elapse_time)
    #         f.write(line + '\n')
    # draw_chart(data_file_path, title='Load requests={} rate={}'.format(requests_number, concurrency),
    #            xlable='Request No', ylable='Request elapse time')

# EOF
