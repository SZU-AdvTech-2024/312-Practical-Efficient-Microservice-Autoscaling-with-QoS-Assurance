import matplotlib.pyplot as plt
from algorithm.db_utils import HistoryDB
import csv
def get_experiment_results():
    history = HistoryDB()
    rows = history.select_response_regression(250, 7)  # 从数据库提取所有实验记录
    response_times = []
    costs = []
    profiles = []
    for row in rows:
        profiles.append(row[1])  # experiment_id
        response_times.append(row[7])  # response latency
        costs.append(row[8])  # cost
    return profiles, response_times, costs


def create_csv_high_exploration():
    history = HistoryDB()
    rows = history.select_response_regression(250, 7)
    with open('output_low.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row.values() if isinstance(row, dict) else row)


def read_csv_high_exploration():
    profiles = []
    response_times = []
    costs = []
    with open('output_high.csv', 'r') as csvfile:
        # 创建一个csv阅读器
        reader = csv.reader(csvfile)
        # 遍历CSV文件中的每一行
        for row in reader:
            profiles.append(row[1])  # experiment_id
            response_times.append(row[7])  # response latency
            costs.append(row[8])  # cost
    return profiles, response_times, costs

def read_csv_low_exploration():
    profiles = []
    response_times = []
    costs = []
    with open('output_low.csv', 'r') as csvfile:
        # 创建一个csv阅读器
        reader = csv.reader(csvfile)
        # 遍历CSV文件中的每一行
        for row in reader:
            profiles.append(row[1])  # experiment_id
            response_times.append(row[7])  # response latency
            costs.append(row[8])  # cost
    return profiles, response_times, costs


def plot_experiment_results():
    high_profiles, high_response_times, high_costs = read_csv_high_exploration()
    low_profiles, low_response_times, low_costs = read_csv_low_exploration()
    # 确保数据类型正确
    high_profiles = [float(p) for p in high_profiles]
    low_profiles = [float(p) for p in low_profiles]
    high_response_times = [float(rt) for rt in high_response_times]
    high_costs = [float(c) for c in high_costs]
    low_response_times = [float(rt) for rt in low_response_times]
    low_costs = [float(c) for c in low_costs]

    optimum_cpu = 12.3  # 假设的最优CPU值
    optimum_response = 250  # 假设的最优响应时间
    plt.figure(figsize=(12, 6))

    # Plot costs
    plt.subplot(1, 2, 1)
    plt.plot(high_profiles, high_costs, 'r-', markersize=5, marker='s', markerfacecolor='none', zorder=2, label="High Exploration")
    plt.plot(low_profiles, low_costs, 'g-', markersize=5, marker='d', markerfacecolor='none', zorder=1, label="Low Exploration")
    plt.axhline(y=optimum_cpu, color='b', linestyle='--', label="Optimum")
    plt.xlabel("Iterations")
    plt.ylabel("Total CPU")
    plt.title("(a) CPU allocation")
    plt.legend()
    plt.xticks([0, 10, 20, 30, 40, 50, 60, 70])
    plt.yticks([10, 20, 30, 40])

    # Plot response times
    plt.subplot(1, 2, 2)
    plt.plot(high_profiles, high_response_times, 'r-', markersize=5, marker='s', markerfacecolor='none', zorder=2, label="High Exploration")
    plt.plot(low_profiles, low_response_times, 'g-', markersize=5, marker='d', markerfacecolor='none', zorder=1, label="Low Exploration")
    plt.axhline(y=optimum_response, color='b', linestyle='--', label="SLO")
    plt.xlabel("Iterations")
    plt.ylabel("Response (ms)")
    plt.title("(b) Response time")
    plt.legend()
    plt.yticks([90, 100, 200, 250, 300, 400])
    plt.xticks([0, 10, 20, 30, 40, 50, 60, 70])

    plt.tight_layout()
    plt.show()

plot_experiment_results()
