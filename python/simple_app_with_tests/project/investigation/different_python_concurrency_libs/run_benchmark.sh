#!/bin/bash

ALL_TESTS=(1_threading_and_queue.py 2_threading_class.py 3_multiprocessing.py 4_gevent.py)

for next_test_file in ${ALL_TESTS[@]}; do
    python $next_test_file
done

./gnuplot_results_benchmark