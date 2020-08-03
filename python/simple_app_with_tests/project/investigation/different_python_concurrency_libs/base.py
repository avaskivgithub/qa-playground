#!/usr/bin/env python

import requests
import time
from pprint import pprint
from collections import Counter
import random
from utils.webserver_deploy import TestServerDeploy

def timed_it(func):

    def wrapper(*args, **kwrgs):
        start = time.time()
        result = func(*args, **kwrgs)
        return result, (time.time() - start)

    return wrapper

def generate_random_port(start=11370, stop=11470):

    return random.randint(start, stop)

def get_result(result):

    try:
        code = getattr(result, 'status_code')
        body = getattr(result, 'text')

        res = '({}, {})'.format(code, body.split()[0])
    except Exception as e:

        res = str(e.message)

    return res

def main(load_func, requests_number=100, concurrency=10, test=''):

    hostname = '127.0.0.1'
    deployer = TestServerDeploy(hostname=hostname)
    # hostname = '192.168.0.103'
    # deployer = TestServerDeploy(hostname=hostname, username='webtest', password='test!')

    # ***** 1. Prepare test data
    port = generate_random_port()
    TEST_URL = 'http://' + hostname + ':' + str(port) + '/{}'

    call_func_args_list = []
    for i in xrange(requests_number):
        call_func_args_list.append({'url': TEST_URL.format(i)})

    # ***** 2. Start test server ==> Load test server ==> Stop test server
    try:
        deployer.deploy_server(port)

        #while True:
        results, all_test_time = load_func(call_func=requests.get, call_func_args_list=call_func_args_list,
                                           res_func=get_result,
                                           concurrency=concurrency)
    finally:
        deployer.kill_server(port)

    print(test)
    print('Test server port was: ', port)

    # ***** 3. Aggregate data
    elapse_times = [el[0] for el in results]
    returned_codes = [str(el[1]) for el in results]

    print('Elapsed Time: ', all_test_time)

    elapse_times.sort()
    data_file_path = '/tmp/{}.dat'.format(test)
    with open(data_file_path, 'w') as f:
        for test_no, elapse_time in enumerate(elapse_times):
            line = '{} {}'.format(test_no, elapse_time)
            f.write(line + '\n')

    elapse_times.sort()
    print('Min', min(elapse_times))
    print('Avg', sum(elapse_times) / len(elapse_times))
    print('Max', max(elapse_times))
    print('Returned Codes', Counter(returned_codes))
    print('Test data file: ', data_file_path)

# EOF
