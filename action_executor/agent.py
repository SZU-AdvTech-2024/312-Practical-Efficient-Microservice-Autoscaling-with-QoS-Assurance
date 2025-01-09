from action_executor.action_manager import SshClient
from system_metrics.collector_backend import get_cpu_utilization
import threading

node_ip_map={
    "slave-node1": "172.31.234.112",
    "slave-node2": "172.31.234.113",
    "slave-node3": "172.31.234.114"
}

def apply_cpu_resource(pod_id, node, cpu):
    node_ip = node_ip_map.get(node)
    if not node_ip:
        raise ValueError(f"No IP address found for node '{node}'")
    client = SshClient(f"Your User:Your Password:{node_ip}")
    result = client.execute("python3 /home/k8s/advanced_pema/cpu_action.py %s %s " % (pod_id, round(cpu, 2)), sudo=True)
    print(result)

# id = "/kubepods.slice/kubepods-podbf345a70_f419_4f1c_9fb0_8bcafa2d55cb.slice/docker-9df051a276d8e3ddfcd02a7e0645a09941fd942f4ade8c1807279e7e5f663f83.scope"
# node = "slave-node2"
# cpu = 100000
# apply_cpu_resource(id, node, cpu)
