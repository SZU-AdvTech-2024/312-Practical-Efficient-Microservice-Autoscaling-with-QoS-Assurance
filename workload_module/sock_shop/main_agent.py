import os.path
import subprocess as sp
import sys

import redis
from data_processing.log_processing import end_to_end_values
# from system_metrics.metric_processing import collect_jaeger_data, collect_prometheus_data
from poisson_rate_generator import poisson_rate_sock_shop

# from system_metrics.metrics_post_processing import process_jaeger_data, process_prometheus_data

base_path = 'log_data/early_detection/'

flush_db_script_path = r'D:\PycharmProjects\advanced-pema\workload_module\sock_shop\flush_db.bat'


def run_program(rate, experiment_time, experiment_no, threads):
    procs = []

    for i in range(1, threads + 1):
        p = sp.Popen(
            [sys.executable, "sock_shop_api.py", rate, experiment_time,
             experiment_no + "/data_p" + rate + "_t" + str(threads) + "_" + str(i) + ".log"])
        procs.append(p)

    for p in procs:
        p.wait()


def avoid_cold_start():
    path = "log_data/temps"

    if not os.path.exists(path):
        os.makedirs(path)

    run_program(str(75), str(120), path, 3)
    sp.call([flush_db_script_path])



def program_runner():
    #rps_list = [300, 700, 1100]
    rps_list = [300]
    for profile in range(30,60):
        for x in rps_list:
            # profile = 0
            # avoid_cold_start()

            # while True:
            # RPS = 200
            RPS = x

            base_file_path = base_path + "rps_" + str(RPS) + '_iteration_' + str(profile) + "/"
            # base_file_path = base_path + "rps_" + str(RPS) + '_algorithm_navigation_' + str(profile) + "/"

            threads = 6
            duration = '120'
            log_path = base_file_path + "logs"
            # log_path = base_file_path

            # filename = path + '/data_p' + rate + "_t" + str(threads) + "_" + str(exp_no) + ".log"
            if not os.path.exists(log_path):
                os.makedirs(log_path)

            rate = poisson_rate_sock_shop(RPS)
            # rate = x

            run_program(str(rate), duration, log_path, threads)

            #sp.call(['sh', './flush_db.sh'])
            sp.call([flush_db_script_path])
            # start = time.time()
            # rps, response_time = end_to_end(log_path, duration=float(duration))

            # take rps, and all responses into a list and write it into redis server
            actual_rps, responses_list = end_to_end_values(log_path)
            print(x, actual_rps/int(duration))
            redis_server.set('RPS', str(actual_rps), ex=9)
            redis_server.set('responses', str(responses_list), ex=9)



if __name__ == '__main__':
    redis_server = redis.Redis(host='127.0.0.1', port=6379, db=0)
    avoid_cold_start()
    program_runner()
