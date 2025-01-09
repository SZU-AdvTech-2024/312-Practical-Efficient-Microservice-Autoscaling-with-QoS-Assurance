import matplotlib.pyplot as plt
import numpy as np

# 假设收集的数据 (这部分需要根据实际数据替换)
# 不同RPS（300, 700, 1100）和不同策略（OPTM, RULE, PEMA）下的Normalized CPU数据
data = {
    300: {'OPTM': 8.8, 'PEMA': 9.1, 'RULE': 10.5},
    700: {'OPTM': 12.3, 'PEMA': 12.6, 'RULE': 15},
    1100: {'OPTM': 28.0, 'PEMA': 28.9, 'RULE': 37}
}

# 归一化函数
def normalize_data(data, baseline_strategy='OPTM'):
    normalized_data = {}
    for rps, strategies in data.items():
        normalized_strategy = {}
        for strategy, value in strategies.items():
            if strategy == baseline_strategy:
                normalized_strategy[strategy] = 1.0  # 基准策略归一化值为1.0
            else:
                normalized_strategy[strategy] = value / strategies[baseline_strategy]
        normalized_data[rps] = normalized_strategy
    return normalized_data

# 归一化数据
normalized_data = normalize_data(data)

# 打印归一化后的数据
print(normalized_data)

# 准备绘图数据
rps_values = list(normalized_data.keys())
strategies = list(normalized_data[rps_values[0]].keys())
bar_width = 0.25  # 每个柱子的宽度

# 生成x轴的位置
x = np.arange(len(rps_values))

# 创建柱状图
fig, ax = plt.subplots()
colors = ['#00008B', '#4682B4', '#66CDAA'] # 定义颜色列表
for i, strategy in enumerate(strategies):
    y_values = [normalized_data[rps][strategy] for rps in rps_values]
    ax.bar(x + i * bar_width, y_values, width=bar_width, label=strategy, color=colors[i])  # 添加颜色参数

# 设置标签和标题
ax.set_xlabel('Workloads (RPS)')
ax.set_ylabel('Normalized CPU')
ax.set_xticks(x + bar_width)
ax.set_xticklabels(rps_values)
ax.legend()
plt.yticks([0.0, 0.5, 1.0, 1.5])

# 显示图表
plt.title('SockShop')
plt.savefig('compare.png')
plt.show()

