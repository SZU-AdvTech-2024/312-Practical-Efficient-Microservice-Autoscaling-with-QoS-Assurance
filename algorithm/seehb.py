import random

from algorithm.algorithm_utils import get_workload_range
from algorithm.db_utils import HistoryDB, QValueDB
from algorithm.dynamic_thresholds import build_linear_regression

history = HistoryDB()
#history.delete_table()
print(history.get_data())
print("PEMA迭代的最优分配")
print(history.select_cost_min(250, 11))

q = QValueDB()
#q.delete_table()
print(q.get_data())
