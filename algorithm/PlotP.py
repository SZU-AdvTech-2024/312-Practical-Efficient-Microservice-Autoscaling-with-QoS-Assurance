import matplotlib.pyplot as plt

# 微服务名称和对应的CPU资源分配
microservices = ['carts', 'catalogue', 'front-end', 'orders', 'payment', 'shipping', 'user']
cpu_resources = [5.0, 0.6, 1.7, 2.6, 0.3, 1.7, 0.7]

# 创建条形图
plt.bar(microservices, cpu_resources, width=0.6)
# 添加标题和标签
plt.title('CPU Resources Allocation for SockShop Microservices')
plt.xlabel('Microservices')
plt.ylabel('CPU Resources')

plt.savefig('cpu_resources_allocation.png')
# 显示图表
plt.show()

print("Costs and config: [12.6] {'carts': 5.0, 'catalogue': 0.6, 'front-end': 1.7, 'orders': 2.6, 'payment': 0.3, 'shipping': 1.7, 'user': 0.7}")