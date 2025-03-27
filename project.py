from flask import Flask, render_template, request, jsonify
import numpy as np
import networkx as nx

app = Flask(__name__)

def is_safe_state(processes, resources, allocation, max_demand, available):
    allocation = np.array(allocation)
    max_demand = np.array(max_demand)
    available = np.array(available)
    need = max_demand - allocation
    work = available.copy()
    finish = [False] * len(processes)
    safe_sequence = []

    while len(safe_sequence) < len(processes):
        allocated = False
        for i in range(len(processes)):
            if not finish[i] and all(need[i] <= work):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(processes[i])
                allocated = True
                break
        if not allocated:
            return False, []
    return True, safe_sequence

def detect_deadlock(processes, resources, allocation, max_demand):
    G = nx.DiGraph()
    for p in processes:
        G.add_node(p, color='blue')
    for r in resources:
        G.add_node(r, color='red')

    for i, process in enumerate(processes):
        for j, res in enumerate(resources):
            if allocation[i][j] > 0:
                G.add_edge(res, process)
            if max_demand[i][j] > allocation[i][j]:
                G.add_edge(process, res)

    try:
        cycle = nx.find_cycle(G, orientation='original')
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data['processes']
    resources = data['resources']
    allocation = data['allocation']
    max_demand = data['max_demand']
    available = data['available']

    safe, sequence = is_safe_state(processes, resources, allocation, max_demand, available)
    deadlock, cycle = detect_deadlock(processes, resources, allocation, max_demand)

    return jsonify({
        "safe_state": safe,
        "safe_sequence": sequence if safe else [],
        "deadlock_detected": deadlock,
        "deadlock_cycle": cycle if deadlock else []
    })

if __name__ == '__main__':
    app.run(debug=True)
